"""
Ad Copy Service
광고 문구 생성 비즈니스 로직
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models.ad_copy import AdCopy
from schemas.ad_copy import AdCopyRequest, AdCopyResponse
from services.ai_factory import ai_factory


class AdCopyService:
    """광고 문구 생성 서비스"""
    
    @staticmethod
    async def generate_ad_copy(
        request: AdCopyRequest,
        db: Session
    ) -> AdCopyResponse:
        """
        광고 문구 생성 및 저장
        
        Args:
            request: 광고 문구 생성 요청
            db: 데이터베이스 세션
            
        Returns:
            생성된 광고 문구 응답
        """
        # AI 제공자 선택 (사용자 선택 또는 자동 폴백)
        provider, provider_name, model_name = ai_factory.get_available_provider(
            preferred_provider=request.ai_provider,
            custom_model=request.ai_model,
            strict_mode=request.strict_mode
        )
        
        # 광고 문구 생성
        generated_copies = await provider.generate_ad_copies(
            product_name=request.product_name,
            category=request.category,
            target_audience=request.target_audience,
            key_features=request.key_features,
            tone=request.tone,
            num_copies=5
        )
        
        # 데이터베이스에 저장
        ad_copy = AdCopy(
            product_name=request.product_name,
            category=request.category,
            target_audience=request.target_audience,
            key_features=request.key_features,
            tone=request.tone,
            ai_provider=provider_name,
            ai_model=model_name,
            generated_copies=generated_copies
        )
        
        db.add(ad_copy)
        db.commit()
        db.refresh(ad_copy)
        
        return AdCopyResponse.model_validate(ad_copy)
    
    @staticmethod
    def get_ad_copy_history(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> List[AdCopyResponse]:
        """
        광고 문구 생성 이력 조회
        
        Args:
            db: 데이터베이스 세션
            skip: 건너뛸 개수
            limit: 조회할 개수
            
        Returns:
            광고 문구 응답 리스트
        """
        ad_copies = db.query(AdCopy)\
            .order_by(AdCopy.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return [AdCopyResponse.model_validate(ac) for ac in ad_copies]
    
    @staticmethod
    def get_ad_copy_by_id(
        db: Session,
        ad_copy_id: int
    ) -> Optional[AdCopyResponse]:
        """
        ID로 광고 문구 조회
        
        Args:
            db: 데이터베이스 세션
            ad_copy_id: 광고 문구 ID
            
        Returns:
            광고 문구 응답 또는 None
        """
        ad_copy = db.query(AdCopy).filter(AdCopy.id == ad_copy_id).first()
        
        if ad_copy:
            return AdCopyResponse.model_validate(ad_copy)
        return None
