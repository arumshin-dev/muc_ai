"""
OpenAI GPT-5 Text Generator
responses API 사용 (새로운 방식)
"""
from openai import AsyncOpenAI
from ai.base import TextGeneratorAI


class OpenAIGPT5(TextGeneratorAI):
    """OpenAI GPT-5 텍스트 생성 (responses)"""
    
    def __init__(self, model: str = "gpt-5-mini"):
        super().__init__("openai", model)
        self.client = AsyncOpenAI(api_key=self.get_api_key())
        print(f"✅ [OpenAI GPT-5] Initialized: {model}")
    
    async def generate_text(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """텍스트 생성 (GPT-5 responses API)"""
        
        # input 메시지 구성
        input_messages = []
        
        if system_prompt:
            input_messages.append({"role": "system", "content": system_prompt})
        
        input_messages.append({"role": "user", "content": prompt})
        
        # GPT-5 responses API 호출
        response = await self.client.responses.create(
            model=self.model,
            input=input_messages,
            max_output_tokens=kwargs.get("max_tokens", 1000),
            reasoning={"effort": kwargs.get("reasoning_effort", "minimal")}
        )
        
        # 응답 파싱
        return self._extract_text_from_response(response)
    
    def _extract_text_from_response(self, response) -> str:
        """GPT-5 response에서 텍스트 추출"""
        texts = []
        
        for item in response.output:
            # item.content 가져오기
            content = getattr(item, "content", None)
            if content is None and isinstance(item, dict):
                content = item.get("content")
            
            if not content:
                continue
            
            # content 안의 text 추출
            for c in content:
                c_type = getattr(c, "type", None)
                if c_type is None and isinstance(c, dict):
                    c_type = c.get("type")
                
                if c_type in ("output_text", "text"):
                    text = getattr(c, "text", None)
                    if text is None and isinstance(c, dict):
                        text = c.get("text")
                    
                    if text:
                        texts.append(text)
        
        result = "\n".join(texts)
        
        # 비었으면 fallback
        if not result.strip():
            return getattr(response, "output_text", "") or str(response)
        
        return result
    
    async def generate(self, **kwargs):
        return await self.generate_text(
            prompt=kwargs.get("prompt"),
            system_prompt=kwargs.get("system_prompt"),
            **kwargs
        )
