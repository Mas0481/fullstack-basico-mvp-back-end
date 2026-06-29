import pytest

from my_api.config import configure
from my_api.model.funcionario import configure_database, inicializar_banco


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test.db"
    configure(database_url=f"sqlite:///{db_path.as_posix()}")
    configure_database(f"sqlite:///{db_path.as_posix()}")
    inicializar_banco()

    from my_api.main import create_app

    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def _payload_base():
    return {
        "nome": "Maria Silva",
        "data_nascimento": "1990-05-15",
        "genero": "Feminino",
        "cpf": "123.456.789-09",
        "email": "maria@email.com",
        "telefone": "11999998888",
        "cargo": "Analista",
        "departamento": "Tecnologia da Informação",
        "data_admissao": "2024-01-10",
        "salario": 4500.50,
        "tipo_contrato": "CLT",
        "horario_entrada": "08:00",
        "horario_saida_almoco": "12:00",
        "horario_retorno_almoco": "13:00",
        "horario_saida": "17:00",
        "dias_trabalho": "Seg, Ter, Qua, Qui, Sex",
    }


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_cadastrar_e_listar_funcionario(client):
    payload = _payload_base()

    create_response = client.post("/funcionarios", json=payload)
    assert create_response.status_code == 201
    assert create_response.get_json()["status"] == "sucesso"

    list_response = client.get("/funcionarios")
    body = list_response.get_json()
    assert list_response.status_code == 200
    assert body["status"] == "sucesso"
    assert len(body["data"]) == 1
    assert body["data"][0]["nome"] == payload["nome"]


def test_buscar_funcionario_por_id(client):
    payload = _payload_base()
    client.post("/funcionarios", json=payload)

    detail_response = client.get("/funcionarios/1")
    body = detail_response.get_json()
    assert detail_response.status_code == 200
    assert body["data"]["cpf"] == payload["cpf"]


def test_cpf_duplicado(client):
    payload = _payload_base()
    client.post("/funcionarios", json=payload)

    duplicate_response = client.post("/funcionarios", json=payload)
    assert duplicate_response.status_code == 400
    assert duplicate_response.get_json()["status"] == "erro"


def test_cpf_invalido(client):
    payload = _payload_base()
    payload["cpf"] = "111.111.111-11"

    response = client.post("/funcionarios", json=payload)
    assert response.status_code == 400
    body = response.get_json()
    assert body["status"] == "erro"
    assert body["mensagem"] == "Dados inválidos."
    assert "detalhes" in body
    assert body["detalhes"][0]["campo"] == "cpf"
    assert body["detalhes"][0]["mensagem"]


def test_atualizar_funcionario(client):
    payload = _payload_base()
    client.post("/funcionarios", json=payload)

    update_response = client.put(
        "/funcionarios/1",
        json={"cargo": "Desenvolvedora Senior", "cpf": payload["cpf"]},
    )
    assert update_response.status_code == 200

    detail_response = client.get("/funcionarios/1")
    assert detail_response.get_json()["data"]["cargo"] == "Desenvolvedora Senior"


def test_atualizar_funcionario_nao_bloqueia_cpf_proprio(client):
    payload = _payload_base()
    client.post("/funcionarios", json=payload)

    update_response = client.put(
        "/funcionarios/1",
        json={"departamento": "Produto", "cpf": payload["cpf"]},
    )
    assert update_response.status_code == 200

    detail_response = client.get("/funcionarios/1")
    body = detail_response.get_json()
    assert body["data"]["departamento"] == "Produto"
    assert body["data"]["cpf"] == payload["cpf"]


def test_excluir_funcionario(client):
    payload = _payload_base()
    client.post("/funcionarios", json=payload)

    delete_response = client.delete("/funcionarios/1")
    assert delete_response.status_code == 200

    detail_response = client.get("/funcionarios/1")
    assert detail_response.status_code == 404


def test_rotas_legadas(client):
    payload = _payload_base()
    legacy_create = client.post("/funcionarios/cadastrar", json=payload)
    assert legacy_create.status_code == 201

    legacy_list = client.get("/funcionarios/listar")
    assert legacy_list.status_code == 200
    assert legacy_list.get_json()["status"] == "sucesso"
