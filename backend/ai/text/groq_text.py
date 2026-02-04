"""
Groq Text Generator
"""
import os
from groq import Groq
from ai.base import TextGeneratorAI


class GroqText(TextGeneratorAI):
    """Groq AI Provider (무료)"""
    
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        super().__init__("groq", model)
        self.client = Groq(api_key=self.get_api_key())
        print(f"✅ [Groq] Initialized: {model}")
    
    async def generate_text(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """텍스트 생성"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # 동기 방식으로 호출 (stream=False)
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 1),
                max_completion_tokens=kwargs.get("max_tokens", 1024),
                top_p=kwargs.get("top_p", 1),
                stream=False  # 스트리밍 비활성화
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Groq API 오류: {e}")

    async def generate(self, **kwargs):
        prompt = kwargs.pop("prompt", "")
        system_prompt = kwargs.pop("system_prompt", None)
        
        return await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs
        )
