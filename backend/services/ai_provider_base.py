"""
AI Service Base Interface
모든 AI 제공자가 구현해야 하는 기본 인터페이스
"""
from abc import ABC, abstractmethod
from typing import List


class AIProviderBase(ABC):
    """AI 제공자 기본 인터페이스"""
    
    def __init__(self, api_key: str, model: str):
        """
        Args:
            api_key: API 키
            model: 사용할 모델명
        """
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate_ad_copies(
        self,
        product_name: str,
        category: str,
        target_audience: str,
        key_features: str,
        tone: str,
        num_copies: int = 5
    ) -> List[str]:
        """
        광고 문구 생성
        
        Args:
            product_name: 제품명
            category: 카테고리
            target_audience: 타겟 고객
            key_features: 핵심 특징
            tone: 톤 (friendly, professional, humorous)
            num_copies: 생성할 문구 개수
            
        Returns:
            생성된 광고 문구 리스트
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        API 키가 유효하고 사용 가능한지 확인
        
        Returns:
            사용 가능 여부
        """
        pass
    
    def _build_prompt(
        self,
        product_name: str,
        category: str,
        target_audience: str,
        key_features: str,
        tone: str,
        num_copies: int
    ) -> str:
        """
        광고 문구 생성을 위한 프롬프트 작성
        
        Returns:
            프롬프트 문자열
        """
        tone_descriptions = {
            "friendly": "친근하고 따뜻한",
            "professional": "전문적이고 신뢰감 있는",
            "humorous": "유머러스하고 재미있는"
        }
        
        tone_desc = tone_descriptions.get(tone, "친근한")
        
        prompt = f"""당신은 소상공인을 위한 광고 문구 전문가입니다.
다음 정보를 바탕으로 {num_copies}개의 매력적인 광고 문구를 작성해주세요.

제품명: {product_name}
카테고리: {category}
타겟 고객: {target_audience}
핵심 특징: {key_features}
톤: {tone_desc}

요구사항:
1. 각 문구는 간결하고 임팩트 있어야 합니다 (20-50자)
2. 타겟 고객의 관심을 끌 수 있어야 합니다
3. 제품의 핵심 특징을 효과적으로 전달해야 합니다
4. {tone_desc} 톤을 유지해야 합니다
5. 각 문구는 번호 없이 한 줄씩 작성해주세요

광고 문구:"""
        
        return prompt

    def _post_process(self, content: str, num_copies: int) -> List[str]:
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        cleaned = []
        for line in lines:
            text = line.lstrip('0123456789.-•* ')
            if text:
                cleaned.append(text)

        return cleaned[:num_copies]
