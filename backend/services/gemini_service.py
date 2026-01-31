"""
Google Gemini Service
Google Gemini API를 사용한 광고 문구 생성 (무료 티어-gemini-pro)
root@c947fb25e528:/app# python - <<'PY'
from google.genai import Client

client = Client(api_key="[ENCRYPTION_KEY]")
models = client.models.list()
print([m.name for m in models])
PY
['models/gemini-2.5-flash', 'models/gemini-2.5-pro', 'models/gemini-2.0-flash', 'models/gemini-2.0-flash-001', 
'models/gemini-2.0-flash-exp-image-generation', 'models/gemini-2.0-flash-lite-001', 'models/gemini-2.0-flash-lite', 'models/gemini-exp-1206', 
'models/gemini-2.5-flash-preview-tts', 'models/gemini-2.5-pro-preview-tts', 
'models/gemma-3-1b-it', 'models/gemma-3-4b-it', 'models/gemma-3-12b-it', 'models/gemma-3-27b-it', 'models/gemma-3n-e4b-it', 'models/gemma-3n-e2b-it', 
'models/gemini-flash-latest', 'models/gemini-flash-lite-latest', 'models/gemini-pro-latest', 'models/gemini-2.5-flash-lite', 'models/gemini-2.5-flash-image', 'models/gemini-2.5-flash-preview-09-2025', 'models/gemini-2.5-flash-lite-preview-09-2025', 'models/gemini-3-pro-preview', 'models/gemini-3-flash-preview', 'models/gemini-3-pro-image-preview', 'models/nano-banana-pro-preview', 'models/gemini-robotics-er-1.5-preview', 'models/gemini-2.5-computer-use-preview-10-2025', 'models/deep-research-pro-preview-12-2025', 'models/embedding-001', 'models/text-embedding-004', 'models/gemini-embedding-001', 'models/aqa', 'models/imagen-4.0-generate-preview-06-06', 'models/imagen-4.0-ultra-generate-preview-06-06', 'models/imagen-4.0-generate-001', 'models/imagen-4.0-ultra-generate-001', 'models/imagen-4.0-fast-generate-001', 'models/veo-2.0-generate-001', 'models/veo-3.0-generate-001', 'models/veo-3.0-fast-generate-001', 'models/veo-3.1-generate-preview', 'models/veo-3.1-fast-generate-preview', 'models/gemini-2.5-flash-native-audio-latest', 'models/gemini-2.5-flash-native-audio-preview-09-2025', 'models/gemini-2.5-flash-native-audio-preview-12-2025']
"""

from typing import List
from google.genai import Client
from services.ai_provider_base import AIProviderBase
import asyncio
def extract_text_from_gemini(resp):
    # candidates 존재 여부 확인
    if not getattr(resp, "candidates", None):
        raise Exception("Gemini 응답에서 candidates를 찾을 수 없습니다.")

    candidate = resp.candidates[0]

    # content 존재 여부 확인
    content = getattr(candidate, "content", None)
    if not content:
        raise Exception("Gemini 응답에서 content를 찾을 수 없습니다.")

    # parts 존재 여부 확인
    parts = getattr(content, "parts", None)
    if not parts:
        raise Exception("Gemini 응답에서 parts를 찾을 수 없습니다.")

    # text 추출
    text = getattr(parts[0], "text", None)
    if not text:
        raise Exception("Gemini 응답에서 텍스트를 찾을 수 없습니다.")

    # return text
    return resp.candidates[0].content.parts[0].text

class GeminiService(AIProviderBase):
    """Google Gemini 광고 문구 생성 서비스"""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
    # def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        super().__init__(api_key, model)
        self.client = Client(api_key=api_key)

    def is_available(self) -> bool:
        """API 키 유효성 확인"""
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
        """Gemini를 사용한 광고 문구 생성"""

        if not self.is_available():
            raise ValueError("Gemini API key is not configured")

        prompt = self._build_prompt(
            product_name, category, target_audience, key_features, tone, num_copies
        )

        resp = self.client.chats.create(model=self.model)
        

        result = resp.send_message(
            message=[
                "당신은 광고 문구 작성 전문가입니다.",
                prompt
            ],
            config={"max_output_tokens": 500}
        )

        content = extract_text_from_gemini(result)
        return self._post_process(content, num_copies)
