from repo.db import PostgreSQLConnection

class UserRepo:
    def __init__(self, db: PostgreSQLConnection):
        self.db = db
        
    def get_users(self) -> dict:
        if not self.db.connect():
            return {"error": "Database connection failed"}

        users = self.db.execute_query("SELECT * FROM users")
        self.db.close()
        return users
    def get_user(self, user_id: int) -> dict:
        if not self.db.connect():
            return {"error": "Database connection failed"}

        users = self.db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
        self.db.close()
        return users
    def save_user(self, username: str, email: str) -> dict:
        if not self.db.connect():
            return {"error": "Database connection failed"}

        query = "INSERT INTO users (username, email) VALUES (%s, %s)"        
        user_id = self.db.execute_command(query, (username, email), True)
        self.db.close()
        if user_id:
            return {"success": True, "user_id": user_id, "username": username, "email": email}
        else:
            return {"error": "Failed to insert user"}

    def delete_user(self, user_id: int) -> dict:
        if not self.db.connect():
            return {"error": "Database connection failed"}

        query = "DELETE FROM users WHERE id = %s"
        result = self.db.execute_command(query, (user_id,))
        
        if result:  # Если запрос выполнился без ошибок
            self.db.close()
            return {"success": True, "message": f"User with id {user_id} deleted successfully"}
        else:
            self.db.close()
            return {"error": f"Failed to delete user with id {user_id}"}