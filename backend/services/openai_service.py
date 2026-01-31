"""
OpenAI Service
OpenAI API를 사용한 광고 문구 생성 (GPT-4 / GPT-5 혼합 운영)
"""
from typing import List
from openai import AsyncOpenAI
from services.ai_provider_base import AIProviderBase


class OpenAIService(AIProviderBase):
    """OpenAI 광고 문구 생성 서비스"""

    def __init__(self, api_key: str, model: str = "gpt-5-nano"):
        super().__init__(api_key, model)
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None

    def is_available(self) -> bool:
        return bool(self.api_key and self.client)

    async def generate_ad_copies(
        self,
        product_name: str,
        category: str,
        target_audience: str,
        key_features: str,
        tone: str,
        num_copies: int = 5
    ) -> List[str]:

        if not self.is_available():
            raise ValueError("OpenAI API key is not configured")

        prompt = self._build_prompt(
            product_name, category, target_audience, key_features, tone, num_copies
        )

        try:
            if self._is_gpt5():
                content = await self._generate_with_responses(prompt)
            else:
                content = await self._generate_with_chat(prompt)

            return self._post_process(content, num_copies)

        except Exception as e:
            raise Exception(f"OpenAI API error ({self.model}): {str(e)}")

    # ========================
    # 내부 메서드
    # ========================

    def _is_gpt5(self) -> bool:
        return self.model.startswith("gpt-5")

    async def _generate_with_chat(self, prompt: str) -> str:
        """GPT-4 계열"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 소상공인을 위한 전문 광고 문구 작성가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content

    async def _generate_with_responses(self, prompt: str) -> str:
        """GPT-5 계열 (공식 방식)"""
        response = await self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": "당신은 소상공인을 위한 전문 광고 문구 작성가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_output_tokens=700,
            reasoning={"effort": "minimal"},
        )
        # print(response)

        content = self._extract_text_from_response(response)

        # 출력이 비었으면, 디버깅용 raw 출력도 반환하도록
        if not content.strip():
            return getattr(response, "output_text", "") or str(response)

        return content

    def _extract_text_from_response(self, response) -> str:
        texts = []

        for item in response.output:
            # item이 객체면 getattr, dict면 get
            content = getattr(item, "content", None)
            if content is None and isinstance(item, dict):
                content = item.get("content")

            if not content:
                continue

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

        return "\n".join(texts)

    def _post_process(self, content: str, num_copies: int) -> List[str]:
        """응답 정리"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        cleaned = []
        for line in lines:
            text = line.lstrip('0123456789.-•* ')
            if text:
                cleaned.append(text)

        return cleaned[:num_copies]
