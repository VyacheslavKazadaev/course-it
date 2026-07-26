import uvicorn
import os
from fastapi import FastAPI, Path
from repo.db import PostgreSQLConnection
from service.user import UserService

class App:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        db = PostgreSQLConnection()
        if not db.connect():
            print("Database connection failed")
            exit()
        db.close()
        self.db = db
        self.api = FastAPI()
        self.user_service = UserService(self.db)

    def server_run(self):
        host = os.getenv('APP_HOST', 'localhost')
        port = int(os.getenv('APP_PORT', 8000))
        uvicorn.run(self.api, host=host, port=port)
        self.db.close()