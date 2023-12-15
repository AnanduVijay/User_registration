from fastapi import FastAPI
from users.router import router as user_router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(user_router)
    return application


app = get_application()
