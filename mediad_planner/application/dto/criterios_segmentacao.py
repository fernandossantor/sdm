from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DefinicaoCriterioSegmentacaoResumo:
    codigo: str
    rotulo: str


@dataclass(frozen=True, slots=True)
class DefinirCriteriosSegmentacaoEntrada:
    codigos: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "codigos", tuple(self.codigos))
