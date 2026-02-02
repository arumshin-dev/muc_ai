"""
Hugging Face Inference API Service
Hugging Face Inference API를 사용한 광고 문구 생성 (무료)
"""
from typing import List
import httpx
from fastapi import HTTPException
from services.ai_provider_base import AIProviderBase


class HuggingFaceService(AIProviderBase):
    """Hugging Face Inference API 광고 문구 생성 서비스"""
    
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.2-3B-Instruct"):
        super().__init__(api_key, model)
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
            raise HTTPException(
                status_code=400,
                detail="Hugging Face API 키가 설정되지 않았습니다."
            )
        
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
                
                # 에러 응답 상세 처리
                if response.status_code != 200:
                    error_body = response.text
                    
                    # 모델 지원 안 됨
                    if "model_not_supported" in error_body or "not found" in error_body.lower():
                        raise HTTPException(
                            status_code=400,
                            detail=f"선택한 모델({self.model})은 Hugging Face Router에서 지원되지 않습니다. Llama-3.2-3B 또는 Llama-3.1-8B를 시도해주세요."
                        )
                    
                    # 권한 오류 (Gemma 등 유료/제한 모델)
                    if "insufficient permissions" in error_body.lower() or response.status_code == 402:
                        raise HTTPException(
                            status_code=403,
                            detail=f"모델({self.model}) 접근 권한이 없습니다. Gemma 모델은 현재 제한될 수 있습니다. Llama 계열 모델을 선택해주세요."
                        )
                    
                    # Rate limit
                    if response.status_code == 429:
                        raise HTTPException(
                            status_code=429,
                            detail="Hugging Face API 요청 한도 초과. 잠시 후 다시 시도하거나 다른 모델을 선택해주세요."
                        )
                    
                    # 기타 에러
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Hugging Face API 오류: {error_body}"
                    )
                
                result = response.json()
                
                # OpenAI 호환 형식 응답 처리
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"예상치 못한 응답 형식: {result}"
                    )
                
                # 후처리
                return self._post_process(content, num_copies)
                
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Hugging Face API 타임아웃. 모델 로딩 중일 수 있습니다. 몇 초 후 다시 시도해주세요."
            )
        except HTTPException:
            # 이미 처리된 HTTPException은 그대로 전달
            raise
        except Exception as e:
            error_msg = str(e)
            raise HTTPException(
                status_code=500,
                detail=f"Hugging Face 처리 중 오류: {error_msg}"
            )
    
    def _post_process(self, content: str, num_copies: int) -> List[str]:
        """응답 텍스트를 광고 문구 리스트로 변환"""
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
