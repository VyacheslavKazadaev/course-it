import uvicorn
import os
from fastapi import FastAPI, Path
from service.user import UserService
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from model.user import Base

class App:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        # Подключение к базе данных через SQLAlchemy
        db_url = f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME', 'postgres')}"
        self.engine = create_engine(db_url)
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.api = FastAPI()
        
        # Создание экземпляра сервиса, передавая фабрику сессий
        self.user_service = UserService(session_factory=self.SessionLocal)

    def server_run(self):
        host = os.getenv('APP_HOST', 'localhost')
        port = int(os.getenv('APP_PORT', 8000))
        uvicorn.run(self.api, host=host, port=port)