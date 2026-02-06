"""
Image AI Factory - 이미지 생성 AI 관리
"""
from ai.base import ImageGeneratorAI
from typing import Optional


class ImageAIFactory:
    """이미지 AI Factory"""
    
    _cache = {}  # 모델 캐시
    
    @staticmethod
    def create(provider: str, model: str, api_key: Optional[str] = None) -> ImageGeneratorAI:
        """
        이미지 생성 AI 생성
        
        Examples:
            # OpenAI
            - ImageAIFactory.create('openai', 'gpt-image-1-mini')
            - ImageAIFactory.create('openai', 'dall-e-3')
            - ImageAIFactory.create('openai', 'dall-e-2')
            
            # Gemini (추후)
            - ImageAIFactory.create('gemini', 'imagen-3.0-generate-001')
            
            # Stability AI (추후)
            - ImageAIFactory.create('stability', 'stable-diffusion-xl-1024-v1-0')
        """
        # API 키가 제공되면 캐시하지 않음 (사용자별로 다를 수 있으므로)
        cache_key = f"{provider}:{model}"
        
        if not api_key and cache_key in ImageAIFactory._cache:
            print(f"♻️  [ImageFactory] Cached: {cache_key}")
            return ImageAIFactory._cache[cache_key]
        
        print(f"🏭 [ImageFactory] Creating: {cache_key}")
        
        if provider == "openai":
            from ai.image_generator import OpenAIImageGenerator
            ai = OpenAIImageGenerator(model=model, api_key=api_key)
        
        # 나중에 추가
        # elif provider == "gemini":
        #     from ai.image_generator import GeminiImageGenerator
        #     ai = GeminiImageGenerator(model=model, api_key=api_key)
        
        # elif provider == "stability":
        #     from ai.image_generator import StabilityImageGenerator
        #     ai = StabilityImageGenerator(model=model, api_key=api_key)
        
        else:
            raise ValueError(f"Unsupported image provider: {provider}")
        
        # API 키가 없을 때만 캐시
        if not api_key:
            ImageAIFactory._cache[cache_key] = ai
        
        return ai
    
    @staticmethod
    def clear_cache():
        """캐시 초기화"""
        ImageAIFactory._cache.clear()
        print("🗑️  [ImageFactory] Cache cleared")
