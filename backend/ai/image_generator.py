"""
Image Generation AI - 텍스트로 이미지 생성
"""
from openai import AsyncOpenAI
from ai.base import BaseAI
import httpx
import base64
from typing import Optional


class OpenAIImageGenerator(BaseAI):
    """OpenAI Image Generation API (gpt-image-1-mini)"""
    
    def __init__(self, model: str = "gpt-image-1-mini", api_key: Optional[str] = None):
        super().__init__("openai", model)
        self.client = AsyncOpenAI(api_key=self.get_api_key())
        print(f"✅ [OpenAI Image] Initialized: {model}")
    
    async def generate_image(
        self, 
        prompt: str,
        size: str = "1024x1024",
        quality: str = "low",
        **kwargs
    ) -> bytes:
        """이미지 생성
        
        quality:
            - "low": 가장 빠르고 저렴
            - "medium": 기본 권장
            - "high": 품질 최상 (느리고 비쌈)
            - "auto": 모델이 알아서 선택
        """
        print(f"🎨 [OpenAI Image] Generating: {prompt[:50]}... (size: {size}, quality: {quality})")
        
        response = await self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            quality=quality,
            response_format="b64_json",  # Base64로 받기
            n=1
        )

        data = response.data[0]
        
        if hasattr(data, "b64_json") and data.b64_json:
            print(f"✅ [OpenAI Image] Generated via base64")
            return base64.b64decode(data.b64_json)
        
        elif hasattr(data, "url") and data.url:
            print(f"✅ [OpenAI Image] Downloading from URL")
            async with httpx.AsyncClient() as client:
                image_response = await client.get(data.url)
                return image_response.content
        
        else:
            raise RuntimeError("No image data returned from OpenAI")
    
    async def generate(self, **kwargs):
        """BaseAI 추상 메서드 구현"""
        return await self.generate_image(
            prompt=kwargs.get("prompt"),
            size=kwargs.get("size", "1024x1024"),
            quality=kwargs.get("quality", "low")
        )


class GeminiImageGenerator(BaseAI):
    """Google Gemini Image Generation (Imagen 3)"""
    
    def __init__(self, model: str = "imagen-3.0-generate-001"):
        super().__init__("gemini", model)
        import google.generativeai as genai
        genai.configure(api_key=self.get_api_key())
        self.client = genai
        print(f"✅ [Gemini Image] Initialized: {model}")
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        **kwargs
    ) -> bytes:
        """Imagen으로 이미지 생성"""
        print(f"🎨 [Gemini Image] Generating: {prompt[:50]}...")
        
        # Gemini Imagen API 호출
        # 실제 구현은 Google AI Python SDK 확인 필요
        raise NotImplementedError("Gemini Image Generation 구현 필요")
    
    async def generate(self, **kwargs):
        return await self.generate_image(
            prompt=kwargs.get("prompt"),
            size=kwargs.get("size", "1024x1024")
        )


class StabilityImageGenerator(BaseAI):
    """Stability AI (SDXL, SD3)"""
    
    def __init__(self, model: str = "stable-diffusion-xl-1024-v1-0"):
        super().__init__("stability", model)
        self.base_url = "https://api.stability.ai/v1/generation"
        print(f"✅ [Stability AI] Initialized: {model}")
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        **kwargs
    ) -> bytes:
        """Stability AI로 이미지 생성"""
        print(f"🎨 [Stability AI] Generating: {prompt[:50]}...")
        
        width, height = map(int, size.split('x'))
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{self.model}/text-to-image",
                headers={
                    "Authorization": f"Bearer {self.get_api_key()}",
                    "Content-Type": "application/json"
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 7,
                    "height": height,
                    "width": width,
                    "samples": 1,
                    "steps": 30,
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Stability AI error: {response.text}")
            
            data = response.json()
            image_base64 = data["artifacts"][0]["base64"]
            return base64.b64decode(image_base64)
    
    async def generate(self, **kwargs):
        return await self.generate_image(
            prompt=kwargs.get("prompt"),
            size=kwargs.get("size", "1024x1024")
        )
