"""Validação descritiva de qualidade programática e localização."""

from datetime import date
import math


class MediaQualityEngine:
    DIMENSOES_PERCENTUAIS = (
        "viewability_percentual",
        "trafego_invalido_percentual",
        "fraude_percentual",
    )
    CAMPOS_LOCALIZACAO = (
        "fonte_sinal",
        "precisao_metros",
        "raio_metros",
        "inicio",
        "fim",
        "finalidade",
        "base_legal",
        "metodo_associacao",
        "confianca_percentual",
        "natureza_visita",
    )

    @staticmethod
    def _vazio(valor):
        return valor is None or (
            isinstance(valor, float) and math.isnan(valor)
        ) or (isinstance(valor, str) and not valor.strip())

    @classmethod
    def _percentual(cls, valor, campo):
        if cls._vazio(valor):
            return None
        numero = float(valor)
        if not 0 <= numero <= 100:
            raise ValueError(f"{campo} deve estar entre 0% e 100%.")
        return numero

    @staticmethod
    def _periodo(inicio, fim):
        try:
            inicio_data = date.fromisoformat(str(inicio)[:10])
            fim_data = date.fromisoformat(str(fim)[:10])
        except (TypeError, ValueError):
            return False
        return inicio_data <= fim_data

    def avaliar_qualidade(self, registros):
        resultado = []
        for registro in registros:
            inventario = str(registro.get("inventario") or "").strip()
            if not inventario:
                continue
            linha = {"inventario": inventario}
            for campo in self.DIMENSOES_PERCENTUAIS:
                linha[campo] = self._percentual(
                    registro.get(campo),
                    campo,
                )
            linha["brand_safety"] = (
                "NAO_AVALIADO"
                if self._vazio(registro.get("brand_safety"))
                else str(registro["brand_safety"]).strip()
            )
            linha["brand_suitability"] = (
                "NAO_AVALIADO"
                if self._vazio(registro.get("brand_suitability"))
                else str(registro["brand_suitability"]).strip()
            )
            linha["fonte"] = (
                ""
                if self._vazio(registro.get("fonte"))
                else str(registro["fonte"]).strip()
            )
            linha["inicio"] = registro.get("inicio")
            linha["fim"] = registro.get("fim")
            linha["observacoes"] = str(
                registro.get("observacoes") or ""
            ).strip()
            dimensoes_informadas = any(
                linha[campo] is not None
                for campo in self.DIMENSOES_PERCENTUAIS
            ) or any(
                linha[campo] != "NAO_AVALIADO"
                for campo in ("brand_safety", "brand_suitability")
            )
            lacunas = []
            if dimensoes_informadas and not linha["fonte"]:
                lacunas.append("fonte")
            if dimensoes_informadas and not self._periodo(
                linha["inicio"], linha["fim"]
            ):
                lacunas.append("período válido")
            linha["lacunas"] = lacunas
            linha["situacao"] = (
                "DOCUMENTADO"
                if dimensoes_informadas and not lacunas
                else "INCOMPLETO"
            )
            resultado.append(linha)
        return resultado

    def avaliar_localizacao(self, registros):
        resultado = []
        for registro in registros:
            inventario = str(registro.get("inventario") or "").strip()
            if not inventario:
                continue
            if all(
                self._vazio(registro.get(campo))
                for campo in self.CAMPOS_LOCALIZACAO
            ):
                continue
            linha = {"inventario": inventario}
            for campo in self.CAMPOS_LOCALIZACAO:
                linha[campo] = registro.get(campo)
            lacunas = [
                campo
                for campo in self.CAMPOS_LOCALIZACAO
                if self._vazio(linha[campo])
            ]
            avisos = []
            if not lacunas:
                precisao = float(linha["precisao_metros"])
                raio = float(linha["raio_metros"])
                confianca = self._percentual(
                    linha["confianca_percentual"],
                    "confianca_percentual",
                )
                if precisao < 0 or raio <= 0:
                    raise ValueError(
                        "Precisão não pode ser negativa e raio deve ser positivo."
                    )
                linha["precisao_metros"] = precisao
                linha["raio_metros"] = raio
                linha["confianca_percentual"] = confianca
                if not self._periodo(linha["inicio"], linha["fim"]):
                    lacunas.append("período válido")
                if precisao > raio:
                    avisos.append(
                        "A precisão declarada é maior que o raio analisado."
                    )
                if linha["natureza_visita"] not in {"OBSERVADA", "INFERIDA"}:
                    lacunas.append("natureza da visita válida")
            linha["lacunas"] = lacunas
            linha["avisos"] = avisos
            linha["situacao"] = "DOCUMENTADO" if not lacunas else "INCOMPLETO"
            resultado.append(linha)
        return resultado

    def avaliar(self, qualidade, localizacao):
        return {
            "qualidade": self.avaliar_qualidade(qualidade),
            "localizacao": self.avaliar_localizacao(localizacao),
            "metodologia": (
                "Dimensões preservadas separadamente; nenhum índice composto "
                "de qualidade é calculado."
            ),
            "limitacoes": [
                "Valores informados dependem da fonte e do período declarados.",
                "Visita observada e visita inferida não são equivalentes.",
                "Localização contextualiza segmentação e medição; não define "
                "sozinha um público.",
            ],
        }
