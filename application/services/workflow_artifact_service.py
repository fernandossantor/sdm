from dataclasses import asdict

from infrastructure.repositories.workflow_artifact_repository import (
    WorkflowArtifactRepository,
)


class WorkflowArtifactService:
    def __init__(self):
        self.repository = WorkflowArtifactRepository()

    def listar(self, tipo):
        try:
            return self.repository.listar(tipo)
        except Exception:
            return []

    def salvar(self, tipo, nome, artefato, planejamento_id=None):
        dados = asdict(artefato) if hasattr(artefato, "__dataclass_fields__") else artefato
        return self.repository.salvar(
            {
                "tipo": tipo,
                "nome": nome,
                "planejamento_id": planejamento_id,
                "dados": dados,
            }
        )
