from application.services.planejamento_service import (
    PlanejamentoService
)

from engine.scenario_engine import (
    ScenarioEngine
)

from engine.allocation_engine import (
    AllocationEngine
)

from domain.models.plano_estrategico import (
    PlanoEstrategico,
    PlanoItem
)


class ScenarioService:

    def __init__(self):

        self.planejamento = PlanejamentoService()

        self.scenario_engine = ScenarioEngine()

        self.allocation_engine = AllocationEngine()

    # =====================================================
    # CENÁRIOS DISPONÍVEIS
    # =====================================================

    def listar(self):

        return self.scenario_engine.listar()

    # =====================================================
    # GERAR CENÁRIO
    # =====================================================

    def gerar(

        self,

        nome_briefing,

        cenario

    ):

        contexto = self.planejamento.context_service.carregar(

            nome_briefing

        )

        briefing = contexto["briefing"]

        objetivo = contexto["objetivo"]

        ranking = self.planejamento.inventory_engine.calcular(

            contexto

        )

        ranking = self.scenario_engine.aplicar(

            ranking,

            cenario

        )

        plano_tatico = self.allocation_engine.distribuir(

            ranking,

            briefing["orcamento"]

        )

        indice = {

            item["inventario"]: item

            for item in ranking

        }

        plano = PlanoEstrategico(

            cliente=briefing["anunciante"],

            campanha=briefing["nome"],

            objetivo=objetivo["nome"],

            orcamento=briefing["orcamento"]

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

                    justificativas=self.planejamento.recomendacao_service.inventario(

                        origem

                    )

                )

            )

        plano.observacoes = [

            f"Cenário estratégico: {cenario}.",

            "Plano gerado automaticamente pelo PlanOS.",

            "Distribuição ajustada conforme o perfil estratégico do cenário."

        ]

        return plano

    # =====================================================
    # GERAR TODOS
    # =====================================================

    def gerar_todos(

        self,

        nome_briefing

    ):

        resultado = {}

        for cenario in self.listar():

            resultado[cenario] = self.gerar(

                nome_briefing,

                cenario

            )

        return resultado

    def gerar_todos_de_plano(self, plano_base):

        ranking_base = [
            {
                "inventario": item.inventario,
                "plataforma": item.plataforma,
                "ambiente": item.ambiente,
                "papel": item.papel,
                "score": item.score,
                "objetivo": item.objetivo_score,
                "kpi": item.kpi_score,
                "audiencia": item.audiencia_score,
                "metricas": item.metricas_score,
                "score_mcp": item.score_mcp,
                "inventario_id": item.inventario_id,
                "preco_unitario": item.preco_unitario,
                "unidade_compra": item.unidade_compra,
            }
            for item in plano_base.itens
        ]

        resultado = {}
        for cenario in self.listar():
            ranking = self.scenario_engine.aplicar(ranking_base, cenario)
            plano = self.planejamento._montar_plano(
                cliente=plano_base.cliente,
                campanha=plano_base.campanha,
                objetivo=plano_base.objetivo,
                verba=plano_base.orcamento,
                ranking=ranking,
                observacao=f"Cenário estratégico: {cenario}.",
            )
            plano.tipo_flight = plano_base.tipo_flight
            plano.frequencia_objetivo = plano_base.frequencia_objetivo
            plano.frequencia_alvo = plano_base.frequencia_alvo
            plano.alcance_objetivo = plano_base.alcance_objetivo
            plano.alcance_percentual = plano_base.alcance_percentual
            plano.grp = plano_base.grp
            plano.publico_referencia = plano_base.publico_referencia
            plano.alcance_meta = plano_base.alcance_meta
            plano.alcance_projetado = plano_base.alcance_projetado
            plano.kpis = plano_base.kpis
            plano.cronograma = plano_base.cronograma
            resultado[cenario] = plano

        return resultado

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(

        self,

        nome_briefing

    ):

        planos = self.gerar_todos(

            nome_briefing

        )

        resumo = []

        for nome, plano in planos.items():

            resumo.append(

                {

                    "cenario": nome,

                    "inventarios": len(plano.itens),

                    "score_medio": round(

                        sum(

                            i.score

                            for i in plano.itens

                        )

                        /

                        len(plano.itens),

                        2

                    ) if plano.itens else 0,

                    "investimento": plano.verba_total,

                    "principais": plano.principal

                }

            )

        return resumo
