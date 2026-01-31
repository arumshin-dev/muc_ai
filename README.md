# MUC AI - 소상공인 광고 콘텐츠 생성 서비스

생성형 AI 기술을 활용하여 소상공인이 광고 콘텐츠를 손쉽게 제작할 수 있도록 하는 서비스입니다.

## 🎯 프로젝트 목표

디자인 역량이나 전문 도구 없이도 제품 이미지, 배너, 광고 문구 같은 콘텐츠를 자동으로 생성하여, 오프라인 중심의 사업자들이 온라인 마케팅에 쉽게 진입할 수 있도록 합니다.

## ✨ 주요 기능

### 현재 제공 (v1.0)
- ✅ **광고 문구 생성**: AI가 제품 특징을 분석하여 매력적인 광고 문구 자동 생성
  - 제품명, 카테고리, 타겟 고객, 핵심 특징 입력
  - 톤 선택 (친근한/전문적인/유머러스한)
  - 여러 버전의 문구 동시 생성
  - 클립보드 복사 기능

### 준비 중
- 🎨 **제품 이미지 생성**: 제품 설명만으로 전문적인 이미지 생성
- 🖼️ **배너 디자인**: SNS, 웹사이트용 배너 자동 디자인
- 📋 **메뉴판 제작**: 음식점, 카페를 위한 메뉴판 간편 제작

## 🤖 지원 AI 모델

### OpenAI
- gpt-5, gpt-5-mini, gpt-5-nano
- gpt-4o, gpt-4o-mini
- gpt-3.5-turbo

### Hugging Face (무료)
- meta-llama/Llama-3.3-70B-Instruct
- meta-llama/Llama-3.1-8B-Instruct

### Google Gemini (무료 티어)
- gemini-1.5-flash
- gemini-1.5-pro

**특징:**
- 사용자가 직접 AI 제공자와 모델 선택 가능
- 자동 폴백: 기본 키 실패 시 다른 제공자로 자동 전환
- 사용자 API 키 입력 지원 (선택사항)

## 🏗️ 기술 스택

### Backend
- **FastAPI** 0.109.0 - 고성능 Python 웹 프레임워크
- **SQLAlchemy** 2.0.25 - ORM
- **PostgreSQL** 15 - 데이터베이스
- **OpenAI** 1.54.0 - OpenAI API 클라이언트
- **httpx** 0.27.0 - HTTP 클라이언트 (Hugging Face API용)
- **Google Generative AI** 0.8.3 - Gemini API 클라이언트

### Frontend
- **Next.js** 14 - React 프레임워크 (App Router)
- **TypeScript** - 타입 안전성
- **CSS** - 모던 스타일링 (Glassmorphism, Gradients, Animations)

### Infrastructure
- **Docker** & **Docker Compose** - 컨테이너화
- **PostgreSQL** - 데이터 저장
- **Jupyter Notebook** - 실험용 (dev 프로필)

## 📁 프로젝트 구조

```
muc_ai/
├── backend/              # FastAPI 백엔드
│   ├── config.py        # 환경 변수 설정
│   ├── database.py      # 데이터베이스 연결
│   ├── main.py          # FastAPI 앱
│   ├── requirements.txt # Python 의존성
│   ├── models/          # SQLAlchemy 모델
│   ├── schemas/         # Pydantic 스키마
│   ├── services/        # 비즈니스 로직
│   │   ├── ai_provider_base.py
│   │   ├── openai_service.py
│   │   ├── groq_service.py
│   │   ├── gemini_service.py
│   │   ├── ai_factory.py
│   │   └── ad_copy_service.py
│   └── routers/         # API 엔드포인트
├── frontend/            # Next.js 프론트엔드
│   ├── app/
│   │   ├── components/  # React 컴포넌트
│   │   ├── ad-copy/     # 광고 문구 생성 페이지
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── package.json
├── .env.example         # 환경 변수 템플릿
├── .env                 # 환경 변수 (gitignore)
└── docker-compose.yml   # Docker Compose 설정
```

## 🚀 시작하기

### 사전 요구사항
- Docker
- Docker Compose

### 1. 환경 설정

`.env` 파일 생성 (`.env.example` 참고):

```bash
# 최소 하나의 AI 제공자 API 키 필요
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# 기본 제공자 설정
DEFAULT_AI_PROVIDER=huggingface
AI_PROVIDER_FALLBACK_ORDER=huggingface,gemini,openai
```

### 2. Docker Compose로 실행

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

### 3. 서비스 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **Jupyter** (dev 프로필): http://localhost:8888

## 📖 API 엔드포인트

### 광고 문구 생성
- `POST /api/ad-copy/generate` - 광고 문구 생성
- `GET /api/ad-copy/history` - 생성 이력 조회
- `GET /api/ad-copy/{id}` - 특정 문구 조회

### 시스템
- `GET /` - 루트 엔드포인트
- `GET /health` - 헬스 체크
- `GET /api/providers` - 사용 가능한 AI 제공자 목록

## 💡 사용 예시

### 광고 문구 생성

1. http://localhost:3000/ad-copy 접속
2. 제품 정보 입력:
   - 제품명: "수제 햄버거"
   - 카테고리: "음식점"
   - 타겟 고객: "20-30대 직장인"
   - 핵심 특징: "100% 국내산 소고기, 수제 패티, 신선한 야채"
   - 톤: "친근한"
3. "광고 문구 생성하기" 클릭
4. 생성된 여러 버전의 광고 문구 확인
5. 원하는 문구 복사 버튼 클릭

## 🎨 디자인 특징

- **다크 테마**: 눈의 피로를 줄이는 어두운 배경
- **글래스모피즘**: 반투명 배경 + 블러 효과
- **그라디언트**: 보라-파랑 계열의 모던한 색상
- **애니메이션**: 부드러운 페이드인, 호버 효과
- **반응형**: 모바일, 태블릿, 데스크톱 최적화

## 🔧 개발 모드

Docker Compose는 개발 모드로 설정되어 있어 코드 변경 시 자동으로 재시작됩니다.

- **백엔드**: `--reload` 옵션으로 Uvicorn 실행
- **프론트엔드**: Next.js 개발 서버 (`npm run dev`)

## 📝 라이선스

MIT

## 🤝 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 📧 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.
