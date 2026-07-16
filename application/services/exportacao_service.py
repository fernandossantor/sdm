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

                    "Percentual": item.percentual,

                    "Verba": item.verba,

                    "Justificativas": "\n".join(

                        item.justificativas

                    )

                }

            )

        return pd.DataFrame(linhas)

    # =====================================================
    # EXCEL
    # =====================================================

    def excel(self, plano, arquivo):

        arquivo = Path(arquivo)

        df = self.dataframe(plano)

        with pd.ExcelWriter(

            arquivo,

            engine="openpyxl"

        ) as writer:

            df.to_excel(

                writer,

                sheet_name="Plano",

                index=False

            )

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