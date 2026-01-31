"""
AdCopy Model
광고 문구 생성 이력 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from database import Base


class AdCopy(Base):
    """광고 문구 생성 이력"""
    
    __tablename__ = "ad_copies"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    target_audience = Column(String(255), nullable=False)
    key_features = Column(Text, nullable=False)
    tone = Column(String(50), nullable=False)
    
    # AI 제공자 정보
    ai_provider = Column(String(50), nullable=False)  # openai, groq, gemini
    ai_model = Column(String(100), nullable=False)
    
    # 생성된 광고 문구들 (JSON 배열)
    generated_copies = Column(JSON, nullable=False)
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<AdCopy(id={self.id}, product_name='{self.product_name}', ai_provider='{self.ai_provider}')>"
