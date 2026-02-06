"""
Image Editing API Router
이미지 편집
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from ai.image_editor import OpenAIImageEditor
from database import SessionLocal
from models import ImageEdit
from datetime import datetime
import base64

router = APIRouter(prefix="/api/image-edit", tags=["image-editing"])


@router.post("/edit")
async def edit_image(
    file: UploadFile = File(...),
    instruction: str = Form(...),
    mask: UploadFile = File(None),
    model: str = Form("gpt-image-1-mini"),
    size: str = Form("1024x1024")
):
    """
    이미지 편집
    
    - **file**: 원본 이미지
    - **instruction**: 편집 지시사항
    - **mask**: 마스크 이미지 (선택사항)
    - **model**: 사용할 모델
    - **size**: 출력 크기
    """
    try:
        # 이미지 읽기
        image_data = await file.read()
        mask_data = await mask.read() if mask else None
        
        # Image Editor 생성
        editor = OpenAIImageEditor(model=model)
        
        # 이미지 편집
        edited_data = await editor.edit_image(
            image_data=image_data,
            instruction=instruction,
            mask_data=mask_data,
            size=size
        )
        
        # Base64 인코딩
        # image_base64 = base64.b64encode(edited_data).decode('utf-8')
        
        # DB 저장
        db = SessionLocal()
        try:
            edit = ImageEdit(
                instruction=instruction,
                ai_model=model,
                ai_provider="openai",
                size=size,
                created_at=datetime.utcnow()
            )
            db.add(edit)
            db.commit()
            db.refresh(edit)
            
            # 이미지 반환
            return Response(
                content=edited_data,
                media_type="image/png",
                headers={
                    "X-Edit-ID": str(edit.id),
                    "X-Model": model
                }
            )
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit-base64")
async def edit_image_base64(
    file: UploadFile = File(...),
    instruction: str = Form(...),
    mask: UploadFile = File(None),
    model: str = Form("gpt-image-1-mini"),
    size: str = Form("1024x1024")
):
    """
    이미지 편집 (Base64 반환)
    """
    try:
        image_data = await file.read()
        mask_data = await mask.read() if mask else None
        
        editor = OpenAIImageEditor(model=model)
        edited_data = await editor.edit_image(
            image_data=image_data,
            instruction=instruction,
            mask_data=mask_data,
            size=size
        )
        
        # Base64 인코딩
        image_base64 = base64.b64encode(edited_data).decode('utf-8')
        
        # DB 저장
        db = SessionLocal()
        try:
            edit = ImageEdit(
                instruction=instruction,
                ai_model=model, 
                ai_provider="openai", 
                size=size,
                created_at=datetime.utcnow()
            )
            db.add(edit)
            db.commit()
            db.refresh(edit)
            
            return {
                "id": edit.id,
                "instruction": instruction,
                "model": model,
                "provider": "openai",
                "size": size,
                "image": f"data:image/png;base64,{image_base64}"
            }
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
