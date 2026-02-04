"""
AI 기본 추상 클래스
"""
from abc import ABC, abstractmethod
from typing import Any
from config import settings


class BaseAI(ABC):
    """AI 기본 추상 클래스"""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
    
    @abstractmethod
    async def generate(self, **kwargs):
        """생성 메서드"""
        pass
    
    def get_api_key(self) -> str:
        """프로바이더별 API 키 반환"""
        if self.provider == "openai":
            # GPT-4 vs GPT-5 구분
            if self.model.startswith("gpt-5"):
                # GPT-5: OPENAI_API_KEY 우선 사용
                if settings.OPENAI_API_KEY:
                    return settings.OPENAI_API_KEY
                else:
                    raise ValueError("OPENAI_API_KEY is not set")
            else:
                # GPT-4: OPENAI_GPT4_API_KEY 사용
                if settings.OPENAI_GPT4_API_KEY:
                    return settings.OPENAI_GPT4_API_KEY
                else:
                    raise ValueError("OPENAI_GPT4_API_KEY is not set")
        
        elif self.provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set")
            return settings.GEMINI_API_KEY
        
        elif self.provider == "groq":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is not set")
            return settings.GROQ_API_KEY
        
        elif self.provider == "huggingface":
            if not settings.HUGGINGFACE_API_KEY:
                raise ValueError("HUGGINGFACE_API_KEY is not set")
            return settings.HUGGINGFACE_API_KEY
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")


class TextGeneratorAI(BaseAI):
    """텍스트 생성 AI 추상 클래스"""
    
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """텍스트 생성"""
        pass
