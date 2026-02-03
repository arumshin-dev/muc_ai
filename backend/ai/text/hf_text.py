"""
HuggingFace Text Generator
Router API (/v1/chat/completions) 사용
"""
import httpx
from ai.base import TextGeneratorAI


class HuggingFaceText(TextGeneratorAI):
    """HuggingFace Router API 텍스트 생성"""
    
    def __init__(self, model: str = "meta-llama/Llama-3.2-3B-Instruct"):
        super().__init__("huggingface", model)
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.get_api_key()}",
            "Content-Type": "application/json"
        }
        print(f"✅ [HuggingFace] Initialized: {model}")
    
    async def generate_text(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """텍스트 생성"""
        
        # 메시지 구성
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": kwargs.get("max_tokens", 1000),
                        "temperature": kwargs.get("temperature", 0.7),
                        "top_p": kwargs.get("top_p", 0.9)
                    }
                )
                
                # 에러 처리
                if response.status_code != 200:
                    error_body = response.text
                    
                    if "model_not_supported" in error_body or "not found" in error_body.lower():
                        raise Exception(f"모델 {self.model}은 지원되지 않습니다")
                    elif "insufficient permissions" in error_body.lower() or response.status_code == 402:
                        raise Exception(f"모델 {self.model} 접근 권한 없음")
                    elif response.status_code == 429:
                        raise Exception("HuggingFace API 요청 한도 초과")
                    else:
                        raise Exception(f"HuggingFace API 오류: {error_body}")
                
                # 응답 파싱 (OpenAI 호환 형식)
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"예상치 못한 응답 형식: {result}")
        
        except httpx.TimeoutException:
            raise Exception("HuggingFace API 타임아웃. 모델 로딩 중일 수 있습니다.")
        except Exception as e:
            raise Exception(f"HuggingFace 처리 중 오류: {str(e)}")
    
    async def generate(self, **kwargs):
        return await self.generate_text(
            prompt=kwargs.get("prompt"),
            system_prompt=kwargs.get("system_prompt"),
            **kwargs
        )
