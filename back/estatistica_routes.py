from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, select
from datetime import datetime

from dependencies import pegar_sessao
from models import Equipe_Atividade, Epi, Atividade, HistoricoConformidade, Atividade_Epi

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

@estatistica_router.get("/conformes")
async def listar_epis_conformes(sessao: Session = Depends(pegar_sessao)):
    try:
        
        subq = (
            sessao.query(
                HistoricoConformidade.equipe_id,
                func.max(HistoricoConformidade.data_validacao).label("ultima_data")
            )
            .group_by(HistoricoConformidade.equipe_id)
            .subquery()
        )

        ultimos = (
            sessao.query(HistoricoConformidade)
            .join(subq, (HistoricoConformidade.equipe_id == subq.c.equipe_id) &
                        (HistoricoConformidade.data_validacao == subq.c.ultima_data))
            .filter(HistoricoConformidade.em_conformidade == True)
            .subquery()
        )

        query = (
            sessao.query(Epi)
            .join(Atividade_Epi, Epi.id == Atividade_Epi.c.Epi_idEpi)
            .join(Atividade, Atividade.id == Atividade_Epi.c.Atividade_idAtividade)
            .join(Equipe_Atividade, Equipe_Atividade.c.Atividade_idAtividade == Atividade.id)
            .join(ultimos, ultimos.c.equipe_id == Equipe_Atividade.c.Equipe_idEquipe)
            .distinct()
        )

        epis = query.all()
        return {"total": len(epis), "epis_conformes": [epi.nome for epi in epis]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar EPIs conformes: {e}")

@estatistica_router.get("/nao-conformes")
async def listar_epis_nao_conformes(sessao: Session = Depends(pegar_sessao)):
    try:
        subq = (
            sessao.query(
                HistoricoConformidade.equipe_id,
                func.max(HistoricoConformidade.data_validacao).label("ultima_data")
            )
            .group_by(HistoricoConformidade.equipe_id)
            .subquery()
        )

        ultimos = (
            sessao.query(HistoricoConformidade)
            .join(subq, (HistoricoConformidade.equipe_id == subq.c.equipe_id) &
                        (HistoricoConformidade.data_validacao == subq.c.ultima_data))
            .filter(HistoricoConformidade.em_conformidade == False)
            .subquery()
        )

        query = (
            sessao.query(Epi)
            .join(Atividade_Epi, Epi.id == Atividade_Epi.c.Epi_idEpi)
            .join(Atividade, Atividade.id == Atividade_Epi.c.Atividade_idAtividade)
            .join(Equipe_Atividade, Equipe_Atividade.c.Atividade_idAtividade == Atividade.id)
            .join(ultimos, ultimos.c.equipe_id == Equipe_Atividade.c.Equipe_idEquipe)
            .distinct()
        )

        epis = query.all()
        return {"total": len(epis), "epis_nao_conformes": [epi.nome for epi in epis]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar EPIs não conformes: {e}")