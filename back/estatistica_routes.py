from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, select
from datetime import datetime

from dependencies import pegar_sessao
from models import Equipe_Atividade

estatistica_router = APIRouter(prefix="/estatisticas", tags=["Estatísticas"])

@estatistica_router.get("/equipes-ativas-mes")
async def contar_equipes_mes_atual(sessao: Session = Depends(pegar_sessao)):
    try:
        agora = datetime.now()

        qtd_equipes = (
            sessao.query(func.count(func.distinct(Equipe_Atividade.c.Equipe_idEquipe)))
            .filter(
                extract("month", Equipe_Atividade.c.data_realizacao) == agora.month,
                extract("year", Equipe_Atividade.c.data_realizacao) == agora.year
            )
            .scalar()
        )
        return {"mes": agora.strftime("%m/%Y"), "quantidade_equipes_ativas": qtd_equipes}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar estatística: {e}")
