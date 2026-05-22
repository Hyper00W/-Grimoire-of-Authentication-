from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext 
from database import engine
from model import UserDB

app = FastAPI()
UserDB.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

@app.get("/")
def home():
    return {"message": "Auth Service Running"}

@app.post("/register")
def register(user: User):
    hashed_password = hash_password(user.password)

    return {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "message": "User registered successfully"
    }
