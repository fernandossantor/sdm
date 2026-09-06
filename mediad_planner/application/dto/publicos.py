from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SalvarPublicoEntrada:
    nome: str | None
    ids_segmentos_origem: tuple[UUID, ...]
    ids_pracas: tuple[UUID, ...]
    prioridade: int | None
    intensidade_importancia: int | None
    tamanho_estimado: str | None
    papel_declarado: str | None
    justificativa: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "ids_segmentos_origem", tuple(self.ids_segmentos_origem))
        object.__setattr__(self, "ids_pracas", tuple(self.ids_pracas))


@dataclass(frozen=True, slots=True)
class PublicoResumo:
    id_publico: UUID
    nome: str | None
    ids_segmentos_origem: tuple[UUID, ...]
    definicoes_segmentos_origem: tuple[str, ...]
    ids_pracas: tuple[UUID, ...]
    rotulos_pracas: tuple[str, ...]
    prioridade: int | None
    intensidade_importancia: int | None
    tamanho_estimado: str | None
    papel_declarado: str | None
    justificativa: str | None
    jornada_aplicavel: bool | None = None
