from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class RealizadoItem:
    inventario: str
    inventario_id: str = ""
    investimento: Optional[float] = None
    impressoes: Optional[float] = None
    cliques: Optional[float] = None
    conversoes: Optional[float] = None


@dataclass
class RealizadoPlano:
    fonte: str
    inicio: date
    fim: date
    itens: list[RealizadoItem] = field(default_factory=list)
    universo: Optional[str] = None
    publico_alvo: Optional[str] = None
    praca: Optional[str] = None
