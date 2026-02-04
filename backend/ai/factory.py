"""
AI Factory - 텍스트 생성 AI 관리
"""
from ai.base import TextGeneratorAI


class TextAIFactory:
    """텍스트 AI Factory"""
    
    _cache = {}  # 모델 캐시
    
    @staticmethod
    def create(provider: str, model: str) -> TextGeneratorAI:
        """
        텍스트 AI 생성
        
        Examples:
            # OpenAI
            - TextAIFactory.create('openai', 'gpt-4o')           # GPT-4
            - TextAIFactory.create('openai', 'gpt-5-mini')       # GPT-5
            - TextAIFactory.create('openai', 'gpt-5-nano')       # GPT-5
            - TextAIFactory.create('openai', 'gpt-5')

            # Gemini
            - TextAIFactory.create('gemini', 'gemini-2.5-flash')
            - TextAIFactory.create('gemini', 'gemini-2.5-pro')
            
            # HuggingFace
            - TextAIFactory.create('huggingface', 'meta-llama/Llama-3.2-3B-Instruct')
            - TextAIFactory.create('huggingface', 'meta-llama/Llama-3.1-8B-Instruct')
            
            # Groq
            - TextAIFactory.create('groq', 'llama-3.3-70b-versatile')
            - TextAIFactory.create('groq', 'deepseek-r1-distill-llama-70b')
        """
        cache_key = f"{provider}:{model}"
        
        if cache_key in TextAIFactory._cache:
            print(f"♻️  [Factory] Cached: {cache_key}")
            return TextAIFactory._cache[cache_key]
        
        print(f"🏭 [Factory] Creating: {cache_key}")
        
        if provider == "openai":
            # GPT-5 vs GPT-4 구분
            if model.startswith("gpt-5"):
                from ai.text.openai_gpt5 import OpenAIGPT5
                ai = OpenAIGPT5(model=model)
            else:
                from ai.text.openai_gpt4 import OpenAIGPT4
                ai = OpenAIGPT4(model=model)
        
        elif provider == "gemini":
            from ai.text.gemini_text import GeminiText
            ai = GeminiText(model=model)
        
        elif provider == "huggingface":
            from ai.text.hf_text import HuggingFaceText
            ai = HuggingFaceText(model=model)
        
        elif provider == "groq":
            from ai.text.groq_text import GroqText
            ai = GroqText(model=model)
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        TextAIFactory._cache[cache_key] = ai
        return ai
    
    @staticmethod
    def clear_cache():
        """캐시 초기화"""
        TextAIFactory._cache.clear()
        print("🗑️  [Factory] Cache cleared")
