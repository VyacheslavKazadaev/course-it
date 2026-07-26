from app.app import App
from app import http

# День 10: FastAPI. Первый сервер

def main():
    app = App()
    http.register_routes(app)
    app.server_run()

if __name__ == "__main__":
    main()