from sqlalchemy.orm import Session
from sqlalchemy import select, delete, insert
from model.user import User


class UserSQLAlchemyRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self) -> list[dict]:
        stmt = select(User)
        result = self.session.execute(stmt)
        users = result.scalars().all()
        return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

    def get_user(self, user_id: int) -> dict:
        stmt = select(User).where(User.id == user_id)
        result = self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return {"id": user.id, "username": user.username, "email": user.email}
        return {}

    def save_user(self, username: str, email: str) -> dict:
        new_user = User(username=username, email=email)
        self.session.add(new_user)
        # flush() чтобы получить id до коммита
        self.session.flush()
        return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

    def delete_user(self, user_id: int) -> bool:
        stmt = delete(User).where(User.id == user_id)
        result = self.session.execute(stmt)
        return result.rowcount > 0