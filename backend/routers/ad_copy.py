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
from config import settings

router = APIRouter(
    prefix="/api/ad-copy",
    tags=["Ad Copy"]
)


@router.options("/generate")
async def options_generate_ad_copy():
    """CORS 사전 요청(preflight)을 위한 OPTIONS 핸들러"""
    return Response(status_code=200)


@router.get("/providers")
async def get_ad_copy_providers():
    """광고 문구 생성용 AI 프로바이더 목록"""
    providers = []
    
    # OpenAI
    if settings.OPENAI_API_KEY or settings.OPENAI_GPT4_API_KEY:
        all_models = []
        default_model = "gpt-5-mini"
        
        if settings.OPENAI_API_KEY:
            all_models.extend(["gpt-5", "gpt-5-mini", "gpt-5-nano"])
        
        if settings.OPENAI_GPT4_API_KEY:
            all_models.extend(["gpt-4o", "gpt-4o-mini"])
            if not settings.OPENAI_API_KEY:
                default_model = "gpt-4o"
        
        providers.append({
            "name": "openai",
            "models": all_models,
            "default_model": default_model,
            "free": False
        })
    
    if settings.GEMINI_API_KEY:
        providers.append({
            "name": "gemini",
            "models": ["gemini-2.5-flash", "gemini-2.5-pro"],
            "default_model": "gemini-2.5-flash",
            "free": True
        })
    
    if settings.HUGGINGFACE_API_KEY:
        providers.append({
            "name": "huggingface",
            "models": ["meta-llama/Llama-3.2-3B-Instruct"],
            "default_model": "meta-llama/Llama-3.2-3B-Instruct",
            "free": True
        })
    
    if settings.GROQ_API_KEY:
        providers.append({
            "name": "groq",
            "models": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
            "default_model": "llama-3.1-8b-instant",
            "free": True
        })
    
    return {"providers": providers}


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

