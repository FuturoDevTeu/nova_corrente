from fastapi import APIRouter, Depends, HTTPException
from schemas import FuncionarioSchemas
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Funcionario

funcionario_router = APIRouter(prefix="/funcionario", tags=["funcionario"])

@funcionario_router.get("/")
async def home():
    return {"mensagem":"Routa funcionario"}

@funcionario_router.post("/cadastrar")
async def cadastrar(funcionario: FuncionarioSchemas, sessao: Session = Depends(pegar_sessao)):
    if funcionario.nome == None or funcionario.nome == "":
        raise HTTPException(status_code=400, detail="Nome do funcionario está vazio")
    novo_funcionario = Funcionario(nome = funcionario.nome)
    sessao.add(novo_funcionario)
    sessao.commit()
    return {"messagem":"cadastrado com sucesso"}


    