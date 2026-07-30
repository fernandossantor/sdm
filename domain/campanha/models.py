"""Entidade canônica de Campanha, independente de interface e persistência."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class TextoEnum(str, Enum):
    pass


class SituacaoCampanha(TextoEnum):
    RASCUNHO = "RASCUNHO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"
    ARQUIVADA = "ARQUIVADA"


class EtapaCampanha(TextoEnum):
    ABERTURA = "ABERTURA"
    BRIEFING = "BRIEFING"
    TRADUCAO_ESTRATEGICA = "TRADUCAO_ESTRATEGICA"
    ARQUITETURA_DE_MIDIA = "ARQUITETURA_DE_MIDIA"
    SIMULACAO = "SIMULACAO"
    CONSOLIDACAO_DO_PLANO = "CONSOLIDACAO_DO_PLANO"
    VALIDACAO_E_APROVACAO = "VALIDACAO_E_APROVACAO"
    ACOMPANHAMENTO_E_RESULTADOS = "ACOMPANHAMENTO_E_RESULTADOS"


def exigir_fuso(valor: datetime) -> datetime:
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ValueError("timestamp deve possuir fuso horário")
    return valor


class SnapshotVinculosCampanha(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    nome_anunciante: str = Field(min_length=1)
    nome_marca: str | None = None
    nome_produto_servico: str | None = None
    identificacao_planejador: str = Field(min_length=1)

    @field_validator("nome_anunciante", "identificacao_planejador")
    @classmethod
    def normalizar_texto_obrigatorio(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("snapshot obrigatório não pode ser vazio")
        return valor


class Campanha(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID
    codigo: str = Field(pattern=r"^MP-\d{6}-\d{4,}$")
    nome: str = Field(min_length=1)
    anunciante_id: UUID
    marca_id: UUID | None = None
    produto_servico_id: UUID | None = None
    planejador_responsavel_id: UUID
    equipe_ids: tuple[UUID, ...] = ()
    observacao_inicial: str | None = None
    campanha_derivada_de_id: UUID | None = None
    snapshot: SnapshotVinculosCampanha
    criado_por: UUID
    criado_em: datetime
    atualizado_em: datetime
    situacao: SituacaoCampanha = SituacaoCampanha.RASCUNHO
    etapa_atual: EtapaCampanha = EtapaCampanha.ABERTURA

    @field_validator("nome")
    @classmethod
    def normalizar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("nome da campanha é obrigatório")
        return valor

    @field_validator("criado_em", "atualizado_em")
    @classmethod
    def validar_timestamp(cls, valor: datetime) -> datetime:
        return exigir_fuso(valor)

    @field_validator("equipe_ids")
    @classmethod
    def equipe_sem_duplicidade(cls, valor: tuple[UUID, ...]) -> tuple[UUID, ...]:
        if len(valor) != len(set(valor)):
            raise ValueError("equipe da campanha não admite duplicidades")
        return valor

    @model_validator(mode="after")
    def validar_snapshot_dos_vinculos(self) -> "Campanha":
        if bool(self.marca_id) != bool(self.snapshot.nome_marca):
            raise ValueError("marca e nome histórico da marca devem coexistir")
        if bool(self.produto_servico_id) != bool(self.snapshot.nome_produto_servico):
            raise ValueError("produto/serviço e seu nome histórico devem coexistir")
        return self

    def iniciar_briefing(self, atualizado_em: datetime) -> "Campanha":
        exigir_fuso(atualizado_em)
        if self.situacao is not SituacaoCampanha.RASCUNHO:
            raise ValueError("somente campanha em rascunho pode concluir a abertura")
        if self.etapa_atual is not EtapaCampanha.ABERTURA:
            raise ValueError("campanha não está na etapa de abertura")
        return self.model_copy(
            update={
                "situacao": SituacaoCampanha.EM_ANDAMENTO,
                "etapa_atual": EtapaCampanha.BRIEFING,
                "atualizado_em": atualizado_em,
            }
        )
