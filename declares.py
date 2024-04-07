from cryptography.fernet import Fernet
import base64
from datetime import datetime, timedelta
from jose import jwt, JWTError
import requests

JWT_TOKEN_EXPIRATION_TIME = 60

ENCRYPTION_KEY = b'Jks8e2lDd-UZf629dFFD3EIAWTe7fLBhGoXquRpJoho='
cipher = Fernet(ENCRYPTION_KEY)

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

def encrypt_credentials(username: str, userpass: str) -> bytes:
    credentials_string = f"{username}:{userpass}".encode()
    encrypted_credentials = cipher.encrypt(credentials_string)
    encoded_credentials = base64.urlsafe_b64encode(encrypted_credentials).decode()
    return encoded_credentials

def decrypt_credentials(_enc: str) -> tuple:
    decoded_enc = base64.urlsafe_b64decode(_enc.encode())
    username, password = cipher.decrypt(decoded_enc).decode().split(':')
    return username, password

def create_access_token(username: str, userpass: str, ansc: str, user_id: int):
    encrypted_credentials = encrypt_credentials(username, userpass)
    encode = {"sub": username, "ansc": ansc, "id": user_id, "_enc": encrypted_credentials}
    expires_delta = timedelta(seconds=JWT_TOKEN_EXPIRATION_TIME)
    expire = datetime.utcnow() + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_token(username: str, password: str) -> str:
    print('inside validate token')
    url = f"http://127.0.01:8001/apilogin/?username={username}&password={password}"
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response:
            return response.json()
        else:
            return False
    except requests.RequestException as e:
        return False

def generate_new_api_token(payload):
    _enc: str = payload.get("_enc")
    username, userpass = decrypt_credentials(_enc)
    new_ansc = validate_token(username, userpass)
    if not new_ansc:
        return False
    print(new_ansc, username, userpass)
    return new_ansc, username, userpass