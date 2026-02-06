'''
블로그 글 생성을 위한 GPT-4 AI 모듈
'''
import os
import re
from openai import AsyncOpenAI
from config import settings # ⭐️ 경로 수정

class BlogGPT4AI:
    '''GPT-4o 모델을 사용하여 SEO 최적화 블로그 글을 생성하는 클래스'''
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_GPT4_API_KEY가 환경 변수에 설정되지 않았습니다.")
        
        self.model = "gpt-4o-mini"
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        self.templates = {
            "일반": {"tone": "친근하고 이해하기 쉬운", "structure": ["서론", "본문", "결론"], "length": {"짧음": 300, "중간": 600, "김": 1000}},
            "전문": {"tone": "전문적이고 신뢰성 있는", "structure": ["개요", "심층 분석", "사례 연구", "결론"], "length": {"짧음": 500, "중간": 1000, "김": 1500}},
            "캐주얼": {"tone": "가볍고 재미있는", "structure": ["도입", "이야기", "팁", "마무리"], "length": {"짧음": 250, "중간": 500, "김": 800}},
            "기술": {"tone": "기술적이고 상세한", "structure": ["문제 정의", "해결책", "구현", "결과"], "length": {"짧음": 400, "중간": 800, "김": 1200}},
            "마케팅": {"tone": "설득력 있고 매력적인", "structure": ["후크", "문제 제시", "해결책", "CTA"], "length": {"짧음": 350, "중간": 700, "김": 1000}}
        }

    async def generate_seo_blog(self, keyword: str, style: str = "일반", length: str = "중간"):
        '''비동기적으로 SEO 블로그 글을 생성합니다.'''
        try:
            template = self.templates.get(style, self.templates["일반"])
            target_length = template["length"].get(length, 600)
            
            prompt = f"""
            You are a Korean SEO blog expert.
            Write a HIGH QUALITY Naver SEO optimized blog post.
            Keyword: {keyword}
            Style: {style} ({template['tone']} 톤)
            Length: 약 {target_length}자
            Requirements:
            - Write in Korean
            - Minimum {target_length} characters
            - Natural keyword usage
            - Catchy title
            - Use headings (H2, H3)
            - {template['tone']} tone
            - Avoid AI detection style
            - Add intro + body + conclusion
            - Format in HTML
            - Include meta description
            - Add 5 relevant hashtags in Korean
            Structure: {", ".join(template['structure'])}
            Your response MUST be a single HTML document structure like this:
            <!DOCTYPE html>
            <html>
            <head>
                <title>[Your Title Here]</title>
                <meta name="description" content="[Your Meta Description Here]">
            </head>
            <body>
                <h2>...</h2>
                <p>...</p>
                <h3>...</h3>
                <p>...</p>
                <div class="hashtags">
                    <span>#해시태그1</span>
                    <span>#해시태그2</span>
                    <span>#해시태그3</span>
                    <span>#해시태그4</span>
                    <span>#해시태그5</span>
                </div>
            </body>
            </html>
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Korean SEO blogger. Your task is to write a high-quality blog post optimized for Naver search. You must follow all user requirements precisely."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=min(target_length * 3, 4000),
                temperature=0.75,
                top_p=1.0,
            )
            
            content = response.choices[0].message.content.strip()
            
            title = self._extract_from_tag(content, 'title')
            meta_description = self._extract_meta_description(content)
            body = self._extract_body(content)
            hashtags = self._extract_hashtags(content)
            
            return {
                "title": title or f"{keyword}에 대한 모든 것",
                "metaDescription": meta_description or f"{keyword}에 대해 자세히 알아보고 전문가가 되세요.",
                "content": body,
                "hashtags": hashtags or [keyword.replace(' ', ''), "꿀팁", "정보"],
                "wordCount": len(re.sub('<[^>]+>', '', body).split()),
                "model": self.model,
                "style": style
            }
            
        except Exception as e:
            print(f"블로그 생성 중 오류 발생: {e}")
            raise e

    def _extract_from_tag(self, html_content: str, tag: str) -> str:
        '''HTML에서 특정 태그의 내용을 추출합니다.'''
        match = re.search(fr'<{tag}[^>]*>(.*?)</{tag}>', html_content, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""

    def _extract_meta_description(self, html_content: str) -> str:
        '''HTML에서 메타 설명을 추출합니다.'''
        match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html_content, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _extract_body(self, html_content: str) -> str:
        '''HTML에서 body 내용을 추출합니다.'''
        match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if match:
            body_content = match.group(1)
            body_content = re.sub(r'<div[^>]*class=["\']hashtags["\'][^>]*>.*?</div>', '', body_content, flags=re.DOTALL | re.IGNORECASE).strip()
            return body_content
        return html_content

    def _extract_hashtags(self, html_content: str) -> list[str]:
        '''HTML에서 해시태그 목록을 추출합니다.'''
        tags = []
        div_match = re.search(r'<div[^>]*class=["\']hashtags["\'][^>]*>(.*?)</div>', html_content, re.DOTALL | re.IGNORECASE)
        if div_match:
            span_matches = re.findall(r'<span[^>]*>(.*?)</span>', div_match.group(1), re.IGNORECASE)
            tags = [tag.strip().lstrip('#') for tag in span_matches]
        return tags
