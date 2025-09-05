from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import validators
import shortuuid
import re

from database import get_db
from models import URL
from schemas import URLCreate, URLResponse, URLInfo
from config import settings

app = FastAPI(
    title="URL Shortener API",
    description="Собственный сервис сокращения ссылок",
    version="1.0.0"
)

# CORS для Tkinter клиента
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_short_code(length: int = settings.SHORT_CODE_LENGTH) -> str:
    """Генерация короткого кода"""
    return shortuuid.ShortUUID().random(length=length)

def validate_url(url: str) -> bool:
    """Валидация URL"""
    return validators.url(url)

def is_valid_custom_code(code: str) -> bool:
    """Проверка кастомного кода"""
    return bool(re.match(r'^[a-zA-Z0-9_-]{3,20}$', code))

@app.on_event("startup")
def startup():
    from database import Base, engine
    Base.metadata.create_all(bind=engine)

@app.post("/api/shorten", response_model=URLResponse)
def create_short_url(url_data: URLCreate, db: Session = Depends(get_db)):
    """Создание короткой ссылки"""
    
    if not validate_url(url_data.original_url):
        raise HTTPException(status_code=400, detail="Некорректный URL")
    
    # Проверяем существование URL
    existing_url = db.query(URL).filter(URL.original_url == url_data.original_url).first()
    if existing_url:
        return URLResponse(
            original_url=existing_url.original_url,
            short_url=f"{settings.BASE_URL}/{existing_url.short_code}",
            clicks=existing_url.clicks,
            created_at=existing_url.created_at,
            title=existing_url.title
        )
    
    # Генерируем или используем кастомный код
    if url_data.custom_code:
        if not is_valid_custom_code(url_data.custom_code):
            raise HTTPException(status_code=400, detail="Некорректный кастомный код")
        if db.query(URL).filter(URL.short_code == url_data.custom_code).first():
            raise HTTPException(status_code=400, detail="Этот код уже занят")
        short_code = url_data.custom_code
    else:
        short_code = generate_short_code()
        # Гарантируем уникальность
        while db.query(URL).filter(URL.short_code == short_code).first():
            short_code = generate_short_code()
    
    # Создаем запись
    db_url = URL(original_url=url_data.original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return URLResponse(
        original_url=db_url.original_url,
        short_url=f"{settings.BASE_URL}/{db_url.short_code}",
        clicks=db_url.clicks,
        created_at=db_url.created_at,
        title=db_url.title
    )

@app.get("/{short_code}")
def redirect_to_original(short_code: str, request: Request, db: Session = Depends(get_db)):
    """Перенаправление по короткой ссылке"""
    
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    
    # Обновляем счетчик кликов
    db_url.clicks += 1
    db.commit()
    
    return RedirectResponse(url=db_url.original_url)

@app.get("/api/info/{short_code}", response_model=URLInfo)
def get_url_info(short_code: str, db: Session = Depends(get_db)):
    """Получение информации о ссылке"""
    
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    
    return URLInfo(
        original_url=db_url.original_url,
        short_url=f"{settings.BASE_URL}/{db_url.short_code}",
        clicks=db_url.clicks,
        created_at=db_url.created_at,
        title=db_url.title
    )

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Статистика сервиса"""
    total_urls = db.query(URL).count()
    total_clicks = db.query(URL.clicks).all()
    total_clicks = sum([click[0] for click in total_clicks])
    
    return {
        "total_urls": total_urls,
        "total_clicks": total_clicks,
        "average_clicks": total_clicks / total_urls if total_urls > 0 else 0
    }

@app.get("/")
def read_root():
    return {"message": "URL Shortener API работает!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
