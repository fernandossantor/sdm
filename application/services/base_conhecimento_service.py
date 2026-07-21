from infrastructure.database.database_schema import (
    INTERESSES,
    JORNADAS,
    MODELOS_COMERCIAIS,
    OBJETIVOS,
    SEGMENTOS,
)
from infrastructure.repositories.catalog_repository import CatalogRepository
from infrastructure.repositories.inventory_repository import InventoryRepository


class BaseConhecimentoService:

    def __init__(self):

        self.catalogos = CatalogRepository()
        self.inventarios = InventoryRepository()

    def carregar_catalogos(self):

        return self.catalogos.carregar_todos()

    def objetivos(self):

        return self.catalogos.ordered(OBJETIVOS, "nome")

    def kpis(self):

        return self.catalogos.kpis()

    def biblioteca_publicos(self):

        return {
            "segmentos": self.catalogos.ordered(SEGMENTOS, "nome"),
            "interesses": self.catalogos.ordered(INTERESSES, "nome"),
            "jornadas": self.catalogos.ordered(JORNADAS, "etapa"),
        }

    def catalogos_inventario(self):

        dados = self.carregar_catalogos()
        dados["modelos_comerciais"] = self.catalogos.ordered(
            MODELOS_COMERCIAIS,
            "nome",
        )
        return dados

    def salvar_inventario(self, dados):

        if not dados.get("nome", "").strip():
            raise ValueError("Nome do inventário é obrigatório.")

        return self.inventarios.salvar(dados)
