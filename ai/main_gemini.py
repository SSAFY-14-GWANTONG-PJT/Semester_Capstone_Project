# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# # API 통신용 
# import httpx
# import asyncio

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# # 결과 예쁘게
# from langchain_core.output_parsers import StrOutputParser
# # 함수 체인으로 만드는 도구 RunnableLambda
# from langchain_core.runnables import RunnableLambda

# import os


# app = FastAPI(root_path="/ai")

# google_api_key=os.environ.get("GOOGLE_API_KEY")

# # 요청 받을 데이터구조
# class StoryRequest(BaseModel):
#     age: int
#     topic: str
#     words: list[str]


# # LangChain 설정, 우선 무료 버전인 gpt-5-mini 사용
# # 텍스트 생성용 LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0.7,
#     google_api_key=google_api_key
# )

# # 이미지 생성용 -> imagen-3.0-generate-002 이거 쓰기
# async def generate_image_for_page(text: str, index: int):
#     """
#     Imagen 3.0 (generate-002) 모델을 사용하여 페이지별 삽화를 생성합니다.
#     """
#     try:
#         # 이미지 프롬프트 작성 (동화 내용을 바탕으로)
#         image_prompt = f"Create a cute, 3d rendered children's book illustration for this story scene: {text[:300]}..."
        
#         # [변경] Imagen 3.0 공식 엔드포인트 적용
#         url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateContent?key={google_api_key}"
        
#         headers = {"Content-Type": "application/json"}
        
#         payload = {
#             "contents": [{"parts": [{"text": image_prompt}]}],
#             "generationConfig": {
#                 "responseModalities": ["IMAGE"] # 이미지만 요청
#             }
#         }

#         async with httpx.AsyncClient() as client:
#             # 이미지 생성 타임아웃 60초
#             response = await client.post(url, json=payload, headers=headers, timeout=60.0)

#         if response.status_code == 200:
#             data = response.json()
#             # 응답 구조 파싱 (Gemini/Imagen 표준)
#             # candidates -> content -> parts -> inlineData (base64)
#             img_data = None
#             try:
#                 parts = data.get("candidates", [])[0].get("content", {}).get("parts", [])
#                 for part in parts:
#                     if "inlineData" in part:
#                         img_data = part["inlineData"]["data"]
#                         break
#             except Exception as e:
#                 print(f"이미지 데이터 파싱 실패: {e}")

#             return {
#                 "page_no": index + 1,
#                 "text": text,
#                 "image": img_data
#             }
#         else:
#             print(f"이미지 생성 실패 (Page {index+1}): {response.status_code} - {response.text}")
#             return {"page_no": index + 1, "text": text, "image": None}

#     except Exception as e:
#         print(f"에러 발생 (Page {index+1}): {e}")
#         return {"page_no": index + 1, "text": text, "image": None}


# # 프롬프트 (동화책 구성을 위해 JSON 리스트 포맷 강제)
# prompt_template = PromptTemplate.from_template(
#     """
#     You are a professional children's book writer.
#     Write a fairy tale based on the inputs.

#     [Structure Requirements]
#     1. The story MUST be divided into **4 to 6 distinct paragraphs**.
#     2. Each paragraph will be one page of the book.
#     3. **Output Format:** You MUST return a **JSON list of strings**. Do not include any other text.
#        Example: ["Page 1 text...", "Page 2 text...", "Page 3 text..."]

#     [Content Instructions]
#     - Language: English Only.
#     - Translate Korean keywords to English if necessary.
#     - Happy ending.
#     - Paragraph length: 3~4 sentences per paragraph.

#     [Inputs]
#     - Target Age: {age} years old
#     - Topic: {topic}
#     - Required Words: {words}
#     """
# )

# @app.get("/")
# def read_root():
#     return {"message": "AI Server is running with Gemini 2.5 Flash & Imagen 3.0!"}

# @app.post("/generate-story")
# async def generate_story(req: StoryRequest):
#     # 1. 텍스트 생성 체인 (JsonOutputParser로 리스트 변환)
#     text_chain = prompt_template | llm | JsonOutputParser()

#     try:
#         # [Step 1] 이야기 생성 (리스트 형태: ["페이지1 내용", "페이지2 내용", ...])
#         # Gemini 2.5가 이야기를 4~6개 문단 리스트로 써줍니다.
#         story_pages = await text_chain.ainvoke({
#             "age": req.age,
#             "topic": req.topic,
#             "words": ", ".join(req.words)
#         })

#         # [Step 2] 이미지 병렬 생성 (각 페이지마다 Imagen 3.0 호출)
#         # asyncio.gather를 사용해 4~6장을 동시에 그림 -> 속도 대폭 향상
#         tasks = []
#         for i, page_text in enumerate(story_pages):
#             tasks.append(generate_image_for_page(page_text, i))
        
#         # 모든 페이지 작업이 끝날 때까지 대기
#         final_pages = await asyncio.gather(*tasks)

#         # [Step 3] 최종 결과 반환
#         return {
#             "title": f"Fairy Tale: {req.topic}",
#             "total_pages": len(final_pages),
#             "pages": final_pages
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))