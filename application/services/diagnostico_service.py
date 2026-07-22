from domain.models.diagnostico import (
    DiagnosticoPlano,
    DiagnosticoInventario
)

from application.services.recomendacao_service import (
    RecomendacaoService
)


class DiagnosticoService:

    def __init__(self):

        self.recomendacao = RecomendacaoService()

    # =====================================================
    # GERAR
    # =====================================================

    def gerar(

        self,

        plano

    ):

        diagnostico = DiagnosticoPlano(

            cliente=plano.cliente,

            campanha=plano.campanha,

            objetivo=plano.objetivo

        )

        for item in plano.itens:

            d = DiagnosticoInventario(

                inventario=item.inventario,

                plataforma=item.plataforma,

                ambiente=item.ambiente,

                papel=item.papel,

                score=item.score,

                objetivo=item.objetivo_score,

                kpi=item.kpi_score,

                audiencia=item.audiencia_score,

                metricas=item.metricas_score

            )

            recomendacoes = item.justificativas

            if not recomendacoes:

                recomendacoes = self.recomendacao.inventario(

                    {

                        "objetivo": 100,

                        "kpi": 100,

                        "audiencia": 100,

                        "metricas": 100,

                        "papel": item.papel

                    }

                )

            for texto in recomendacoes:

                t = texto.lower()

                if any(

                    palavra in t

                    for palavra in

                    [

                        "excelente",

                        "boa",

                        "elevada",

                        "acima"

                    ]

                ):

                    d.pontos_fortes.append(

                        texto

                    )

                elif any(

                    palavra in t

                    for palavra in

                    [

                        "baixa",

                        "limitada",

                        "reduzido",

                        "medianas"

                    ]

                ):

                    d.pontos_fracos.append(

                        texto

                    )

                else:

                    d.recomendacoes.append(

                        texto

                    )

            diagnostico.adicionar(

                d

            )

        diagnostico.observacoes.extend(

            self.recomendacao.resumo(

                [

                    {

                        "score": i.score,

                        "papel": i.papel

                    }

                    for i in plano.itens

                ]

            )

        )

        diagnostico.observacoes.extend(

            self.recomendacao.riscos(

                [

                    {

                        "score": i.score,

                        "papel": i.papel

                    }

                    for i in plano.itens

                ]

            )

        )

        return diagnostico
