from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


def _obrigatorio(valor: str, campo: str) -> str:
    valor_normalizado = valor.strip()
    if not valor_normalizado:
        raise ValueError(f"{campo} não pode ser vazio")
    return valor_normalizado


def _opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    return valor.strip() or None


def _congelar_valor(valor: object) -> object:
    if isinstance(valor, Mapping):
        conteudo_congelado = {
            chave: _congelar_valor(valor_interno)
            for chave, valor_interno in valor.items()
        }
        return MappingProxyType(conteudo_congelado)
    if isinstance(valor, (list, tuple)):
        return tuple(_congelar_valor(item) for item in valor)
    if isinstance(valor, (set, frozenset)):
        return frozenset(_congelar_valor(item) for item in valor)
    return valor


@dataclass(frozen=True, slots=True)
class ReferenciaVersionada:
    codigo: str
    versao: str
    tipo: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "codigo", _obrigatorio(self.codigo, "codigo"))
        object.__setattr__(self, "versao", _obrigatorio(self.versao, "versao"))
        object.__setattr__(self, "tipo", _opcional(self.tipo))


@dataclass(frozen=True, slots=True)
class ParametroLocal:
    nome: str
    valor: object
    justificativa: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "nome", _obrigatorio(self.nome, "nome"))
        object.__setattr__(self, "valor", _congelar_valor(self.valor))
        object.__setattr__(self, "justificativa", _opcional(self.justificativa))


@dataclass(frozen=True, slots=True)
class LimitesExecucao:
    tempo_maximo_segundos: int | None = None
    maximo_objetos: int | None = None
    maximo_alternativas: int | None = None
    maximo_iteracoes: int | None = None
    profundidade_maxima: int | None = None

    def __post_init__(self) -> None:
        for campo in self.__dataclass_fields__:
            valor = getattr(self, campo)
            if valor is not None and (type(valor) is not int or valor <= 0):
                raise ValueError(f"{campo} deve ser inteiro maior que zero")
