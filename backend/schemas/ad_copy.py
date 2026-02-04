"""
AdCopy Schemas
광고 문구 생성 요청/응답 스키마
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AIProviderInfo(BaseModel):
    """AI 제공자 정보"""
    provider: str = Field(..., description="AI 제공자 (openai, groq, gemini)")
    model: str = Field(..., description="사용된 모델명")


class AdCopyRequest(BaseModel):
    """광고 문구 생성 요청"""
    product_name: str = Field(..., min_length=1, max_length=255, description="제품명")
    category: str = Field(..., min_length=1, max_length=100, description="카테고리")
    target_audience: str = Field(..., min_length=1, max_length=255, description="타겟 고객")
    key_features: str = Field(..., min_length=1, description="핵심 특징")
    tone: str = Field(..., description="톤 (friendly, professional, humorous)")
    
    # 선택적 AI 제공자 설정
    ai_provider: Optional[str] = Field(None, description="사용할 AI 제공자 (선택사항)")
    ai_model: Optional[str] = Field(None, description="사용할 모델 (선택사항)")
    strict_mode: bool = Field(False, description="실패 시 폴백 방지 (디버깅용)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_name": "수제 햄버거",
                "category": "음식점",
                "target_audience": "20-30대 직장인",
                "key_features": "100% 국내산 소고기, 수제 패티, 신선한 야채",
                "tone": "friendly",
                "ai_provider": "gemini",
                "ai_model": "gemini-2.5-flash"
            }
        }


class AdCopyResponse(BaseModel):
    """광고 문구 생성 응답"""
    id: int
    product_name: str
    category: str
    target_audience: str
    key_features: str
    tone: str
    ai_provider: str
    ai_model: str
    generated_copies: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AdCopyListResponse(BaseModel):
    """광고 문구 목록 응답"""
    total: int
    items: List[AdCopyResponse]


# New schemas for ad-copy providers
class AdCopyProviderItem(BaseModel):
    name: str
    models: List[str]
    default_model: str
    free: bool = False # Default to False, since not all providers are free


class AdCopyProvidersResponse(BaseModel):
    providers: List[AdCopyProviderItem]