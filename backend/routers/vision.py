"""
Vision API Router
이미지 분석 및 텍스트 생성
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ai.vision_analyzer import OpenAIVision
from database import SessionLocal
from models import VisionAnalysis
from datetime import datetime
from ai.vision_analyzer import HuggingFaceVisionSimple

# BLIP 사용 (빠름, 간단)
vision_ai = HuggingFaceVisionSimple(model="Salesforce/blip-image-captioning-large")

# 또는 LLaVA 사용 (강력, 느림)
# vision_ai = HuggingFaceVision(model="llava-hf/llava-1.5-7b-hf")
router = APIRouter(prefix="/api/vision", tags=["vision"])


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form("이 이미지를 자세히 설명해주세요"),
    model: str = Form("gpt-5-mini")
):
    """
    이미지 분석
    
    - **file**: 이미지 파일 (JPG, PNG)
    - **prompt**: 분석 요청 프롬프트
    - **model**: 사용할 모델 (기본: gpt-5-mini)
    """
    try:
        # 이미지 읽기
        image_data = await file.read()
        
        # Vision AI 생성
        vision_ai = OpenAIVision(model=model)
        
        # 이미지 분석
        result = await vision_ai.analyze_image(
            image_data=image_data,
            prompt=prompt
        )
        
        # DB 저장
        db = SessionLocal()
        try:
            analysis = VisionAnalysis(
                prompt=prompt,
                result=result,
                ai_model=model,
                ai_provider="openai",
                created_at=datetime.utcnow()
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            return {
                "id": analysis.id,
                "prompt": prompt,
                "result": result,
                "model": model,
                "provider": "openai",
                "filename": file.filename
            }
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
