from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
import time

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

users = {
    "admin": "pass",
    "user1": "pass"
}
#S
@app.post("/apilogin/")
async def apilogin(login_data: LoginRequest):
    username = login_data.username
    password = login_data.password
    # Check if username exists in the database
    if username in users:
        # Check if the password matches
        if users[username] == password:
            # If the username and password are valid, generate an API token
            token = str(uuid4())
            expire = int(time.time()) + 20
            return { "ansc": {"token": token, "expire": expire}, "id": 1}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
#E