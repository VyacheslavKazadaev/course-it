import sys
import os
# Добавляем родительскую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestUserAPI:
    def test_read_users(self, client):
        """Test the GET /users endpoint."""
        response = client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["username"] == "test"

    def test_create_user(self, client):
        """Test the POST /users/ endpoint."""
        payload = {"username": "new_user", "email": "new@example.com"}
        response = client.post("/users/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "new_user"
        assert data["email"] == "new@example.com"
        client._mock_user_service.save_user.assert_called_once_with("new_user", "new@example.com")

    def test_read_user(self, client):
        """Test the GET /users/{user_id} endpoint."""
        user_id = 1
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "test"

    def test_read_user_invalid_id(self, client):
        """Test the GET /users/{user_id} endpoint with an invalid ID (less than 1)."""
        user_id = -1
        response = client.get(f"/users/{user_id}")
        # FastAPI's Path(...) validation should cause a 422 error
        assert response.status_code == 422

    def test_delete_user(self, client):
        """Test the DELETE /users/{user_id} endpoint."""
        user_id = 1
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        client._mock_user_service.delete_user.assert_called_once_with(user_id)