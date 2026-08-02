from dataclasses import dataclass
from uuid import UUID


def _normalizar_nome_snapshot(nome: str) -> str:
    nome_normalizado = nome.strip()
    if not nome_normalizado:
        raise ValueError("nome_snapshot não pode ser vazio")
    return nome_normalizado


@dataclass(frozen=True, slots=True)
class AnuncianteCampanha:
    id_anunciante: UUID
    nome_snapshot: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "nome_snapshot",
            _normalizar_nome_snapshot(self.nome_snapshot),
        )


@dataclass(frozen=True, slots=True)
class MarcaCampanha:
    id_marca: UUID
    id_anunciante: UUID
    nome_snapshot: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "nome_snapshot",
            _normalizar_nome_snapshot(self.nome_snapshot),
        )


@dataclass(frozen=True, slots=True)
class ProdutoServicoCampanha:
    id_produto_servico: UUID
    id_anunciante: UUID
    id_marca: UUID | None
    nome_snapshot: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "nome_snapshot",
            _normalizar_nome_snapshot(self.nome_snapshot),
        )


@dataclass(frozen=True, slots=True)
class ParticipanteCampanha:
    id_usuario: UUID
    nome_snapshot: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "nome_snapshot",
            _normalizar_nome_snapshot(self.nome_snapshot),
        )
