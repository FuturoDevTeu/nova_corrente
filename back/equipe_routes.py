from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import EquipeSchemas
from models import Equipe, Funcionario, Atividade, FuncionarioEquipe
equipe_router = APIRouter(prefix="/equipe", tags=["equipe"])

@equipe_router.get("/")
async def home():
    return {"mensagem":"Rota equipe"}

@equipe_router.post("/cadastrar")
async def cadastrar(equipe: EquipeSchemas, sessao: Session = Depends(pegar_sessao)):
    try:
        nova_equipe = Equipe()
        sessao.add(nova_equipe)
        sessao.flush()

        for nome_funcionario in equipe.nome_funcionarios:
            funcionario_existente = sessao.query(Funcionario).filter_by(nome=nome_funcionario).first()
            if not funcionario_existente:
                funcionario_existente = Funcionario(nome = nome_funcionario)
                sessao.add(funcionario_existente)
                sessao.flush()
            
            func_eq = FuncionarioEquipe(
                funcionario_id = funcionario_existente.id,
                equipe_id = nova_equipe.id
            )
            sessao.add(func_eq)

        for nome_atividade in equipe.atividades:
            atividade_existente = sessao.query(Atividade).filter_by(nome=nome_atividade).first()

            if not atividade_existente:
                atividade_existente = Atividade(nome = atividade_existente)
                sessao.add(atividade_existente)
                sessao.flush()

            nova_equipe.atividades.append(atividade_existente)
        sessao.commit()
        return {"messagem":"Equipe cadastrada com sucesso"}
    except Exception as e:
        sessao.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar equipe: {e}")