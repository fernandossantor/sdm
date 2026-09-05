from dataclasses import dataclass
from enum import Enum
from uuid import UUID


def _texto(valor: object, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} é obrigatório")
    return valor.strip()


def _opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise TypeError("valor deve ser texto")
    return valor.strip() or None


def _escala(valor: int, campo: str) -> None:
    if type(valor) is not int or not 1 <= valor <= 5:
        raise ValueError(f"{campo} deve estar entre 1 e 5")


class TipoEntidadePrioridade(str, Enum):
    PRACA = "PRACA"
    SEGMENTO = "SEGMENTO"
    PERIODO = "PERIODO"


class CategoriaRestricao(str, Enum):
    GEOGRAFICA = "GEOGRAFICA"
    POPULACIONAL = "POPULACIONAL"
    PUBLICO = "PUBLICO"
    SEGMENTO = "SEGMENTO"
    PERIODO = "PERIODO"
    ORCAMENTARIA = "ORCAMENTARIA"
    LEGAL = "LEGAL"
    ETICA = "ETICA"
    INSTITUCIONAL = "INSTITUCIONAL"
    MERCADOLOGICA = "MERCADOLOGICA"
    COMPETITIVA = "COMPETITIVA"
    OPERACIONAL = "OPERACIONAL"
    DISPONIBILIDADE = "DISPONIBILIDADE"
    MENSURACAO = "MENSURACAO"
    OUTRA = "OUTRA"


class CategoriaPretensao(str, Enum):
    AMPLIAR_PRESENCA = "AMPLIAR_PRESENCA"
    ALCANCAR_NOVOS_PUBLICOS = "ALCANCAR_NOVOS_PUBLICOS"
    REFORCAR_PUBLICOS_ATUAIS = "REFORCAR_PUBLICOS_ATUAIS"
    AUMENTAR_CONHECIMENTO = "AUMENTAR_CONHECIMENTO"
    MELHORAR_LEMBRANCA = "MELHORAR_LEMBRANCA"
    APOIAR_LANCAMENTO = "APOIAR_LANCAMENTO"
    APOIAR_VENDAS = "APOIAR_VENDAS"
    ESTIMULAR_EXPERIMENTACAO = "ESTIMULAR_EXPERIMENTACAO"
    GERAR_TRAFEGO = "GERAR_TRAFEGO"
    AMPLIAR_PRESENCA_TERRITORIAL = "AMPLIAR_PRESENCA_TERRITORIAL"
    CONCENTRAR_PUBLICOS_PRIORITARIOS = "CONCENTRAR_PUBLICOS_PRIORITARIOS"
    ACOMPANHAR_ETAPAS_JORNADA = "ACOMPANHAR_ETAPAS_JORNADA"
    RESPONDER_PRESSAO_COMPETITIVA = "RESPONDER_PRESSAO_COMPETITIVA"
    RECUPERAR_PRESENCA = "RECUPERAR_PRESENCA"
    MANTER_LIDERANCA = "MANTER_LIDERANCA"
    SUSTENTAR_PRESENCA = "SUSTENTAR_PRESENCA"
    GERAR_RAPIDA_VISIBILIDADE = "GERAR_RAPIDA_VISIBILIDADE"
    OUTRA = "OUTRA"


ROTULOS_RESTRICOES = dict(zip(CategoriaRestricao, (
    "Geográfica", "Populacional", "Público", "Segmento", "Período",
    "Orçamentária", "Legal", "Ética", "Institucional", "Mercadológica",
    "Competitiva", "Operacional", "Disponibilidade", "Mensuração",
    "Outra restrição controlada",
)))
ROTULOS_PRETENSOES = dict(zip(CategoriaPretensao, (
    "Ampliar presença", "Alcançar novos públicos",
    "Reforçar presença entre públicos atuais", "Aumentar conhecimento",
    "Melhorar lembrança", "Apoiar lançamento", "Apoiar vendas",
    "Estimular experimentação", "Gerar tráfego",
    "Ampliar presença territorial", "Concentrar esforços em públicos prioritários",
    "Acompanhar etapas específicas da jornada", "Responder à pressão competitiva",
    "Recuperar presença", "Manter liderança", "Sustentar presença",
    "Gerar rápida visibilidade", "Outra pretensão controlada",
)))


@dataclass(frozen=True, slots=True)
class PrioridadeContextual:
    id_prioridade: UUID
    tipo_entidade: TipoEntidadePrioridade
    id_entidade: UUID | None
    prioridade: int
    ordem: int | None
    justificativa: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_prioridade, UUID):
            raise TypeError("id_prioridade deve ser UUID")
        if not isinstance(self.tipo_entidade, TipoEntidadePrioridade):
            raise TypeError("tipo_entidade inválido")
        if self.tipo_entidade is TipoEntidadePrioridade.PERIODO:
            if self.id_entidade is not None:
                raise ValueError("Prioridade do Período não usa id_entidade")
        elif not isinstance(self.id_entidade, UUID):
            raise TypeError("id_entidade deve ser UUID")
        _escala(self.prioridade, "prioridade")
        if self.ordem is not None and (type(self.ordem) is not int or self.ordem <= 0):
            raise ValueError("ordem deve ser inteiro positivo")
        object.__setattr__(self, "justificativa", _opcional(self.justificativa))


@dataclass(frozen=True, slots=True)
class RestricaoDeclarada:
    id_restricao: UUID
    categoria: CategoriaRestricao
    descricao: str
    entidade_afetada: str | None
    intensidade: int
    prioridade: int
    origem: str | None
    justificativa: str | None
    documento_fonte: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_restricao, UUID):
            raise TypeError("id_restricao deve ser UUID")
        if not isinstance(self.categoria, CategoriaRestricao):
            raise TypeError("categoria inválida")
        object.__setattr__(self, "descricao", _texto(self.descricao, "descricao"))
        _escala(self.intensidade, "intensidade")
        _escala(self.prioridade, "prioridade")
        for campo in ("entidade_afetada", "origem", "justificativa", "documento_fonte", "observacao"):
            object.__setattr__(self, campo, _opcional(getattr(self, campo)))

    def diagnosticos(self) -> tuple[str, ...]:
        alertas = []
        if not self.entidade_afetada:
            alertas.append("Restrição sem entidade afetada.")
        if self.categoria is CategoriaRestricao.LEGAL and not (
            self.documento_fonte or self.justificativa
        ):
            alertas.append("Restrição legal sem fundamento informado.")
        if self.intensidade >= 4 and not self.justificativa:
            alertas.append("Restrição de alta intensidade sem justificativa.")
        return tuple(alertas)


@dataclass(frozen=True, slots=True)
class PretensaoDeclarada:
    id_pretensao: UUID
    categoria: CategoriaPretensao
    descricao_controlada: str | None
    prioridade: int
    intensidade: int
    id_publico: UUID | None
    id_praca: UUID | None
    id_etapa_jornada: UUID | None
    periodo_associado: str | None
    flexibilidade_declarada: str | None
    justificativa: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_pretensao, UUID):
            raise TypeError("id_pretensao deve ser UUID")
        if not isinstance(self.categoria, CategoriaPretensao):
            raise TypeError("categoria inválida")
        _escala(self.prioridade, "prioridade")
        _escala(self.intensidade, "intensidade")
        for campo in ("id_publico", "id_praca", "id_etapa_jornada"):
            valor = getattr(self, campo)
            if valor is not None and not isinstance(valor, UUID):
                raise TypeError(f"{campo} deve ser UUID")
        for campo in ("descricao_controlada", "periodo_associado", "flexibilidade_declarada", "justificativa"):
            object.__setattr__(self, campo, _opcional(getattr(self, campo)))
        if self.categoria is CategoriaPretensao.OUTRA and not self.descricao_controlada:
            raise ValueError("Descreva a outra pretensão controlada")
