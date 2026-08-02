from dataclasses import dataclass
from enum import Enum

from .common import texto_obrigatorio


class Prioridade(str, Enum):
    MUITO_BAIXA = "muito baixa"
    BAIXA = "baixa"
    MEDIA = "média"
    ALTA = "alta"
    MUITO_ALTA = "muito alta"


@dataclass(frozen=True, slots=True)
class ObjetivoMarketing:
    categoria: str
    ordem_declarada: int
    prioridade: Prioridade

    def __post_init__(self) -> None:
        texto_obrigatorio(self.categoria, "categoria")
        if self.ordem_declarada < 1:
            raise ValueError("ordem_declarada deve ser positiva")


@dataclass(frozen=True, slots=True)
class ObjetivoComunicacaoCandidato:
    categoria: str

    def __post_init__(self) -> None:
        texto_obrigatorio(self.categoria, "categoria")
