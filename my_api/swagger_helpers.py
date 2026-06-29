"""Helpers para documentação Swagger derivada dos schemas Pydantic."""

from flask_restx import fields

from .schemas import FuncionarioSchema, FuncionarioUpdateSchema


def build_swagger_models(api):
    """Cria modelos Swagger mínimos com referência aos schemas Pydantic."""
    funcionario_example = {
        "nome": "Maria Silva",
        "data_nascimento": "1990-05-20",
        "genero": "Feminino",
        "cpf": "12345678909",
        "email": "maria.silva@empresa.com",
        "telefone": "11999999999",
        "cargo": "Analista de Sistemas",
        "departamento": "TI",
        "data_admissao": "2024-01-15",
        "salario": 6500.0,
        "tipo_contrato": "CLT",
        "horario_entrada": "08:00",
        "horario_saida_almoco": "12:00",
        "horario_retorno_almoco": "13:00",
        "horario_saida": "17:00",
        "dias_trabalho": "Segunda a sexta",
    }

    funcionario_model = api.model(
        "Funcionario",
        {
            "nome": fields.String(required=True, description="Nome completo", example=funcionario_example["nome"]),
            "data_nascimento": fields.String(required=True, description="YYYY-MM-DD", example=funcionario_example["data_nascimento"]),
            "genero": fields.String(required=False, example=funcionario_example["genero"]),
            "cpf": fields.String(required=True, description="CPF com ou sem máscara", example=funcionario_example["cpf"]),
            "email": fields.String(required=False, example=funcionario_example["email"]),
            "telefone": fields.String(required=False, description="10 ou 11 dígitos com DDD", example=funcionario_example["telefone"]),
            "cargo": fields.String(required=True, example=funcionario_example["cargo"]),
            "departamento": fields.String(required=True, example=funcionario_example["departamento"]),
            "data_admissao": fields.String(required=True, description="YYYY-MM-DD", example=funcionario_example["data_admissao"]),
            "salario": fields.Float(required=False, example=funcionario_example["salario"]),
            "tipo_contrato": fields.String(required=False, default="CLT", example=funcionario_example["tipo_contrato"]),
            "horario_entrada": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_entrada"]),
            "horario_saida_almoco": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_saida_almoco"]),
            "horario_retorno_almoco": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_retorno_almoco"]),
            "horario_saida": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_saida"]),
            "dias_trabalho": fields.String(required=False, example=funcionario_example["dias_trabalho"]),
        },
    )

    funcionario_update_model = api.model(
        "FuncionarioUpdate",
        {
            "nome": fields.String(required=False, example=funcionario_example["nome"]),
            "data_nascimento": fields.String(required=False, description="YYYY-MM-DD", example=funcionario_example["data_nascimento"]),
            "genero": fields.String(required=False, example=funcionario_example["genero"]),
            "cpf": fields.String(required=False, description="CPF com ou sem máscara", example=funcionario_example["cpf"]),
            "email": fields.String(required=False, example=funcionario_example["email"]),
            "telefone": fields.String(required=False, description="10 ou 11 dígitos com DDD", example=funcionario_example["telefone"]),
            "cargo": fields.String(required=False, example=funcionario_example["cargo"]),
            "departamento": fields.String(required=False, example=funcionario_example["departamento"]),
            "data_admissao": fields.String(required=False, description="YYYY-MM-DD", example=funcionario_example["data_admissao"]),
            "salario": fields.Float(required=False, example=funcionario_example["salario"]),
            "tipo_contrato": fields.String(required=False, example=funcionario_example["tipo_contrato"]),
            "horario_entrada": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_entrada"]),
            "horario_saida_almoco": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_saida_almoco"]),
            "horario_retorno_almoco": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_retorno_almoco"]),
            "horario_saida": fields.String(required=False, description="HH:MM", example=funcionario_example["horario_saida"]),
            "dias_trabalho": fields.String(required=False, example=funcionario_example["dias_trabalho"]),
        },
    )

    response_model = api.model(
        "ApiResponse",
        {
            "status": fields.String(required=True, description="sucesso ou erro"),
            "mensagem": fields.String(required=True),
            "data": fields.Raw(required=False),
            "detalhes": fields.Raw(required=False),
        },
    )

    funcionario_out_model = api.model(
        "FuncionarioOut",
        {
            "id": fields.Integer(required=True),
            **{field: fields.Raw(required=False) for field in FuncionarioSchema.model_fields},
        },
    )

    return {
        "funcionario": funcionario_model,
        "funcionario_update": funcionario_update_model,
        "response": response_model,
        "funcionario_out": funcionario_out_model,
    }
