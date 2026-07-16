from infrastructure.database.database_schema import *

from infrastructure.repositories.base_repository import (
    BaseRepository
)


class CatalogRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # CATÁLOGOS
    # =====================================================

    def canais(self):

        return self.ordered(

            CANAIS,

            "nome"

        )

    def ambientes(self):

        return self.ordered(

            AMBIENTES,

            "nome"

        )

    def estruturas(self):

        return self.ordered(

            ESTRUTURAS,

            "nome"

        )

    def formatos(self):

        return self.ordered(

            FORMATOS,

            "nome"

        )

    def tecnologias(self):

        return self.ordered(

            TECNOLOGIAS,

            "nome"

        )

    def perfis(self):

        return self.ordered(

            PERFIS,

            "nome"

        )

    def modalidades(self):

        return self.ordered(

            MODALIDADES,

            "nome"

        )

    def unidades(self):

        return self.ordered(

            UNIDADES,

            "nome"

        )

    def plataformas(self):

        return self.ordered(

            PLATAFORMAS,

            "nome"

        )

    def kpis(self):

        return self.ordered(

            KPIS,

            "nome"

        )

    # =====================================================
    # TODOS
    # =====================================================

    def carregar_todos(self):

        return {

            "canais": self.canais(),

            "ambientes": self.ambientes(),

            "estruturas": self.estruturas(),

            "formatos": self.formatos(),

            "tecnologias": self.tecnologias(),

            "perfis": self.perfis(),

            "modalidades": self.modalidades(),

            "unidades": self.unidades(),

            "plataformas": self.plataformas(),

            "kpis": self.kpis()

        }