from typing import Callable

from model.user import User
from repo.db import PostgreSQLConnection
from repo.users import UserRepo
from repo.users_sqlalchemy import UserSQLAlchemyRepo
from sqlalchemy.orm import Session
from contextlib import contextmanager


class UserService:
    def __init__(self, db=None, session: Session = None, session_factory=None):
        """
        Инициализирует сервис.
        Если передана session_factory (функция создания SQLAlchemy сессии), использует её для создания UserSQLAlchemyRepo.
        Если передана session (SQLAlchemy), использует UserSQLAlchemyRepo.
        Иначе использует старый UserRepo с PostgreSQLConnection.
        """
        self.session_factory = session_factory
        if session is not None:
            self.repo = UserSQLAlchemyRepo(session)
        elif db is not None:
            self.repo = UserRepo(db)
        elif session_factory is not None:
            # Создаем репозиторий без сессии, будем создавать её в каждом методе
            self.repo_class = UserSQLAlchemyRepo
        else:
            raise ValueError("Either 'db' (PostgreSQLConnection), 'session' (Session), or 'session_factory' must be provided")

    def _get_repo_with_session(self):
        """Вспомогательный метод для получения репо с новой сессией"""
        if self.session_factory:
            session = self.session_factory()
            return self.repo_class(session), session
        else:
            # Если session_factory нет, но repo уже инициализирован, возвращаем его (старое поведение для других конструкторов)
            return self.repo, None

    def get_users(self) -> dict:
        repo, session = self._get_repo_with_session()
        try:
            users = repo.get_users()
            return users
        finally:
            if session:
                session.close()

    def save_user(self, username: str, email: str) -> dict:
        repo, session = self._get_repo_with_session()
        try:
            result = repo.save_user(username, email)
            session.commit()  # Подтверждаем транзакцию
            return result
        except Exception:
            session.rollback()  # Откатываем при ошибке
            raise
        finally:
            if session:
                session.close()

    def get_user(self, user_id: int) -> dict:
        repo, session = self._get_repo_with_session()
        try:
            result = repo.get_user(user_id)
            return result
        finally:
            if session:
                session.close()
    
    def delete_user(self, user_id: int) -> dict:
        def trx (repo, session):
            result = repo.delete_user(user_id)
            session.commit()  # Подтверждаем транзакцию
            if result:
                response = {"success": True, "message": f"User with id {user_id} deleted successfully"}
            else:
                response = {"error": f"Failed to delete user with id {user_id}"}
            return response 

        return self.transaction(trx)

    def transaction(self, trx: Callable[['SomeRepositoryType', 'SomeSessionType'], str]):
        repo, session = self._get_repo_with_session()
        try:
            return trx(repo, session)
        finally:
            if session:
                session.close()
