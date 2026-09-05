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
        raise TypeError("valor opcional deve ser texto")
    return valor.strip() or None


def _escala(valor: int | None, campo: str) -> None:
    if valor is not None and (type(valor) is not int or not 1 <= valor <= 5):
        raise ValueError(f"{campo} deve estar entre 1 e 5")


class CategoriaEtapaJornada(str, Enum):
    DESCOBERTA = "DESCOBERTA"
    CONHECIMENTO = "CONHECIMENTO"
    CONSIDERACAO = "CONSIDERACAO"
    AVALIACAO = "AVALIACAO"
    DECISAO = "DECISAO"
    COMPRA = "COMPRA"
    EXPERIENCIA = "EXPERIENCIA"
    RECOMPRA = "RECOMPRA"
    FIDELIZACAO = "FIDELIZACAO"
    RECOMENDACAO = "RECOMENDACAO"


ROTULOS_ETAPAS = {
    CategoriaEtapaJornada.DESCOBERTA: "Descoberta",
    CategoriaEtapaJornada.CONHECIMENTO: "Conhecimento",
    CategoriaEtapaJornada.CONSIDERACAO: "Consideração",
    CategoriaEtapaJornada.AVALIACAO: "Avaliação",
    CategoriaEtapaJornada.DECISAO: "Decisão",
    CategoriaEtapaJornada.COMPRA: "Compra",
    CategoriaEtapaJornada.EXPERIENCIA: "Experiência",
    CategoriaEtapaJornada.RECOMPRA: "Recompra",
    CategoriaEtapaJornada.FIDELIZACAO: "Fidelização",
    CategoriaEtapaJornada.RECOMENDACAO: "Recomendação",
}


@dataclass(frozen=True, slots=True)
class EtapaJornadaDeclarada:
    id_etapa: UUID
    categoria: CategoriaEtapaJornada
    ordem: int | None
    existe: bool
    relevancia: int | None
    intensidade: int | None
    prioridade: int | None
    ids_publicos: tuple[UUID, ...]
    ids_objetivos_comunicacao: tuple[UUID, ...]
    situacao_atual: str | None
    situacao_pretendida: str | None
    observacao: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.id_etapa, UUID):
            raise TypeError("id_etapa deve ser UUID")
        if not isinstance(self.categoria, CategoriaEtapaJornada):
            raise TypeError("categoria inválida")
        if self.ordem is not None and (type(self.ordem) is not int or self.ordem <= 0):
            raise ValueError("ordem deve ser inteiro positivo")
        if type(self.existe) is not bool:
            raise TypeError("existe deve ser bool")
        _escala(self.relevancia, "relevancia")
        _escala(self.intensidade, "intensidade")
        _escala(self.prioridade, "prioridade")
        for campo in ("ids_publicos", "ids_objetivos_comunicacao"):
            valores = tuple(getattr(self, campo))
            if any(not isinstance(item, UUID) for item in valores):
                raise TypeError(f"{campo} deve conter UUIDs")
            if len(valores) != len(set(valores)):
                raise ValueError(f"{campo} possui duplicatas")
            object.__setattr__(self, campo, valores)
        if not self.ids_publicos:
            raise ValueError("Etapa deve possuir Público associado")
        for campo in ("situacao_atual", "situacao_pretendida", "observacao"):
            object.__setattr__(self, campo, _opcional(getattr(self, campo)))


@dataclass(frozen=True, slots=True)
class JornadaDeclarada:
    id_jornada: UUID
    nome: str
    descricao: str | None
    ids_publicos: tuple[UUID, ...]
    referencia_modelo: str | None
    adaptada_localmente: bool
    etapas: tuple[EtapaJornadaDeclarada, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.id_jornada, UUID):
            raise TypeError("id_jornada deve ser UUID")
        object.__setattr__(self, "nome", _texto(self.nome, "nome"))
        object.__setattr__(self, "descricao", _opcional(self.descricao))
        object.__setattr__(self, "referencia_modelo", _opcional(self.referencia_modelo))
        if type(self.adaptada_localmente) is not bool:
            raise TypeError("adaptada_localmente deve ser bool")
        publicos = tuple(self.ids_publicos)
        if not publicos:
            raise ValueError("Jornada deve possuir Público associado")
        if any(not isinstance(item, UUID) for item in publicos):
            raise TypeError("ids_publicos deve conter UUIDs")
        if len(publicos) != len(set(publicos)):
            raise ValueError("ids_publicos possui duplicatas")
        etapas = tuple(self.etapas)
        if any(not isinstance(item, EtapaJornadaDeclarada) for item in etapas):
            raise TypeError("etapas contém item inválido")
        if any(not set(item.ids_publicos) <= set(publicos) for item in etapas):
            raise ValueError("Público da Etapa não pertence à Jornada")
        ids = tuple(item.id_etapa for item in etapas)
        if len(ids) != len(set(ids)):
            raise ValueError("IDs de etapa duplicados")
        categorias = tuple(item.categoria for item in etapas)
        if len(categorias) != len(set(categorias)):
            raise ValueError("Categoria de etapa duplicada na Jornada")
        ordens = tuple(item.ordem for item in etapas if item.ordem is not None)
        if len(ordens) != len(set(ordens)):
            raise ValueError("Ordem de etapa duplicada na Jornada")
        object.__setattr__(self, "ids_publicos", publicos)
        object.__setattr__(self, "etapas", etapas)

    def adicionar_etapa(self, etapa: EtapaJornadaDeclarada) -> "JornadaDeclarada":
        return JornadaDeclarada(
            self.id_jornada, self.nome, self.descricao, self.ids_publicos,
            self.referencia_modelo, self.adaptada_localmente, self.etapas + (etapa,),
        )

    def editar_etapa(self, etapa: EtapaJornadaDeclarada) -> "JornadaDeclarada":
        if not any(item.id_etapa == etapa.id_etapa for item in self.etapas):
            raise LookupError("Etapa não encontrada")
        return JornadaDeclarada(
            self.id_jornada, self.nome, self.descricao, self.ids_publicos,
            self.referencia_modelo, self.adaptada_localmente,
            tuple(etapa if item.id_etapa == etapa.id_etapa else item for item in self.etapas),
        )

    def remover_etapa(self, id_etapa: UUID) -> "JornadaDeclarada":
        if not any(item.id_etapa == id_etapa for item in self.etapas):
            raise LookupError("Etapa não encontrada")
        return JornadaDeclarada(
            self.id_jornada, self.nome, self.descricao, self.ids_publicos,
            self.referencia_modelo, self.adaptada_localmente,
            tuple(item for item in self.etapas if item.id_etapa != id_etapa),
        )
