from domain.models.plano_estrategico import (
    PlanoEstrategico,
    PlanoItem
)

from application.services.context_service import (
    ContextService
)

from application.services.recomendacao_service import (
    RecomendacaoService
)

from engine.inventory_engine import InventoryEngine
from engine.allocation_engine import AllocationEngine


class PlanejamentoService:

    def __init__(self):

        self.context_service = ContextService()

        self.inventory_engine = InventoryEngine()

        self.allocation_engine = AllocationEngine()

        self.recomendacao_service = RecomendacaoService()

    # ======================================================
    # GERAÇÃO
    # ======================================================

    def gerar(

        self,

        briefing=None,

        nome_briefing=None

    ):

        if isinstance(
            briefing,
            str,
        ) and nome_briefing is None:

            nome_briefing = briefing

            briefing = None

        if briefing is None:

            contexto = self.context_service.carregar(

                nome_briefing

            )

            # =====================================================
            # NORMALIZAÇÃO DO CONTEXTO V3
            # =====================================================

            if "audiencias" not in contexto:

                contexto["audiencias"] = []

            for audiencia in contexto["audiencias"]:

                #
                # Compatibilidade V3
                #

                if "peso" not in audiencia:

                    audiencia["peso"] = 1

            briefing_bd = contexto["briefing"]

            objetivo = contexto["objetivo"]

            verba = briefing_bd["orcamento"]

            cliente = briefing_bd["anunciante"]

            campanha = briefing_bd["nome"]

        else:

            contexto = self.context_service.carregar_por_objeto(

                briefing

            )

            objetivo = contexto["objetivo"]

            verba = briefing.orcamento

            cliente = briefing.cliente

            campanha = briefing.campanha

        ranking = self.inventory_engine.calcular(

            contexto

        )

        return self._montar_plano(

            cliente=cliente,

            campanha=campanha,

            objetivo=objetivo["nome"],

            verba=verba,

            ranking=ranking,

            observacao="Plano estratégico gerado automaticamente pelo SDM."

        )

    # ======================================================
    # RECÁLCULO
    # ======================================================

    def recalcular(

        self,

        nome_briefing,

        inventarios

    ):

        contexto = self.context_service.carregar(

            nome_briefing

        )

        briefing = contexto["briefing"]

        objetivo = contexto["objetivo"]

        ranking = self.inventory_engine.calcular(

            contexto

        )

        ranking = [

            item

            for item in ranking

            if item["inventario"] in inventarios

        ]

        return self._montar_plano(

            cliente=briefing["anunciante"],

            campanha=briefing["nome"],

            objetivo=objetivo["nome"],

            verba=briefing["orcamento"],

            ranking=ranking,

            observacao="Plano recalculado pelo Planejamento Assistido."

        )

    # ======================================================
    # MONTAGEM
    # ======================================================

    def _montar_plano(

        self,

        cliente,

        campanha,

        objetivo,

        verba,

        ranking,

        observacao

    ):

        plano_tatico = self.allocation_engine.distribuir(

            ranking,

            verba

        )

        indice = {

            item["inventario"]: item

            for item in ranking

        }

        plano = PlanoEstrategico(

            cliente=cliente,

            campanha=campanha,

            objetivo=objetivo,

            orcamento=verba

        )

        for item in plano_tatico.itens:

            origem = indice[item.inventario]

            plano.adicionar_item(

                PlanoItem(

                    inventario=item.inventario,

                    plataforma=item.plataforma,

                    ambiente=item.ambiente,

                    papel=item.papel,

                    score=item.score,

                    verba=item.verba,

                    percentual=item.percentual,

                    justificativas=self.recomendacao_service.inventario(

                        origem

                    )

                )

            )

        plano.observacoes = [

            observacao,

            "Distribuição proporcional ao score estratégico.",

            "Recomendações geradas automaticamente pelo SDM."

        ]

        return plano