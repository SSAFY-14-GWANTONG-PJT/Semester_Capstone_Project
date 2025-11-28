from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import asyncio
import io
import base64

# [2025 최신] Google GenAI SDK
from google import genai
from google.genai import types
from PIL import Image

# LangChain 관련
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

app = FastAPI(root_path="/ai")

# 1. API 키 설정
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    print("❌ Error: GOOGLE_API_KEY가 없습니다.")

# 2. GenAI 클라이언트 초기화 (이미지 생성용)
# [핵심] API 버전을 명시하여 모델 인식률을 높입니다.
client = genai.Client(
    api_key=google_api_key,
    http_options={'api_version': 'v1beta'} 
)

# 3. LangChain LLM 초기화 (텍스트 생성용 - Gemini 2.5 Flash)
# 사용자 요청대로 2.5 버전을 사용합니다.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7,
    google_api_key=google_api_key
)

class StoryRequest(BaseModel):
    age: int
    topic: str
    words: list[str]

# ---------------------------------------------------------
# [동기 함수] 실제 SDK를 호출하여 이미지를 만드는 부분
# ---------------------------------------------------------
def _generate_image_sync(prompt: str):
    """
    Google GenAI SDK (Imagen 3.0)를 사용하여 이미지를 생성
    """
    try:
        # [요청하신 모델 적용] imagen-3.0-generate-002
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        # 결과 처리 (PIL Image -> Base64 변환)
        if response.generated_images:
            generated_image = response.generated_images[0]
            image_pil = generated_image.image # PIL Image 객체
            
            # 메모리 버퍼에 이미지를 저장하여 Base64로 변환
            buffered = io.BytesIO()
            image_pil.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return img_str
            
        return None
    except Exception as e:
        # 에러 발생 시 로그 출력 (디버깅용)
        print(f"SDK 이미지 생성 중 오류: {e}")
        return None

# ---------------------------------------------------------
# [비동기 래퍼] FastAPI가 멈추지 않게 스레드로 실행
# ---------------------------------------------------------
async def generate_image_for_page(text: str, index: int):
    # 이미지 프롬프트 (동화 내용을 영어 묘사로 변환)
    image_prompt = f"Cute 3D rendered children's book illustration: {text[:300]}"
    
    try:
        # [핵심] 동기 함수(_generate_image_sync)를 비동기(Thread)로 실행!
        img_base64 = await asyncio.to_thread(_generate_image_sync, image_prompt)
        
        return {
            "page_no": index + 1,
            "text": text,
            "image": img_base64 # 성공 시 문자열, 실패 시 None
        }
    except Exception as e:
        print(f"페이지 {index+1} 처리 실패: {e}")
        return {"page_no": index + 1, "text": text, "image": None}


# ---------------------------------------------------------
# 프롬프트 및 메인 로직
# ---------------------------------------------------------
prompt_template = PromptTemplate.from_template(
    """
    You are a professional children's book writer.
    Write a fairy tale based on the inputs.

    [Structure Requirements]
    1. The story MUST be divided into **4 to 6 distinct paragraphs**.
    2. Each paragraph will be one page of the book.
    3. **Output Format:** You MUST return a **JSON list of strings**. Do not include any other text.
       Example: ["Page 1 text...", "Page 2 text...", "Page 3 text..."]

    [Content Instructions]
    - Language: English Only.
    - Translate Korean keywords to English if necessary.
    - Happy ending.
    - Paragraph length: 3~4 sentences per paragraph.

    [Inputs]
    - Target Age: {age} years old
    - Topic: {topic}
    - Required Words: {words}
    """
)

@app.get("/")
def read_root():
    return {"message": "AI Server running with Gemini 2.5 Flash & Imagen 3.0 (002)"}

@app.post("/generate-story")
async def generate_story(req: StoryRequest):
    # 1. 텍스트 생성 (JsonOutputParser로 리스트 변환)
    text_chain = prompt_template | llm | JsonOutputParser()

    try:
        # [Step 1] 동화 텍스트 생성
        story_pages = await text_chain.ainvoke({
            "age": req.age,
            "topic": req.topic,
            "words": ", ".join(req.words)
        })

        # [Step 2] 이미지 병렬 생성 (asyncio.gather)
        tasks = []
        for i, page_text in enumerate(story_pages):
            tasks.append(generate_image_for_page(page_text, i))
        
        final_pages = await asyncio.gather(*tasks)

        return {
            "title": f"Fairy Tale: {req.topic}",
            "total_pages": len(final_pages),
            "pages": final_pages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))