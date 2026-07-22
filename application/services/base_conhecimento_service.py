from infrastructure.database.database_schema import (
    AMBIENTES,
    CANAIS,
    ESTRUTURAS,
    FORMATOS,
    INTERESSES,
    JORNADAS,
    KPIS,
    MODALIDADES,
    MODELOS_COMERCIAIS,
    OBJETIVOS,
    PLATAFORMAS,
    SEGMENTOS,
    TECNOLOGIAS,
    UNIDADES,
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

        try:
            jornadas = self.catalogos.ordered(JORNADAS, "ordem")
        except Exception:
            jornadas = self.catalogos.ordered(JORNADAS, "etapa")

        return {
            "segmentos": self.catalogos.ordered(SEGMENTOS, "nome"),
            "interesses": self.catalogos.ordered(INTERESSES, "nome"),
            "jornadas": [
                item
                for item in jornadas
                if item.get("ativo", True)
            ],
        }

    def catalogos_inventario(self):

        dados = self.carregar_catalogos()
        dados["modelos_comerciais"] = self.catalogos.ordered(
            MODELOS_COMERCIAIS,
            "nome",
        )
        dados["formatos_ambientes"] = self.catalogos.formatos_ambientes()
        dados["modalidades_unidades"] = self.catalogos.modalidades_unidades()
        return dados

    def salvar_opcao_catalogo(
        self,
        categoria,
        nome,
        descricao="",
        parent_id=None,
        empresa="",
        site="",
    ):
        nome = nome.strip()
        if not nome:
            raise ValueError("Informe o nome da nova opção.")

        tabelas = {
            "tecnologia": TECNOLOGIAS,
            "canal": CANAIS,
            "ambiente": AMBIENTES,
            "estrutura": ESTRUTURAS,
            "formato": FORMATOS,
            "modelo_comercial": MODELOS_COMERCIAIS,
            "modalidade": MODALIDADES,
            "unidade": UNIDADES,
            "plataforma": PLATAFORMAS,
            "kpi": KPIS,
        }
        if categoria not in tabelas:
            raise ValueError("Categoria de catálogo inválida.")
        if categoria in {"canal", "ambiente", "formato", "unidade"} and not parent_id:
            raise ValueError("Selecione a opção anterior da hierarquia.")

        tabela = tabelas[categoria]
        campos_parent = {"canal": "tecnologia_id", "ambiente": "canal_id"}
        existente = self.catalogos.buscar_por_nome(
            tabela,
            nome,
            campos_parent.get(categoria),
            parent_id,
        )
        if existente:
            item = existente
        else:
            dados = {"nome": nome, "ativo": True}
            if categoria == "plataforma":
                dados.update(
                    {
                        "empresa": empresa.strip() or nome,
                        "site": site.strip() or None,
                    }
                )
            else:
                dados["descricao"] = descricao.strip() or None
            if categoria == "canal":
                dados["tecnologia_id"] = parent_id
            elif categoria == "ambiente":
                dados["canal_id"] = parent_id
            resposta = self.catalogos.salvar_opcao(tabela, dados)
            item = resposta.data[0]

        if categoria == "formato":
            if not parent_id:
                raise ValueError("O formato precisa estar relacionado a um ambiente.")
            self.catalogos.vincular_formato_ambiente(item["id"], parent_id)
        elif categoria == "unidade":
            if not parent_id:
                raise ValueError("A unidade precisa estar relacionada a uma modalidade.")
            self.catalogos.vincular_modalidade_unidade(parent_id, item["id"])
        return item

    def salvar_inventario(self, dados):

        if not dados.get("nome", "").strip():
            raise ValueError("Nome do inventário é obrigatório.")

        return self.inventarios.salvar(dados)

    def listar_inventarios(self):

        return self.inventarios.listar()

    def atualizar_inventario(self, inventario_id, dados):

        if not dados.get("nome", "").strip():
            raise ValueError("Nome do inventário é obrigatório.")
        return self.inventarios.atualizar(inventario_id, dados)

    def precos_inventario(self, inventario_id):

        return self.inventarios.listar_precos(inventario_id)

    def salvar_preco_inventario(self, dados):

        if float(dados.get("valor_bruto", -1)) < 0:
            raise ValueError("O preço não pode ser negativo.")

        return self.inventarios.salvar_preco(dados)

    def inventarios_com_papeis(self, campanha_ref):

        papeis = {
            item["inventario_id"]: item
            for item in self.inventarios.listar_papeis(campanha_ref)
        }
        return [
            {**inventario, "classificacao": papeis.get(inventario["id"])}
            for inventario in self.inventarios.listar()
        ]

    def salvar_papel_inventario(self, dados):

        return self.inventarios.salvar_papel(dados)

    def desmarcar_papeis_campanha(self, campanha_ref):

        return self.inventarios.desmarcar_papeis(campanha_ref)

    def excluir_papeis_campanha(self, campanha_ref):
        return self.inventarios.excluir_papeis(campanha_ref)
