from uuid import uuid4

from my_api.main import app


client = app.test_client()
cpf = f"mig-{uuid4().hex}"
payload = {
    "nome": "Mig Teste",
    "data_nascimento": "1990-01-01",
    "genero": "Não informar",
    "cpf": cpf,
    "email": "mig@example.com",
    "telefone": "11999999999",
    "cargo": "Analista",
    "departamento": "TI",
    "data_admissao": "2026-06-11",
    "salario": 1000.0,
    "tipo_contrato": "CLT",
    "horario_entrada": "08:00",
    "horario_saida_almoco": "12:00",
    "horario_retorno_almoco": "13:00",
    "horario_saida": "17:00",
    "dias_trabalho": "Seg, Ter",
}

post_response = client.post("/funcionarios", json=payload)
print("POST", post_response.status_code, post_response.get_json())
items = client.get("/funcionarios").get_json()
created = next((item for item in items if item.get("cpf") == cpf), None)
print("GET_FOUND", created is not None)
if created:
    delete_response = client.delete(f"/funcionarios/{created['id']}")
    print("DELETE", delete_response.status_code, delete_response.get_json())
