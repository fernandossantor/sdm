from infrastructure.database.database_schema import PROJETOS
from infrastructure.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository):
    def listar(self):
        return self.ordered(PROJETOS, "atualizado_em")

    def criar(self, nome):
        return self.insert(PROJETOS, {"nome": nome.strip()})

    def salvar(self, dados):
        return self.insert(PROJETOS, dados)

    def atualizar(self, projeto_id, dados):
        return self.update(PROJETOS, "id", projeto_id, dados)

    def excluir(self, projeto_id):
        return self.update(PROJETOS, "id", projeto_id, {"ativo": False})
