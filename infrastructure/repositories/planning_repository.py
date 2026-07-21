from infrastructure.database.database_schema import PLANEJAMENTOS
from infrastructure.repositories.base_repository import BaseRepository


class PlanningRepository(BaseRepository):

    def listar(self):
        return self.ordered(PLANEJAMENTOS, "atualizado_em")

    def salvar(self, dados):
        return self.insert(PLANEJAMENTOS, dados)

    def atualizar(self, planejamento_id, dados):
        return self.update(PLANEJAMENTOS, "id", planejamento_id, dados)

    def excluir(self, planejamento_id):
        return self.delete(PLANEJAMENTOS, "id", planejamento_id)
