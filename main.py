from fastapi import FastAPI

from src.users.endpoints import users_router
from src.library.endpoints import library_router

import uvicorn

app = FastAPI()
app.include_router(users_router)
app.include_router(library_router)

if __name__ == "__main__":
    uvicorn.run(app)