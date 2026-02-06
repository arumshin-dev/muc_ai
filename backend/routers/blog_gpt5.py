from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ai.blog_gpt5 import BlogGPT5AI # GPT-5용 AI 모듈 임포트

router = APIRouter(
    prefix="/api/v1", # ⭐️ API 주소 prefix 추가
    tags=["Blog Generation (GPT-5)"],
)

# ⭐️ JSON 요청 본문을 위한 Pydantic 모델 정의
class BlogGPT5Request(BaseModel):
    topic: str
    style: str
    length: str

# ⭐️ API 경로 수정 및 요청 모델 적용
@router.post("/generate-gpt5-blog", summary="GPT-5 기반 블로그 글 생성")
async def generate_blog_post(request: BlogGPT5Request):
    """
    사용자 요청에 따라 GPT-5 모델을 사용하여 블로그 글을 생성합니다.

    - **topic**: 글의 주제
    - **style**: 원하는 글의 스타일 (예: 일반, 전문, 캐주얼 등)
    - **length**: 원하는 글의 길이 (예: 짧음, 중간, 김)
    """
    try:
        ai_module = BlogGPT5AI()
        result = await ai_module.generate_blog_post(
            topic=request.topic,
            style=request.style,
            length=request.length
        )
        return result
    except ValueError as ve:
        # API 키가 설정되지 않은 경우 등 값 관련 오류 처리
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(ve)
        )
    except Exception as e:
        # 기타 모든 예외 처리
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GPT-5 블로그 생성 중 서버 오류 발생: {str(e)}"
        )
