from pathlib import Path

import pandas as pd


class ExportacaoService:

    # =====================================================
    # DATAFRAME
    # =====================================================

    def dataframe(self, plano):
        return pd.DataFrame(
            [
                {
                    "Papel": item.papel,
                    "Score do papel": (
                        item.score_mcp
                        if item.score_mcp is not None
                        else item.score
                    ),
                    "Flight": plano.tipo_flight,
                    "Frequência média": plano.frequencia_alvo,
                    "Alcance (%)": plano.alcance_percentual,
                    "Inventário": item.inventario,
                    "Plataforma": item.plataforma,
                    "Ambiente": item.ambiente,
                    "Verba": item.verba,
                    "Frequência do meio": item.frequencia,
                    "Alcance do meio (%)": item.alcance_percentual,
                    "Alcance incremental (%)": item.alcance_incremental,
                    "GRP": plano.grp,
                    "GRP do meio": item.grp,
                    "Score estratégico": item.score,
                    "Participação da verba (%)": item.percentual,
                    "Aderência ao objetivo": item.objetivo_score,
                    "Aderência ao KPI": item.kpi_score,
                    "Aderência ao público": item.audiencia_score,
                    "Qualidade das métricas": item.metricas_score,
                    "Preço unitário": item.preco_unitario,
                    "Unidade de compra": item.unidade_compra,
                    "Quantidade comprada": item.quantidade_estimada,
                    "Impressões estimadas": item.impressoes_estimadas,
                    "Alcance estimado (pessoas)": item.alcance_estimado,
                    "CPP": item.cpp,
                    "CPM": item.cpm,
                    "CPC": item.cpc,
                    "CPA": item.cpa,
                    "Cliques projetados": item.cliques_estimados,
                    "Conversões projetadas": item.conversoes_estimadas,
                    "Retorno projetado": item.retorno_estimado,
                    "ROI": item.roi,
                    "Excesso de frequência": item.excesso_frequencia,
                    "Premissas": item.premissas,
                    "ID do inventário": item.inventario_id,
                    "Justificativas": "\n".join(item.justificativas),
                }
                for item in plano.itens
            ]
        )

    def tabelas(self, plano):
        resumo = pd.DataFrame(
            [
                {"Campo": "Cliente", "Valor": plano.cliente},
                {"Campo": "Código", "Valor": plano.codigo},
                {"Campo": "Campanha", "Valor": plano.campanha},
                {"Campo": "Objetivo", "Valor": plano.objetivo},
                {"Campo": "Orçamento", "Valor": plano.orcamento},
                {"Campo": "Flight", "Valor": plano.tipo_flight},
                {"Campo": "Frequência", "Valor": plano.frequencia_objetivo},
                {"Campo": "Frequência alvo", "Valor": plano.frequencia_alvo},
                {"Campo": "Faixa de alcance", "Valor": plano.alcance_objetivo},
                {"Campo": "Alcance desejado (%)", "Valor": plano.alcance_percentual},
                {"Campo": "GRP", "Valor": plano.grp},
                {"Campo": "Público de referência", "Valor": plano.publico_referencia},
                {"Campo": "Meta de alcance", "Valor": plano.alcance_meta},
                {"Campo": "Alcance projetado", "Valor": plano.alcance_projetado},
                {"Campo": "Estratégia", "Valor": plano.estrategia},
                {"Campo": "Resultados consolidados", "Valor": plano.resultados_consolidados},
                {"Campo": "Auditoria do cálculo", "Valor": plano.auditoria_calculo},
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
