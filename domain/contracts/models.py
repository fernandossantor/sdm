"""Modelos serializáveis e independentes de interface e persistência."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import (
    Confianca,
    EstadoDeduplicacao,
    EstadoEquivalencia,
    EstadoExecucao,
    NivelExecucao,
    NaturezaValor,
    PoliticaReexecucao,
    ResultadoValidacao,
    Severidade,
    TipoDependencia,
)


class ContratoBase(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", use_enum_values=False)


def _exigir_fuso(valor: datetime) -> datetime:
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ValueError("timestamp deve possuir fuso horário")
    return valor


class ReferenciaVersionada(ContratoBase):
    id: str = Field(min_length=1)
    tipo: str = Field(min_length=1)
    versao: str = Field(min_length=1)
    origem: str = Field(min_length=1)


class ValorTipado(ContratoBase):
    """Preserva ausência, zero, natureza, origem e valor bruto."""

    valor: Any | None
    natureza: NaturezaValor
    origem: str
    valor_bruto: Any | None = None
    unidade_observacao: str | None = None
    universo_referencia: str | None = None
    estado_deduplicacao: EstadoDeduplicacao = EstadoDeduplicacao.INDETERMINADO
    estado_equivalencia: EstadoEquivalencia = EstadoEquivalencia.INDETERMINADO
    nivel_confianca: Confianca = Confianca.INDETERMINADA


class ValidacaoLocal(ContratoBase):
    codigo: str
    objeto_validado: str
    resultado: ResultadoValidacao
    severidade: Severidade
    mensagem: str
    impacto_na_execucao: str | None = None
    acao_recomendada: str | None = None


class Alerta(ContratoBase):
    codigo: str
    severidade: Severidade
    titulo: str
    mensagem: str
    objeto_afetado: str | None = None
    impacto: str | None = None
    acao_possivel: str | None = None
    origem: str


class Restricao(ContratoBase):
    codigo: str
    descricao: str
    bloqueante: bool = False
    origem: str


class Dependencia(ContratoBase):
    referencia: ReferenciaVersionada
    tipo: TipoDependencia
    invalida_quando: tuple[str, ...] = ()
    recalcula_quando: tuple[str, ...] = ()
    preserva_quando: tuple[str, ...] = ()


class PlanoReexecucao(ContratoBase):
    politica: PoliticaReexecucao
    motivo: str
    alvos: tuple[str, ...] = ()


class Rastreabilidade(ContratoBase):
    entradas_utilizadas: tuple[ReferenciaVersionada, ...] = ()
    conhecimentos_aplicados: tuple[ReferenciaVersionada, ...] = ()
    procedimentos: tuple[ReferenciaVersionada, ...] = ()
    valores_padrao_aplicados: dict[str, Any] = Field(default_factory=dict)
    intervencoes_humanas: tuple[dict[str, Any], ...] = ()


class ComandoMotor(ContratoBase):
    id_comando: UUID = Field(default_factory=uuid4)
    motor_destino: str = Field(min_length=1)
    modo_execucao: str = Field(min_length=1)
    nivel_execucao: NivelExecucao = NivelExecucao.PADRAO
    id_campanha: UUID
    id_snapshot_campanha: UUID
    id_usuario: UUID
    perfil_de_acesso: str = Field(min_length=1)
    solicitado_em: datetime
    origem_do_comando: str = Field(min_length=1)
    objetivo_da_execucao: str = Field(min_length=1)
    referencias_de_entrada: tuple[ReferenciaVersionada, ...] = ()
    parametros_locais: dict[str, Any] = Field(default_factory=dict)
    limites_de_execucao: dict[str, int | float] = Field(default_factory=dict)

    _timestamp_com_fuso = field_validator("solicitado_em")(_exigir_fuso)


class SaidaMotor(ContratoBase):
    id_execucao: UUID = Field(default_factory=uuid4)
    id_comando: UUID
    motor: str
    modo_execucao: str
    nivel_execucao: NivelExecucao
    estado_execucao: EstadoExecucao
    resultado_principal: Any | None = None
    resultados_secundarios: tuple[Any, ...] = ()
    validacoes: tuple[ValidacaoLocal, ...] = ()
    alertas: tuple[Alerta, ...] = ()
    restricoes: tuple[Restricao, ...] = ()
    confianca: Confianca = Confianca.INDETERMINADA
    explicacao: dict[str, Any] = Field(default_factory=dict)
    rastreabilidade: Rastreabilidade = Field(default_factory=Rastreabilidade)
    dependencias: tuple[Dependencia, ...] = ()
    reexecucao: PlanoReexecucao
    produzido_em: datetime
    versao_do_contrato: str = "1.0"

    _timestamp_com_fuso = field_validator("produzido_em")(_exigir_fuso)
