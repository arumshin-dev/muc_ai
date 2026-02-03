"""
AI Factory 테스트
"""
import asyncio
from ai.factory import TextAIFactory


async def test_openai_gpt4():
    """OpenAI GPT-4 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Testing OpenAI GPT-4")
    print("=" * 60)
    
    try:
        ai = TextAIFactory.create("openai", "gpt-4o")
        result = await ai.generate_text(
            prompt="Python Factory Pattern을 한 문장으로 설명해줘",
            system_prompt="당신은 전문 개발자입니다."
        )
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_openai_gpt5():
    """OpenAI GPT-5 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Testing OpenAI GPT-5")
    print("=" * 60)
    
    try:
        ai = TextAIFactory.create("openai", "gpt-5-mini")
        result = await ai.generate_text(
            prompt="Python Factory Pattern을 한 문장으로 설명해줘",
            system_prompt="당신은 전문 개발자입니다.",
            reasoning_effort="medium"
        )
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_gemini():
    """Gemini 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Testing Gemini")
    print("=" * 60)
    
    try:
        ai = TextAIFactory.create("gemini", "gemini-2.5-flash")
        result = await ai.generate_text(
            prompt="Python Factory Pattern을 한 문장으로 설명해줘",
            system_prompt="당신은 전문 개발자입니다."
        )
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_huggingface():
    """HuggingFace 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Testing HuggingFace")
    print("=" * 60)
    
    try:
        ai = TextAIFactory.create("huggingface", "meta-llama/Llama-3.2-3B-Instruct")
        result = await ai.generate_text(
            prompt="Python Factory Pattern을 한 문장으로 설명해줘",
            system_prompt="당신은 전문 개발자입니다."
        )
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_all():
    """모든 AI 제공자 테스트"""
    print("\n🚀 Starting AI Factory Tests...")
    
    # 순차 실행
    await test_openai_gpt4()
    await test_openai_gpt5()
    await test_gemini()
    await test_huggingface()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


async def test_cache():
    """캐시 테스트"""
    print("\n" + "=" * 60)
    print("🧪 Testing Cache")
    print("=" * 60)
    
    # 첫 번째 호출 (새로 생성)
    print("\n1️⃣ First call (should create new model)")
    ai1 = TextAIFactory.create("openai", "gpt-4o")
    
    # 두 번째 호출 (캐시 사용)
    print("\n2️⃣ Second call (should use cache)")
    ai2 = TextAIFactory.create("openai", "gpt-4o")
    
    # 같은 인스턴스인지 확인
    print(f"\n✅ Same instance? {ai1 is ai2}")
    
    # 캐시 초기화
    print("\n3️⃣ Clearing cache...")
    TextAIFactory.clear_cache()
    
    # 세 번째 호출 (다시 생성)
    print("\n4️⃣ Third call (should create new model after cache clear)")
    ai3 = TextAIFactory.create("openai", "gpt-4o")
    
    print(f"\n✅ Different instance after clear? {ai1 is not ai3}")


if __name__ == "__main__":
    # 실행할 테스트 선택
    import sys
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        
        if test_name == "gpt4":
            asyncio.run(test_openai_gpt4())
        elif test_name == "gpt5":
            asyncio.run(test_openai_gpt5())
        elif test_name == "gemini":
            asyncio.run(test_gemini())
        elif test_name == "hf":
            asyncio.run(test_huggingface())
        elif test_name == "cache":
            asyncio.run(test_cache())
        else:
            print(f"Unknown test: {test_name}")
            print("Available tests: gpt4, gpt5, gemini, hf, cache, all")
    else:
        # 인자 없으면 전체 테스트
        asyncio.run(test_all())
