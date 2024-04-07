from fastapi import FastAPI, Request
from jose import jwt
import models
from database import engine
from routers import auth, todos
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from time import time
from declares import SECRET_KEY, ALGORITHM
from declares import create_access_token, generate_new_api_token

app = FastAPI()

#S
allowed_origins = [
    "http://127.0.0.1:8001"
]

# Setup CORS for the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_token_expiry(request: Request, call_next):
    response = await call_next(request)
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            ansc: dict = payload.get("ansc")
            _expire = ansc['expire']
            if ( _expire - 10 ) < int(time()):
                new_ansc, username, userpass = generate_new_api_token(payload)
                token = create_access_token(username, userpass, new_ansc['ansc'], new_ansc['id'])
                response.set_cookie(key="access_token", value=token, httponly=True)
                return response
        except Exception as e:
            print(f"Error decoding JWT: {e}")
    return response
#E
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)
