from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from uuid import UUID


def _texto(valor: object, campo: str) -> str:
    if not isinstance(valor, str):
        raise TypeError(f"{campo} deve ser texto")
    normalizado = valor.strip()
    if not normalizado:
        raise ValueError(f"{campo} é obrigatório")
    return normalizado


def _opcional(valor: str | None, campo: str) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise TypeError(f"{campo} deve ser texto")
    return valor.strip() or None


def _validar_decimal(valor: Decimal | None, campo: str) -> None:
    if valor is None:
        return
    if not isinstance(valor, Decimal):
        raise TypeError(f"{campo} deve ser Decimal")
    if not valor.is_finite() or valor <= 0:
        raise ValueError(f"{campo} deve ser positivo")


class TipoPracaTerritorial(str, Enum):
    PAIS = "PAIS"
    REGIAO = "REGIAO"
    ESTADO_UF = "ESTADO_UF"
    REGIAO_GEOGRAFICA_INTERMEDIARIA = (
        "REGIAO_GEOGRAFICA_INTERMEDIARIA"
    )
    REGIAO_GEOGRAFICA_IMEDIATA = "REGIAO_GEOGRAFICA_IMEDIATA"
    REGIAO_METROPOLITANA = "REGIAO_METROPOLITANA"
    MUNICIPIO = "MUNICIPIO"
    DISTRITO = "DISTRITO"
    BAIRRO = "BAIRRO"
    ZONA = "ZONA"
    AREA_DE_INFLUENCIA = "AREA_DE_INFLUENCIA"
    OUTRA = "OUTRA"


@dataclass(frozen=True, slots=True)
class DefinicaoTipoPracaTerritorial:
    codigo: TipoPracaTerritorial
    rotulo: str
    descricao: str

    def __post_init__(self) -> None:
        if not isinstance(self.codigo, TipoPracaTerritorial):
            raise TypeError("codigo deve ser TipoPracaTerritorial")
        object.__setattr__(self, "rotulo", _texto(self.rotulo, "rotulo"))
        object.__setattr__(self, "descricao", _texto(self.descricao, "descricao"))


@dataclass(frozen=True, slots=True)
class DefinicaoUnidadePopulacional:
    codigo: str
    rotulo: str
    descricao: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "codigo", _texto(self.codigo, "codigo"))
        object.__setattr__(self, "rotulo", _texto(self.rotulo, "rotulo"))
        object.__setattr__(self, "descricao", _texto(self.descricao, "descricao"))


_TIPOS_PRACA = (
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.PAIS,
        "País",
        "Território nacional.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.REGIAO,
        "Região",
        "Região territorial declarada.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.ESTADO_UF,
        "Estado ou unidade federativa",
        "Estado ou unidade federativa.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.REGIAO_GEOGRAFICA_INTERMEDIARIA,
        "Região Geográfica Intermediária",
        "Divisão regional oficial intermediária do IBGE.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.REGIAO_GEOGRAFICA_IMEDIATA,
        "Região Geográfica Imediata",
        "Divisão regional oficial imediata do IBGE.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.REGIAO_METROPOLITANA,
        "Região metropolitana",
        "Região metropolitana declarada.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.MUNICIPIO,
        "Município",
        "Território municipal.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.DISTRITO,
        "Distrito",
        "Distrito territorial.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.BAIRRO,
        "Bairro",
        "Bairro ou localidade equivalente.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.ZONA,
        "Zona ou setor territorial",
        "Zona ou setor declarado.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.AREA_DE_INFLUENCIA,
        "Área de influência ou delimitação personalizada",
        "Área delimitada pelo contexto informado.",
    ),
    DefinicaoTipoPracaTerritorial(
        TipoPracaTerritorial.OUTRA,
        "Outra delimitação territorial",
        "Outra delimitação declarada.",
    ),
)

_UNIDADES = (
    DefinicaoUnidadePopulacional("pessoas", "Pessoas", "Quantidade de pessoas."),
    DefinicaoUnidadePopulacional("domicilios", "Domicílios", "Quantidade de domicílios."),
    DefinicaoUnidadePopulacional("familias", "Famílias", "Quantidade de famílias."),
    DefinicaoUnidadePopulacional("empresas", "Empresas", "Quantidade de empresas."),
    DefinicaoUnidadePopulacional(
        "estabelecimentos",
        "Estabelecimentos",
        "Quantidade de estabelecimentos.",
    ),
    DefinicaoUnidadePopulacional(
        "pontos_de_venda",
        "Pontos de venda",
        "Quantidade de pontos de venda.",
    ),
)


def listar_tipos_praca_territorial() -> tuple[DefinicaoTipoPracaTerritorial, ...]:
    return _TIPOS_PRACA


def listar_unidades_populacionais() -> tuple[DefinicaoUnidadePopulacional, ...]:
    return _UNIDADES


@dataclass(frozen=True, slots=True)
class PracaDeclarada:
    id_praca: UUID
    tipo: TipoPracaTerritorial
    nome: str
    codigo_oficial: str | None
    abrangencia: str | None
    valor_populacao_referencia: Decimal | None
    codigo_unidade_populacional: str | None
    unidade_populacional: str | None
    fonte: str | None
    data_referencia: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_praca, UUID):
            raise TypeError("id_praca deve ser UUID")
        if not isinstance(self.tipo, TipoPracaTerritorial):
            raise TypeError("tipo inválido")
        object.__setattr__(self, "nome", _texto(self.nome, "nome"))
        for campo in (
            "codigo_oficial", "abrangencia", "codigo_unidade_populacional",
            "unidade_populacional", "fonte", "data_referencia", "observacao",
        ):
            object.__setattr__(self, campo, _opcional(getattr(self, campo), campo))
        _validar_decimal(self.valor_populacao_referencia, "valor_populacao_referencia")
        if self.valor_populacao_referencia is None:
            if self.codigo_unidade_populacional or self.unidade_populacional:
                raise ValueError("Unidade populacional exige valor")
        elif self.unidade_populacional is None:
            raise ValueError("Unidade populacional é obrigatória")


@dataclass(frozen=True, slots=True)
class UniversoDeclarado:
    id_universo: UUID
    nome: str
    definicao: str
    ids_pracas: tuple[UUID, ...]
    valor_populacional: Decimal | None
    codigo_unidade: str | None
    unidade: str
    fonte: str | None
    data_referencia: str | None
    criterios_inclusao: str | None
    criterios_exclusao: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_universo, UUID):
            raise TypeError("id_universo deve ser UUID")
        object.__setattr__(self, "nome", _texto(self.nome, "nome"))
        object.__setattr__(self, "definicao", _texto(self.definicao, "definicao"))
        ids = tuple(self.ids_pracas)
        if not ids:
            raise ValueError("Informe ao menos uma Praça para o Universo")
        if any(not isinstance(item, UUID) for item in ids):
            raise TypeError("ids_pracas devem conter UUIDs")
        if len(ids) != len(set(ids)):
            raise ValueError("ids_pracas possui duplicatas")
        object.__setattr__(self, "ids_pracas", ids)
        object.__setattr__(self, "codigo_unidade", _opcional(self.codigo_unidade, "codigo_unidade"))
        object.__setattr__(self, "unidade", _texto(self.unidade, "unidade"))
        for campo in (
            "fonte", "data_referencia", "criterios_inclusao",
            "criterios_exclusao", "observacao",
        ):
            object.__setattr__(self, campo, _opcional(getattr(self, campo), campo))
        _validar_decimal(self.valor_populacional, "valor_populacional")


@dataclass(frozen=True, slots=True)
class EstruturaTerritorialPopulacional:
    pracas: tuple[PracaDeclarada, ...]
    universos: tuple[UniversoDeclarado, ...]

    def __post_init__(self) -> None:
        pracas = tuple(self.pracas)
        universos = tuple(self.universos)
        if any(not isinstance(item, PracaDeclarada) for item in pracas):
            raise TypeError("pracas contém item inválido")
        if any(not isinstance(item, UniversoDeclarado) for item in universos):
            raise TypeError("universos contém item inválido")
        ids_pracas = tuple(item.id_praca for item in pracas)
        ids_universos = tuple(item.id_universo for item in universos)
        if len(ids_pracas) != len(set(ids_pracas)):
            raise ValueError("IDs de praça duplicados")
        if len(ids_universos) != len(set(ids_universos)):
            raise ValueError("IDs de universo duplicados")
        existentes = set(ids_pracas)
        if any(not set(item.ids_pracas) <= existentes for item in universos):
            raise ValueError("Praça relacionada não existe")
        object.__setattr__(self, "pracas", pracas)
        object.__setattr__(self, "universos", universos)

    def adicionar_praca(self, praca: PracaDeclarada) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(self.pracas + (praca,), self.universos)

    def remover_praca(self, id_praca: UUID) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_praca == id_praca for item in self.pracas):
            raise LookupError("Praça não encontrada")
        if any(id_praca in item.ids_pracas for item in self.universos):
            raise ValueError("Praça vinculada a Universo não pode ser removida")
        restantes = tuple(item for item in self.pracas if item.id_praca != id_praca)
        return EstruturaTerritorialPopulacional(restantes, self.universos)

    def adicionar_universo(self, universo: UniversoDeclarado) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(self.pracas, self.universos + (universo,))

    def remover_universo(self, id_universo: UUID) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_universo == id_universo for item in self.universos):
            raise LookupError("Universo não encontrado")
        restantes = tuple(
            item for item in self.universos if item.id_universo != id_universo
        )
        return EstruturaTerritorialPopulacional(self.pracas, restantes)
