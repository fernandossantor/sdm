from infrastructure.database.workspace_context import bind_workspace
from infrastructure.repositories.workspace_repository import WorkspaceRepository


CHAVES_CONTEXTO_PROJETO = (
    "projeto_id",
    "projeto_nome",
    "projeto_codigo",
    "projeto_progresso",
    "briefing",
    "briefing_id",
    "briefing_ref",
    "plano",
    "planejamento_id",
    "forecast",
    "diagnostico",
    "dashboard",
    "exportacao",
)


class WorkspaceService:
    def __init__(self, repository=None):
        self.repository = repository or WorkspaceRepository()

    def listar(self, usuario_id, administrador=False):
        espacos = self.repository.listar()
        if administrador:
            return [{**item, "papel": "ADMINISTRADOR"} for item in espacos]

        papeis = {
            item["espaco_id"]: item["papel"]
            for item in self.repository.papeis_do_usuario(usuario_id)
        }
        return [
            {**item, "papel": papeis[item["id"]]}
            for item in espacos
            if item["id"] in papeis
        ]

    def selecionar(self, espaco_id, espacos, session_state):
        espaco = next(
            (item for item in espacos if item["id"] == espaco_id),
            None,
        )
        if not espaco:
            raise PermissionError("Espaço de trabalho não autorizado.")

        anterior = session_state.get("espaco_id")
        session_state["espaco_id"] = espaco["id"]
        session_state["espaco_nome"] = espaco["nome"]
        session_state["espaco_papel"] = espaco["papel"]
        bind_workspace(espaco["id"])

        if anterior and anterior != espaco["id"]:
            for chave in CHAVES_CONTEXTO_PROJETO:
                session_state.pop(chave, None)
        return espaco
