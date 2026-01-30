FROM node:18-alpine

WORKDIR /app

# 의존성 파일 복사
COPY package.json package-lock.json* ./

# 의존성 설치
RUN npm ci || npm install

# 애플리케이션 코드 복사
COPY . .

# Next.js 빌드 (프로덕션용)
# 개발 모드에서는 이 단계를 건너뛰고 docker-compose에서 npm run dev 실행
# RUN npm run build

# 포트 노출
EXPOSE 3000

# 개발 서버 실행
CMD ["npm", "run", "dev"]
