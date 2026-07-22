from infrastructure.repositories.public_repository import (
    PublicRepository
)
from infrastructure.repositories.segment_repository import SegmentRepository
from infrastructure.repositories.universe_repository import UniverseRepository
from infrastructure.repositories.catalog_repository import CatalogRepository
from infrastructure.database.database_schema import INTERESSES, JORNADAS
from application.services.identifier_service import IdentifierService


class PublicService:

    def __init__(self):

        self.repository = PublicRepository()

        self.segmentos_repository = SegmentRepository()

        self.universos_repository = UniverseRepository()

        self.catalogos_repository = CatalogRepository()

    # =====================================================
    # LISTAGEM
    # =====================================================

    def listar(self):

        return self.repository.listar()

    def listar_detalhados(self):

        publicos = self.listar()

        segmentos = {
            item["id"]: item
            for item in self.segmentos_repository.listar()
        }

        universos = {
            item["id"]: item
            for item in self.universos_repository.listar()
        }

        interesses = {
            item["id"]: item
            for item in self.catalogos_repository.ordered(INTERESSES, "nome")
        }

        try:
            lista_jornadas = self.catalogos_repository.ordered(JORNADAS, "ordem")
        except Exception:
            lista_jornadas = self.catalogos_repository.ordered(JORNADAS, "etapa")

        jornadas = {item["id"]: item for item in lista_jornadas}

        resultado = []

        for publico in publicos:
            item = dict(publico)
            rel_segmentos = self.repository.segmentos(publico["id"])
            rel_interesses = self.repository.interesses(publico["id"])
            rel_jornadas = self.repository.jornadas(publico["id"])

            item["segmentos"] = []
            item["universos"] = []

            for relacao in rel_segmentos:
                segmento = segmentos.get(relacao.get("segmento_id"))
                if not segmento:
                    continue
                item["segmentos"].append(segmento)
                universo = universos.get(segmento.get("universo_id"))
                if universo and universo not in item["universos"]:
                    item["universos"].append(universo)

            item["interesses"] = [
                {
                    **interesses[relacao["interesse_id"]],
                    "peso": float(relacao.get("peso", 100)),
                }
                for relacao in rel_interesses
                if relacao.get("interesse_id") in interesses
            ]

            item["jornada"] = None
            if rel_jornadas:
                item["jornada"] = jornadas.get(rel_jornadas[0].get("jornada_id"))

            populacao_segmentos = sum(
                int(segmento.get("populacao") or 0)
                for segmento in item["segmentos"]
            )
            limite_universos = sum(
                int(universo.get("publico_alvo") or universo.get("populacao") or 0)
                for universo in item["universos"]
            )
            item["populacao_estimada"] = (
                min(populacao_segmentos, limite_universos)
                if populacao_segmentos > 0 and limite_universos > 0
                else max(populacao_segmentos, limite_universos)
            )

            resultado.append(item)

        return resultado

    # =====================================================
    # BUSCA
    # =====================================================

    def buscar(

        self,

        publico_id

    ):

        publico = self.repository.buscar(

            publico_id

        )

        publico["segmentos"] = self.repository.segmentos(

            publico_id

        )

        publico["interesses"] = self.repository.interesses(

            publico_id

        )

        publico["jornadas"] = self.repository.jornadas(

            publico_id

        )

        return publico

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar(

        self,

        dados

    ):

        erros = []

        if not dados["nome"]:

            erros.append(

                "Nome é obrigatório."

            )

        if "segmentos" in dados and not dados.get("segmentos"):
            erros.append("Selecione pelo menos um Segmento.")

        return erros

    # =====================================================
    # SALVAR
    # =====================================================

    def salvar(

        self,

        dados,

        segmentos=None,

        interesses=None,

        jornada=None

    ):

        segmentos = segmentos or []

        interesses = interesses or []

        dados_publico = dict(dados)
        dados_validacao = {**dados_publico, "segmentos": segmentos}
        erros = self.validar(dados_validacao)

        if erros:

            return False, erros

        try:
            resposta = self.repository.salvar(dados_publico)
            publico = resposta.data[0]
            publico_id = publico["id"]
        except Exception as erro:
            return False, [f"Não foi possível salvar o Público: {erro}"]

        registros_segmentos = [

            {

                "publico_id": publico_id,

                "segmento_id": segmento

            }

            for segmento in segmentos

        ]

        registros_interesses = [

            {

                "publico_id": publico_id,

                "interesse_id": interesse

            }

            for interesse in interesses

        ]

        try:
            self.repository.salvar_segmentos(registros_segmentos)
            self.repository.salvar_interesses(registros_interesses)

            if jornada:
                self.repository.salvar_jornada(publico_id, jornada)
        except Exception:
            # Evita deixar um público órfão quando uma relação falha.
            self.repository.excluir(publico_id)
            return False, [
                "Não foi possível salvar as relações de Segmentos, "
                "Interesses e Jornada do Público."
            ]

        return True, publico

    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(

        self,

        publico_id,

        dados

    ):

        erros = self.validar(

            dados

        )

        if erros:

            return False, erros

        self.repository.atualizar(

            publico_id,

            dados

        )

        return True, None

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir(

        self,

        publico_id

    ):

        self.repository.excluir(

            publico_id

        )

    def duplicar(self, publico):
        novo_id, codigo = IdentifierService.preparar_copia(publico, "biblioteca_publicos")
        dados = {
            "id": novo_id, "codigo": codigo,
            "nome": f"{publico['nome']} — cópia",
            "descricao": publico.get("descricao"), "ativo": publico.get("ativo", True),
        }
        resposta = self.repository.salvar(dados)
        self.repository.salvar_segmentos([
            {"publico_id": novo_id, "segmento_id": item["id"]}
            for item in publico.get("segmentos", [])
        ])
        self.repository.salvar_interesses([
            {"publico_id": novo_id, "interesse_id": item["id"], "peso": item.get("peso", 100)}
            for item in publico.get("interesses", [])
        ])
        if publico.get("jornada"):
            self.repository.salvar_jornada(novo_id, publico["jornada"]["id"])
        return resposta.data[0]

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        publicos = self.listar()

        return {

            "total": len(

                publicos

            ),

            "ativos": len(

                [

                    p

                    for p in publicos

                    if p["ativo"]

                ]

            )

        }
