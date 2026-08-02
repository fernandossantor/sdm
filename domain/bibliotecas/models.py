"""Objetos mínimos, tipados e versionados das Bibliotecas 15, 17 e 18."""

from pydantic import BaseModel, ConfigDict


class ObjetoBiblioteca(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    codigo: str
    biblioteca: int
    versao: str
    status: str = "ATIVO"


class IndicadorPlanejamento(ObjetoBiblioteca):
    nome: str
    familia: str
    unidade: str
    pode_receber_meta: bool = True


class RegraComunicacaoMidia(ObjetoBiblioteca):
    objetivo_comunicacao: str
    objetivos_midia: tuple[str, ...]
    indicadores: tuple[str, ...]
    conhecimento_aplicado: str
    problema_atendido: str


class ConhecimentoTecnico(ObjetoBiblioteca):
    nome: str
    tipo: str
    pre_condicoes: tuple[str, ...]
    limitacoes: tuple[str, ...]


class ProblemaTecnico(ObjetoBiblioteca):
    nome: str
    pergunta_orientadora: str
    objetivo_decisorio: str
    conhecimentos_aplicaveis: tuple[str, ...]
    criterios_conclusao: tuple[str, ...]
