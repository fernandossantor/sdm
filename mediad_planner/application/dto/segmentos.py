from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SalvarSegmentoEntrada:
    id_universo_origem: UUID
    ids_pracas: tuple[UUID, ...]
    criterios_aplicados: tuple[str, ...]
    definicao: str
    tamanho_estimado: str | None
    fonte: str | None
    data_referencia: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "ids_pracas", tuple(self.ids_pracas))
        object.__setattr__(self, "criterios_aplicados", tuple(self.criterios_aplicados))


@dataclass(frozen=True, slots=True)
class SegmentoResumo:
    id_segmento: UUID
    id_universo_origem: UUID
    nome_universo_origem: str
    ids_pracas: tuple[UUID, ...]
    rotulos_pracas: tuple[str, ...]
    criterios_aplicados: tuple[str, ...]
    rotulos_criterios: tuple[str, ...]
    definicao: str
    tamanho_estimado: str | None
    unidade: str
    fonte: str | None
    data_referencia: str | None
