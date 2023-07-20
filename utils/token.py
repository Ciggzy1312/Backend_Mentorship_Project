import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt

load_dotenv()
secret = os.environ["SECRET_KEY"]

async def generateToken(payload: dict, expires: timedelta):
    encode_payload = payload.copy()

    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode_payload.update({"exp": expire})
    encoded_jwt = jwt.encode(encode_payload, secret, algorithm="HS256")
    return encoded_jwt