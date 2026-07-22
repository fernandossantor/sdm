from dataclasses import asdict

from infrastructure.repositories.workflow_artifact_repository import (
    WorkflowArtifactRepository,
)


class WorkflowArtifactService:
    def __init__(self):
        self.repository = WorkflowArtifactRepository()

    def listar(self, tipo, projeto_id=None):
        try:
            return self.repository.listar(tipo, projeto_id)
        except Exception:
            return []

    def salvar(self, tipo, nome, artefato, planejamento_id=None):
        dados = self._serializar(artefato)
        return self.repository.salvar(
            {
                "tipo": tipo,
                "nome": nome,
                "planejamento_id": planejamento_id,
                "projeto_id": None,
                "dados": dados,
            }
        )

    def salvar_no_projeto(
        self, tipo, nome, artefato, session_state, planejamento_id=None
    ):
        dados = self._serializar(artefato)
        return self.repository.salvar(
            {
                "tipo": tipo,
                "nome": nome,
                "planejamento_id": planejamento_id,
                "projeto_id": session_state.get("projeto_id"),
                "dados": dados,
            }
        )

    def renomear(self, artefato_id, nome):
        if not nome.strip():
            raise ValueError("O nome não pode ficar vazio.")
        return self.repository.atualizar(artefato_id, {"nome": nome.strip()})

    def atualizar_dados(self, artefato_id, dados):
        return self.repository.atualizar(artefato_id, {"dados": dados})

    def excluir(self, artefato_id):
        return self.repository.excluir(artefato_id)

    @classmethod
    def _serializar(cls, valor):
        if hasattr(valor, "__dataclass_fields__"):
            return cls._serializar(asdict(valor))
        if isinstance(valor, dict):
            return {chave: cls._serializar(item) for chave, item in valor.items()}
        if isinstance(valor, (list, tuple)):
            return [cls._serializar(item) for item in valor]
        return valor
