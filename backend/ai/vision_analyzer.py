"""
Vision Analysis AI - 이미지 분석
"""
from openai import AsyncOpenAI
from ai.base import VisionAnalyzerAI
from typing import Optional
import base64


class OpenAIVision(VisionAnalyzerAI):
    """OpenAI Vision API (GPT-4o, GPT-5)"""
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        super().__init__("openai", model, api_key)
        self.client = AsyncOpenAI(api_key=self.api_key)
        print(f"✅ [OpenAI Vision] Initialized: {model}")
    
    async def analyze_image(
        self,
        image_data: bytes,
        prompt: str = "이 이미지를 상세히 설명해주세요.",
        **kwargs
    ) -> str:
        """이미지 분석 (API 방식)"""
        print(f"👁️ [OpenAI Vision] Analyzing image with {self.model}")
        print(f"   Prompt: {prompt[:50]}...")
        
        # 이미지를 base64로 인코딩
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        try:
            # GPT-5는 max_completion_tokens, GPT-4는 max_tokens
            params = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            # GPT-5 계열은 max_completion_tokens 사용
            if self.model.startswith("gpt-5"):
                params["max_completion_tokens"] = kwargs.get("max_completion_tokens", 500)
            else:
                params["max_tokens"] = kwargs.get("max_tokens", 1000)
            
            response = await self.client.chat.completions.create(**params)
            
            if not response.choices:
                raise RuntimeError("No response from OpenAI Vision API")
            
            result = response.choices[0].message.content
            print(f"✅ [OpenAI Vision] Analysis complete")
            return result or "Error: Empty response"
            
        except Exception as e:
            print(f"❌ [OpenAI Vision] Error: {e}")
            raise
    
    async def generate(self, **kwargs):
        """BaseAI 추상 메서드 구현"""
        return await self.analyze_image(
            image_data=kwargs.get("image_data"),
            prompt=kwargs.get("prompt", "이 이미지를 설명해주세요.")
        )


class GeminiVision(VisionAnalyzerAI):
    """Gemini Vision API"""
    
    def __init__(self, model: str = "gemini-2.0-flash-exp", api_key: Optional[str] = None):
        super().__init__("gemini", model, api_key)
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(model)
        print(f"✅ [Gemini Vision] Initialized: {model}")
    
    async def analyze_image(
        self,
        image_data: bytes,
        prompt: str = "이 이미지를 상세히 설명해주세요.",
        **kwargs
    ) -> str:
        """Gemini로 이미지 분석"""
        print(f"👁️ [Gemini Vision] Analyzing image with {self.model}")
        
        try:
            # PIL Image로 변환
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            
            response = await self.client.generate_content_async([prompt, image])
            
            print(f"✅ [Gemini Vision] Analysis complete")
            return response.text
            
        except Exception as e:
            print(f"❌ [Gemini Vision] Error: {e}")
            raise
    
    async def generate(self, **kwargs):
        return await self.analyze_image(
            image_data=kwargs.get("image_data"),
            prompt=kwargs.get("prompt", "이 이미지를 설명해주세요.")
        )


# 🚫 HuggingFace 로컬 모델 제거 (torch/transformers 필요)
# 추후 필요하면 별도 서비스로 분리
