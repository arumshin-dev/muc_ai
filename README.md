# MUC AI

FastAPI 백엔드와 Next.js 프론트엔드로 구성된 풀스택 애플리케이션입니다.

## 프로젝트 구조

```
muc_ai/
├── backend/              # FastAPI 백엔드
│   ├── main.py          # FastAPI 애플리케이션
│   ├── requirements.txt # Python 의존성
│   ├── Dockerfile       # 백엔드 Docker 이미지
│   └── .dockerignore
├── frontend/            # Next.js 프론트엔드
│   ├── app/            # Next.js App Router
│   │   ├── layout.tsx  # 루트 레이아웃
│   │   ├── page.tsx    # 홈 페이지
│   │   └── globals.css # 글로벌 스타일
│   ├── package.json    # Node.js 의존성
│   ├── tsconfig.json   # TypeScript 설정
│   ├── next.config.js  # Next.js 설정
│   ├── Dockerfile      # 프론트엔드 Docker 이미지
│   └── .dockerignore
└── docker-compose.yml   # Docker Compose 설정
```

## 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Uvicorn**: ASGI 서버
- **Pydantic**: 데이터 검증

### 프론트엔드
- **Next.js 14**: React 프레임워크 (App Router)
- **TypeScript**: 타입 안전성
- **CSS**: 모던 스타일링 (Glassmorphism, Gradients, Animations)

### 인프라
- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 컨테이너 오케스트레이션

## 시작하기

### 사전 요구사항
- Docker
- Docker Compose

### 실행 방법

1. **프로젝트 클론 또는 다운로드**

2. **Docker Compose로 실행**
   ```bash
   docker-compose up -d
   ```

3. **서비스 접속**
   - 프론트엔드: http://localhost:3000
   - 백엔드 API: http://localhost:8000
   - API 문서: http://localhost:8000/docs

4. **로그 확인**
   ```bash
   docker-compose logs -f
   ```

5. **중지**
   ```bash
   docker-compose down
   ```

## API 엔드포인트

- `GET /` - 루트 엔드포인트
- `GET /health` - 헬스 체크
- `GET /api/items` - 모든 아이템 조회
- `GET /api/items/{item_id}` - 특정 아이템 조회
- `POST /api/items` - 새 아이템 생성

## 개발 모드

Docker Compose는 개발 모드로 설정되어 있어 코드 변경 시 자동으로 재시작됩니다.

- **백엔드**: `--reload` 옵션으로 Uvicorn 실행
- **프론트엔드**: Next.js 개발 서버 (`npm run dev`)

## 주요 기능

✅ FastAPI 백엔드 with CORS 설정  
✅ Next.js 14 프론트엔드 (App Router)  
✅ TypeScript 지원  
✅ Docker Compose 통합  
✅ Hot Reload 개발 환경  
✅ 모던 UI 디자인 (Glassmorphism, Gradients)  
✅ API 자동 문서화 (Swagger UI)

## 라이선스

MIT
