"""
MUC AI Backend
소상공인 광고 콘텐츠 생성 서비스
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from database import engine, Base

# 모델 import (테이블 생성을 위해 필요)
from models import AdCopy, ImageGeneration#, VisionAnalysis, ImageEdit


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 이벤트"""
    # 시작 시: 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("=" * 60)
    print("✅ Database tables created")
    print(f"📊 Tables: ad_copies, vision_analyses, image_generations, image_edits")
    print("=" * 60)
    yield
    # 종료 시: 정리 작업
    print("👋 Shutting down...")


# FastAPI 앱 생성
app = FastAPI(
    title="MUC AI - 소상공인 광고 콘텐츠 생성 서비스",
    description="생성형 AI를 활용한 광고 문구 자동 생성 서비스",
    version="1.0.0",
    lifespan=lifespan
)


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 import
from routers import ad_copy, text, image_gen #, vision, image_edit


# 라우터 등록
app.include_router(text.router)     # 텍스트 생성 (Factory 사용)
app.include_router(ad_copy.router)  # 광고 문구 생성 (기존)
app.include_router(image_gen.router)
# app.include_router(vision.router)
# app.include_router(image_edit.router)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Welcome to MUC AI - 소상공인 광고 콘텐츠 생성 서비스",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "광고 문구 생성 (Text → Text)",
            "텍스트 생성 (Factory Pattern)",
            "이미지 분석 (Image → Text)",
            "이미지 생성 (Text → Image)",
            "이미지 편집 (Image → Image)"
        ]
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "message": "Backend is running",
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/providers")
async def get_available_providers():
    """사용 가능한 AI 제공자 목록"""
    providers = []
    
    # OpenAI: GPT-4 또는 GPT-5 키가 있으면 사용 가능
    if settings.OPENAI_API_KEY or settings.OPENAI_GPT4_API_KEY:
        available_models = {
            "gpt5": [],
            "gpt4": [],
            "image": ["gpt-image-1-mini"]
        }
        
        # GPT-5 키가 있으면 GPT-5 모델 추가
        if settings.OPENAI_API_KEY:
            available_models["gpt5"] = ["gpt-5", "gpt-5-mini", "gpt-5-nano"]
        
        # GPT-4 키가 있으면 GPT-4 모델 추가
        if settings.OPENAI_GPT4_API_KEY:
            available_models["gpt4"] = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
        
        providers.append({
            "name": "openai",
            "models": {
                "gpt4": ["gpt-4o", "gpt-4o-mini"],
                "gpt5": ["gpt-5", "gpt-5-mini", "gpt-5-nano"],
                "image": ["gpt-image-1-mini"]
            },# available_models,
            "default_model": settings.OPENAI_DEFAULT_MODEL,
            "features": ["text", "vision", "image-generation", "image-editing"]
        })
    
    if settings.HUGGINGFACE_API_KEY:
        providers.append({
            "name": "huggingface",
            "models": {
                "llama": [
                    "meta-llama/Llama-3.2-3B-Instruct",
                    "meta-llama/Llama-3.1-8B-Instruct",
                    "meta-llama/Llama-3.3-70B-Instruct"
                ]
            },
            "default_model": settings.HUGGINGFACE_DEFAULT_MODEL,
            "free": True,
            "features": ["text"]
        })
    
    if settings.GEMINI_API_KEY:
        providers.append({
            "name": "gemini",
            "models": {
                "flash": ["gemini-2.5-flash", "gemini-2.0-flash"],
                "pro": ["gemini-2.5-pro"]
            },
            "default_model": settings.GEMINI_DEFAULT_MODEL,
            "free": True,
            "features": ["text", "vision"]
        })

    if settings.GROQ_API_KEY:
        providers.append({
            "name": "groq",
            "models": {
                "llama": [
                    "llama3-8b-8192",
                    "llama3-70b-8192"
                ],
                "mixtral": [
                    "mixtral-8x7b-32768"
                ],
                "gemma": [
                    "gemma-7b-it"
                ]
            },
            "default_model": "llama3-8b-8192",
            "free": True,
            "features": ["text"]
        })
    
    return {
        "providers": providers,
        "default_provider": settings.DEFAULT_AI_PROVIDER,
        "fallback_order": settings.ai_provider_fallback_list if hasattr(settings, 'ai_provider_fallback_list') else []
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
