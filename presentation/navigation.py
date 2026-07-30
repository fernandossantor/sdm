"""Definição declarativa da navegação inicial."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ItemNavegacao:
    chave: str
    titulo: str
    icone: str
    etapa: int | None


NAVEGACAO_INICIAL = (
    ItemNavegacao("inicio", "Visão geral", "🏠", None),
    ItemNavegacao("campanha", "Abertura da campanha", "📁", 1),
    ItemNavegacao("briefing", "Briefing de mídia", "📋", 2),
)

ETAPAS_FUTURAS = (
    "Tradução estratégica",
    "Arquitetura de mídia",
    "Ambiente de simulação",
    "Consolidação do plano",
    "Validação e aprovação",
    "Acompanhamento e resultados",
)
