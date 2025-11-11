from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchemas
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return "Teste"


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schemas: UsuarioSchemas, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.login==usuario_schemas.login).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Já existe um usuário com este login")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schemas.senha)
        novoUsuario = Usuario(login= usuario_schemas.login, senha=senha_criptografada)
        session.add(novoUsuario)
        session.commit()
        return {"mensagem":"usuario cadastrado com sucesso"}

@auth_router.post("/logar")
async def logar(usuario_schemas: UsuarioSchemas, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.login == usuario_schemas.login).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Login não encontrado")
    
    senha_valida = bcrypt_context.verify(usuario_schemas.senha, usuario.senha)
    if not senha_valida:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    return {"mensagem": "login realizado com sucesso ", "usuario":usuario.login}


