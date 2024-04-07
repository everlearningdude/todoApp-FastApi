import sys
sys.path.append("..")

from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from typing import Optional
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

#S
from declares import SECRET_KEY, ALGORITHM
from declares import validate_token, create_access_token
#E

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        ansc: dict = payload.get("ansc")
        if username is None or user_id is None:
            # logout(request)
            return None
        return {"username": username, "id": user_id, "apitoken": ansc['token']}
    except ExpiredSignatureError:
        print("JWT token has expired.")
    except JWTError as jwterr:
        print(jwterr)
        raise HTTPException(status_code=404, detail="Not found")


@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print('inside login_for_access_token')
    print(form_data.username, form_data.password)
    user = validate_token(form_data.username, form_data.password)
    if not user:
        return False
    print(user, user['ansc'])
    token = create_access_token(form_data.username, form_data.password, user['ansc'], user['id'])
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True

@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)
        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException as e:
        print(e)
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

@router.get("/logout")
async def logout(request: Request):
    print('logout')
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...),
                        db: Session = Depends(get_db)):

    validation1 = db.query(models.Users).filter(models.Users.username == username).first()

    validation2 = db.query(models.Users).filter(models.Users.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model = models.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname

    hash_password = get_password_hash(password)
    user_model.hashed_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
