"""
Image Generation API Router
텍스트로 이미지 생성
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Literal
from ai.image_generator import OpenAIImageGenerator
from database import SessionLocal
from models import ImageGeneration
from datetime import datetime
import base64
import logging

router = APIRouter(prefix="/api/image", tags=["image-generation"])
logger = logging.getLogger(__name__)


class ImageGenerateRequest(BaseModel):
    prompt: str
    model: Literal["gpt-image-1-mini"] = "gpt-image-1-mini"
    size: Literal["256x256", "512x512", "1024x1024"] = "256x256"
    quality: Literal["low", "medium", "high", "auto"] = "low"


@router.post("/generate")
async def generate_image(request: ImageGenerateRequest):
    """
    텍스트로 이미지 생성 (Binary PNG 반환)(Base64 파일 반환)
    
    - **prompt**: 이미지 생성 프롬프트
    - **model**: 사용할 모델 (기본: gpt-image-1-mini)
    - **size**: 이미지 크기 (1024x1024, 512x512 등)
    - **quality**: 품질 ("low"	가장 빠르고 저렴,
                        "medium"	기본 권장,
                        "high"	품질 최상 (느리고 비쌈),
                        "auto"	모델이 알아서 선택)
    """
    # Image Generator 생성
    generator = OpenAIImageGenerator(model=request.model)

    try:
        # 1️⃣ 이미지 생성
        image_data = await generator.generate_image(
            prompt=request.prompt,
            size=request.size,
            quality=request.quality
        )
    except Exception as e:
        # OpenAI 실패는 명확히 500
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")

    generation_id = None

    # 2️⃣ DB 저장 (실패해도 이미지 반환)
    try:
        db = SessionLocal()
        generation = ImageGeneration(
            prompt=request.prompt,
            ai_model=request.model,
            ai_provider="openai",
            size=request.size,
            quality=request.quality,
            created_at=datetime.utcnow()
        )
        db.add(generation)
        db.commit()
        db.refresh(generation)
        generation_id = generation.id
    except Exception as e:
        logger.error(f"DB save failed: {e}")
    finally:
        db.close()

    # 3️⃣ 이미지 반환
    return Response(
        content=image_data,
        media_type="image/png",
        headers={
            "X-Generation-ID": str(generation_id) if generation_id else "N/A",
            "X-Model": request.model
        }
    )


# @router.post("/generate-with-metadata")
# async def generate_image_with_metadata(request: ImageGenerateRequest):
#     """이미지 생성 + 메타데이터 반환 (Base64)"""
@router.post("/generate-base64")
async def generate_image_base64(request: ImageGenerateRequest):
    """
    텍스트로 이미지 생성 (Base64 반환)
    """
    generator = OpenAIImageGenerator(model=request.model)

    try:
        image_data = await generator.generate_image(
            prompt=request.prompt,
            size=request.size,
            quality=request.quality
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")
    # Base64 인코딩
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    generation_id = None

    try:
        # DB 저장
        db = SessionLocal()
        generation = ImageGeneration(
            prompt=request.prompt,
            ai_model=request.model,
            ai_provider="openai",
            size=request.size,
            quality=request.quality,
            created_at=datetime.utcnow()
        )
        db.add(generation)
        db.commit()
        db.refresh(generation)
        generation_id = generation.id
    except Exception as e:
        logger.error(f"DB save failed: {e}")
    finally:
        db.close()

    return {
        "id": generation_id,
        "prompt": request.prompt,
        "model": request.model,
        "provider": "openai",
        "size": request.size,
        "quality": request.quality,
        "image": f"data:image/png;base64,{image_base64}",
    }
