"""
Ad Copy Service
광고 문구 생성 비즈니스 로직
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models.ad_copy import AdCopy
from schemas.ad_copy import AdCopyRequest, AdCopyResponse
from ai.factory import TextAIFactory  # ← 새 Factory 사용!


class AdCopyService:
    """광고 문구 생성 서비스"""
    
    @staticmethod
    async def generate_ad_copy(
        request: AdCopyRequest,
        db: Session
    ) -> AdCopyResponse:
        """광고 문구 생성 및 저장"""
        
        # 새로운 Factory 사용
        ai = TextAIFactory.create(
            provider=request.ai_provider or "openai",
            model=request.ai_model or "gpt-5-mini"
        )
        
        # 광고 문구 생성 프롬프트 구성
        prompt = f"""
다음 제품의 광고 문구 5개를 생성해주세요:

- 제품명: {request.product_name}
- 카테고리: {request.category}
- 타겟 고객: {request.target_audience}
- 핵심 특징: {request.key_features}
- 톤: {request.tone}

각 광고 문구는 한 줄로, 명확하고 매력적이게 작성해주세요.
번호를 매겨서 5개를 작성해주세요.
"""
        
        system_prompt = "당신은 전문 카피라이터입니다. 매력적이고 효과적인 광고 문구를 작성합니다."
        
        # AI 생성
        result = await ai.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.8
        )
        
        # 결과 파싱 (줄 단위로 분리)
        generated_copies = [
            line.strip() 
            for line in result.split('\n') 
            if line.strip() and not line.strip().startswith('#')
        ][:5]  # 최대 5개
        
        # 데이터베이스 저장
        ad_copy = AdCopy(
            product_name=request.product_name,
            category=request.category,
            target_audience=request.target_audience,
            key_features=request.key_features,
            tone=request.tone,
            ai_provider=request.ai_provider or "openai",
            ai_model=request.ai_model or "gpt-5-mini",
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
