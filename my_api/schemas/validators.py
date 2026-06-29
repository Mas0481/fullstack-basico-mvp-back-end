import re


def _apenas_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor)


def normalizar_e_validar_cpf(cpf: str) -> str:
    """Valida dígitos verificadores e retorna CPF apenas com números."""
    numeros = _apenas_digitos(cpf)

    if len(numeros) != 11:
        raise ValueError("CPF deve conter 11 dígitos.")

    if numeros == numeros[0] * 11:
        raise ValueError("CPF inválido.")

    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito_1 = 0 if resto == 10 else resto
    if digito_1 != int(numeros[9]):
        raise ValueError("CPF inválido.")

    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito_2 = 0 if resto == 10 else resto
    if digito_2 != int(numeros[10]):
        raise ValueError("CPF inválido.")

    return numeros


def formatar_cpf(cpf: str) -> str:
    numeros = _apenas_digitos(cpf)
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"


def normalizar_e_validar_telefone(telefone: str) -> str:
    """Aceita telefone brasileiro com 10 ou 11 dígitos."""
    numeros = _apenas_digitos(telefone)

    if len(numeros) not in (10, 11):
        raise ValueError("Telefone deve conter 10 ou 11 dígitos (com DDD).")

    return numeros
