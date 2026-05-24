from fastapi import FastAPI, Depends
from pydantic import BaseModel
from passlib.context import CryptContext 
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from model import UserDB

app = FastAPI()

UserDB.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: str
    password: str
    age: int

def hash_password(password: str):
    return pwd_context.hash(password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Auth Service Running"}

@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)

    new_user = UserDB(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password,
        age = user.age  
    )

    db.add(new_user)
    db.commit()

    return {
        "message" : "User Registered successfully"
    }
