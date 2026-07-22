from pathlib import Path

import pandas as pd


class ExportacaoService:

    # =====================================================
    # DATAFRAME
    # =====================================================

    def dataframe(self, plano):

        linhas = []

        for item in plano.itens:

            linhas.append(

                {

                    "Inventário": item.inventario,

                    "Plataforma": item.plataforma,

                    "Ambiente": item.ambiente,

                    "Papel": item.papel,

                    "Score": item.score,

                    "Score MCP": item.score_mcp,

                    "Aderência ao objetivo": item.objetivo_score,

                    "Aderência ao KPI": item.kpi_score,

                    "Aderência à audiência": item.audiencia_score,

                    "Score de métricas": item.metricas_score,

                    "Percentual": item.percentual,

                    "Verba": item.verba,

                    "ID do inventário": item.inventario_id,

                    "Preço unitário": item.preco_unitario,

                    "Unidade de compra": item.unidade_compra,

                    "Quantidade estimada": item.quantidade_estimada,

                    "Impressões estimadas": item.impressoes_estimadas,

                    "Alcance estimado": item.alcance_estimado,

                    "Justificativas": "\n".join(

                        item.justificativas

                    )

                }

            )

        return pd.DataFrame(linhas)

    def tabelas(self, plano):
        resumo = pd.DataFrame(
            [
                {"Campo": "Cliente", "Valor": plano.cliente},
                {"Campo": "Campanha", "Valor": plano.campanha},
                {"Campo": "Objetivo", "Valor": plano.objetivo},
                {"Campo": "Orçamento", "Valor": plano.orcamento},
                {"Campo": "Flight", "Valor": plano.tipo_flight},
                {"Campo": "Frequência", "Valor": plano.frequencia_objetivo},
                {"Campo": "Frequência alvo", "Valor": plano.frequencia_alvo},
                {"Campo": "Faixa de alcance", "Valor": plano.alcance_objetivo},
                {"Campo": "Alcance desejado (%)", "Valor": plano.alcance_percentual},
                {"Campo": "Público de referência", "Valor": plano.publico_referencia},
                {"Campo": "Meta de alcance", "Valor": plano.alcance_meta},
                {"Campo": "Alcance projetado", "Valor": plano.alcance_projetado},
            ]
        )
        cronograma = pd.DataFrame(plano.cronograma)
        kpis = pd.DataFrame(plano.kpis)
        observacoes = pd.DataFrame(
            {"Observações": plano.observacoes or []}
        )
        return {
            "Resumo": resumo,
            "Plano": self.dataframe(plano),
            "Cronograma": cronograma,
            "KPIs": kpis,
            "Observações": observacoes,
        }

    # =====================================================
    # EXCEL
    # =====================================================

    def excel(self, plano, arquivo):

        arquivo = Path(arquivo)

        with pd.ExcelWriter(

            arquivo,

            engine="openpyxl"

        ) as writer:

            for aba, tabela in self.tabelas(plano).items():
                tabela.to_excel(writer, sheet_name=aba, index=False)

        return arquivo

    # =====================================================
    # CSV
    # =====================================================

    def csv(self, plano, arquivo):

        arquivo = Path(arquivo)

        self.dataframe(plano).to_csv(

            arquivo,

            index=False,

            encoding="utf-8-sig"

        )

        return arquivo
