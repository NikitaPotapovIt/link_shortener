from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    original_url: str
    custom_code: Optional[str] = None

class URLCreate(URLBase):
    pass

class URLResponse(URLBase):
    short_url: str
    clicks: int
    created_at: datetime
    title: Optional[str] = None
    
    class Config:
        from_attributes = True

class URLInfo(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    created_at: datetime
    title: Optional[str] = None
    