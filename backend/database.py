"""
MUC AI Backend Database Configuration
SQLAlchemy 데이터베이스 연결 및 세션 관리
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 데이터베이스 URL (동기 방식)
# asyncpg 대신 psycopg2 사용
database_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

# SQLAlchemy 엔진 생성
engine = create_engine(
    database_url,
    pool_pre_ping=True,  # 연결 유효성 확인
    pool_size=5,
    max_overflow=10,
    echo=settings.ENVIRONMENT == "development"  # 개발 환경에서 SQL 로깅
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성
    FastAPI 엔드포인트에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
