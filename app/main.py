from fastapi import FastAPI
from app.routers import auth, users, shanyraks, comments
from app.database import Base, engine

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(shanyraks.router)
app.include_router(comments.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Şañıraq.kz API"}
