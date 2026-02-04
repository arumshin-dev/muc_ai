"""
Text Generation API Router
AI Factory 테스트 (GPT-4/GPT-5 키 분리)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from ai.factory import TextAIFactory
from config import settings  

router = APIRouter(prefix="/api/text", tags=["text"])


class TextRequest(BaseModel):
    prompt: str
    provider: str = "openai"
    model: str = "gpt-5-mini"
    max_tokens: int = 1000
    temperature: float = 0.7


@router.post("/generate")
async def generate_text(request: TextRequest):
    """텍스트 생성"""
    try:
        ai = TextAIFactory.create(provider=request.provider, model=request.model)
        result = await ai.generate_text(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return {
            "provider": request.provider,
            "model": request.model,
            "text": result  # ← "result" → "text"로 변경 (프론트와 일치)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def get_text_providers():
    """텍스트 생성 전용 프로바이더 목록"""
    providers_list = []
    
    # OpenAI GPT-4
    if settings.OPENAI_GPT4_API_KEY:
        providers_list.append({
            "id": "openai",
            "name": "OpenAI GPT-4",
            "models": [
                {"id": "gpt-4o", "name": "GPT-4o"},
                {"id": "gpt-4o-mini", "name": "GPT-4o Mini"},
                {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"},  # ← 추가!
            ]
        })
    
    # OpenAI GPT-5
    if settings.OPENAI_API_KEY:
        providers_list.append({
            "id": "openai",
            "name": "OpenAI GPT-5",
            "models": [
                {"id": "gpt-5", "name": "GPT-5"},
                {"id": "gpt-5-mini", "name": "GPT-5 Mini"},
                {"id": "gpt-5-nano", "name": "GPT-5 Nano"},
            ]
        })
    
    # Google Gemini
    if settings.GEMINI_API_KEY:
        providers_list.append({
            "id": "gemini",
            "name": "Google Gemini",
            "models": [
                {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash"},
                {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro"},
            ]
        })
    
    # HuggingFace
    if settings.HUGGINGFACE_API_KEY:
        providers_list.append({
            "id": "huggingface",
            "name": "HuggingFace",
            "models": [
                {"id": "meta-llama/Llama-3.2-3B-Instruct", "name": "Llama 3.2 3B"},
                {"id": "meta-llama/Llama-3.1-8B-Instruct", "name": "Llama 3.1 8B"},  # ← 추가!
                {"id": "meta-llama/Llama-3.3-70B-Instruct", "name": "Llama 3.3 70B"},  # ← 추가!
                # {"id": "mistralai/Mistral-7B-Instruct-v0.3", "name": "Mistral 7B"},  # ← 추가!
            ]
        })
    
    # Groq
    if settings.GROQ_API_KEY:
        providers_list.append({
            "id": "groq",
            "name": "Groq (무료)",
            "models": [
                {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B Instant"},
                {"id": "llama-3.3-70b-versatile", "name": "Llama 3.3 70B"},
                # {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"},  # ← 추가!
                # {"id": "gemma2-9b-it", "name": "Gemma 2 9B"},  # ← 추가!
            ]
        })
    
    return {"providers": providers_list}