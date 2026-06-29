import logging

from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from flask_restx import Api, Namespace, Resource
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from .config import Config
from .logging_config import configure_logging
from .model import (
    atualizar_funcionario_no_banco,
    buscar_funcionario_por_id,
    cadastrar_funcionario_no_banco,
    excluir_funcionario_do_banco,
    inicializar_banco,
    listar_funcionarios_do_banco,
)
from .responses import error_response, success_response
from .schemas import FuncionarioSchema, FuncionarioUpdateSchema
from .swagger_helpers import build_swagger_models

logger = logging.getLogger(__name__)


def create_app():
    configure_logging()
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def home():
        return jsonify(
            {
                "status": "ok",
                "mensagem": "API Flask ativa",
                "docs": "/docs",
                "rotas": [
                    "GET /funcionarios",
                    "GET /funcionarios/<id>",
                    "POST /funcionarios",
                    "PUT /funcionarios/<id>",
                    "DELETE /funcionarios/<id>",
                ],
            }
        )

    api = Api(
        app,
        version="1.0.0",
        title="API de Cadastro de Funcionários",
        description=(
            "API REST em Flask para gestão de colaboradores. "
            "Validação feita com Pydantic; persistência com SQLAlchemy."
        ),
        doc="/docs",
    )

    @api.documentation
    def custom_documentation():
        return render_template_string(
            """
<!doctype html>
<html lang="pt-BR">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{{ title }}</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
        <style>
            body { margin: 0; background: #f6f7fb; }
            .swagger-ui .topbar { display: none; }
            .swagger-ui .info { margin: 24px 0; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = () => {
                SwaggerUIBundle({
                    url: {{ specs_url|tojson }},
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [SwaggerUIBundle.presets.apis],
                    layout: 'BaseLayout',
                });

                const preencherPayloadEdicao = async (input) => {
                    const valor = input.value.trim();
                    if (!valor) {
                        return;
                    }

                    const id = Number.parseInt(valor, 10);
                    if (Number.isNaN(id)) {
                        return;
                    }

                    const opblock = input.closest('.opblock');
                    if (!opblock) {
                        return;
                    }

                    const textarea = opblock.querySelector('textarea.body-param__text');
                    if (!textarea) {
                        return;
                    }

                    const response = await fetch(`/funcionarios/${id}`, {
                        headers: { Accept: 'application/json' },
                    });
                    const json = await response.json();
                    if (!response.ok || !json || !json.data) {
                        return;
                    }

                    const payload = Object.fromEntries(
                        Object.entries(json.data).filter(([chave]) => chave !== 'id')
                    );

                    const valueSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
                    valueSetter.call(textarea, JSON.stringify(payload, null, 2));
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    textarea.dispatchEvent(new Event('change', { bubbles: true }));
                };

                document.addEventListener('input', (event) => {
                    const target = event.target;
                    if (!(target instanceof HTMLInputElement)) {
                        return;
                    }

                    const identificador = `${target.name || ''} ${target.id || ''} ${target.placeholder || ''}`;
                    if (/funcionario_id/i.test(identificador)) {
                        preencherPayloadEdicao(target);
                    }
                });

                document.addEventListener('change', (event) => {
                    const target = event.target;
                    if (!(target instanceof HTMLInputElement)) {
                        return;
                    }

                    const identificador = `${target.name || ''} ${target.id || ''} ${target.placeholder || ''}`;
                    if (/funcionario_id/i.test(identificador)) {
                        preencherPayloadEdicao(target);
                    }
                });
            };
        </script>
    </body>
</html>
            """,
            title=api.title,
            specs_url=api.specs_url,
        )

    ns = Namespace("funcionarios", description="CRUD de funcionários")
    api.add_namespace(ns, path="/funcionarios")
    models = build_swagger_models(api)

    def _parse_json_schema(schema_class):
        data = request.get_json(silent=True)
        if data is None:
            return None, *error_response("Corpo JSON ausente.", status_code=400)

        try:
            return schema_class.model_validate(data), None, None
        except ValidationError as exc:
            detalhes = [
                {
                    "campo": ".".join(str(part) for part in error.get("loc", ())),
                    "mensagem": error.get("msg"),
                    "tipo": error.get("type"),
                }
                for error in exc.errors(include_context=False)
            ]
            return None, *error_response("Dados inválidos.", detalhes=detalhes, status_code=400)

    def _listar_funcionarios():
        funcionarios = listar_funcionarios_do_banco()
        return success_response(
            data=funcionarios,
            mensagem="Funcionários listados com sucesso.",
        )

    def _buscar_funcionario(funcionario_id):
        funcionario = buscar_funcionario_por_id(funcionario_id)
        if funcionario is None:
            return error_response("Funcionário não encontrado.", status_code=404)
        return success_response(
            data=funcionario,
            mensagem="Funcionário encontrado.",
        )

    def _cadastrar_funcionario():
        payload, error_body, status_code = _parse_json_schema(FuncionarioSchema)
        if error_body:
            return error_body, status_code

        try:
            cadastrar_funcionario_no_banco(payload)
            return success_response(
                mensagem="Funcionário cadastrado com sucesso!",
                status_code=201,
            )
        except IntegrityError:
            return error_response("Erro: este CPF já está cadastrado.", status_code=400)
        except Exception:
            logger.exception("Erro ao cadastrar funcionário.")
            return error_response("Erro interno no servidor.", status_code=500)

    def _atualizar_funcionario(funcionario_id):
        payload, error_body, status_code = _parse_json_schema(FuncionarioUpdateSchema)
        if error_body:
            return error_body, status_code

        try:
            atualizado, erro = atualizar_funcionario_no_banco(funcionario_id, payload)
            if not atualizado:
                status = 404 if erro == "Funcionário não encontrado." else 400
                return error_response(erro, status_code=status)

            return success_response(mensagem="Funcionário atualizado com sucesso!")
        except IntegrityError:
            return error_response(
                "Erro: este CPF já está cadastrado para outro funcionário.",
                status_code=400,
            )
        except Exception:
            logger.exception("Erro ao atualizar funcionário %s.", funcionario_id)
            return error_response("Erro interno no servidor.", status_code=500)

    def _excluir_funcionario(funcionario_id):
        try:
            excluido = excluir_funcionario_do_banco(funcionario_id)
            if not excluido:
                return error_response("Funcionário não encontrado.", status_code=404)

            return success_response(mensagem="Funcionário excluído com sucesso!")
        except Exception:
            logger.exception("Erro ao excluir funcionário %s.", funcionario_id)
            return error_response("Erro interno no servidor.", status_code=500)

    @ns.route("")
    class FuncionarioCollection(Resource):
        def get(self):
            """Lista todos os funcionários cadastrados."""
            return _listar_funcionarios()

        @ns.expect(models["funcionario"], validate=False)
        def post(self):
            """Cadastra um novo funcionário."""
            return _cadastrar_funcionario()

    @ns.route("/<int:funcionario_id>")
    class FuncionarioItem(Resource):
        def get(self, funcionario_id):
            """Busca um funcionário pelo ID."""
            return _buscar_funcionario(funcionario_id)

        @ns.expect(models["funcionario_update"], validate=False)
        def put(self, funcionario_id):
            """Atualiza um funcionário existente."""
            return _atualizar_funcionario(funcionario_id)

        def delete(self, funcionario_id):
            """Exclui um funcionário pelo ID."""
            return _excluir_funcionario(funcionario_id)

    @app.cli.command("init-db")
    def init_db_command():
        """Inicializa o banco de dados via CLI: flask --app my_api.main:app init-db"""
        inicializar_banco()
        print("Banco inicializado com sucesso.")

    with app.app_context():
        inicializar_banco()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
