from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
import re
from types import MappingProxyType
from uuid import UUID


class EscopoSituacaoMercadologica(str, Enum):
    ANUNCIANTE = "ANUNCIANTE"
    MERCADO = "MERCADO"
    CATEGORIA = "CATEGORIA"
    CONCORRENCIA = "CONCORRENCIA"


class NaturezaRegistroSituacao(str, Enum):
    QUANTITATIVO = "QUANTITATIVO"
    QUALITATIVO = "QUALITATIVO"


def _texto(valor: str, campo: str) -> str:
    texto = valor.strip()
    if not texto:
        raise ValueError(f"{campo} é obrigatório")
    return texto


def _opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    return valor.strip() or None


@dataclass(frozen=True, slots=True)
class DefinicaoAspectoSituacao:
    codigo: str
    rotulo: str
    descricao: str
    unidades_sugeridas: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "codigo", _validar_codigo(self.codigo))
        object.__setattr__(self, "rotulo", _texto(self.rotulo, "rotulo"))
        object.__setattr__(self, "descricao", _texto(self.descricao, "descricao"))
        unidades = tuple(
            unidade.strip()
            for unidade in self.unidades_sugeridas
            if unidade.strip()
        )
        object.__setattr__(self, "unidades_sugeridas", tuple(dict.fromkeys(unidades)))


def _aspecto(
    codigo: str,
    rotulo: str,
    descricao: str,
    unidades: tuple[str, ...] = (),
) -> DefinicaoAspectoSituacao:
    return DefinicaoAspectoSituacao(codigo, rotulo, descricao, unidades)


_PADRAO_CODIGO = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", re.ASCII)


def _validar_codigo(codigo: str) -> str:
    codigo_normalizado = codigo.strip()
    if not codigo_normalizado or not _PADRAO_CODIGO.fullmatch(codigo_normalizado):
        raise ValueError("codigo deve possuir formato semântico válido")
    return codigo_normalizado


_ASPECTOS = MappingProxyType(
    {
        EscopoSituacaoMercadologica.ANUNCIANTE: (
            _aspecto(
                "posicao_competitiva",
                "Posição competitiva",
                "Posição declarada diante dos concorrentes.",
            ),
            _aspecto(
                "participacao_mercado",
                "Participação de mercado",
                "Parcela declarada das vendas, receitas, unidades ou clientes "
                "atribuída ao anunciante no mercado ou categoria de referência.",
                ("%",),
            ),
            _aspecto(
                "penetracao", "Penetração",
                "Presença declarada na base ou universo relevante.", ("%",),
            ),
            _aspecto(
                "notoriedade",
                "Notoriedade",
                "Nível declarado de conhecimento do anunciante.",
                ("%", "pontos", "índice"),
            ),
            _aspecto(
                "lembranca",
                "Lembrança",
                "Nível declarado de lembrança da marca.",
                ("%", "pontos", "índice"),
            ),
            _aspecto(
                "imagem_percebida", "Imagem percebida",
                "Percepções declaradas associadas ao anunciante.",
            ),
            _aspecto(
                "preferencia",
                "Preferência",
                "Preferência declarada diante das alternativas.",
                ("%", "pontos", "índice"),
            ),
            _aspecto(
                "fidelizacao",
                "Fidelização",
                "Nível declarado de permanência ou recorrência.",
                ("%", "pontos", "índice"),
            ),
            _aspecto(
                "desempenho_comercial",
                "Desempenho comercial",
                "Resultado comercial informado no período.",
                ("R$", "unidades", "%", "índice"),
            ),
            _aspecto(
                "amplitude_distribuicao",
                "Amplitude da distribuição",
                "Extensão declarada da disponibilidade.",
                ("pontos de venda", "localidades", "%"),
            ),
            _aspecto(
                "presenca_geografica", "Presença geográfica",
                "Abrangência territorial declarada.",
            ),
            _aspecto(
                "estagio_ciclo_vida",
                "Estágio do ciclo de vida",
                "Situação declarada do produto, serviço ou marca em introdução, "
                "crescimento, maturidade ou declínio.",
            ),
            _aspecto(
                "tendencia_desempenho",
                "Tendência de desempenho",
                "Direção observada do desempenho, que pode ser descrita como "
                "crescimento, estabilidade, retração ou outra condição informada.",
            ),
        ),
        EscopoSituacaoMercadologica.MERCADO: (
            _aspecto(
                "tamanho_mercado",
                "Tamanho do mercado",
                "Volume ou valor declarado do mercado.",
                ("R$", "unidades", "pessoas"),
            ),
            _aspecto(
                "taxa_crescimento_mercado",
                "Taxa de crescimento do mercado",
                "Variação do tamanho do mercado entre dois períodos de referência.",
                ("%",),
            ),
            _aspecto(
                "sazonalidade_mercado", "Sazonalidade",
                "Variação recorrente declarada ao longo do tempo.",
            ),
            _aspecto(
                "grau_concentracao_mercado",
                "Grau de concentração",
                "Distribuição declarada da participação entre agentes.",
                ("%", "índice"),
            ),
            _aspecto(
                "estagio_maturidade_mercado", "Estágio de maturidade",
                "Estágio declarado de desenvolvimento do mercado.",
            ),
            _aspecto(
                "tendencia_desempenho_mercado",
                "Tendência de desempenho do mercado",
                "Direção observada do desempenho do mercado.",
            ),
            _aspecto(
                "intensidade_competitiva_mercado", "Intensidade competitiva",
                "Nível declarado de competição no mercado.",
            ),
            _aspecto(
                "mudancas_relevantes_mercado",
                "Mudanças relevantes no mercado",
                "Mudanças observáveis informadas para o mercado.",
            ),
        ),
        EscopoSituacaoMercadologica.CATEGORIA: (
            _aspecto(
                "tamanho_categoria",
                "Tamanho da categoria",
                "Volume ou valor declarado da categoria.",
                ("R$", "unidades", "pessoas"),
            ),
            _aspecto(
                "taxa_crescimento_categoria",
                "Taxa de crescimento da categoria",
                "Variação do tamanho da categoria entre períodos.",
                ("%",),
            ),
            _aspecto(
                "sazonalidade_categoria", "Sazonalidade",
                "Variação recorrente declarada ao longo do tempo.",
            ),
            _aspecto(
                "grau_concentracao_categoria",
                "Grau de concentração",
                "Distribuição declarada da participação entre agentes.",
                ("%", "índice"),
            ),
            _aspecto(
                "estagio_maturidade_categoria", "Estágio de maturidade",
                "Estágio declarado de desenvolvimento da categoria.",
            ),
            _aspecto(
                "tendencia_desempenho_categoria",
                "Tendência de desempenho da categoria",
                "Direção observada do desempenho da categoria.",
            ),
            _aspecto(
                "intensidade_competitiva_categoria", "Intensidade competitiva",
                "Nível declarado de competição na categoria.",
            ),
            _aspecto(
                "mudancas_relevantes_categoria",
                "Mudanças relevantes na categoria",
                "Mudanças observáveis informadas para a categoria.",
            ),
        ),
        EscopoSituacaoMercadologica.CONCORRENCIA: (
            _aspecto(
                "posicao_competitiva_concorrente", "Posição competitiva",
                "Posição declarada do concorrente.",
            ),
            _aspecto(
                "participacao_mercado_concorrente",
                "Participação de mercado do concorrente",
                "Parcela declarada atribuída ao concorrente.",
                ("%",),
            ),
            _aspecto(
                "intensidade_competitiva_concorrente", "Intensidade competitiva",
                "Pressão competitiva declarada.",
            ),
            _aspecto(
                "presenca_territorial_concorrente", "Presença territorial",
                "Abrangência territorial declarada do concorrente.",
            ),
            _aspecto(
                "presenca_comunicacao_concorrente",
                "Presença de comunicação",
                "Presença observada de comunicação do concorrente.",
            ),
            _aspecto(
                "investimento_midia_concorrente",
                "Investimento em mídia",
                "Investimento informado do concorrente em mídia.",
                ("R$",),
            ),
            _aspecto(
                "share_of_voice_concorrente",
                "Share of Voice",
                "Participação estimada da presença ou do investimento de "
                "comunicação do concorrente em relação ao conjunto competitivo.",
                ("%",),
            ),
            _aspecto(
                "vantagens_percebidas_concorrente", "Vantagens percebidas",
                "Vantagens declaradas do concorrente.",
            ),
            _aspecto(
                "desvantagens_percebidas_concorrente", "Desvantagens percebidas",
                "Desvantagens declaradas do concorrente.",
            ),
            _aspecto(
                "tendencia_desempenho_concorrente",
                "Tendência de desempenho do concorrente",
                "Direção observada do desempenho do concorrente.",
            ),
        ),
    }
)

_CODIGOS_TAXONOMIA = tuple(
    aspecto.codigo
    for aspectos in _ASPECTOS.values()
    for aspecto in aspectos
)
if len(_CODIGOS_TAXONOMIA) != len(set(_CODIGOS_TAXONOMIA)):
    raise ValueError("Taxonomia possui códigos de aspecto duplicados")


def listar_aspectos_iniciais(
    escopo: EscopoSituacaoMercadologica,
) -> tuple[DefinicaoAspectoSituacao, ...]:
    return _ASPECTOS[escopo]


@dataclass(frozen=True, slots=True)
class RegistroSituacaoMercadologica:
    id_registro: UUID
    escopo: EscopoSituacaoMercadologica
    codigo_aspecto: str | None
    aspecto: str
    entidade_referencia: str | None
    natureza: NaturezaRegistroSituacao
    valor_quantitativo: Decimal | None
    unidade: str | None
    valor_qualitativo: str | None
    fonte: str | None
    periodo_referencia: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_registro, UUID):
            raise TypeError("id_registro deve ser UUID")
        if not isinstance(self.escopo, EscopoSituacaoMercadologica):
            raise TypeError("escopo inválido")
        if not isinstance(self.natureza, NaturezaRegistroSituacao):
            raise TypeError("natureza inválida")
        if self.codigo_aspecto is not None:
            object.__setattr__(
                self,
                "codigo_aspecto",
                _validar_codigo(self.codigo_aspecto),
            )
        object.__setattr__(self, "aspecto", _texto(self.aspecto, "aspecto"))
        for campo in (
            "entidade_referencia", "unidade", "valor_qualitativo", "fonte",
            "periodo_referencia", "observacao",
        ):
            object.__setattr__(self, campo, _opcional(getattr(self, campo)))
        if self.escopo is EscopoSituacaoMercadologica.CONCORRENCIA:
            if self.entidade_referencia is None:
                raise ValueError("Concorrente relacionado é obrigatório")
        elif self.entidade_referencia is not None:
            raise ValueError("entidade_referencia só pertence à Concorrência")
        if self.natureza is NaturezaRegistroSituacao.QUANTITATIVO:
            if not isinstance(self.valor_quantitativo, Decimal):
                raise ValueError("valor_quantitativo é obrigatório")
            if not self.valor_quantitativo.is_finite():
                raise ValueError("valor_quantitativo deve ser finito")
            if self.unidade is None:
                raise ValueError("unidade é obrigatória")
            if self.valor_qualitativo is not None:
                raise ValueError("quantitativo não aceita valor_qualitativo")
        else:
            if self.valor_qualitativo is None:
                raise ValueError("valor_qualitativo é obrigatório")
            if self.valor_quantitativo is not None or self.unidade is not None:
                raise ValueError("qualitativo não aceita valor ou unidade")


@dataclass(frozen=True, slots=True)
class SituacaoMercadologicaCompetitiva:
    registros: tuple[RegistroSituacaoMercadologica, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "registros", tuple(self.registros))
        ids = tuple(registro.id_registro for registro in self.registros)
        if len(ids) != len(set(ids)):
            raise ValueError("IDs de registros duplicados")

    def adicionar(
        self,
        registro: RegistroSituacaoMercadologica,
    ) -> "SituacaoMercadologicaCompetitiva":
        if any(item.id_registro == registro.id_registro for item in self.registros):
            raise ValueError("ID de registro duplicado")
        return SituacaoMercadologicaCompetitiva(self.registros + (registro,))

    def remover(self, id_registro: UUID) -> "SituacaoMercadologicaCompetitiva":
        restantes = tuple(
            registro for registro in self.registros
            if registro.id_registro != id_registro
        )
        if len(restantes) == len(self.registros):
            raise LookupError("Registro não encontrado")
        return SituacaoMercadologicaCompetitiva(restantes)
