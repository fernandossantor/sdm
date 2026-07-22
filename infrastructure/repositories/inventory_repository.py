from infrastructure.database.database_schema import (
    INVENTARIOS,
    INVENTARIOS_METRICAS,
    INVENTARIOS_PAPEIS,
    PRECOS_INVENTARIO,
)
from infrastructure.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository):

    def listar(self):

        return self.ordered(INVENTARIOS, "nome")

    def salvar(self, dados):

        return self.insert(INVENTARIOS, dados)

    def atualizar(self, inventario_id, dados):

        return self.update(INVENTARIOS, "id", inventario_id, dados)

    def salvar_preco(self, dados):

        return self.insert(PRECOS_INVENTARIO, dados)

    def listar_precos(self, inventario_id):

        return self.by_field(PRECOS_INVENTARIO, "inventario_id", inventario_id)

    def listar_papeis(self, campanha_ref):

        return self.by_field(
            INVENTARIOS_PAPEIS,
            "campanha_ref",
            campanha_ref,
        )

    def salvar_papel(self, dados):

        return (
            self.db
            .table(INVENTARIOS_PAPEIS)
            .upsert(dados, on_conflict="campanha_ref,inventario_id")
            .execute()
        )

    def desmarcar_papeis(self, campanha_ref):

        return self.update(
            INVENTARIOS_PAPEIS,
            "campanha_ref",
            campanha_ref,
            {"selecionado": False},
        )

    def excluir_papeis(self, campanha_ref):
        return self.delete(INVENTARIOS_PAPEIS, "campanha_ref", campanha_ref)

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
