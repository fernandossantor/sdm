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
from infrastructure.repositories.planning_repository import PlanningRepository
from copy import deepcopy


class PlanejamentoService:

    def __init__(self):

        self.context_service = ContextService()

        self.inventory_engine = InventoryEngine()

        self.allocation_engine = AllocationEngine()

        self.recomendacao_service = RecomendacaoService()

        self.repository = PlanningRepository()

    # ======================================================
    # GERAÇÃO
    # ======================================================

    def gerar(

        self,

        briefing=None,

        nome_briefing=None,

        configuracao=None,

    ):

        # Compatibilidade com chamadores legados que enviam o nome do
        # briefing como primeiro argumento posicional.
        if isinstance(briefing, str) and nome_briefing is None:
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

            briefing_bd = dict(contexto["briefing"])

            if configuracao:
                briefing_bd["kpi"] = configuracao.get("kpi", briefing_bd.get("kpi"))

            contexto["briefing"] = briefing_bd

            objetivo = contexto["objetivo"]

            verba = float((configuracao or {}).get("orcamento", briefing_bd["orcamento"]))

            cliente = briefing_bd["anunciante"]

            campanha = briefing_bd["nome"]

        else:

            briefing_calculo = deepcopy(briefing)

            if configuracao:
                briefing_calculo.kpi = configuracao.get("kpi", briefing_calculo.kpi)
                briefing_calculo.kpis = configuracao.get("kpis", briefing_calculo.kpis)
                briefing_calculo.tipo_flight = configuracao.get(
                    "tipo_flight", briefing_calculo.tipo_flight
                )
                briefing_calculo.frequencia_objetivo = configuracao.get(
                    "frequencia_objetivo", briefing_calculo.frequencia_objetivo
                )
                briefing_calculo.frequencia_alvo = configuracao.get(
                    "frequencia_alvo", briefing_calculo.frequencia_alvo
                )

            contexto = self.context_service.carregar_por_objeto(

                briefing_calculo

            )

            objetivo = contexto["objetivo"]

            verba = float((configuracao or {}).get("orcamento", briefing.orcamento))

            cliente = briefing.cliente

            campanha = briefing.campanha

        ranking = self.inventory_engine.calcular(

            contexto

        )

        plano = self._montar_plano(

            cliente=cliente,

            campanha=campanha,

            objetivo=objetivo["nome"],

            verba=verba,

            ranking=ranking,

            observacao="Plano estratégico gerado automaticamente pelo PMAH."

        )

        fonte = configuracao or {}
        if briefing is not None:
            plano.tipo_flight = fonte.get("tipo_flight", briefing.tipo_flight)
            plano.frequencia_objetivo = fonte.get(
                "frequencia_objetivo", briefing.frequencia_objetivo or "MEDIA"
            )
            plano.frequencia_alvo = int(
                fonte.get("frequencia_alvo", briefing.frequencia_alvo or 5)
            )
            plano.kpis = fonte.get("kpis", briefing.kpis)
            plano.cronograma = self._cronograma(
                briefing.inicio,
                briefing.fim,
                plano.tipo_flight,
            )
        else:
            plano.tipo_flight = fonte.get("tipo_flight", briefing_bd.get("tipo_flight", "LINEAR"))
            plano.frequencia_objetivo = fonte.get("frequencia_objetivo", "MEDIA")
            plano.frequencia_alvo = int(fonte.get("frequencia_alvo", 5))
            plano.kpis = fonte.get("kpis", [{"nome": fonte.get("kpi", briefing_bd.get("kpi")), "peso": 100}])

        self._calcular_entrega(plano)

        return plano

    @staticmethod
    def _calcular_entrega(plano):

        for item in plano.itens:
            if item.preco_unitario <= 0:
                continue
            item.quantidade_estimada = round(item.verba / item.preco_unitario, 2)
            if "CPM" in item.unidade_compra.upper():
                item.impressoes_estimadas = round(item.quantidade_estimada * 1000)
                item.alcance_estimado = round(
                    item.impressoes_estimadas / max(plano.frequencia_alvo, 1)
                )

    @staticmethod
    def _cronograma(inicio, fim, tipo_flight):

        if not inicio or not fim or fim < inicio:
            return []

        dias = (fim - inicio).days + 1
        semanas = max(1, (dias + 6) // 7)

        if tipo_flight == "ONDA":
            pesos = [1.5 if indice % 2 == 0 else 0.5 for indice in range(semanas)]
        elif tipo_flight == "CONCENTRADO":
            ativas = max(1, (semanas + 2) // 3)
            pesos = [1.0 if indice < ativas else 0.0 for indice in range(semanas)]
        else:
            pesos = [1.0] * semanas

        total = sum(pesos)
        return [
            {"semana": indice + 1, "percentual": round(peso / total * 100, 2)}
            for indice, peso in enumerate(pesos)
        ]

    def listar(self):

        try:
            return self.repository.listar()
        except Exception:
            return []

    def salvar(self, nome, plano, configuracao, briefing_id=None):

        itens = [
            {
                "inventario": item.inventario,
                "plataforma": item.plataforma,
                "ambiente": item.ambiente,
                "papel": item.papel,
                "score": item.score,
                "score_mcp": item.score_mcp,
                "verba": item.verba,
                "percentual": item.percentual,
                "justificativas": item.justificativas,
                "inventario_id": item.inventario_id,
                "preco_unitario": item.preco_unitario,
                "unidade_compra": item.unidade_compra,
                "quantidade_estimada": item.quantidade_estimada,
                "impressoes_estimadas": item.impressoes_estimadas,
                "alcance_estimado": item.alcance_estimado,
            }
            for item in plano.itens
        ]

        return self.repository.salvar(
            {
                "nome": nome,
                "briefing_id": briefing_id,
                "configuracao": configuracao,
                "resultado": {
                    "cliente": plano.cliente,
                    "campanha": plano.campanha,
                    "objetivo": plano.objetivo,
                    "orcamento": plano.orcamento,
                    "itens": itens,
                "observacoes": plano.observacoes,
                    "tipo_flight": plano.tipo_flight,
                    "frequencia_objetivo": plano.frequencia_objetivo,
                    "frequencia_alvo": plano.frequencia_alvo,
                    "kpis": plano.kpis,
                    "cronograma": plano.cronograma,
                },
                "status": "SALVO",
            }
        )

    def excluir(self, planejamento_id):

        return self.repository.excluir(planejamento_id)

    @staticmethod
    def restaurar(registro):

        dados = registro["resultado"]
        plano = PlanoEstrategico(
            cliente=dados["cliente"],
            campanha=dados["campanha"],
            objetivo=dados["objetivo"],
            orcamento=float(dados["orcamento"]),
            tipo_flight=dados.get("tipo_flight", "LINEAR"),
            frequencia_objetivo=dados.get("frequencia_objetivo", "MEDIA"),
            frequencia_alvo=int(dados.get("frequencia_alvo", 5)),
            kpis=dados.get("kpis", []),
            cronograma=dados.get("cronograma", []),
            observacoes=dados.get("observacoes", []),
        )

        for item in dados.get("itens", []):
            plano.adicionar_item(PlanoItem(**item))

        return plano

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

                    score_mcp=float(origem.get("score_mcp") or 0),

                    verba=item.verba,

                    percentual=item.percentual,

                    justificativas=self.recomendacao_service.inventario(

                        origem

                    ),

                    inventario_id=origem.get("inventario_id", ""),

                    preco_unitario=float(origem.get("preco_unitario") or 0),

                    unidade_compra=origem.get("unidade_compra") or "",

                )

            )

        plano.observacoes = [

            observacao,

            "Distribuição proporcional ao score estratégico.",

            "Recomendações geradas automaticamente pelo PMAH."

        ]

        return plano
