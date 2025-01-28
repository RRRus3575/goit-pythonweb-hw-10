from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from .models import Base
from .database import engine
from .routers import contacts, auth
from app.config import settings
from app.limiter import add_rate_limit_middleware

app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Лимитер запросов
add_rate_limit_middleware(app)

@app.get("/")
def read_root():
    return {"message": "API работает!"}


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Маршруты
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
