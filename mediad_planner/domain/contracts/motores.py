from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from mediad_planner.domain.common.enums import (
    EstadoExecucao,
    MotorDestino,
    NivelConfianca,
    NivelExecucao,
    OrigemComando,
    PapelAcesso,
    PoliticaReexecucao,
    ResultadoValidacao,
    Severidade,
    TipoDependencia,
)
from mediad_planner.domain.common.value_objects import (
    LimitesExecucao,
    ParametroLocal,
    ReferenciaVersionada,
)


VERSAO_CONTRATO_MOTORES = "1.0.0"
TResultado = TypeVar("TResultado")


def _texto(valor: str, campo: str) -> str:
    valor_normalizado = valor.strip()
    if not valor_normalizado:
        raise ValueError(f"{campo} não pode ser vazio")
    return valor_normalizado


def _fuso(valor: datetime, campo: str) -> None:
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ValueError(f"{campo} deve possuir fuso horário")


@dataclass(frozen=True, slots=True)
class ComandoMotor:
    id_comando: UUID
    motor_destino: MotorDestino
    modo_execucao: str
    nivel_execucao: NivelExecucao
    id_campanha: UUID
    id_snapshot_campanha: UUID
    id_usuario: UUID
    perfil_de_acesso: PapelAcesso
    solicitado_em: datetime
    origem_do_comando: OrigemComando
    objetivo_da_execucao: str
    referencias_de_entrada: tuple[ReferenciaVersionada, ...]
    parametros_locais: tuple[ParametroLocal, ...]
    limites_de_execucao: LimitesExecucao

    def __post_init__(self) -> None:
        modo_execucao = _texto(self.modo_execucao, "modo_execucao")
        objetivo = _texto(self.objetivo_da_execucao, "objetivo_da_execucao")
        _fuso(self.solicitado_em, "solicitado_em")

        referencias = tuple(self.referencias_de_entrada)
        parametros = tuple(self.parametros_locais)
        chaves_referencias = {
            (referencia.codigo, referencia.versao, referencia.tipo)
            for referencia in referencias
        }
        nomes_parametros = {parametro.nome for parametro in parametros}

        if len(chaves_referencias) != len(referencias):
            raise ValueError("referencias_de_entrada contém duplicidade")
        if len(nomes_parametros) != len(parametros):
            raise ValueError("parametros_locais contém nomes duplicados")

        object.__setattr__(self, "modo_execucao", modo_execucao)
        object.__setattr__(self, "objetivo_da_execucao", objetivo)
        object.__setattr__(self, "referencias_de_entrada", referencias)
        object.__setattr__(self, "parametros_locais", parametros)


@dataclass(frozen=True, slots=True)
class ValidacaoExecucao:
    codigo: str
    objeto_validado: str
    resultado: ResultadoValidacao
    severidade: Severidade
    mensagem: str
    impacto_na_execucao: str | None = None
    acao_recomendada: str | None = None


@dataclass(frozen=True, slots=True)
class AlertaExecucao:
    codigo: str
    severidade: Severidade
    titulo: str
    mensagem: str
    objeto_afetado: str | None
    impacto: str | None
    acao_possivel: str | None
    origem: str


@dataclass(frozen=True, slots=True)
class ConfiancaExecucao:
    metodologica: NivelConfianca
    dados: NivelConfianca
    aplicacao: NivelConfianca
    resultado: NivelConfianca


@dataclass(frozen=True, slots=True)
class ExplicacaoExecucao:
    conclusao_pratica: str
    principais_razoes: tuple[str, ...]
    restricoes_relevantes: tuple[str, ...]
    alternativas_rejeitadas: tuple[str, ...]
    trade_offs: tuple[str, ...]
    conhecimentos_aplicados: tuple[ReferenciaVersionada, ...]
    memoria_tecnica: tuple[str, ...]

    def __post_init__(self) -> None:
        campos = (
            "principais_razoes",
            "restricoes_relevantes",
            "alternativas_rejeitadas",
            "trade_offs",
            "conhecimentos_aplicados",
            "memoria_tecnica",
        )
        for campo in campos:
            object.__setattr__(self, campo, tuple(getattr(self, campo)))


@dataclass(frozen=True, slots=True)
class DependenciaExecucao:
    tipo: TipoDependencia
    depende_de: tuple[str, ...]
    produz_para: tuple[str, ...]
    invalida_quando: tuple[str, ...]
    recalcula_quando: tuple[str, ...]
    preserva_quando: tuple[str, ...]

    def __post_init__(self) -> None:
        campos = (
            "depende_de",
            "produz_para",
            "invalida_quando",
            "recalcula_quando",
            "preserva_quando",
        )
        for campo in campos:
            object.__setattr__(self, campo, tuple(getattr(self, campo)))


@dataclass(frozen=True, slots=True)
class RastreabilidadeExecucao:
    versoes_consumidas: tuple[ReferenciaVersionada, ...]
    entradas_utilizadas: tuple[str, ...]
    problemas_identificados: tuple[ReferenciaVersionada, ...]
    procedimentos_executados: tuple[ReferenciaVersionada, ...]
    intervencoes_humanas: tuple[str, ...]

    def __post_init__(self) -> None:
        for campo in self.__dataclass_fields__:
            object.__setattr__(self, campo, tuple(getattr(self, campo)))


@dataclass(frozen=True, slots=True)
class SaidaMotor(Generic[TResultado]):
    id_execucao: UUID
    id_comando: UUID
    motor: MotorDestino
    modo_execucao: str
    nivel_execucao: NivelExecucao
    estado_execucao: EstadoExecucao
    resultado_principal: TResultado | None
    resultados_secundarios: tuple[object, ...]
    validacoes: tuple[ValidacaoExecucao, ...]
    alertas: tuple[AlertaExecucao, ...]
    restricoes: tuple[str, ...]
    confianca: ConfiancaExecucao
    explicacao: ExplicacaoExecucao
    rastreabilidade: RastreabilidadeExecucao
    dependencias: tuple[DependenciaExecucao, ...]
    reexecucao: PoliticaReexecucao
    produzido_em: datetime
    versao_do_contrato: str

    def __post_init__(self) -> None:
        modo_execucao = _texto(self.modo_execucao, "modo_execucao")
        versao = _texto(self.versao_do_contrato, "versao_do_contrato")
        _fuso(self.produzido_em, "produzido_em")

        if (
            self.estado_execucao is EstadoExecucao.NAO_EXECUTAVEL
            and self.resultado_principal is not None
        ):
            raise ValueError("NAO_EXECUTAVEL não admite resultado_principal")

        object.__setattr__(self, "modo_execucao", modo_execucao)
        object.__setattr__(self, "versao_do_contrato", versao)
        campos = (
            "resultados_secundarios",
            "validacoes",
            "alertas",
            "restricoes",
            "dependencias",
        )
        for campo in campos:
            object.__setattr__(self, campo, tuple(getattr(self, campo)))
