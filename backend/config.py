"""
MUC AI Backend Configuration
환경 변수 및 설정 관리
"""
import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings


# 루트 디렉토리 자동 감지
def find_root_dir():
    """프로젝트 루트 디렉토리 찾기"""
    current = Path(__file__).resolve()
    
    # backend 폴더에서 상위로 이동
    while current.name != 'muc_ai' and current.parent != current:
        current = current.parent
    
    return current


ROOT_DIR = find_root_dir()
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 환경
    ENVIRONMENT: str = "development"
    
    # URL 설정
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    # 데이터베이스
    DATABASE_URL: str = "postgresql://user:password@db:5432/muc_db"
    
    # AI Keys
    OPENAI_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # AI 모델
    OPENAI_DEFAULT_MODEL: str = "gpt-5-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    HUGGINGFACE_DEFAULT_MODEL: str = "meta-llama/Llama-3.2-3B-Instruct"
    GEMINI_DEFAULT_MODEL: str = "models/gemini-2.5-flash"
    
    # AI 제공자
    DEFAULT_AI_PROVIDER: str = "huggingface"
    AI_PROVIDER_FALLBACK_ORDER: str = "huggingface,gemini,openai"
    
    # 포트
    BACKEND_PORT: int = 8000
    
    # 보안
    SECRET_KEY: str = "dev_secret_key"
    CORS_ORIGINS: str = "*"
    
    # 로깅
    LOG_LEVEL: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        return origins
    
    @property
    def ai_provider_fallback_list(self) -> List[str]:
        return [p.strip() for p in self.AI_PROVIDER_FALLBACK_ORDER.split(",")]
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT in ["development", "local"]
    
    class Config:
        env_file = str(ENV_FILE)  # 루트의 .env 사용
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()

# 시작 시 로그
print("=" * 60)
print(f"📁 Loading config from: {ENV_FILE}")
print(f"🌍 Environment: {settings.ENVIRONMENT}")
print(f"🔗 Backend: {settings.BACKEND_URL}")
print(f"🔗 Frontend: {settings.FRONTEND_URL}")
print(f"🔐 CORS Origins: {settings.cors_origins_list}")
print("=" * 60)
