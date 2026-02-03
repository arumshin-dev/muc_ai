"""
Google Gemini Text Generator
google.genai.Client 사용 (새 방식)
"""
from google.genai import Client
from google.genai.errors import ClientError
from ai.base import TextGeneratorAI


class GeminiText(TextGeneratorAI):
    """Google Gemini 텍스트 생성"""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        super().__init__("gemini", model)
        self.client = Client(api_key=self.get_api_key())
        print(f"✅ [Gemini] Initialized: {model}")
    
    async def generate_text(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """텍스트 생성"""
        try:
            # Chat 세션 생성
            chat = self.client.chats.create(model=self.model)
            
            # 메시지 구성
            messages = []
            if system_prompt:
                messages.append(system_prompt)
            messages.append(prompt)
            
            # 메시지 전송
            result = chat.send_message(
                message=messages,
                config={
                    "max_output_tokens": kwargs.get("max_tokens", 1000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
            )
            
            # 응답 파싱
            return self._extract_text(result)
        
        except ClientError as e:
            error_msg = str(e)
            
            if "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                raise Exception("Gemini API 무료 사용량 초과")
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                raise Exception("Gemini API 요청 한도 초과")
            elif "SAFETY" in error_msg:
                raise Exception("Gemini 안전 정책 차단")
            else:
                raise Exception(f"Gemini API 오류: {error_msg}")
    
    def _extract_text(self, resp) -> str:
        """Gemini 응답에서 텍스트 추출"""
        if not getattr(resp, "candidates", None):
            raise Exception("Gemini 응답에 candidates 없음")
        
        candidate = resp.candidates[0]
        content = getattr(candidate, "content", None)
        
        if not content:
            raise Exception("Gemini 응답에 content 없음")
        
        parts = getattr(content, "parts", None)
        if not parts:
            raise Exception("Gemini 응답에 parts 없음")
        
        text = getattr(parts[0], "text", None)
        if not text:
            raise Exception("Gemini 응답에 text 없음")
        
        return text
    
    async def generate(self, **kwargs):
        return await self.generate_text(
            prompt=kwargs.get("prompt"),
            system_prompt=kwargs.get("system_prompt"),
            **kwargs
        )
