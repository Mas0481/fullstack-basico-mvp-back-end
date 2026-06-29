from datetime import date, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .validators import normalizar_e_validar_cpf, normalizar_e_validar_telefone


class FuncionarioSchema(BaseModel):
    """Define os dados obrigatórios e opcionais para criar um funcionário."""

    nome: str = Field(min_length=2, max_length=120)
    data_nascimento: date
    genero: Optional[str] = None
    cpf: str
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cargo: str = Field(min_length=2, max_length=120)
    departamento: str = Field(min_length=2, max_length=120)
    data_admissao: date
    salario: Optional[Decimal] = Decimal("0.00")
    tipo_contrato: Optional[str] = "CLT"
    horario_entrada: Optional[time] = None
    horario_saida_almoco: Optional[time] = None
    horario_retorno_almoco: Optional[time] = None
    horario_saida: Optional[time] = None
    dias_trabalho: Optional[str] = None

    @field_validator("nome", "cargo", "departamento")
    @classmethod
    def validar_texto_obrigatorio(cls, valor: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError("Campo não pode ser vazio.")
        return texto

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, valor: str) -> str:
        return normalizar_e_validar_cpf(valor)

    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None or valor.strip() == "":
            return None
        return normalizar_e_validar_telefone(valor)

    @field_validator("genero", "tipo_contrato", "dias_trabalho")
    @classmethod
    def validar_texto_opcional(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return None
        texto = valor.strip()
        return texto or None


class FuncionarioUpdateSchema(BaseModel):
    """Define os campos que podem ser enviados quando um funcionário for editado."""

    nome: Optional[str] = Field(default=None, min_length=2, max_length=120)
    data_nascimento: Optional[date] = None
    genero: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cargo: Optional[str] = Field(default=None, min_length=2, max_length=120)
    departamento: Optional[str] = Field(default=None, min_length=2, max_length=120)
    data_admissao: Optional[date] = None
    salario: Optional[Decimal] = None
    tipo_contrato: Optional[str] = None
    horario_entrada: Optional[time] = None
    horario_saida_almoco: Optional[time] = None
    horario_retorno_almoco: Optional[time] = None
    horario_saida: Optional[time] = None
    dias_trabalho: Optional[str] = None

    @field_validator("nome", "cargo", "departamento")
    @classmethod
    def validar_texto_opcional_obrigatorio(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return None
        texto = valor.strip()
        if not texto:
            raise ValueError("Campo não pode ser vazio.")
        return texto

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return None
        return normalizar_e_validar_cpf(valor)

    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None or valor.strip() == "":
            return None
        return normalizar_e_validar_telefone(valor)

    @field_validator("genero", "tipo_contrato", "dias_trabalho")
    @classmethod
    def validar_texto_opcional(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return None
        texto = valor.strip()
        return texto or None


class FuncionarioOut(FuncionarioSchema):
    """Representa o funcionário retornado pela API, incluindo o ID do registro."""

    id: int

    model_config = ConfigDict(from_attributes=True)
