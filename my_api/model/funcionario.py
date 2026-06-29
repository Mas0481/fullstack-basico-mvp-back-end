from contextlib import contextmanager
from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import Column, Date, Integer, Numeric, String, Time, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import Config


Base = declarative_base()
ENGINE = None
SessionLocal = None


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    genero = Column(String, nullable=True)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    cargo = Column(String, nullable=False)
    departamento = Column(String, nullable=False)
    data_admissao = Column(Date, nullable=False)
    salario = Column(Numeric(12, 2), nullable=True)
    tipo_contrato = Column(String, nullable=True)
    horario_entrada = Column(Time, nullable=True)
    horario_saida_almoco = Column(Time, nullable=True)
    horario_retorno_almoco = Column(Time, nullable=True)
    horario_saida = Column(Time, nullable=True)
    dias_trabalho = Column(String, nullable=True)


def configure_database(database_url=None):
    """Inicializa ou reinicializa engine e session factory."""
    global ENGINE, SessionLocal

    url = database_url or Config.DATABASE_URL
    ENGINE = create_engine(url, future=True)
    SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)


def inicializar_banco():
    """Cria as tabelas do banco SQLite se elas ainda não existirem."""
    if ENGINE is None:
        configure_database()
    Base.metadata.create_all(ENGINE)


@contextmanager
def get_session():
    """Gerencia sessão SQLAlchemy com commit/rollback automático."""
    if SessionLocal is None:
        configure_database()

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _formatar_valor(valor):
    """Converte datas, horários e decimais para JSON."""
    if isinstance(valor, (date, datetime)):
        return valor.isoformat()
    if isinstance(valor, time):
        return valor.isoformat(timespec="minutes")
    if isinstance(valor, Decimal):
        return float(valor)
    return valor


def _funcionario_para_dict(funcionario):
    """Transforma um objeto do banco em um dicionário simples para a API retornar."""
    from ..schemas.validators import formatar_cpf

    return {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "data_nascimento": _formatar_valor(funcionario.data_nascimento),
        "genero": funcionario.genero,
        "cpf": formatar_cpf(funcionario.cpf),
        "email": funcionario.email,
        "telefone": funcionario.telefone,
        "cargo": funcionario.cargo,
        "departamento": funcionario.departamento,
        "data_admissao": _formatar_valor(funcionario.data_admissao),
        "salario": _formatar_valor(funcionario.salario),
        "tipo_contrato": funcionario.tipo_contrato,
        "horario_entrada": _formatar_valor(funcionario.horario_entrada),
        "horario_saida_almoco": _formatar_valor(funcionario.horario_saida_almoco),
        "horario_retorno_almoco": _formatar_valor(funcionario.horario_retorno_almoco),
        "horario_saida": _formatar_valor(funcionario.horario_saida),
        "dias_trabalho": funcionario.dias_trabalho,
    }


def _criar_entidade(funcionario):
    return Funcionario(
        nome=funcionario.nome,
        data_nascimento=funcionario.data_nascimento,
        genero=funcionario.genero,
        cpf=funcionario.cpf,
        email=str(funcionario.email) if funcionario.email else None,
        telefone=funcionario.telefone,
        cargo=funcionario.cargo,
        departamento=funcionario.departamento,
        data_admissao=funcionario.data_admissao,
        salario=funcionario.salario,
        tipo_contrato=funcionario.tipo_contrato,
        horario_entrada=funcionario.horario_entrada,
        horario_saida_almoco=funcionario.horario_saida_almoco,
        horario_retorno_almoco=funcionario.horario_retorno_almoco,
        horario_saida=funcionario.horario_saida,
        dias_trabalho=funcionario.dias_trabalho,
    )


def cadastrar_funcionario_no_banco(funcionario):
    """Salva um novo funcionário no banco de dados."""
    try:
        with get_session() as session:
            session.add(_criar_entidade(funcionario))
    except IntegrityError:
        raise


def listar_funcionarios_do_banco():
    """Busca todos os funcionários cadastrados e devolve uma lista pronta para o frontend."""
    with get_session() as session:
        funcionarios = session.execute(select(Funcionario).order_by(Funcionario.id)).scalars().all()
        return [_funcionario_para_dict(funcionario) for funcionario in funcionarios]


def buscar_funcionario_por_id(funcionario_id):
    """Busca um funcionário pelo ID ou retorna None se não existir."""
    with get_session() as session:
        funcionario = session.get(Funcionario, funcionario_id)
        if funcionario is None:
            return None
        return _funcionario_para_dict(funcionario)


def atualizar_funcionario_no_banco(funcionario_id, dados):
    """Atualiza apenas os campos enviados para um funcionário já existente."""
    alteracoes = dados.model_dump(exclude_unset=True)
    if not alteracoes:
        return False, "Nenhum dado foi enviado para atualização."

    if "email" in alteracoes and alteracoes["email"] is not None:
        alteracoes["email"] = str(alteracoes["email"])

    try:
        with get_session() as session:
            funcionario = session.get(Funcionario, funcionario_id)
            if funcionario is None:
                return False, "Funcionário não encontrado."

            for campo, valor in alteracoes.items():
                setattr(funcionario, campo, valor)

            return True, None
    except IntegrityError:
        raise


def excluir_funcionario_do_banco(funcionario_id):
    """Remove do banco o funcionário identificado pelo ID informado."""
    with get_session() as session:
        funcionario = session.get(Funcionario, funcionario_id)
        if funcionario is None:
            return False

        session.delete(funcionario)
        return True


configure_database()
