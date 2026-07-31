from infrastructure.database.workspace_context import bind_workspace
from infrastructure.repositories.workspace_repository import WorkspaceRepository

CHAVES_CONTEXTO_PROJETO = (
    "campanha_id",
    "campanha_codigo",
    "campanha_nome",
    "campanha_etapa",
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
        papeis = {
            item["espaco_id"]: item["papel"]
            for item in self.repository.papeis_do_usuario(usuario_id)
        }
        if administrador:
            return [
                {
                    **item,
                    "papel": (
                        "PROPRIETARIO"
                        if str(item.get("proprietario_id")) == str(usuario_id)
                        else papeis.get(item["id"], "ADMINISTRADOR")
                    ),
                }
                for item in espacos
            ]
        return [
            {
                **item,
                "papel": (
                    "PROPRIETARIO"
                    if str(item.get("proprietario_id")) == str(usuario_id)
                    else papeis.get(item["id"], "COMPARTILHADO")
                ),
            }
            for item in espacos
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
        session_state["espaco_proprietario_id"] = espaco.get("proprietario_id")
        if espaco["papel"] == "ADMINISTRADOR":
            session_state["espaco_planejador_padrao_id"] = espaco.get("proprietario_id")
            session_state["espaco_planejador_padrao_nome"] = "Proprietário do espaço"
        else:
            session_state["espaco_planejador_padrao_id"] = session_state.get(
                "auth_user_id"
            )
            session_state["espaco_planejador_padrao_nome"] = session_state.get(
                "auth_email"
            )
        bind_workspace(espaco["id"])

        if anterior and anterior != espaco["id"]:
            for chave in CHAVES_CONTEXTO_PROJETO:
                session_state.pop(chave, None)
        return espaco
