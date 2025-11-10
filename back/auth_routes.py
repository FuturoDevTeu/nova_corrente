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

