from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Literal, TypeAlias


class EstadoMensurabilidade(str, Enum):
    OPERACIONALIZADO = "OPERACIONALIZADO"
    OPERACIONALIZAVEL_COM_DADOS_PENDENTES = (
        "OPERACIONALIZAVEL_COM_DADOS_PENDENTES"
    )
    OPERACIONALIZAVEL_POR_PROXY = "OPERACIONALIZAVEL_POR_PROXY"
    QUALITATIVO_ESTRUTURADO = "QUALITATIVO_ESTRUTURADO"
    NAO_OPERACIONALIZADO = "NAO_OPERACIONALIZADO"


FormaMensuracao: TypeAlias = Literal[
    "METRICA_DIRETA",
    "INDICE_COMPOSTO",
    "ESCALA_ORDINAL_ESTRUTURADA",
    "PROXY_DECLARADO",
    "CONDICAO_VERIFICAVEL",
]
ValorMensuravel: TypeAlias = int | float | Decimal | str


@dataclass(frozen=True, slots=True)
class ObjetivoDeclarado:
    codigo: str
    texto_original: str
    objeto_da_mudanca: str | None = None
    publico: str | None = None
    praca: str | None = None
    direcao: str | None = None
    indicador: str | None = None
    unidade_ou_escala: str | None = None
    linha_de_base: ValorMensuravel | None = None
    meta_ou_intensidade: ValorMensuravel | None = None
    horizonte_temporal: str | None = None
    fonte: str | None = None
    confianca: str | None = None
    forma_mensuracao: FormaMensuracao | None = None
    proxy_de: str | None = None
    limitacao_do_proxy: str | None = None


@dataclass(frozen=True, slots=True)
class ResultadoMensurabilidade:
    estado: EstadoMensurabilidade
    evidencias: tuple[str, ...]
    dados_presentes: tuple[str, ...]
    dados_ausentes: tuple[str, ...]
    possibilidade_de_pontuacao: bool
    alerta: str | None
    explicacao_curta: str


_CAMPOS_MENSURABILIDADE = (
    "objeto_da_mudanca",
    "publico",
    "praca",
    "direcao",
    "indicador",
    "unidade_ou_escala",
    "linha_de_base",
    "meta_ou_intensidade",
    "horizonte_temporal",
    "fonte",
    "confianca",
)
_FORMAS_QUALITATIVAS = {
    "INDICE_COMPOSTO",
    "ESCALA_ORDINAL_ESTRUTURADA",
    "CONDICAO_VERIFICAVEL",
}


def _presente(valor: object) -> bool:
    if valor is None:
        return False
    if isinstance(valor, str):
        return bool(valor.strip())
    return True


def _inventariar_dados(
    objetivo: ObjetivoDeclarado,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    presentes = tuple(
        campo for campo in _CAMPOS_MENSURABILIDADE if _presente(getattr(objetivo, campo))
    )
    ausentes = tuple(campo for campo in _CAMPOS_MENSURABILIDADE if campo not in presentes)
    return presentes, ausentes


def classificar_mensurabilidade(
    objetivo: ObjetivoDeclarado,
) -> ResultadoMensurabilidade:
    presentes, ausentes = _inventariar_dados(objetivo)
    evidencias = list(presentes)

    if objetivo.forma_mensuracao == "PROXY_DECLARADO":
        proxy_estruturado = all(
            _presente(valor)
            for valor in (
                objetivo.indicador,
                objetivo.unidade_ou_escala,
                objetivo.proxy_de,
                objetivo.limitacao_do_proxy,
            )
        )
        if proxy_estruturado:
            evidencias.extend(("proxy_de", "limitacao_do_proxy"))
            return ResultadoMensurabilidade(
                estado=EstadoMensurabilidade.OPERACIONALIZAVEL_POR_PROXY,
                evidencias=tuple(evidencias),
                dados_presentes=presentes,
                dados_ausentes=ausentes,
                possibilidade_de_pontuacao=True,
                alerta="O proxy não pode ser apresentado como o resultado que representa.",
                explicacao_curta="O objetivo possui proxy declarado e limitação explícita.",
            )

    if objetivo.forma_mensuracao in _FORMAS_QUALITATIVAS and all(
        _presente(valor)
        for valor in (
            objetivo.indicador,
            objetivo.unidade_ou_escala,
            objetivo.meta_ou_intensidade,
        )
    ):
        evidencias.append("forma_mensuracao")
        return ResultadoMensurabilidade(
            estado=EstadoMensurabilidade.QUALITATIVO_ESTRUTURADO,
            evidencias=tuple(evidencias),
            dados_presentes=presentes,
            dados_ausentes=ausentes,
            possibilidade_de_pontuacao=True,
            alerta=None,
            explicacao_curta="O objetivo usa mensuração qualitativa estruturada.",
        )

    campos_diretos_sem_linha_base = (
        "objeto_da_mudanca",
        "publico",
        "praca",
        "direcao",
        "indicador",
        "unidade_ou_escala",
        "meta_ou_intensidade",
        "horizonte_temporal",
        "fonte",
        "confianca",
    )
    metrica_direta_estruturada = objetivo.forma_mensuracao == "METRICA_DIRETA" and all(
        _presente(getattr(objetivo, campo)) for campo in campos_diretos_sem_linha_base
    )
    if metrica_direta_estruturada and _presente(objetivo.linha_de_base):
        evidencias.append("forma_mensuracao")
        return ResultadoMensurabilidade(
            estado=EstadoMensurabilidade.OPERACIONALIZADO,
            evidencias=tuple(evidencias),
            dados_presentes=presentes,
            dados_ausentes=ausentes,
            possibilidade_de_pontuacao=True,
            alerta=None,
            explicacao_curta="O objetivo possui contexto e mensuração direta completos.",
        )

    if objetivo.forma_mensuracao == "METRICA_DIRETA" and _presente(
        objetivo.indicador
    ) and _presente(objetivo.unidade_ou_escala):
        return ResultadoMensurabilidade(
            estado=EstadoMensurabilidade.OPERACIONALIZAVEL_COM_DADOS_PENDENTES,
            evidencias=tuple(evidencias),
            dados_presentes=presentes,
            dados_ausentes=ausentes,
            possibilidade_de_pontuacao=True,
            alerta="Há dados pendentes; a pontuação deve preservar a ressalva.",
            explicacao_curta="A métrica é direta, mas faltam dados declarados.",
        )

    return ResultadoMensurabilidade(
        estado=EstadoMensurabilidade.NAO_OPERACIONALIZADO,
        evidencias=tuple(evidencias),
        dados_presentes=presentes,
        dados_ausentes=ausentes,
        possibilidade_de_pontuacao=False,
        alerta="O objetivo não pode alimentar pontuação sem mensuração estruturada.",
        explicacao_curta="Não há forma de mensuração estruturada suficiente.",
    )
