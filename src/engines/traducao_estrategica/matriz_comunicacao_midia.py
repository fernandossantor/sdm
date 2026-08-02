from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from src.domain.objetivos import Prioridade
from src.knowledge.loader import carregar_conhecimento


@dataclass(frozen=True, slots=True)
class ObjetivoComunicacaoPriorizado:
    codigo: str
    ordem: int
    forca_contextual: float
    prioridade: Prioridade
    confianca: float


@dataclass(frozen=True, slots=True)
class AdequacaoObjetivoMidia:
    codigo_objetivo_midia: str
    publico: float
    praca: float
    jornada: float
    periodo: float


@dataclass(frozen=True, slots=True)
class ContextoDerivacaoMidia:
    objetivos_comunicacao: tuple[ObjetivoComunicacaoPriorizado, ...]
    publico: str
    praca: str
    jornada: str
    periodo: str
    verba: str
    intensidade_restricao_orcamentaria: float
    restricoes: tuple[str, ...]
    adequacoes: tuple[AdequacaoObjetivoMidia, ...] = ()


@dataclass(frozen=True, slots=True)
class ComponenteAdequacao:
    dimensao: str
    valor: float
    peso: float
    contribuicao: float


@dataclass(frozen=True, slots=True)
class RastroRelacao:
    codigo_relacao: str
    versao_relacao: str
    objetivo_comunicacao: str
    objetivo_midia: str
    fonte_documental_interna: str


@dataclass(frozen=True, slots=True)
class ObjetivoMidiaDerivado:
    codigo: str
    nome: str
    adequacao_contextual: float
    ordem: int
    intensidade: str
    prioridade: str
    peso: float
    condicao: str
    indicadores_possiveis: tuple[str, ...]
    componentes: tuple[ComponenteAdequacao, ...]
    rastreabilidade: tuple[RastroRelacao, ...]
    confianca: float
    alertas: tuple[str, ...]
    versao_configuracao: str


def _ler_json(caminho: Path) -> dict[str, Any]:
    return json.loads(caminho.read_text(encoding="utf-8"))


def _carregar_configuracao(raiz: Path) -> dict[str, Any]:
    configuracao = _ler_json(raiz / "configuracao_matriz_comunicacao_midia.yaml")
    if not configuracao.get("ativo") or not configuracao.get("versao"):
        raise ValueError("configuração deve estar ativa e versionada")
    if abs(sum(configuracao["pesos"].values()) - 1.0) > 1e-9:
        raise ValueError("pesos da derivação devem somar 1,00")
    return configuracao


def _carregar_relacoes(raiz: Path) -> tuple[dict[str, Any], ...]:
    base = carregar_conhecimento(raiz)
    objetivos = {item["codigo"]: item for item in base["objetivos"]}
    indicadores = {item["codigo"]: item for item in base["indicadores"]}
    principais: list[dict[str, Any]] = []
    for relacao in base["relacoes_comunicacao_midia"]:
        destino = objetivos[relacao["destino"]]
        enriquecida = dict(relacao)
        enriquecida["destino_nome"] = destino["nome"]
        enriquecida["indicadores"] = tuple(
            indicadores[codigo]["nome"] for codigo in destino.get("indicadores", ())
        )
        principais.append(enriquecida)
    contrastes = _ler_json(raiz / "relacoes_comunicacao_midia_contrastes.yaml")[
        "registros"
    ]
    relacoes = tuple(principais) + tuple(contrastes)
    codigos: set[str] = set()
    for relacao in relacoes:
        for campo in (
            "codigo",
            "versao",
            "ativo",
            "origem",
            "destino",
            "destino_nome",
            "condicao",
            "faixa_forca_padrao",
            "indicadores",
            "fonte_documental_interna",
        ):
            if campo not in relacao:
                raise ValueError(f"relação sem campo obrigatório {campo}")
        if relacao["codigo"] in codigos:
            raise ValueError(f"relação duplicada {relacao['codigo']}")
        if not relacao["ativo"] or not relacao["versao"]:
            raise ValueError("relações consultadas devem estar ativas e versionadas")
        faixa = relacao["faixa_forca_padrao"]
        if not 0 <= faixa["minimo"] <= faixa["maximo"] <= 100:
            raise ValueError("faixa de força padrão inválida")
        codigos.add(relacao["codigo"])
    return relacoes


def _validar_contexto(contexto: ContextoDerivacaoMidia) -> None:
    if not contexto.objetivos_comunicacao:
        raise ValueError("ao menos um objetivo de Comunicação priorizado é obrigatório")
    if len({item.codigo for item in contexto.objetivos_comunicacao}) != len(
        contexto.objetivos_comunicacao
    ):
        raise ValueError("objetivos de Comunicação devem ter códigos únicos")
    if not 0 <= contexto.intensidade_restricao_orcamentaria <= 100:
        raise ValueError("intensidade da restrição deve estar entre 0 e 100")
    for objetivo in contexto.objetivos_comunicacao:
        if objetivo.ordem < 1:
            raise ValueError("ordem de Comunicação deve ser positiva")
        if not 0 <= objetivo.forca_contextual <= 100 or not 0 <= objetivo.confianca <= 100:
            raise ValueError("força e confiança devem estar entre 0 e 100")
    for adequacao in contexto.adequacoes:
        valores = (adequacao.publico, adequacao.praca, adequacao.jornada, adequacao.periodo)
        if any(valor < 0 or valor > 100 for valor in valores):
            raise ValueError("adequações devem estar entre 0 e 100")


def _intensidade(valor: float, configuracao: dict[str, Any]) -> str:
    for faixa in configuracao["faixas_intensidade"]:
        if valor >= faixa["minimo"]:
            return faixa["nome"]
    raise AssertionError("configuração de intensidade sem cobertura")


def _avaliar_caminho(
    comunicacao: ObjetivoComunicacaoPriorizado,
    relacao: dict[str, Any],
    adequacao: AdequacaoObjetivoMidia | None,
    configuracao: dict[str, Any],
    restricao_orcamentaria: float,
) -> tuple[float, tuple[ComponenteAdequacao, ...], str, tuple[str, ...]]:
    neutro = configuracao["valor_contextual_neutro"]
    valores = {
        "forca_padrao": (
            relacao["faixa_forca_padrao"]["minimo"]
            + relacao["faixa_forca_padrao"]["maximo"]
        )
        / 2,
        "forca_comunicacao": comunicacao.forca_contextual,
        "prioridade_comunicacao": configuracao["prioridades_entrada"][
            comunicacao.prioridade.value
        ],
        "publico": adequacao.publico if adequacao else neutro,
        "praca": adequacao.praca if adequacao else neutro,
        "jornada": adequacao.jornada if adequacao else neutro,
        "periodo": adequacao.periodo if adequacao else neutro,
        "confianca": comunicacao.confianca,
    }
    componentes = tuple(
        ComponenteAdequacao(
            dimensao=dimensao,
            valor=float(valor),
            peso=configuracao["pesos"][dimensao],
            contribuicao=round(valor * configuracao["pesos"][dimensao], 4),
        )
        for dimensao, valor in valores.items()
    )
    pontuacao = sum(item.contribuicao for item in componentes)
    condicao = relacao["condicao"]
    alertas: list[str] = []
    regra_orcamento = configuracao["restricao_orcamentaria"]
    if restricao_orcamentaria >= regra_orcamento["limiar"]:
        pontuacao -= regra_orcamento["penalizacao"]
        condicao = regra_orcamento["condicao_resultante"]
        alertas.extend(
            (
                "restrição orçamentária reduziu a adequação do piloto",
                "viabilidade econômica não foi determinada",
            )
        )
    return max(0.0, round(pontuacao, 2)), componentes, condicao, tuple(alertas)


def derivar_objetivos_midia(
    contexto: ContextoDerivacaoMidia,
    diretorio_conhecimento: str | Path | None = None,
) -> tuple[ObjetivoMidiaDerivado, ...]:
    """Deriva objetivos de Mídia sem selecionar mídia ou calcular plano."""
    _validar_contexto(contexto)
    raiz = (
        Path(diretorio_conhecimento)
        if diretorio_conhecimento is not None
        else Path(__file__).parents[2] / "knowledge"
    )
    configuracao = _carregar_configuracao(raiz)
    relacoes = _carregar_relacoes(raiz)
    adequacoes = {item.codigo_objetivo_midia: item for item in contexto.adequacoes}
    por_destino: dict[str, list[tuple[Any, ...]]] = {}
    for comunicacao in contexto.objetivos_comunicacao:
        aplicaveis = [item for item in relacoes if item["origem"] == comunicacao.codigo]
        for relacao in aplicaveis:
            avaliacao = _avaliar_caminho(
                comunicacao,
                relacao,
                adequacoes.get(relacao["destino"]),
                configuracao,
                contexto.intensidade_restricao_orcamentaria,
            )
            por_destino.setdefault(relacao["destino"], []).append(
                (comunicacao, relacao, *avaliacao)
            )

    candidatos: list[ObjetivoMidiaDerivado] = []
    for codigo, caminhos in por_destino.items():
        melhor = max(caminhos, key=lambda item: item[2])
        comunicacao, relacao, pontuacao, componentes, condicao, alertas = melhor
        rastros = tuple(
            RastroRelacao(
                codigo_relacao=item[1]["codigo"],
                versao_relacao=item[1]["versao"],
                objetivo_comunicacao=item[0].codigo,
                objetivo_midia=codigo,
                fonte_documental_interna=item[1]["fonte_documental_interna"],
            )
            for item in caminhos
        )
        indicadores = tuple(
            dict.fromkeys(indicador for item in caminhos for indicador in item[1]["indicadores"])
        )
        candidatos.append(
            ObjetivoMidiaDerivado(
                codigo=codigo,
                nome=relacao["destino_nome"],
                adequacao_contextual=pontuacao,
                ordem=0,
                intensidade=_intensidade(pontuacao, configuracao),
                prioridade="",
                peso=0.0,
                condicao=condicao,
                indicadores_possiveis=indicadores,
                componentes=componentes,
                rastreabilidade=rastros,
                confianca=min(item[0].confianca for item in caminhos),
                alertas=alertas,
                versao_configuracao=configuracao["versao"],
            )
        )

    candidatos.sort(key=lambda item: (-item.adequacao_contextual, item.codigo))
    total = sum(item.adequacao_contextual for item in candidatos)
    prioridades = configuracao["prioridade_por_ordem"]
    return tuple(
        replace(
            item,
            ordem=ordem,
            prioridade=prioridades.get(str(ordem), prioridades["demais"]),
            peso=round(item.adequacao_contextual / total, 6) if total else 0.0,
        )
        for ordem, item in enumerate(candidatos, 1)
    )
