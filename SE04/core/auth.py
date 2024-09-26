from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext # type: ignore
from jose import JWTError, jwt # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # type: ignore
from pydantic import BaseModel # type: ignore
import pytz # type: ignore
from core.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key"  # Troque por uma chave secreta real
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LogIN(BaseModel):
    email: str
    password: str

# faz o hashcode da senha, ou cryptographa a senha.....
def get_password_hash(password):
    return pwd_context.hash(password)


# valida a senha inserida, retorna true
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def cria_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}
    sp =  pytz.timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    payload['type'] = tipo_token
    payload['exp'] = expira
    payload['iat'] = datetime.now(tz=sp)
    payload['sub'] = str(sub)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(db: AsyncSession = Depends(get_session), token: str= Depends(oauth2_scheme) ):

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail      = "Credenciais inválidas",
        headers     = {"WWW-Authenticate": "Bearer"}
    )

    credenciais_expired = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Faça login novamente",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except jwt.ExpiredSignatureError:
        raise credenciais_expired
    
    except jwt.JWTError:
        raise credentials_exception