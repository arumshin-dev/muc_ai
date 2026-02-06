
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Form 대신 BaseModel 임포트
from ai.text.review_reply import ReviewReplyAI

router = APIRouter(prefix="/api/v1", tags=["review"])
review_reply_ai = ReviewReplyAI()

# JSON 요청 본문을 위한 Pydantic 모델 정의
class ReviewReplyRequest(BaseModel):
    customer_review: str
    tone: str = "neutral"
    language: str = "ko"

@router.post("/generate-review-reply")
# 엔드포인트가 Form 대신 Pydantic 모델을 받도록 수정
async def generate_review_reply_endpoint(request: ReviewReplyRequest):
    """
    고객 리뷰에 대한 상점 주인의 답글을 AI가 생성합니다.
    """
    try:
        # Pydantic 모델(request)에서 데이터를 가져오도록 수정
        reply = await review_reply_ai.generate_reply(
            request.customer_review,
            request.tone,
            request.language
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"리뷰 답글 생성 중 오류 발생: {e}")
