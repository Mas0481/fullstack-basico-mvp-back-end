from typing import Any, Optional


def success_response(
    data: Any = None,
    mensagem: str = "Operação realizada com sucesso.",
    status_code: int = 200,
):
    body = {"status": "sucesso", "mensagem": mensagem}
    if data is not None:
        body["data"] = data
    return body, status_code


def error_response(
    mensagem: str,
    detalhes: Optional[Any] = None,
    status_code: int = 400,
):
    body = {"status": "erro", "mensagem": mensagem}
    if detalhes is not None:
        body["detalhes"] = detalhes
    return body, status_code
