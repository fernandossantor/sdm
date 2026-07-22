from infrastructure.database.database_schema import ARTEFATOS_WORKFLOW
from infrastructure.repositories.base_repository import BaseRepository


class WorkflowArtifactRepository(BaseRepository):
    def listar(self, tipo):
        return self.by_field(ARTEFATOS_WORKFLOW, "tipo", tipo)

    def salvar(self, dados):
        return self.insert(ARTEFATOS_WORKFLOW, dados)
