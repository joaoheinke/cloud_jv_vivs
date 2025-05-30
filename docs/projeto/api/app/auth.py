from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "chave_super_secreta"
ALGORITHM = "HS256"

def gerar_hash(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha, hash):
    return pwd_context.verify(senha, hash)

def criar_token(email):
    expiracao = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expiracao}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token):
    from jose import JWTError
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
