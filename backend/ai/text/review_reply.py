"""
AI for generating replies to customer reviews.
Uses OpenAI's gpt-4o model via the chat.completions API.
"""
from openai import AsyncOpenAI
from ai.base import BaseAI
import os

class ReviewReplyAI(BaseAI):
    """AI for generating replies to customer reviews."""
    
    def __init__(self, model: str = "gpt-4o"):
        super().__init__("openai", model)
        self.client = AsyncOpenAI(api_key=self.get_api_key())
        print(f"✅ [ReviewReplyAI] Initialized: {model}")
    
    async def generate_reply(self, customer_review: str, tone: str = "neutral", language: str = "ko") -> str:
        """
        Generates a reply to a customer review.
        
        Args:
            customer_review (str): The text of the customer's review.
            tone (str): The desired tone for the reply (e.g., "formal", "friendly", "apologetic", "grateful").
            language (str): The desired language for the reply (e.g., "ko" for Korean, "en" for English).
            
        Returns:
            str: The AI-generated reply.
        """
        system_prompt = f"""당신은 상점 주인의 입장에서 고객 리뷰에 대한 답글을 작성하는 AI 어시스턴트입니다.
        
        다음 지침을 따르세요:
        1. 고객의 리뷰 내용을 이해하고, 긍정적인지 부정적인지 파악합니다.
        2. {tone} 톤으로 답글을 작성합니다.
        3. 답글은 {language} 언어로 작성합니다.
        4. 긍정적인 리뷰에는 감사함을 표현하고, 부정적인 리뷰에는 공감과 사과, 그리고 문제 해결 의지를 보여줍니다.
        5. 답글은 너무 길지 않게, 진정성 있고 간결하게 작성합니다.
        """
        
        user_prompt = f'고객 리뷰: """{customer_review}"""\n\n이 리뷰에 대한 상점 주인의 답글을 작성해 주세요.'
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,  # Limit reply length
                temperature=0.7  # Moderate creativity
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating review reply: {e}")
            return "답글 생성 중 오류가 발생했습니다. 다시 시도해주세요."
            
    async def generate(self, **kwargs):
        """
        Generic generate method for compatibility with base.py,
        though generate_reply is the primary method for this class.
        """
        return await self.generate_reply(
            customer_review=kwargs.get("customer_review", ""),
            tone=kwargs.get("tone", "neutral"),
            language=kwargs.get("language", "ko"),
        )
