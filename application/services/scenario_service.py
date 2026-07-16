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

        contexto = self.planejamento.repository.carregar_contexto(

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

            "Plano gerado automaticamente pelo SDM.",

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

                    ),

                    "investimento": plano.verba_total,

                    "principais": plano.principal

                }

            )

        return resumo