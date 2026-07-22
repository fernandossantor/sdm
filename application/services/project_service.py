from datetime import datetime, timezone

from infrastructure.repositories.project_repository import ProjectRepository
from application.services.identifier_service import IdentifierService


class ProjectService:
    def __init__(self):
        self.repository = ProjectRepository()

    def listar(self):
        try:
            return [item for item in self.repository.listar() if item.get("ativo", True)]
        except Exception:
            return []

    def criar(self, nome, session_state):
        if not nome.strip():
            raise ValueError("Informe o nome do projeto.")
        resposta = self.repository.criar(nome)
        projeto = resposta.data[0]
        self.selecionar(projeto, session_state)
        return projeto

    def duplicar(self, projeto_id, session_state):
        origem = next((item for item in self.listar() if item["id"] == projeto_id), None)
        if not origem:
            raise ValueError("Projeto não encontrado.")
        novo_id, codigo = IdentifierService.preparar_copia(origem, "projetos")
        resposta = self.repository.salvar({
            "id": novo_id, "codigo": codigo,
            "nome": f"{origem['nome']} — cópia",
            "etapa_atual": "briefing", "progresso": {}, "ativo": True,
        })
        projeto = resposta.data[0]
        self.selecionar(projeto, session_state)
        return projeto

    @staticmethod
    def selecionar(projeto, session_state):
        session_state["projeto_id"] = projeto["id"]
        session_state["projeto_nome"] = projeto["nome"]
        session_state["projeto_codigo"] = projeto.get("codigo")
        session_state["projeto_progresso"] = projeto.get("progresso") or {}

    def registrar(self, session_state, etapa, concluida=True, **dados):
        projeto_id = session_state.get("projeto_id")
        if not projeto_id:
            return None
        progresso = dict(session_state.get("projeto_progresso") or {})
        progresso[etapa] = concluida
        session_state["projeto_progresso"] = progresso
        payload = {
            "etapa_atual": etapa,
            "progresso": progresso,
            "atualizado_em": datetime.now(timezone.utc).isoformat(),
            **dados,
        }
        return self.repository.atualizar(projeto_id, payload)

    def excluir(self, projeto_id):
        return self.repository.excluir(projeto_id)
