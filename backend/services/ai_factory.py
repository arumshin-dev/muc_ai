"""
AI Provider Factory
AI 제공자 팩토리 및 폴백 로직
"""
from typing import Optional
from config import settings
from services.ai_provider_base import AIProviderBase
from services.openai_service import OpenAIService
from services.huggingface_service import HuggingFaceService
from services.gemini_service import GeminiService


class AIProviderFactory:
    """AI 제공자 팩토리"""
    
    @staticmethod
    def create_provider(
        provider_name: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> AIProviderBase:
        """
        AI 제공자 인스턴스 생성
        
        Args:
            provider_name: 제공자 이름 (openai, huggingface, gemini)
            api_key: 사용자 제공 API 키 (선택사항)
            model: 사용할 모델 (선택사항)
            
        Returns:
            AIProviderBase 인스턴스
        """
        provider_name = provider_name.lower()
        
        if provider_name == "openai":
            key = api_key or settings.OPENAI_API_KEY
            raw_mdl = model or settings.OPENAI_DEFAULT_MODEL
            # '#' 분리 로직 추가
            mdl = raw_mdl.split('#')[-1] if '#' in raw_mdl else raw_mdl
            return OpenAIService(api_key=key, model=mdl)
        
        elif provider_name == "huggingface":
            key = api_key or settings.HUGGINGFACE_API_KEY
            raw_mdl = model or settings.HUGGINGFACE_DEFAULT_MODEL
            mdl = raw_mdl.split('#')[-1] if '#' in raw_mdl else raw_mdl
            return HuggingFaceService(api_key=key, model=mdl)
        
        elif provider_name == "gemini":
            key = api_key or settings.GEMINI_API_KEY
            raw_mdl = model or settings.GEMINI_DEFAULT_MODEL
            mdl = raw_mdl.split('#')[-1] if '#' in raw_mdl else raw_mdl
            return GeminiService(api_key=key, model=mdl)
        
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")

    
    @staticmethod
    def get_available_provider(
        preferred_provider: Optional[str] = None,
        custom_model: Optional[str] = None,
        strict_mode: bool = False
    ) -> tuple[AIProviderBase, str, str]:
        """
        사용 가능한 AI 제공자 반환 (폴백 로직 포함)
        
        Args:
            preferred_provider: 선호하는 제공자
            custom_model: 사용자 모델
            strict_mode: 성공할 때까지 폴백할지 여부 (True면 폴백 안함)
            
        Returns:
            (provider_instance, provider_name, model_name)
        """
        # 선호 제공자가 있으면 먼저 시도
        if preferred_provider:
            try:
                provider = AIProviderFactory.create_provider(
                    preferred_provider,
                    model=custom_model
                )
                if provider.is_available():
                    return provider, preferred_provider, provider.model
                elif strict_mode:
                    raise Exception(f"AI provider {preferred_provider} is not available (check API key)")
            except Exception as e:
                if strict_mode:
                    raise e
                pass
        
        if strict_mode:
             raise Exception("Requested AI provider failed in strict mode")
        
        # 폴백 순서대로 시도
        for provider_name in settings.ai_provider_fallback_list:
            try:
                provider = AIProviderFactory.create_provider(provider_name)
                if provider.is_available():
                    return provider, provider_name, provider.model
            except Exception:
                continue
        
        # 모든 제공자가 실패한 경우
        raise Exception(
            "No AI provider is available. Please configure at least one API key in .env file."
        )


# 전역 팩토리 인스턴스
ai_factory = AIProviderFactory()
