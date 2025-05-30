from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Usuario
from .schemas import UsuarioCreate, UsuarioLogin, TokenResponse
from .auth import gerar_hash, verificar_senha, criar_token, validar_token
from .scrapping import pegar_dados_ibovespa


# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Instancia a aplicação FastAPI
app = FastAPI()

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint de registro de usuário
@app.post("/registrar", response_model=TokenResponse)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado.")
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    token = criar_token(usuario.email)
    return {"jwt": token}

# Endpoint de login de usuário
@app.post("/login", response_model=TokenResponse)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    token = criar_token(usuario.email)
    return {"jwt": token}

# Endpoint de consulta de dados
@app.get("/consultar")
def consultar(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = validar_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
    dados = pegar_dados_ibovespa()
    return dados
