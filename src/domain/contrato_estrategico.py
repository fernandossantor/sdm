from dataclasses import dataclass
from enum import Enum

from .common import texto_obrigatorio


class EstadoContratoEstrategico(str, Enum):
    DEFINITIVO = "DEFINITIVO"
    PROVISORIO = "PROVISORIO"
    PARCIAL = "PARCIAL"
    INSUFICIENTE = "INSUFICIENTE"
    SUPERADO = "SUPERADO"


@dataclass(frozen=True, slots=True)
class ContratoEstrategico:
    id_campanha: str
    versao: str
    estado: EstadoContratoEstrategico
    objetivos_marketing: tuple[str, ...] = ()
    objetivos_comunicacao: tuple[str, ...] = ()
    objetivos_midia: tuple[str, ...] = ()
    restricoes: tuple[str, ...] = ()
    tensoes: tuple[str, ...] = ()
    lacunas: tuple[str, ...] = ()
    explicacoes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        texto_obrigatorio(self.id_campanha, "id_campanha")
        texto_obrigatorio(self.versao, "versao")

    @classmethod
    def vazio(cls, *, id_campanha: str, versao: str) -> "ContratoEstrategico":
        return cls(
            id_campanha=id_campanha,
            versao=versao,
            estado=EstadoContratoEstrategico.INSUFICIENTE,
        )
