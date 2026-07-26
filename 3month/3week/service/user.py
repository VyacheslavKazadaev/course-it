from model.user import User
from repo.db import PostgreSQLConnection
from repo.users import UserRepo

class UserService:
    def __init__(self, db: PostgreSQLConnection):
        self.db = db
        self.repo = UserRepo(db)

    def get_users(self) -> dict:
        users = self.repo.get_users()
        return users

    def save_user(self, username: str, email: str) -> dict:
        result = self.repo.save_user(username, email)
        return result

    def get_user(self, user_id: int) -> dict:
        result = self.repo.get_user(user_id)
        return result
    def delete_user(self, user_id: int) -> dict:
        result = self.repo.delete_user(user_id)
        return result