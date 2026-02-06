"""
AI for generating shopping mall product reviews.
Uses OpenAI's gpt-4o model via the chat.completions API.
"""
from openai import AsyncOpenAI
from ai.base import BaseAI
import os

class ProductReviewAI(BaseAI):
    """AI for generating product reviews."""
    
    def __init__(self, model: str = "gpt-4o"):
        super().__init__("openai", model)
        self.client = AsyncOpenAI(api_key=self.get_api_key())
        print(f"✅ [ProductReviewAI] Initialized: {model}")
    
    async def generate_product_review(
        self, 
        product_name: str, 
        sentiment: str, 
        pros: str = "", 
        cons: str = "", 
        length: int = 500,
        language: str = "ko"
    ) -> str:
        """
        Generates a product review.
        
        Args:
            product_name (str): The name of the product.
            sentiment (str): The overall sentiment of the review ("good" or "bad").
            pros (str): Comma-separated list of pros.
            cons (str): Comma-separated list of cons.
            length (int): Desired length of the review (e.g., 50, 500, 1000 characters).
            language (str): The desired language for the reply (e.g., "ko" for Korean, "en" for English).
            
        Returns:
            str: The AI-generated product review.
        """
        
        sentiment_description = "긍정적인" if sentiment == "good" else "부정적인"
        
        system_prompt = f"""당신은 쇼핑몰 제품 리뷰를 작성하는 AI 어시스턴트입니다.
        
        다음 지침을 따르세요:
        1. 지정된 제품에 대해 {sentiment_description} 관점에서 리뷰를 작성합니다.
        2. 제공된 장점과 단점을 자연스럽게 포함합니다.
        3. 리뷰는 약 {length}자 정도로 작성합니다.
        4. 리뷰는 {language} 언어로 작성합니다.
        5. 진정성 있고 설득력 있는 문체를 사용합니다.
        """
        
        user_prompt = f"제품명: {product_name}\n"
        if pros:
            user_prompt += f"장점: {pros}\n"
        if cons:
            user_prompt += f"단점: {cons}\n"
        user_prompt += f"이 제품에 대한 {sentiment_description} 리뷰를 작성해 주세요."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=int(length * 1.5),  # Allow some buffer for token calculation
                temperature=0.7  # Moderate creativity
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating product review: {e}")
            return "제품 리뷰 생성 중 오류가 발생했습니다. 다시 시도해주세요."
            
    async def generate(self, **kwargs):
        """
        Generic generate method for compatibility with base.py,
        though generate_product_review is the primary method for this class.
        """
        return await self.generate_product_review(
            product_name=kwargs.get("product_name", ""),
            sentiment=kwargs.get("sentiment", "good"),
            pros=kwargs.get("pros", ""),
            cons=kwargs.get("cons", ""),
            length=kwargs.get("length", 500),
            language=kwargs.get("language", "ko"),
        )
