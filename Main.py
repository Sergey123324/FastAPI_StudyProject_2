from fastapi import FastAPI

from Routers.Auth import router as auth_router
from Routers.Users import router as users_router
from Routers.Tasks import router as tasks_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)