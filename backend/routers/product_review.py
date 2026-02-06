
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai.text.product_review import ProductReviewAI

router = APIRouter()
product_review_ai = ProductReviewAI()

# 1. JSON 요청 본문을 처리하기 위한 Pydantic 모델 정의
class ProductReviewRequest(BaseModel):
    product_name: str
    sentiment: str
    pros: str = ""
    cons: str = ""
    length: int = 500
    language: str = "ko"

@router.post("/api/v1/generate-product-review")
# 2. 엔드포인트가 Form 대신 Pydantic 모델을 받도록 수정
async def generate_product_review_endpoint(request: ProductReviewRequest):
    """
    쇼핑몰 제품 리뷰를 AI가 생성합니다.
    """
    try:
        # 3. Pydantic 모델(request)에서 데이터를 가져오도록 수정
        review = await product_review_ai.generate_product_review(
            product_name=request.product_name,
            sentiment=request.sentiment,
            pros=request.pros,
            cons=request.cons,
            length=request.length,
            language=request.language
        )
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"제품 리뷰 생성 중 오류 발생: {e}")
