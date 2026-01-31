"""
Hugging Face Inference API Service
Hugging Face Inference API를 사용한 광고 문구 생성 (무료)
"""
from typing import List
import httpx
from services.ai_provider_base import AIProviderBase


class HuggingFaceService(AIProviderBase):
    """Hugging Face Inference API 광고 문구 생성 서비스"""
    
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.2-3B-Instruct"):
        super().__init__(api_key, model)
        # OpenAI 호환 엔드포인트
        # HF Router 엔드포인트 (v1 권장)
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def is_available(self) -> bool:
        """API 키 유효성 확인"""
        return bool(self.api_key)
    
    async def generate_ad_copies(
        self,
        product_name: str,
        category: str,
        target_audience: str,
        key_features: str,
        tone: str,
        num_copies: int = 5
    ) -> List[str]:
        """Hugging Face Inference API를 사용한 광고 문구 생성"""
        
        if not self.is_available():
            raise ValueError("Hugging Face API key is not configured")
        
        prompt = self._build_prompt(
            product_name, category, target_audience, key_features, tone, num_copies
        )
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 500,
                        "temperature": 0.8,
                        "top_p": 0.9
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Hugging Face API error: {response.text}")
                
                result = response.json()
                
                # OpenAI 호환 형식 응답 처리
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"Unexpected API response format: {result}")
                
                # 줄바꿈으로 분리하고 빈 줄 제거
                copies = [line.strip() for line in content.split('\n') if line.strip()]
                
                # 번호나 불릿 포인트 제거
                cleaned_copies = []
                for copy in copies:
                    # "1. ", "- ", "• " 등 제거
                    cleaned = copy.lstrip('0123456789.-•* ')
                    if cleaned:
                        cleaned_copies.append(cleaned)
                
                return cleaned_copies[:num_copies]
                
        except httpx.TimeoutException:
            raise Exception("Hugging Face API timeout - model may be loading. Please try again in a few seconds.")
        except Exception as e:
            error_msg = str(e)
            if "insufficient permissions" in error_msg.lower():
                raise Exception(
                    "Hugging Face 권한 오류: 선택한 모델이 무료가 아니거나 토큰 권한이 부족합니다. "
                    "Gemma-2B 또는 Llama-3.2-1B/3B 등을 시도해 보세요."
                )
            raise Exception(f"Hugging Face API error ({self.model}): {error_msg}")
