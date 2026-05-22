from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Grimoire of Authentication",
    description="A humble apprentice's ongoing quest to master the arcane arts of user authentication. I am continuously learning and updating this mystical artifact!",
    version="0.1.0"
)

# 🧙‍♂️ The Sacred Scroll of User Information
class User(BaseModel):
    username: str
    email: str
    password: str
    age: int

# 🛡️ An illusory database to store our brave adventurers (for learning purposes!)
fake_db = {}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {
        "message": "Welcome to the Authentication Sanctum! The service is running.",
        "status": "Apprentice level, but grinding XP daily."
    }

@app.post("/register")
def register(user: User):
    # 📝 Inscribing the user's essence into our mystical tomes
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="Alas! A hero with this name already exists in the realm.")
    
    # ⚠️ WARNING: I'm currently storing raw passwords. 
    # My next quest involves learning the 'Hashing' spell (bcrypt) to protect these secrets!
    fake_db[user.username] = user
    return {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "message": f"Huzzah! {user.username} has been registered successfully into the annals of history."
    }

@app.post("/login")
def login(creds: LoginRequest):
    # 🔍 Scrying the database for the user's credentials
    user = fake_db.get(creds.username)
    if not user or user.password != creds.password:
        raise HTTPException(status_code=401, detail="Access Denied! Your credentials are as flawed as a goblin's logic.")
    
    return {
        "message": f"Welcome back, {creds.username}! The gates are open.",
        "quest_status": "Learning JWT tokens is next on the agenda."
    }
