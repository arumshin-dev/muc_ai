"""
VisionAnalysis Model
이미지 분석 이력 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class VisionAnalysis(Base):
    """이미지 분석 이력"""
    
    __tablename__ = "vision_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    
    # AI 제공자 정보
    ai_provider = Column(String(50), nullable=False)
    ai_model = Column(String(100), nullable=False)
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<VisionAnalysis(id={self.id}, ai_model='{self.ai_model}')>"
