"""
Image Editing AI - 이미지 편집
"""
from openai import AsyncOpenAI
from ai.base import ImageEditorAI
import httpx
from io import BytesIO


class OpenAIImageEditor(ImageEditorAI):
    """OpenAI Image Edit API (gpt-image-1-mini)"""
    
    def __init__(self, model: str = "gpt-image-1-mini"):
        super().__init__("openai", model)
        self.client = AsyncOpenAI(api_key=self.get_api_key())
    
    async def edit_image(
        self, 
        image_data: bytes,
        instruction: str,
        mask_data: bytes = None,
        **kwargs
    ) -> bytes:
        """이미지 편집"""
        
        # BytesIO로 변환
        image_file = BytesIO(image_data)
        image_file.name = "image.png"
        
        if mask_data:
            mask_file = BytesIO(mask_data)
            mask_file.name = "mask.png"
        else:
            mask_file = None
        
        response = await self.client.images.edit(
            image=image_file,
            mask=mask_file,
            prompt=instruction,
            n=1,
            size=kwargs.get("size", "1024x1024")
        )
        
        # URL에서 이미지 다운로드
        image_url = response.data[0].url
        
        async with httpx.AsyncClient() as client:
            image_response = await client.get(image_url)
            return image_response.content
    
    async def generate(self, **kwargs):
        """BaseAI 추상 메서드 구현"""
        return await self.edit_image(
            image_data=kwargs.get("image_data"),
            instruction=kwargs.get("instruction"),
            mask_data=kwargs.get("mask_data")
        )
