from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ApontamentoRevisaoResumo:
    subetapa: str
    mensagem: str
    referencia_normativa: str
    id_entidade: UUID | None = None
