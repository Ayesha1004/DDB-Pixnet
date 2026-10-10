from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.init_db import create_tables
from app.routers.auth import authRouter
from app.routers.posts import router
from app.routers.follow import router as followsRouter   
from app.routers.users import router as usersRouter 
from app.utils.storage import STORAGE_BACKEND
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os


@asynccontextmanager
async def lifespan(app : FastAPI):
    create_tables()
    if STORAGE_BACKEND == "s3":                             # new
        from app.utils.s3_storage import ensure_bucket_exists
        ensure_bucket_exists()
    yield


app = FastAPI(lifespan= lifespan, title = "PixNet Auth/Posts")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port — adjust if yours differs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(authRouter)
app.include_router(router)
app.include_router(followsRouter)   
app.include_router(usersRouter) 

#/auth/signup or login



@app.get("/health")
def health():
    return {"status": "running..."}







