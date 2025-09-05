from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    clicks = Column(Integer, default=0)
    title = Column(String, nullable=True)
    