import uuid
from sqlalchemy import (create_engine, Column, String, Integer, ForeignKey, Table, DateTime, UniqueConstraint, func, Boolean)
from sqlalchemy.orm import declarative_base, relationship, foreign

db = create_engine("mysql+pymysql://root:@localhost:3306/nova", echo=True)

Base = declarative_base()

Funcionario_Epi = Table(
    "Funcionario_Possui_Epi",
    Base.metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("Funcionario_idFuncionario", ForeignKey("tb_funcionario.id")),
    Column("Epi_idEpi", ForeignKey("tb_epi.id"))
)

Equipe_Atividade = Table(
    "Equipe_Possui_Atividade",
    Base.metadata,
    Column("Equipe_idEquipe", ForeignKey("tb_equipe.id"), primary_key=True),
    Column("Atividade_idAtividade", ForeignKey("tb_atividade.id"), primary_key=True),
    Column("data_realizacao", DateTime, nullable=True)
)

Atividade_Epi = Table(
    "Atividade_Possui_Epi",
    Base.metadata,
    Column("Atividade_idAtividade", ForeignKey("tb_atividade.id"), primary_key=True),
    Column("Epi_idEpi", ForeignKey("tb_epi.id"), primary_key=True)
)

class Funcionario(Base):
    __tablename__ = "tb_funcionario"

    id = Column("id", Integer, autoincrement=True, unique=True, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    epis = relationship("Epi", secondary=Funcionario_Epi, back_populates="funcionarios")
    funcionario_equipes = relationship("FuncionarioEquipe", back_populates="funcionario", cascade="all, delete-orphan") 

class Epi(Base):
    __tablename__ = "tb_epi"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    nome = Column("nome", String(150))
    funcionarios = relationship("Funcionario", secondary=Funcionario_Epi, back_populates="epis")
    atividades = relationship("Atividade", secondary=Atividade_Epi, back_populates="epis")

class Atividade(Base):
    __tablename__ = "tb_atividade"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    nome = Column("nome", String(100))
    epis = relationship("Epi", secondary=Atividade_Epi, back_populates="atividades")
    equipes = relationship("Equipe", secondary=Equipe_Atividade, back_populates="atividades")
        
class Equipe(Base):
    __tablename__ = "tb_equipe"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    atividades = relationship("Atividade", secondary=Equipe_Atividade, back_populates="equipes")
    funcionario_equipes = relationship("FuncionarioEquipe", back_populates="equipe", cascade="all, delete-orphan")
    historico_conformidades = relationship(
        "HistoricoConformidade",
        back_populates="equipe",
        cascade="all, delete-orphan"
    )

class HistoricoConformidade(Base):
    __tablename__ = "tb_historico_conformidade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipe_id = Column(ForeignKey("tb_equipe.id"), nullable=False)
    data_validacao = Column(DateTime, server_default=func.now(), nullable=False)
    em_conformidade = Column(Boolean, nullable=False)
    observacao = Column(String(255), nullable=True)  
    
    equipe = relationship("Equipe", back_populates="historico_conformidades")

class FuncionarioEquipe(Base):
    __tablename__ = "tb_funcionario_equipe"

    id = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_id = Column(ForeignKey("tb_funcionario.id"))
    equipe_id =  Column(ForeignKey("tb_equipe.id"))
    funcionario = relationship("Funcionario", back_populates="funcionario_equipes")
    equipe = relationship("Equipe", back_populates="funcionario_equipes")
    fotos = relationship(
        "Foto",
        back_populates="funcionario_equipe",
        cascade="all, delete-orphan"
    )
    __table_args__ = (
        UniqueConstraint("funcionario_id", "equipe_id", name="uq_funcionario_equipe"),
    )

class Usuario(Base):
    __tablename__ = "tb_usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)

    login = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)

class Foto(Base):
    __tablename__ = "tb_foto"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    foto = Column(String(255), nullable=False)
    funcionario_equipe_id = Column(Integer, ForeignKey("tb_funcionario_equipe.id"))
    
    funcionario_equipe = relationship("FuncionarioEquipe", back_populates="fotos")

if __name__ == "__main__":
    Base.metadata.create_all(db)