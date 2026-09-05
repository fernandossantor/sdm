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


def _validar_escala_opcional(valor: int | None, campo: str) -> None:
    if valor is None:
        return
    if type(valor) is not int or not 1 <= valor <= 5:
        raise ValueError(f"{campo} deve estar entre 1 e 5")


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


class CriterioSegmentacao(str, Enum):
    GEOGRAFICA = "GEOGRAFICA"
    DEMOGRAFICA = "DEMOGRAFICA"
    SOCIOECONOMICA = "SOCIOECONOMICA"
    PSICOGRAFICA = "PSICOGRAFICA"
    COMPORTAMENTAL = "COMPORTAMENTAL"
    CONSUMO = "CONSUMO"
    RELACIONAMENTO_CATEGORIA = "RELACIONAMENTO_CATEGORIA"
    RELACIONAMENTO_MARCA = "RELACIONAMENTO_MARCA"
    JORNADA = "JORNADA"
    INTENCAO = "INTENCAO"
    CONTEXTO = "CONTEXTO"


@dataclass(frozen=True, slots=True)
class DefinicaoCriterioSegmentacao:
    codigo: CriterioSegmentacao
    rotulo: str


_CRITERIOS_SEGMENTACAO = tuple(
    DefinicaoCriterioSegmentacao(codigo, rotulo)
    for codigo, rotulo in (
        (CriterioSegmentacao.GEOGRAFICA, "Geográfica"),
        (CriterioSegmentacao.DEMOGRAFICA, "Demográfica"),
        (CriterioSegmentacao.SOCIOECONOMICA, "Socioeconômica"),
        (CriterioSegmentacao.PSICOGRAFICA, "Psicográfica"),
        (CriterioSegmentacao.COMPORTAMENTAL, "Comportamental"),
        (CriterioSegmentacao.CONSUMO, "Consumo"),
        (CriterioSegmentacao.RELACIONAMENTO_CATEGORIA, "Relacionamento com a categoria"),
        (CriterioSegmentacao.RELACIONAMENTO_MARCA, "Relacionamento com a marca"),
        (CriterioSegmentacao.JORNADA, "Jornada"),
        (CriterioSegmentacao.INTENCAO, "Intenção"),
        (CriterioSegmentacao.CONTEXTO, "Contexto"),
    )
)


def listar_criterios_segmentacao() -> tuple[DefinicaoCriterioSegmentacao, ...]:
    return _CRITERIOS_SEGMENTACAO


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
class SegmentoDeclarado:
    id_segmento: UUID
    id_universo_origem: UUID
    ids_pracas: tuple[UUID, ...]
    criterios_aplicados: tuple[CriterioSegmentacao, ...]
    definicao: str
    tamanho_estimado: Decimal | None
    fonte: str | None
    data_referencia: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_segmento, UUID):
            raise TypeError("id_segmento deve ser UUID")
        if not isinstance(self.id_universo_origem, UUID):
            raise TypeError("id_universo_origem deve ser UUID")
        ids_pracas = tuple(self.ids_pracas)
        if not ids_pracas:
            raise ValueError("Informe ao menos uma Praça para o Segmento")
        if any(not isinstance(item, UUID) for item in ids_pracas):
            raise TypeError("ids_pracas devem conter UUIDs")
        if len(ids_pracas) != len(set(ids_pracas)):
            raise ValueError("ids_pracas possui duplicatas")
        criterios = tuple(self.criterios_aplicados)
        if not criterios:
            raise ValueError("Informe ao menos um critério de segmentação")
        if any(not isinstance(item, CriterioSegmentacao) for item in criterios):
            raise TypeError("criterios_aplicados contém item inválido")
        if len(criterios) != len(set(criterios)):
            raise ValueError("criterios_aplicados possui duplicatas")
        object.__setattr__(self, "ids_pracas", ids_pracas)
        object.__setattr__(self, "criterios_aplicados", criterios)
        object.__setattr__(self, "definicao", _texto(self.definicao, "definicao"))
        object.__setattr__(self, "fonte", _opcional(self.fonte, "fonte"))
        object.__setattr__(
            self, "data_referencia", _opcional(self.data_referencia, "data_referencia")
        )
        _validar_decimal(self.tamanho_estimado, "tamanho_estimado")


@dataclass(frozen=True, slots=True)
class PublicoDeclarado:
    id_publico: UUID
    nome: str | None
    ids_segmentos_origem: tuple[UUID, ...]
    ids_pracas: tuple[UUID, ...]
    prioridade: int | None
    intensidade_importancia: int | None
    tamanho_estimado: Decimal | None
    papel_declarado: str | None
    justificativa: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_publico, UUID):
            raise TypeError("id_publico deve ser UUID")
        segmentos = tuple(self.ids_segmentos_origem)
        pracas = tuple(self.ids_pracas)
        if not segmentos:
            raise ValueError("Informe ao menos um Segmento de origem")
        if any(not isinstance(item, UUID) for item in segmentos):
            raise TypeError("ids_segmentos_origem devem conter UUIDs")
        if len(segmentos) != len(set(segmentos)):
            raise ValueError("ids_segmentos_origem possui duplicatas")
        if not pracas:
            raise ValueError("Informe ao menos uma Praça para o Público")
        if any(not isinstance(item, UUID) for item in pracas):
            raise TypeError("ids_pracas devem conter UUIDs")
        if len(pracas) != len(set(pracas)):
            raise ValueError("ids_pracas possui duplicatas")
        object.__setattr__(self, "ids_segmentos_origem", segmentos)
        object.__setattr__(self, "ids_pracas", pracas)
        for campo in ("nome", "papel_declarado", "justificativa"):
            object.__setattr__(self, campo, _opcional(getattr(self, campo), campo))
        _validar_escala_opcional(self.prioridade, "prioridade")
        _validar_escala_opcional(
            self.intensidade_importancia, "intensidade_importancia"
        )
        _validar_decimal(self.tamanho_estimado, "tamanho_estimado")


@dataclass(frozen=True, slots=True)
class EstruturaTerritorialPopulacional:
    pracas: tuple[PracaDeclarada, ...]
    universos: tuple[UniversoDeclarado, ...]
    criterios_segmentacao: tuple[CriterioSegmentacao, ...] = ()
    segmentos: tuple[SegmentoDeclarado, ...] = ()
    publicos: tuple[PublicoDeclarado, ...] = ()

    def __post_init__(self) -> None:
        pracas = tuple(self.pracas)
        universos = tuple(self.universos)
        criterios = tuple(self.criterios_segmentacao)
        segmentos = tuple(self.segmentos)
        publicos = tuple(self.publicos)
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
        if any(not isinstance(item, CriterioSegmentacao) for item in criterios):
            raise TypeError("criterios_segmentacao contém item inválido")
        if len(criterios) != len(set(criterios)):
            raise ValueError("Critérios de segmentação duplicados")
        if any(not isinstance(item, SegmentoDeclarado) for item in segmentos):
            raise TypeError("segmentos contém item inválido")
        ids_segmentos = tuple(item.id_segmento for item in segmentos)
        if len(ids_segmentos) != len(set(ids_segmentos)):
            raise ValueError("IDs de segmento duplicados")
        universos_por_id = {item.id_universo: item for item in universos}
        for segmento in segmentos:
            universo = universos_por_id.get(segmento.id_universo_origem)
            if universo is None:
                raise ValueError("Universo de origem do Segmento não existe")
            if not set(segmento.ids_pracas) <= set(universo.ids_pracas):
                raise ValueError("Praça do Segmento é incompatível com o Universo")
            if not set(segmento.criterios_aplicados) <= set(criterios):
                raise ValueError("Critério do Segmento não foi selecionado")
            if (
                segmento.tamanho_estimado is not None
                and universo.valor_populacional is not None
                and segmento.tamanho_estimado > universo.valor_populacional
            ):
                raise ValueError("Tamanho do Segmento não pode superar o Universo")
        if any(not isinstance(item, PublicoDeclarado) for item in publicos):
            raise TypeError("publicos contém item inválido")
        ids_publicos = tuple(item.id_publico for item in publicos)
        if len(ids_publicos) != len(set(ids_publicos)):
            raise ValueError("IDs de público duplicados")
        segmentos_por_id = {item.id_segmento: item for item in segmentos}
        assinaturas: set[tuple[frozenset[UUID], frozenset[UUID]]] = set()
        for publico in publicos:
            if not set(publico.ids_segmentos_origem) <= set(segmentos_por_id):
                raise ValueError("Segmento de origem do Público não existe")
            pracas_compativeis = {
                id_praca
                for id_segmento in publico.ids_segmentos_origem
                for id_praca in segmentos_por_id[id_segmento].ids_pracas
            }
            if not set(publico.ids_pracas) <= pracas_compativeis:
                raise ValueError("Praça do Público é incompatível com os Segmentos")
            assinatura = (
                frozenset(publico.ids_segmentos_origem),
                frozenset(publico.ids_pracas),
            )
            if assinatura in assinaturas:
                raise ValueError("Público duplicado")
            assinaturas.add(assinatura)
        object.__setattr__(self, "pracas", pracas)
        object.__setattr__(self, "universos", universos)
        object.__setattr__(self, "criterios_segmentacao", criterios)
        object.__setattr__(self, "segmentos", segmentos)
        object.__setattr__(self, "publicos", publicos)

    def adicionar_praca(self, praca: PracaDeclarada) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(self.pracas + (praca,), self.universos, self.criterios_segmentacao, self.segmentos, self.publicos)

    def remover_praca(self, id_praca: UUID) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_praca == id_praca for item in self.pracas):
            raise LookupError("Praça não encontrada")
        if any(id_praca in item.ids_pracas for item in self.universos):
            raise ValueError("Praça vinculada a Universo não pode ser removida")
        restantes = tuple(item for item in self.pracas if item.id_praca != id_praca)
        return EstruturaTerritorialPopulacional(restantes, self.universos, self.criterios_segmentacao, self.segmentos, self.publicos)

    def adicionar_universo(self, universo: UniversoDeclarado) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(self.pracas, self.universos + (universo,), self.criterios_segmentacao, self.segmentos, self.publicos)

    def remover_universo(self, id_universo: UUID) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_universo == id_universo for item in self.universos):
            raise LookupError("Universo não encontrado")
        if any(item.id_universo_origem == id_universo for item in self.segmentos):
            raise ValueError("Universo vinculado a Segmento não pode ser removido")
        restantes = tuple(
            item for item in self.universos if item.id_universo != id_universo
        )
        return EstruturaTerritorialPopulacional(self.pracas, restantes, self.criterios_segmentacao, self.segmentos, self.publicos)

    def definir_criterios_segmentacao(
        self, criterios: tuple[CriterioSegmentacao, ...],
    ) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(
            self.pracas, self.universos, criterios, self.segmentos, self.publicos
        )

    def adicionar_segmento(
        self, segmento: SegmentoDeclarado,
    ) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(
            self.pracas,
            self.universos,
            self.criterios_segmentacao,
            self.segmentos + (segmento,),
            self.publicos,
        )

    def editar_segmento(
        self, segmento: SegmentoDeclarado,
    ) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_segmento == segmento.id_segmento for item in self.segmentos):
            raise LookupError("Segmento não encontrado")
        atualizados = tuple(
            segmento if item.id_segmento == segmento.id_segmento else item
            for item in self.segmentos
        )
        return EstruturaTerritorialPopulacional(
            self.pracas, self.universos, self.criterios_segmentacao, atualizados,
            self.publicos,
        )

    def remover_segmento(self, id_segmento: UUID) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_segmento == id_segmento for item in self.segmentos):
            raise LookupError("Segmento não encontrado")
        if any(id_segmento in item.ids_segmentos_origem for item in self.publicos):
            raise ValueError("Segmento vinculado a Público não pode ser removido")
        restantes = tuple(
            item for item in self.segmentos if item.id_segmento != id_segmento
        )
        return EstruturaTerritorialPopulacional(
            self.pracas, self.universos, self.criterios_segmentacao, restantes,
            self.publicos,
        )

    def adicionar_publico(
        self, publico: PublicoDeclarado,
    ) -> "EstruturaTerritorialPopulacional":
        return EstruturaTerritorialPopulacional(
            self.pracas, self.universos, self.criterios_segmentacao,
            self.segmentos, self.publicos + (publico,),
        )

    def editar_publico(
        self, publico: PublicoDeclarado,
    ) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_publico == publico.id_publico for item in self.publicos):
            raise LookupError("Público não encontrado")
        atualizados = tuple(
            publico if item.id_publico == publico.id_publico else item
            for item in self.publicos
        )
        return EstruturaTerritorialPopulacional(
            self.pracas, self.universos, self.criterios_segmentacao,
            self.segmentos, atualizados,
        )

    def remover_publico(self, id_publico: UUID) -> "EstruturaTerritorialPopulacional":
        if not any(item.id_publico == id_publico for item in self.publicos):
            raise LookupError("Público não encontrado")
        restantes = tuple(item for item in self.publicos if item.id_publico != id_publico)
        return EstruturaTerritorialPopulacional(
            self.pracas, self.universos, self.criterios_segmentacao,
            self.segmentos, restantes,
        )
