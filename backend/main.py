"""
MUC AI Backend
소상공인 광고 콘텐츠 생성 서비스
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from database import engine, Base
from routers import ad_copy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 이벤트"""
    # 시작 시: 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
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

# CORS 설정 (임시로 모든 오리진 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # settings.cors_origins_list -> ["*"] 로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(ad_copy_router)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Welcome to MUC AI - 소상공인 광고 콘텐츠 생성 서비스",
        "version": "1.0.0",
        "docs": "/docs"
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
    
    if settings.OPENAI_API_KEY:
        providers.append({
            "name": "openai",
            "models": ["gpt-5-nano", "gpt-5-mini", "gpt-5"],
            "default_model": settings.OPENAI_DEFAULT_MODEL
        })
    
    if settings.HUGGINGFACE_API_KEY:
        providers.append({
            "name": "huggingface",
            "models": ["meta-llama/Llama-3.1-8B-Instruct", "meta-llama/Llama-3.2-3B-Instruct", "meta-llama/Llama-3.3-70B-Instruct"],
            "default_model": settings.HUGGINGFACE_DEFAULT_MODEL,
            "free": True
        })
    
    if settings.GEMINI_API_KEY:
        providers.append({
            "name": "gemini",
            "models": ['models/gemini-2.5-flash', 'models/gemini-2.5-pro', 'models/gemini-2.0-flash'],
            "default_model": settings.GEMINI_DEFAULT_MODEL,
            "free": True
        })
    
    return {
        "providers": [
            {
                **p,
                "default_model": p["default_model"].split('#')[-1] if '#' in p["default_model"] else p["default_model"]
            } for p in providers
        ],
        "default_provider": settings.DEFAULT_AI_PROVIDER,
        "fallback_order": settings.ai_provider_fallback_list
    }
