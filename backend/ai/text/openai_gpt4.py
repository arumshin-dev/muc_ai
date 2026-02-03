"""
OpenAI GPT-4 Text Generator
chat.completions API 사용
"""
from openai import AsyncOpenAI
from ai.base import TextGeneratorAI


class OpenAIGPT4(TextGeneratorAI):
    """OpenAI GPT-4 텍스트 생성 (chat.completions)"""
    
    def __init__(self, model: str = "gpt-4o"):
        super().__init__("openai", model)
        self.client = AsyncOpenAI(api_key=self.get_api_key())
        print(f"✅ [OpenAI GPT-4] Initialized: {model}")
    
    async def generate_text(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """텍스트 생성"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7)
        )
        
        return response.choices[0].message.content
    
    async def generate(self, **kwargs):
        return await self.generate_text(
            prompt=kwargs.get("prompt"),
            system_prompt=kwargs.get("system_prompt"),
            **kwargs
        )
