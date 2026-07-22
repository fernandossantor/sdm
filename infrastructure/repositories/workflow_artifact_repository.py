from infrastructure.database.database_schema import ARTEFATOS_WORKFLOW
from infrastructure.repositories.base_repository import BaseRepository


class WorkflowArtifactRepository(BaseRepository):
    def listar(self, tipo, projeto_id=None):
        consulta = self.db.table(ARTEFATOS_WORKFLOW).select("*").eq("tipo", tipo)
        if projeto_id:
            consulta = consulta.eq("projeto_id", projeto_id)
        return consulta.execute().data

    def salvar(self, dados):
        return self.insert(ARTEFATOS_WORKFLOW, dados)

    def atualizar(self, artefato_id, dados):
        return self.update(ARTEFATOS_WORKFLOW, "id", artefato_id, dados)

    def excluir(self, artefato_id):
        return self.delete(ARTEFATOS_WORKFLOW, "id", artefato_id)
