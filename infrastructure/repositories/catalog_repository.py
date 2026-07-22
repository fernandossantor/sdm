from infrastructure.database.database_schema import *

from infrastructure.repositories.base_repository import (
    BaseRepository
)


class CatalogRepository(BaseRepository):

    TABELAS_EDITAVEIS = {
        CANAIS,
        AMBIENTES,
        ESTRUTURAS,
        FORMATOS,
        TECNOLOGIAS,
        MODALIDADES,
        UNIDADES,
        PLATAFORMAS,
        KPIS,
        MODELOS_COMERCIAIS,
    }

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

    def formatos_ambientes(self):

        return self.ordered(FORMATOS_AMBIENTES, "ambiente_id")

    def modalidades_unidades(self):

        return self.ordered(MODALIDADES_UNIDADES, "modalidade_id")

    def buscar_por_nome(self, tabela, nome, campo_parent=None, parent_id=None):

        if tabela not in self.TABELAS_EDITAVEIS:
            raise ValueError("Catálogo não permitido para edição.")
        consulta = (
            self.db.table(tabela)
            .select("*")
            .ilike("nome", nome.strip())
        )
        if campo_parent and parent_id:
            consulta = consulta.eq(campo_parent, parent_id)
        resposta = consulta.limit(1).execute()
        return resposta.data[0] if resposta.data else None

    def salvar_opcao(self, tabela, dados):

        if tabela not in self.TABELAS_EDITAVEIS:
            raise ValueError("Catálogo não permitido para edição.")
        return self.insert(tabela, dados)

    def vincular_formato_ambiente(self, formato_id, ambiente_id):

        return (
            self.db.table(FORMATOS_AMBIENTES)
            .upsert(
                {"formato_id": formato_id, "ambiente_id": ambiente_id},
                on_conflict="formato_id,ambiente_id",
            )
            .execute()
        )

    def vincular_modalidade_unidade(self, modalidade_id, unidade_id):

        return (
            self.db.table(MODALIDADES_UNIDADES)
            .upsert(
                {"modalidade_id": modalidade_id, "unidade_id": unidade_id},
                on_conflict="modalidade_id,unidade_id",
            )
            .execute()
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
