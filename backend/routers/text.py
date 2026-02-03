"""
Text Generation API Router
AI Factory 테스트 (GPT-4/GPT-5 키 분리)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from ai.factory import TextAIFactory

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
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
