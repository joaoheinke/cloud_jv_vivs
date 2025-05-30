# api/app/app.py

from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .models import Usuario
from .schemas import UsuarioCreate, UsuarioLogin, TokenResponse
from .auth import gerar_hash, verificar_senha, criar_token, validar_token
from .scrapping import pegar_dados_ibovespa

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Instancia a aplicação
app = FastAPI()

# Dependência de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/registrar", response_model=TokenResponse)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(409, "Email já cadastrado.")
    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash(usuario.senha)
    )
    db.add(novo); db.commit(); db.refresh(novo)
    return {"jwt": criar_token(usuario.email)}

@app.post("/login", response_model=TokenResponse)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(401, "Credenciais inválidas.")
    return {"jwt": criar_token(usuario.email)}

@app.get("/consultar")
def consultar(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if not validar_token(token):
        raise HTTPException(403, "Token inválido ou expirado.")
    return pegar_dados_ibovespa()
