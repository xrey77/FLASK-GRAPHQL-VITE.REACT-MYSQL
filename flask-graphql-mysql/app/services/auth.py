from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from graphql import GraphQLError

JWT_SECRET_KEY = "4fd86fa150307ee13ba122f48fb8953cdde4319dbaf757d3" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])        
    except jwt.ExpiredSignatureError:
        raise GraphQLError(f"Token has expired.")
    except jwt.InvalidTokenError:
        raise GraphQLError(f"Invalid Token.")
