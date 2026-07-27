from datetime import datetime, timezone

from infrastructure.database.database_schema import (
    PLANEJAMENTOS,
    VERSOES_PLANEJAMENTO,
)
from infrastructure.repositories.base_repository import BaseRepository


class PlanningRepository(BaseRepository):

    def listar(self):
        return self.ordered(PLANEJAMENTOS, "atualizado_em")

    def salvar(self, dados):
        return self.insert(PLANEJAMENTOS, dados)

    def obter(self, planejamento_id):
        return self.by_id(PLANEJAMENTOS, planejamento_id)

    def atualizar(self, planejamento_id, dados):
        return self.update(PLANEJAMENTOS, "id", planejamento_id, dados)

    def excluir(self, planejamento_id):
        return self.update(
            PLANEJAMENTOS,
            "id",
            planejamento_id,
            {
                "status": "ARQUIVADO",
                "arquivado_em": datetime.now(timezone.utc).isoformat(),
            },
        )

    def versoes(self, planejamento_id):
        return (
            self.db
            .table(VERSOES_PLANEJAMENTO)
            .select("*")
            .eq("planejamento_id", planejamento_id)
            .order("numero", desc=True)
            .execute()
            .data
        )
