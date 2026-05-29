from fastapi import FastAPI, HTTPException, Depends
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

class LoginUser(BaseModel):
    email: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

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
@app.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):

    db_user = db.query(UserDB).filter(
        UserDB.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code = 404,
            detail="User not found"
        )
    if not verify_password(
        user.passowrd,
        db_user.password
    ):
        raise HTTPException(
            status_code = 401,
            detail="Invalid Passowrd"
        )
    return {
        "message": "Login Successful"
    }
    