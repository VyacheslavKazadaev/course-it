from fastapi import Path
from model.user import UserInput

def register_routes(app):
    @app.api.get("/users")
    def read_users():
        return app.user_service.get_users()

    @app.api.post("/users/")
    def create_user(user: UserInput):
        return app.user_service.save_user(user.username, user.email)

    @app.api.get("/users/{user_id}")
    def read_user(user_id: int = Path(..., gt=0)):
        return app.user_service.get_user(user_id)

    @app.api.delete("/users/{user_id}")
    def delete_user(user_id: int = Path(..., gt=0)):        
        return app.user_service.delete_user(user_id)