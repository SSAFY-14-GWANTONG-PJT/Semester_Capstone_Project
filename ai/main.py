from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
import os
import asyncio
import io
import base64

# LangChain 관련
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Gemini 관련
from google import genai
from google.genai import types
from PIL import Image

# 리스트 타입 사용 위해
from typing import List, Optional

app = FastAPI(root_path="/ai")

google_api_key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(
    api_key=google_api_key,
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7,
    google_api_key=google_api_key
)

# 동화 생성 요청모델
class StoryRequest(BaseModel):
    age: int = Field(description="동화가 고려한 독자 나이")
    story_level: int = Field(description="동화의 난이도(읽을 때의 어려움 정도)")
    genre: str = "General" # 우선 General로 세우고 생성
    keywords: List[str] = Field(default=[], description="아이가 원하는 동화에 들어갈 요소(마법의 성, 공주, 전설의 검, 용)")
    vocab_words: List[str] = Field(default=[], description="오늘 배워야 할 Voca 리스트")
    study_set_id: Optional[int] = Field(default=None, description="가리키는 StudySet")

# 동화 페이지 모델
class StoryPageResponse(BaseModel):
    page_number: int
    content: str
    image_data: Optional[str] = None # Base64 문자열 들어가는 image_data

# 동화 요청 결과 모델
class StoryResponse(BaseModel):
    study_set_id: Optional[int]
    title: str
    summary: str
    genre: str
    keywords: List[str] # 동화에 사용된 키워드 (요청받은 것 그대로 반환)
    story_level: int 
    pages: List[StoryPageResponse]


# 동화 기반 문제생성 모델
class ProblemRequest(BaseModel):
    story_text: str # 동화내용 들어가야
    num_questions: int = 5 # 만들 문제의 개수

# 문제 선택지 모델
class ChoiceItem(BaseModel):
    content: str # 선택지 내용
    is_correct: bool # 정답 여부

# 질문 모델
class QuestionItem(BaseModel):
    question: str # 문제 내용
    choices: List[ChoiceItem] # 선택지를 담는 List


# 동화 생성 프롬프트 업데이트
story_prompt_template = PromptTemplate.from_template(
    """
    You are a professional children's book writer.
    Write a fairy tale based on the inputs.

    [Structure Requirements]
    1. The story MUST be divided into **4 to 6 distinct paragraphs**.
    2. Each paragraph will be one page of the book.
    3. **Output Format:** You MUST return a **Single JSON Object**. Do not include any other text.
       
       JSON Structure Example:
       {{
         "title": "The Title of the Story",
         "summary": "A short summary of the story in 1-2 sentences.",
         "pages": ["Page 1 text...", "Page 2 text...", "Page 3 text..."]
       }}

    [Content Instructions]
    - Language: English Only.
    - Target Audience Age: {age} years old (Level {level})
    - Genre: {genre}
    - Story Elements (Keywords): {keywords} (Use these to build the plot)
    
    [Vocabulary Instructions]
    - **Target Vocabulary Words**: {vocab_words}
    - Try to include these vocabulary words naturally in the story.
    - **IMPORTANT**: If a word does not fit the context or genre (e.g., 'pregnancy' in a children's hero story), **OMIT it**. Do not force it.
    - Prioritize a natural, engaging story flow over including every single word.

    [Inputs]
    - Age: {age}
    - Keywords: {keywords}
    - Vocab: {vocab_words}
    """
)

# 문제 생성 프롬프트
problem_prompt_template = PromptTemplate.from_template(
    """
    You are an English education expert for children.
    Based on the provided story, create {num_questions} multiple-choice questions.

    [Story]
    {story_text}

    [Requirements]
    1. Create exactly {num_questions} questions.
    2. Each question must have **5 choices**.
    3. Only **one choice** must be correct (`is_correct`: true).
    4. The questions should test reading comprehension.
    5. Language: English Only.

    [Output Format]
    You MUST return a JSON list of objects matching this exact structure:
    [
      {{
        "question": "Who is the main character?",
        "choices": [
          {{"content": "A Rabbit", "is_correct": true}},
          {{"content": "A Lion", "is_correct": false}},
          {{"content": "A Car", "is_correct": false}},
          {{"content": "A Tree", "is_correct": false}},
          {{"content": "A Bear", "is_correct": false}}
        ]
      }}
    ]
    Do not include any markdown formatting (like ```json). Just return the raw JSON list.
    """
)

# [동기 함수] 실제 SDK를 호출하여 이미지를 만드는 부분
def _generate_image_sync(prompt: str):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=prompt,
        )
        
        # 사용량 로그 출력
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage = response.usage_metadata
            print(f"이미지 생성 토큰 사용량:")
            print(f"   - 입력 토큰: {usage.prompt_token_count if hasattr(usage, 'prompt_token_count') else 'N/A'}")
            print(f"   - 총 토큰: {usage.total_token_count if hasattr(usage, 'total_token_count') else 'N/A'}")
        
        # 이미지가 inline_data로 반환됨
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # inline_data.data는 bytes 객체이므로 base64 문자열로 변환
                    img_data = part.inline_data.data
                    
                    # bytes인 경우 base64 인코딩
                    if isinstance(img_data, bytes):
                        return base64.b64encode(img_data).decode('utf-8')
                    # 이미 문자열인 경우 그대로 반환
                    return img_data
        
        return None
    except Exception as e:
        print(f"SDK 이미지 생성 중 오류: {e}")
        return None

# [비동기 래퍼] FastAPI가 멈추지 않게 스레드로 실행
async def generate_image_for_page(text: str, index: int, max_retries=2) -> StoryPageResponse:
    """
    이미지 생성 with 재시도 로직
    """
    # 이미지 프롬프트 (동화 내용을 영어 묘사로 변환)
    image_prompt = f"Create a cute 3D rendered children's book illustration: {text[:300]}"
    
    img_base64 = None
    for attempt in range(max_retries):
        try:
            img_base64 = await asyncio.to_thread(_generate_image_sync, image_prompt)
            if img_base64:
                break
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
        except Exception as e:
            print(f"페이지 {index+1} 시도 {attempt+1} 실패: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
    
    # ERD의 StoryPage 모델 구조에 맞춰 반환
    return StoryPageResponse(
        page_number=index + 1,
        content=text,
        image_data=img_base64
    )



@app.get("/")
def read_root():
    return {
        "message": "AI Server running with Gemini 2.5 Flash & Free Image Generation",
        "info": {
            "text_model": "gemini-2.5-flash",
            "image_model": "gemini-2.5-flash-image",
            "free_tier_limits": {
                "text": "1500 RPD (Requests Per Day)",
                "image": "500 RPD"
            }
        }
    }

@app.get("/list-models")
def list_available_models():
    try:
        models = client.models.list()
        return {"models": [model.name for model in models]}
    except Exception as e:
        return {"error": str(e)}


# 동화 생성 api 요청 & 함수
@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(req: StoryRequest):
    
    text_chain = story_prompt_template | llm | JsonOutputParser()

    try:
        print("동화 텍스트(제목, 줄거리, 내용) 생성 중...")
        
        # 키워드와 단어장 목록을 쉼표로 구분된 문자열로 변환
        keywords_str = ", ".join(req.keywords) if req.keywords else "Creative Story"
        vocab_str = ", ".join(req.vocab_words) if req.vocab_words else "None"

        story_data = await text_chain.ainvoke({
            "age": req.age,
            "level": req.story_level,
            "keywords": keywords_str,
            "genre": req.genre,
            "vocab_words": vocab_str
        })
        
        pages_text_list = story_data.get("pages", [])
        title = story_data.get("title", f"Fairy Tale: {req.genre}")
        summary = story_data.get("summary", "")
        
        print(f"총 {len(pages_text_list)}개 페이지 텍스트 생성 완료")

        final_pages_data = []
        for i, page_text in enumerate(pages_text_list):
            print(f"페이지 {i+1}/{len(pages_text_list)} 이미지 생성 중...")
            page_result = await generate_image_for_page(page_text, i)
            final_pages_data.append(page_result)
            
            if i < len(pages_text_list) - 1:
                await asyncio.sleep(2)
        
        print(f"\n전체 동화 생성 완료!")

        result = StoryResponse(
            study_set_id=req.study_set_id, # 요청받은 ID 그대로 반환
            title=title,
            summary=summary,
            genre=req.genre,
            keywords=req.keywords, # 요청받은 키워드 그대로 반환
            story_level=req.story_level, # 요청받은 레벨 그대로 반환
            pages=final_pages_data
        )
        
        # 미리보기용 저장
        app.state.last_story = result.model_dump()
        app.state.last_story['preview_url'] = f"/ai/preview-story" 
        
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

# 동화기반 문제 생성 api 요청 & 함수
@app.post("/story-problem", response_model=List[QuestionItem])
async def story_problem(req: ProblemRequest):
    """
    동화 텍스트를 입력받고, 문제를 생성(Question + Choices)
    """
    # 체인 연결
    problem_chain = problem_prompt_template | llm | JsonOutputParser()

    try: 
        print(f"문제 생성 시작 (동화 길이 : {len(req.story_text)}자)")

        # 비동기 호출로 AI에 요청
        result = await problem_chain.ainvoke({
            "story_text" : req.story_text,
            "num_questions" : req.num_questions
        })

        print(f"문제 len{(result)}개 생성 완료!")

        return result
    
    except Exception as e :
        print(f"문제 생성 중 에러 발생 : {e}")

        raise HTTPException(status_code=500, detail=str(e))



@app.get("/preview-story", response_class=HTMLResponse)
async def preview_story():
    """
    마지막 생성된 동화를 HTML로 미리보기
    """
    if not hasattr(app.state, 'last_story') or not app.state.last_story:
        return "<h1>No story generated yet. Please generate a story first.</h1>"
    
    story = app.state.last_story
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{story['title']}</title>
        <style>
            body {{
                font-family: 'Comic Sans MS', cursive, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(to bottom, #87CEEB, #98FB98);
            }}
            h1 {{
                text-align: center;
                color: #FF6B6B;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            .summary {{
                background: #FFFACD;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 2px dashed #FFD700;
            }}
            .page {{
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .page-number {{
                color: #666;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .text {{
                line-height: 1.8;
                color: #333;
                margin: 15px 0;
            }}
            .image {{
                width: 100%;
                max-width: 512px;
                height: auto;
                border-radius: 10px;
                margin: 15px auto;
                display: block;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .no-image {{
                background: #f0f0f0;
                padding: 40px;
                text-align: center;
                color: #999;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>📚 {story['title']} 📚</h1>
        <div class="summary">
            <strong>Summary:</strong> {story['summary']}
        </div>
        <p style="text-align: center; color: #666;">Genre: {story['genre']} | Level: {story['story_level']}</p>
    """
    
    for page in story['pages']:
        # Pydantic model이 dump된 상태이므로 dict로 접근
        # page_no가 ERD의 page_number로 변경됨
        page_num = page.get('page_number')
        content = page.get('content')
        image_data = page.get('image_data')

        html_content += f"""
        <div class="page">
            <div class="page-number">📖 Page {page_num}</div>
            <div class="text">{content}</div>
        """
        
        if image_data:
            html_content += f"""
            <img class="image" src="data:image/png;base64,{image_data}" alt="Page illustration">
            """
        else:
            html_content += """
            <div class="no-image">🎨 Image generation failed</div>
            """
        
        html_content += "</div>"
    
    html_content += """
    </body>
    </html>
    """
    
    return html_content


@app.get("/preview-image/{page_no}", response_class=Response)
async def preview_single_image(page_no: int):
    if not hasattr(app.state, 'last_story') or not app.state.last_story:
        raise HTTPException(status_code=404, detail="No story found")
    
    story = app.state.last_story
    # page_number로 검색
    page = next((p for p in story['pages'] if p['page_number'] == page_no), None)
    
    if not page or not page['image_data']:
        raise HTTPException(status_code=404, detail="Image not found")
    
    image_bytes = base64.b64decode(page['image_data'])
    return Response(content=image_bytes, media_type="image/png")