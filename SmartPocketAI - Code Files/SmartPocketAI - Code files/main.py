
import os
 
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from auth import hash_password
from database import Base, SessionLocal, engine
from models import User
from routers.auth_router import router as auth_router
from routers.history_router import router as history_router
from routers.recommend_router import router as recommend_router
 
load_dotenv()
 
app = FastAPI(title="Smartpocket AI Backend")
 
origins = [o.strip() for o in os.getenv("FRONTEND_ORIGINS", "").split(",") if o.strip()]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
Base.metadata.create_all(bind=engine)
 
app.include_router(auth_router)
app.include_router(recommend_router)
app.include_router(history_router)
 
 
@app.on_event("startup")
def create_demo_account():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "demo").first():
            demo = User(
                name="Demo User",
                username="demo",
                email="demo@smartpocket.local",
                password_hash=hash_password("demo1234"),
            )
            db.add(demo)
            db.commit()
    finally:
        db.close()
 
 
@app.get("/")
def root():
    return {"status": "ok", "service": "smartpocket-ai-backend"}