from infrastructure.database.database_schema import (
    INVENTARIOS,
    INVENTARIOS_METRICAS,
)
from infrastructure.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository):

    def listar(self):

        return self.ordered(INVENTARIOS, "nome")

    def salvar(self, dados):

        return self.insert(INVENTARIOS, dados)

    def listar_por_ambiente(self, ambiente_id):

        return self.by_field(
            INVENTARIOS,
            "ambiente_id",
            ambiente_id,
            campos=(
                "id,nome,descricao,plataforma_id,ambiente_id,formato_id,"
                "estrutura_id,modelo_comercial_id,modalidade_compra_id,"
                "unidade_compra_id"
            ),
        )

    def obter_metricas(self, inventario_id):

        metricas = self.by_field(
            INVENTARIOS_METRICAS,
            "inventario_id",
            inventario_id,
        )

        return metricas[0] if metricas else None
