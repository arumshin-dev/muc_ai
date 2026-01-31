"""
MUC AI Backend Configuration
환경 변수 및 설정 관리
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 데이터베이스
    DATABASE_URL: str = "postgresql://user:password@db:5432/muc_db"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_DEFAULT_MODEL: str = "gpt-5-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Hugging Face (무료)
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_DEFAULT_MODEL: str = "meta-llama/Llama-3.3-70B-Instruct"
    
    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_DEFAULT_MODEL: str = "gemini-pro"
    
    # AI 제공자 설정
    DEFAULT_AI_PROVIDER: str = "huggingface"
    AI_PROVIDER_FALLBACK_ORDER: str = "huggingface,gemini,openai"
    
    # 애플리케이션
    ENVIRONMENT: str = "development"
    BACKEND_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # 보안
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """CORS 허용 오리진 리스트"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def ai_provider_fallback_list(self) -> List[str]:
        """AI 제공자 폴백 순서 리스트"""
        return [provider.strip() for provider in self.AI_PROVIDER_FALLBACK_ORDER.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()
