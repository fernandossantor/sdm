from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ARQUIVOS = {
    "objetivos": "objetivos.yaml",
    "relacoes_marketing_comunicacao": "relacoes_marketing_comunicacao.yaml",
    "relacoes_comunicacao_midia": "relacoes_comunicacao_midia.yaml",
    "indicadores": "indicadores.yaml",
}

TIPOS_RELACAO = {
    "CONTRIBUI_PARA", "SUSTENTA", "POTENCIALIZA", "HABILITA", "COMPLEMENTA",
    "ANTECEDE", "DEPENDE_DE", "COMPENSA", "DISPUTA_RECURSO_COM",
    "PODE_CONFLITAR_COM", "INCOMPATIVEL_NO_CONTEXTO",
}
DIRECOES = {"POSITIVA", "NEGATIVA", "NEUTRA", "CONDICIONAL"}
CONDICOES = {
    "ESSENCIAL", "PRIORITARIA", "COMPLEMENTAR", "OPCIONAL", "COMPENSAVEL",
    "CONFLITANTE", "EXCLUDENTE",
}
FAIXAS_FORCA = {
    (0, 19): "MUITO_FRACA", (20, 39): "FRACA", (40, 59): "MODERADA",
    (60, 79): "FORTE", (80, 100): "MUITO_FORTE",
}


class ErroConhecimento(ValueError):
    pass


def _ler_registros(caminho: Path) -> tuple[dict[str, Any], ...]:
    try:
        documento = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erro:
        raise ErroConhecimento(f"não foi possível carregar {caminho.name}: {erro}") from erro
    if not isinstance(documento, dict) or not isinstance(documento.get("registros"), list):
        raise ErroConhecimento(f"{caminho.name}: registros deve ser uma lista")
    if not all(isinstance(registro, dict) for registro in documento["registros"]):
        raise ErroConhecimento(f"{caminho.name}: cada registro deve ser um objeto")
    return tuple(documento["registros"])


def _validar_campos_comuns(registro: dict[str, Any], arquivo: str) -> None:
    campos_texto = ("codigo", "nome", "descricao", "versao", "fonte_documental_interna")
    for campo in (*campos_texto, "ativo"):
        if campo not in registro:
            raise ErroConhecimento(f"{arquivo}: registro sem campo obrigatório {campo}")
    for campo in campos_texto:
        if not isinstance(registro[campo], str) or not registro[campo].strip():
            raise ErroConhecimento(f"{arquivo}: {campo} deve ser texto não vazio")
    if not isinstance(registro["ativo"], bool):
        raise ErroConhecimento(f"{arquivo}: ativo deve ser booleano")


def _validar_relacao(relacao, arquivo, objetivos, nivel_origem, nivel_destino):
    for campo in ("origem", "destino", "tipo_relacao", "direcao", "condicao", "faixa_forca_padrao"):
        if campo not in relacao:
            raise ErroConhecimento(f"{arquivo}: relação sem campo {campo}")
    origem, destino = relacao["origem"], relacao["destino"]
    if origem not in objetivos:
        raise ErroConhecimento(f"{arquivo}: referência inexistente {origem}")
    if destino not in objetivos:
        raise ErroConhecimento(f"{arquivo}: referência inexistente {destino}")
    if objetivos[origem].get("nivel") != nivel_origem or objetivos[destino].get("nivel") != nivel_destino:
        raise ErroConhecimento(f"{arquivo}: relação inválida entre {origem} e {destino}")
    if relacao["tipo_relacao"] not in TIPOS_RELACAO:
        raise ErroConhecimento(f"{arquivo}: tipo de relação inválido")
    if relacao["direcao"] not in DIRECOES:
        raise ErroConhecimento(f"{arquivo}: direção inválida")
    if relacao["condicao"] not in CONDICOES:
        raise ErroConhecimento(f"{arquivo}: condição inválida")
    faixa = relacao["faixa_forca_padrao"]
    if not isinstance(faixa, dict):
        raise ErroConhecimento(f"{arquivo}: faixa de força inválida")
    limites = (faixa.get("minimo"), faixa.get("maximo"))
    if limites not in FAIXAS_FORCA or faixa.get("classe") != FAIXAS_FORCA[limites]:
        raise ErroConhecimento(f"{arquivo}: faixa de força inválida")


def carregar_conhecimento(diretorio: str | Path | None = None) -> dict[str, tuple[dict[str, Any], ...]]:
    """Carrega e valida somente os quatro arquivos da base mínima."""
    raiz = Path(diretorio) if diretorio is not None else Path(__file__).parent
    base = {nome: _ler_registros(raiz / arquivo) for nome, arquivo in ARQUIVOS.items()}
    codigos: dict[str, str] = {}
    for arquivo, registros in base.items():
        for registro in registros:
            _validar_campos_comuns(registro, arquivo)
            codigo = registro["codigo"]
            if codigo in codigos:
                raise ErroConhecimento(f"código duplicado {codigo} em {codigos[codigo]} e {arquivo}")
            codigos[codigo] = arquivo

    objetivos = {registro["codigo"]: registro for registro in base["objetivos"]}
    indicadores = {registro["codigo"]: registro for registro in base["indicadores"]}
    for objetivo in objetivos.values():
        if objetivo.get("nivel") not in {"MARKETING", "COMUNICACAO", "MIDIA"}:
            raise ErroConhecimento("objetivos: nível inválido")
        for codigo in objetivo.get("indicadores", ()):
            if codigo not in indicadores:
                raise ErroConhecimento(f"objetivos: referência inexistente {codigo}")
    for indicador in indicadores.values():
        if not isinstance(indicador.get("relacoes"), list):
            raise ErroConhecimento("indicadores: relações deve ser uma lista")
        for codigo in indicador["relacoes"]:
            if codigo not in objetivos:
                raise ErroConhecimento(f"indicadores: referência inexistente {codigo}")

    for relacao in base["relacoes_marketing_comunicacao"]:
        _validar_relacao(relacao, "relacoes_marketing_comunicacao", objetivos, "MARKETING", "COMUNICACAO")
    for relacao in base["relacoes_comunicacao_midia"]:
        _validar_relacao(relacao, "relacoes_comunicacao_midia", objetivos, "COMUNICACAO", "MIDIA")
    return base
