from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticle(BaseModel):
    id: str
    title: str
    blurb: Optional[str] = None
    source: str
    url: str
    published_at: datetime
    category: Optional[str] = "General"
    image_url: Optional[str] = None

class NewsResponse(BaseModel):
    articles: list[NewsArticle]
    total: int
    cached: bool