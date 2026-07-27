"""Serviço de qualidade programática e localização."""

from engine.media_quality_engine import MediaQualityEngine


class MediaQualityService:
    def __init__(self):
        self.engine = MediaQualityEngine()

    def avaliar(self, qualidade, localizacao):
        resultado = self.engine.avaliar(qualidade, localizacao)
        resultado["resumo"] = {
            "qualidade_documentada": sum(
                item["situacao"] == "DOCUMENTADO"
                for item in resultado["qualidade"]
            ),
            "qualidade_incompleta": sum(
                item["situacao"] == "INCOMPLETO"
                for item in resultado["qualidade"]
            ),
            "localizacao_documentada": sum(
                item["situacao"] == "DOCUMENTADO"
                for item in resultado["localizacao"]
            ),
            "localizacao_incompleta": sum(
                item["situacao"] == "INCOMPLETO"
                for item in resultado["localizacao"]
            ),
        }
        return resultado
