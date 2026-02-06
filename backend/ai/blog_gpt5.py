'''
GPT-5를 사용한 블로그 글 생성을 위한 AI 모듈
'''
import os
import re
import asyncio
from openai import AsyncOpenAI
from config import settings

class BlogGPT5AI:
    '''GPT-5 모델을 사용하여 블로그 글을 생성하는 클래스'''
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY가 환경 변수에 설정되지 않았습니다.")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-5-mini"
        # self.internal_model_name = settings.OPENAI_DEFAULT_MODEL
        
        # ⭐️ 모델 이름 매핑: 내부용 이름을 실제 OpenAI 모델 이름으로 변환
        # self.model_mapping = {
        #     "gpt-5": "gpt-4o",
        #     "gpt-5-mini": "gpt-4o",
        #     "gpt-5-nano": "gpt-4o",
        # }
        # self.openai_model_name = self.model_mapping.get(self.internal_model_name, self.internal_model_name)
        self.templates = {
            "일반": {
                "tone": "친근하고 이해하기 쉬운",
                "structure": ["서론", "본문", "결론"],
                "length": {"짧음": 300, "중간": 600, "김": 1000}
            },
            "전문": {
                "tone": "전문적이고 신뢰성 있는",
                "structure": ["개요", "심층 분석", "사례 연구", "결론"],
                "length": {"짧음": 500, "중간": 1000, "김": 1500}
            },
            "캐주얼": {
                "tone": "가볍고 재미있는",
                "structure": ["도입", "이야기", "팁", "마무리"],
                "length": {"짧음": 250, "중간": 500, "김": 800}
            },
            "기술": {
                "tone": "기술적이고 상세한",
                "structure": ["문제 정의", "해결책", "구현", "결과"],
                "length": {"짧음": 400, "중간": 800, "김": 1200}
            },
            "마케팅": {
                "tone": "설득력 있고 매력적인",
                "structure": ["후크", "문제 제시", "해결책", "CTA"],
                "length": {"짧음": 350, "중간": 700, "김": 1000}
            }
        }
        
        self.length_configs = {
            "short": {"paragraphs": 2, "features": 2},
            "medium": {"paragraphs": 3, "features": 3},
            "long": {"paragraphs": 4, "features": 4}
        }
    
    def generate_features(self, topic: str, count: int):
        """주제에 대한 특징 생성"""
        feature_templates = [
            f"{topic}의 핵심 원리",
            f"{topic}의 실제 적용 사례",
            f"{topic}의 장점과 단점",
            f"{topic}의 미래 전망",
            f"{topic} 관련 최신 동향",
            f"{topic}의 기술적 특징",
            f"{topic}의 사회적 영향",
            f"{topic}의 실습 방법"
        ]
        return feature_templates[:count]
    
    async def generate_blog_post(self, topic: str, style: str, length: str):
        '''비동기적으로 GPT-5 블로그 글을 생성합니다.'''
        try:
            template = self.templates.get(style, self.templates["일반"])
            target_length = template["length"].get(length, 600)
            
            prompt = f"""
            다음 조건에 맞춰 SEO에 최적화된 블로그 글을 한국어로 작성해주세요:
            주제: {topic}
            스타일: {style} ({template['tone']} 톤)
            길이: 약 {target_length}자
            구조: {', '.join(template['structure'])}
            요구사항:
            - SEO에 최적화된, 흥미를 끄는 제목
            - 독자의 시선을 사로잡는 명확한 도입부
            - 실질적이고 가치있는 정보를 담은 본문
            - 내용을 요약하고 행동을 유도하는 명확한 결론 및 콜투액션
            - 주제와 관련된 해시태그 5개 포함
            응답 형식 (반드시 이 형식을 지켜주세요):
            제목: [여기에 제목 작성]
            
            [여기에 본문 내용 작성]
            
            해시태그: #태그1 #태그2 #태그3 #태그4 #태그5
            """
            
            # GPT-5 responses API 호출
            response = await self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": f"당신은 {template['tone']} 블로그 작가입니다. 독자에게 가치 있는 정보를 제공하고, 검색 엔진에 최적화된 글을 작성하세요."},
                    {"role": "user", "content": prompt}
                ],
                max_output_tokens=min(target_length * 2, 2000),
                reasoning={"effort": "minimal"}
            )
            
            # GPT-5 응답에서 텍스트 추출
            content = self._extract_text_from_response(response)
            
            # 결과 파싱
            lines = content.split('\n')
            title = ""
            body = ""
            hashtags = ""
            
            current_section = "title"
            body_lines = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("제목:"):
                    title = line.replace("제목:", "").strip()
                    current_section = "body"
                elif line.startswith("해시태그:"):
                    hashtags = line.replace("해시태그:", "").strip()
                    current_section = "hashtags"
                elif line and current_section == "body":
                    body_lines.append(line)
                elif line and current_section == "hashtags":
                    hashtags += " " + line
            
            body = '\n\n'.join(body_lines)
            
            return {
                "title": title or f"{topic}에 대한 완벽한 가이드",
                "content": body or content,
                "hashtags": hashtags or f"#{topic.replace(' ', '')} #블로그 #정보 #가이드 #팁",
                "style": style,
                "length": length,
                "word_count": len(body.split()),
                # ⭐️ UI에는 내부 모델 이름을 표시
                "model_used": self.model 
            }
            
        except Exception as e:
            print(f"GPT-5 블로그 생성 중 오류 발생: {e}")
            return self._generate_fallback_blog(topic, style, length, str(e))
    
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
    
    def generate_blog_post_sync(self, topic: str, style: str, length: str):
        """동기 버전 (FastAPI 호환)"""
        return asyncio.run(self.generate_blog_post(topic, style, length))
  
    def _generate_fallback_blog(self, topic: str, style: str, length: str, error_message: str):
        '''API 오류 시 대체 템플릿 방식'''
        template = self.templates.get(style, self.templates["일반"])
        
        title = f"{topic}에 대한 완벽한 가이드"
        
        introduction = f"{topic}에 대해 알아보겠습니다. 이 글에서는 {template['tone']} 방식으로 {topic}의 핵심 내용을 다룹니다."
        
        features = self.generate_features(topic, 3)
        body_content = "\n\n".join([f"## {feature}\n{topic}와 관련된 중요한 내용입니다." for feature in features])
        
        conclusion = f"이상으로 {topic}에 대해 알아보았습니다. 궁금한 점이 있다면 언제든지 문의해주세요."
        
        content = f"{introduction}\n\n{body_content}\n\n{conclusion}"
        
        return {
            "error": f"GPT-5 블로그 생성 중 오류 발생: {error_message}",
            "title": title,
            "content": content,
            "topic": topic,
            "style": style,
            "length": length,
            "word_count": len(content.replace(" ", ""))
        }