import csv
import json
from pathlib import Path
from dataclasses import asdict, is_dataclass


class ExportEngine:

    # =====================================================
    # EXPORTAR
    # =====================================================

    def exportar(

        self,

        dashboard,

        arquivo,

        formato=None

    ):

        caminho = Path(arquivo)

        if formato is None:

            formato = caminho.suffix.replace(".", "").lower()

        formato = formato.lower()

        if formato == "json":

            return self.exportar_json(

                dashboard,

                caminho

            )

        if formato == "csv":

            return self.exportar_csv(

                dashboard,

                caminho

            )

        if formato == "xlsx":

            return self.exportar_excel(

                dashboard,

                caminho

            )

        if formato == "pdf":

            return self.exportar_pdf(

                dashboard,

                caminho

            )

        raise ValueError(

            f"Formato '{formato}' não suportado."

        )

    # =====================================================
    # DICT
    # =====================================================

    def para_dict(

        self,

        objeto

    ):

        if objeto is None:

            return None

        if is_dataclass(objeto):

            return asdict(objeto)

        if isinstance(objeto, list):

            return [

                self.para_dict(

                    item

                )

                for item in objeto

            ]

        if isinstance(objeto, tuple):

            return [

                self.para_dict(

                    item

                )

                for item in objeto

            ]

        if isinstance(objeto, dict):

            return {

                chave: self.para_dict(

                    valor

                )

                for chave, valor in objeto.items()

            }

        if hasattr(

            objeto,

            "__dict__"

        ):

            return {

                chave: self.para_dict(

                    valor

                )

                for chave, valor in vars(objeto).items()

                if not chave.startswith("_")

            }

        return objeto

    # =====================================================
    # JSON
    # =====================================================

    def exportar_json(

        self,

        dashboard,

        caminho

    ):

        dados = self.para_dict(

            dashboard

        )

        with open(

            caminho,

            "w",

            encoding="utf-8"

        ) as arquivo:

            json.dump(

                dados,

                arquivo,

                ensure_ascii=False,

                indent=4

            )

        return caminho

    # =====================================================
    # CSV
    # =====================================================

    def exportar_csv(

        self,

        dashboard,

        caminho

    ):

        dados = self.para_dict(

            dashboard

        )

        with open(

            caminho,

            "w",

            newline="",

            encoding="utf-8"

        ) as arquivo:

            writer = csv.writer(

                arquivo,

                delimiter=";"

            )

            writer.writerow(

                [

                    "campo",

                    "valor"

                ]

            )

            self._csv(

                writer,

                "",

                dados

            )

        return caminho

    # =====================================================
    # RECURSIVO CSV
    # =====================================================

    def _csv(

        self,

        writer,

        prefixo,

        valor

    ):

        if isinstance(

            valor,

            dict

        ):

            for chave, item in valor.items():

                novo = (

                    f"{prefixo}.{chave}"

                    if prefixo

                    else chave

                )

                self._csv(

                    writer,

                    novo,

                    item

                )

            return

        if isinstance(

            valor,

            list

        ):

            for indice, item in enumerate(valor):

                novo = (

                    f"{prefixo}[{indice}]"

                )

                self._csv(

                    writer,

                    novo,

                    item

                )

            return

        writer.writerow(

            [

                prefixo,

                valor

            ]

        )

    # =====================================================
    # EXCEL
    # =====================================================

    def exportar_excel(

        self,

        dashboard,

        caminho

    ):

        raise NotImplementedError(

            "Exportação Excel será implementada no módulo xlsx."

        )

    # =====================================================
    # PDF
    # =====================================================

    def exportar_pdf(

        self,

        dashboard,

        caminho

    ):

        raise NotImplementedError(

            "Exportação PDF será implementada no módulo report."

        )