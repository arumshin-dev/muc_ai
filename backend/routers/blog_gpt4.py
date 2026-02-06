from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ai.blog_gpt4 import BlogGPT4AI

router = APIRouter(
    prefix="/api/v1",
    tags=["Blog Generation"],
)

class BlogRequest(BaseModel):
    keyword: str
    style: str
    length: str
    model: str

@router.post("/generate-gpt4-blog", summary="SEO 블로그 글 생성")
async def generate_blog_post(request: BlogRequest):
    """
    사용자 요청에 따라 SEO에 최적화된 블로그 글을 생성합니다.

    - **keyword**: 글의 주제가 될 핵심 키워드
    - **style**: 원하는 글의 스타일 (예: 일반, 전문, 캐주얼)
    - **length**: 원하는 글의 길이 (예: 짧음, 중간, 김)
    - **model**: 사용할 AI 모델 (현재 'gpt-4' 지원)
    """
    try:
        # 현재는 GPT-4 모델군만 지원
        if 'gpt-4' not in request.model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported model: {request.model}. Please use a 'gpt-4' variant."
            )
        
        ai_module = BlogGPT4AI()
        result = await ai_module.generate_seo_blog(
            keyword=request.keyword,
            style=request.style,
            length=request.length
        )
        return result
    except ValueError as ve:
        # API 키가 설정되지 않은 경우
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(ve)
        )
    except Exception as e:
        # 기타 모든 예외 처리
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"블로그 글 생성 중 서버 오류 발생: {str(e)}"
        )
