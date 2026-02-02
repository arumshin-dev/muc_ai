"""
Ad Copy Router
광고 문구 생성 API 엔드포인트
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from schemas.ad_copy import AdCopyRequest, AdCopyResponse, AdCopyListResponse
from services.ad_copy_service import AdCopyService

router = APIRouter(
    prefix="/api/ad-copy",
    tags=["Ad Copy"]
)


@router.options("/generate")
async def options_generate_ad_copy():
    """CORS 사전 요청(preflight)을 위한 OPTIONS 핸들러"""
    return Response(status_code=200)


@router.post("/generate", response_model=AdCopyResponse, status_code=201)
async def generate_ad_copy(
    request: AdCopyRequest,
    db: Session = Depends(get_db)
):
    """
    광고 문구 생성
    
    - **product_name**: 제품명
    - **category**: 카테고리
    - **target_audience**: 타겟 고객
    - **key_features**: 핵심 특징
    - **tone**: 톤 (friendly, professional, humorous)
    - **ai_provider**: 사용할 AI 제공자 (선택사항)
    - **ai_model**: 사용할 모델 (선택사항)
    - **custom_api_key**: 사용자 API 키 (선택사항)
    """
    try:
        result = await AdCopyService.generate_ad_copy(request, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=AdCopyListResponse)
def get_ad_copy_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    광고 문구 생성 이력 조회
    
    - **skip**: 건너뛸 개수
    - **limit**: 조회할 개수 (최대 100)
    """
    if limit > 100:
        limit = 100
    
    items = AdCopyService.get_ad_copy_history(db, skip, limit)
    total = len(items)  # 실제로는 count 쿼리 필요
    
    return AdCopyListResponse(total=total, items=items)


@router.get("/{ad_copy_id}", response_model=AdCopyResponse)
def get_ad_copy(
    ad_copy_id: int,
    db: Session = Depends(get_db)
):
    """
    ID로 광고 문구 조회
    
    - **ad_copy_id**: 광고 문구 ID
    """
    result = AdCopyService.get_ad_copy_by_id(db, ad_copy_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Ad copy not found")
    
    return result
