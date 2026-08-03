import re
from dataclasses import dataclass
from enum import Enum
from uuid import UUID


_PADRAO_CODIGO = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", re.ASCII)


def _validar_codigo(codigo: object) -> str:
    if not isinstance(codigo, str):
        raise TypeError("codigo deve ser texto")
    if not _PADRAO_CODIGO.fullmatch(codigo):
        raise ValueError("codigo inválido")
    return codigo


def _normalizar_texto(valor: object, campo: str) -> str:
    if not isinstance(valor, str):
        raise TypeError(f"{campo} deve ser texto")
    normalizado = valor.strip()
    if not normalizado:
        raise ValueError(f"{campo} é obrigatório")
    return normalizado


def _normalizar_opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    normalizado = valor.strip()
    return normalizado or None


def _validar_escala(valor: object, campo: str) -> None:
    if type(valor) is not int or not 1 <= valor <= 5:
        raise ValueError(f"{campo} deve ser inteiro entre 1 e 5")


@dataclass(frozen=True, slots=True)
class DefinicaoObjetivoDeclarado:
    codigo: str
    rotulo: str
    descricao: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "codigo", _validar_codigo(self.codigo))
        object.__setattr__(self, "rotulo", _normalizar_texto(self.rotulo, "rotulo"))
        object.__setattr__(
            self,
            "descricao",
            _normalizar_texto(self.descricao, "descricao"),
        )


class DimensaoCompostoMarketing(str, Enum):
    PRODUTO = "PRODUTO"
    PRECO = "PRECO"
    PRACA = "PRACA"
    PROMOCAO = "PROMOCAO"


@dataclass(frozen=True, slots=True)
class DefinicaoDimensaoCompostoMarketing:
    codigo: DimensaoCompostoMarketing
    rotulo: str
    descricao: str

    def __post_init__(self) -> None:
        if not isinstance(self.codigo, DimensaoCompostoMarketing):
            raise TypeError("codigo deve ser DimensaoCompostoMarketing")
        object.__setattr__(self, "rotulo", _normalizar_texto(self.rotulo, "rotulo"))
        object.__setattr__(
            self,
            "descricao",
            _normalizar_texto(self.descricao, "descricao"),
        )


_OBJETIVOS_MARKETING = (
    DefinicaoObjetivoDeclarado(
        "marketing_branding",
        "Branding",
        "Fortalecer o valor, a identidade ou a presença geral da marca.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_posicionamento",
        "Posicionamento",
        "Estabelecer, reforçar ou alterar a posição pretendida da oferta no mercado.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_segmentacao",
        "Segmentação",
        "Concentrar a atuação em segmentos definidos do mercado.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_diferenciacao",
        "Diferenciação",
        "Destacar atributos ou benefícios que distingam a oferta das alternativas.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_crescimento",
        "Crescimento",
        "Expandir vendas, receitas, base de clientes, presença ou volume de negócios.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_participacao_mercado",
        "Participação de mercado",
        "Ampliar, defender ou recuperar a parcela ocupada no mercado ou categoria.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_fidelizacao",
        "Fidelização",
        "Aumentar retenção, recorrência ou permanência de clientes.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_penetracao",
        "Penetração",
        "Ampliar a adoção da oferta dentro do mercado ou segmento atendido.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_desenvolvimento_produto",
        "Desenvolvimento de produto",
        "Criar, ampliar ou aperfeiçoar produtos ou serviços destinados aos mercados atuais.",
    ),
    DefinicaoObjetivoDeclarado(
        "marketing_diversificacao",
        "Diversificação",
        "Expandir a atuação para novas ofertas, mercados ou combinações entre ambos.",
    ),
)


_OBJETIVOS_COMUNICACAO = (
    DefinicaoObjetivoDeclarado(
        "comunicacao_notoriedade",
        "Notoriedade",
        "Ampliar o reconhecimento da existência da marca, produto, serviço ou organização.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_conhecimento",
        "Conhecimento",
        "Aumentar a informação disponível ao público sobre a oferta.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_lembranca",
        "Lembrança",
        "Fortalecer a capacidade de recordar a marca ou oferta.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_compreensao",
        "Compreensão",
        "Favorecer o entendimento da proposta, funcionamento ou benefício oferecido.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_imagem",
        "Imagem",
        "Influenciar as associações e percepções atribuídas à marca ou oferta.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_posicionamento_percebido",
        "Posicionamento percebido",
        "Consolidar na percepção do público a posição pretendida para a marca ou oferta.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_diferenciacao_percebida",
        "Diferenciação percebida",
        "Tornar reconhecíveis diferenças relevantes em relação às alternativas.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_persuasao",
        "Persuasão",
        "Influenciar atitudes, opiniões ou disposições do público.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_preferencia",
        "Preferência",
        "Favorecer a escolha da marca ou oferta diante das alternativas.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_consideracao",
        "Consideração",
        "Inserir ou fortalecer a marca entre as opções avaliadas pelo público.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_engajamento",
        "Engajamento",
        "Estimular envolvimento, participação ou interação.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_experimentacao",
        "Experimentação",
        "Estimular o primeiro uso, teste ou contato com a oferta.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_acao",
        "Ação",
        "Estimular uma ação declarada de comunicação, sem definir KPI ou objetivo de mídia.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_relacionamento",
        "Relacionamento",
        "Desenvolver interação continuada entre a organização e seus públicos.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_fidelizacao",
        "Fidelização",
        "Fortalecer permanência, recorrência ou vínculo comunicacional.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_recomendacao",
        "Recomendação",
        "Estimular a indicação da marca, produto ou serviço a outras pessoas.",
    ),
    DefinicaoObjetivoDeclarado(
        "comunicacao_defesa_marca",
        "Defesa da marca",
        "Estimular apoio ativo e manifestação favorável em defesa da marca.",
    ),
)


_DIMENSOES_COMPOSTO = (
    DefinicaoDimensaoCompostoMarketing(
        DimensaoCompostoMarketing.PRODUTO,
        "Produto",
        "Características, benefícios, portfólio ou configuração da oferta.",
    ),
    DefinicaoDimensaoCompostoMarketing(
        DimensaoCompostoMarketing.PRECO,
        "Preço",
        "Preço, condições comerciais ou percepção de valor.",
    ),
    DefinicaoDimensaoCompostoMarketing(
        DimensaoCompostoMarketing.PRACA,
        "Praça (distribuição)",
        "Disponibilidade, acesso, distribuição ou presença comercial. "
        "Não representa a praça territorial da campanha.",
    ),
    DefinicaoDimensaoCompostoMarketing(
        DimensaoCompostoMarketing.PROMOCAO,
        "Promoção",
        "Ações promocionais e de comunicação do composto de Marketing. "
        "Não define objetivo de mídia.",
    ),
)


_CODIGOS_CATALOGOS = tuple(
    item.codigo for item in _OBJETIVOS_MARKETING + _OBJETIVOS_COMUNICACAO
)
if len(_CODIGOS_CATALOGOS) != len(set(_CODIGOS_CATALOGOS)):
    raise ValueError("Catálogos possuem códigos duplicados")


def listar_objetivos_marketing_iniciais() -> tuple[DefinicaoObjetivoDeclarado, ...]:
    return _OBJETIVOS_MARKETING


def listar_objetivos_comunicacao_iniciais() -> tuple[DefinicaoObjetivoDeclarado, ...]:
    return _OBJETIVOS_COMUNICACAO


def listar_dimensoes_composto_marketing(
) -> tuple[DefinicaoDimensaoCompostoMarketing, ...]:
    return _DIMENSOES_COMPOSTO


@dataclass(frozen=True, slots=True)
class ObjetivoMarketingDeclarado:
    id_objetivo: UUID
    codigo_objetivo: str | None
    objetivo: str
    dimensoes_composto: tuple[DimensaoCompostoMarketing, ...]
    prioridade_declarada: int
    intensidade_declarada: int
    justificativa: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_objetivo, UUID):
            raise TypeError("id_objetivo deve ser UUID")
        if self.codigo_objetivo is not None:
            object.__setattr__(
                self,
                "codigo_objetivo",
                _validar_codigo(self.codigo_objetivo),
            )
        object.__setattr__(self, "objetivo", _normalizar_texto(self.objetivo, "objetivo"))
        dimensoes = tuple(self.dimensoes_composto)
        if any(not isinstance(item, DimensaoCompostoMarketing) for item in dimensoes):
            raise TypeError("dimensoes_composto inválidas")
        if len(dimensoes) != len(set(dimensoes)):
            raise ValueError("dimensoes_composto possui duplicatas")
        object.__setattr__(self, "dimensoes_composto", dimensoes)
        _validar_escala(self.prioridade_declarada, "prioridade_declarada")
        _validar_escala(self.intensidade_declarada, "intensidade_declarada")
        object.__setattr__(self, "justificativa", _normalizar_opcional(self.justificativa))


@dataclass(frozen=True, slots=True)
class ObjetivoComunicacaoDeclarado:
    id_objetivo: UUID
    codigo_objetivo: str | None
    objetivo: str
    ids_objetivos_marketing_relacionados: tuple[UUID, ...]
    prioridade_declarada: int
    intensidade_declarada: int
    justificativa: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_objetivo, UUID):
            raise TypeError("id_objetivo deve ser UUID")
        if self.codigo_objetivo is not None:
            object.__setattr__(
                self,
                "codigo_objetivo",
                _validar_codigo(self.codigo_objetivo),
            )
        object.__setattr__(self, "objetivo", _normalizar_texto(self.objetivo, "objetivo"))
        relacionados = tuple(self.ids_objetivos_marketing_relacionados)
        if any(not isinstance(item, UUID) for item in relacionados):
            raise TypeError("IDs relacionados devem ser UUID")
        if len(relacionados) != len(set(relacionados)):
            raise ValueError("IDs relacionados possuem duplicatas")
        object.__setattr__(self, "ids_objetivos_marketing_relacionados", relacionados)
        _validar_escala(self.prioridade_declarada, "prioridade_declarada")
        _validar_escala(self.intensidade_declarada, "intensidade_declarada")
        object.__setattr__(self, "justificativa", _normalizar_opcional(self.justificativa))


@dataclass(frozen=True, slots=True)
class ObjetivosDeclarados:
    marketing: tuple[ObjetivoMarketingDeclarado, ...]
    comunicacao: tuple[ObjetivoComunicacaoDeclarado, ...]

    def __post_init__(self) -> None:
        marketing = tuple(self.marketing)
        comunicacao = tuple(self.comunicacao)
        if any(
            not isinstance(item, ObjetivoMarketingDeclarado)
            for item in marketing
        ):
            raise TypeError("marketing contém objetivo de tipo inválido")
        if any(
            not isinstance(item, ObjetivoComunicacaoDeclarado)
            for item in comunicacao
        ):
            raise TypeError("comunicacao contém objetivo de tipo inválido")
        ids = tuple(item.id_objetivo for item in marketing + comunicacao)
        if len(ids) != len(set(ids)):
            raise ValueError("IDs de objetivos duplicados")
        self._validar_duplicidade_tipo(marketing)
        self._validar_duplicidade_tipo(comunicacao)
        ids_marketing = {item.id_objetivo for item in marketing}
        for objetivo in comunicacao:
            if not set(objetivo.ids_objetivos_marketing_relacionados) <= ids_marketing:
                raise ValueError("Objetivo de Marketing relacionado não existe")
        object.__setattr__(self, "marketing", marketing)
        object.__setattr__(self, "comunicacao", comunicacao)

    @staticmethod
    def _validar_duplicidade_tipo(objetivos: tuple[object, ...]) -> None:
        codigos = [
            item.codigo_objetivo
            for item in objetivos
            if item.codigo_objetivo is not None
        ]
        personalizados = [
            item.objetivo.strip().casefold()
            for item in objetivos
            if item.codigo_objetivo is None
        ]
        if len(codigos) != len(set(codigos)):
            raise ValueError("Código de objetivo duplicado")
        if len(personalizados) != len(set(personalizados)):
            raise ValueError("Objetivo personalizado duplicado")

    def adicionar_marketing(
        self,
        objetivo: ObjetivoMarketingDeclarado,
    ) -> "ObjetivosDeclarados":
        return ObjetivosDeclarados(self.marketing + (objetivo,), self.comunicacao)

    def adicionar_comunicacao(
        self,
        objetivo: ObjetivoComunicacaoDeclarado,
    ) -> "ObjetivosDeclarados":
        return ObjetivosDeclarados(self.marketing, self.comunicacao + (objetivo,))

    def remover_marketing(self, id_objetivo: UUID) -> "ObjetivosDeclarados":
        if not any(item.id_objetivo == id_objetivo for item in self.marketing):
            raise LookupError("Objetivo de Marketing não encontrado")
        if any(
            id_objetivo in item.ids_objetivos_marketing_relacionados
            for item in self.comunicacao
        ):
            raise ValueError(
                "Objetivo de Marketing está vinculado a Objetivos de Comunicação"
            )
        restantes = tuple(
            item for item in self.marketing if item.id_objetivo != id_objetivo
        )
        return ObjetivosDeclarados(restantes, self.comunicacao)

    def remover_comunicacao(self, id_objetivo: UUID) -> "ObjetivosDeclarados":
        if not any(item.id_objetivo == id_objetivo for item in self.comunicacao):
            raise LookupError("Objetivo de Comunicação não encontrado")
        restantes = tuple(
            item for item in self.comunicacao if item.id_objetivo != id_objetivo
        )
        return ObjetivosDeclarados(self.marketing, restantes)
