"""Composição contextual transparente aplicada ao contrato qualitativo."""

from __future__ import annotations

from datetime import date
from typing import Any

from domain.contracts import Confianca
from .models import ContribuicaoRelacao, PenalizacaoRelacao, ReferenciaBibliotecaAplicada


def _texto(valor: Any) -> str:
    return str(valor or "").strip().casefold()


def _prioridade_declarada(briefing, categoria: str, nivel: str, config) -> float | None:
    colecao = (
        briefing.conteudo.objetivos_marketing
        if nivel == "MARKETING"
        else briefing.conteudo.objetivos_comunicacao
    )
    item = next((obj for obj in colecao if _texto(obj.get("categoria")) == _texto(categoria)), None)
    valor = _texto((item or {}).get("prioridade"))
    if not valor:
        candidatos = {
            _texto(categoria), _texto(nivel),
            "objetivos de marketing" if nivel == "MARKETING" else "objetivos de comunicação",
        }
        registro = next((obj for obj in briefing.conteudo.prioridades if _texto(obj.get("entidade")) in candidatos), None)
        valor = _texto((registro or {}).get("nivel"))
    return config["prioridades"].get(valor) if valor else None


def _nivel(valor: Any) -> float | None:
    return {
        "muito baixa": 20.0, "baixa": 35.0, "média": 55.0,
        "media": 55.0, "moderada": 55.0, "alta": 80.0,
        "muito alta": 95.0,
    }.get(_texto(valor))


def _periodo_curto(periodo: dict[str, Any]) -> bool | None:
    try:
        inicio = date.fromisoformat(str(periodo["inicio"]))
        fim = date.fromisoformat(str(periodo["fim"]))
    except (KeyError, TypeError, ValueError):
        return None
    return (fim - inicio).days <= 60


def _restricao_orcamentaria(briefing) -> bool:
    if "ríg" in _texto(briefing.conteudo.verba.get("natureza")):
        return True
    return any("orçament" in _texto(item.get("categoria")) for item in briefing.conteudo.restricoes)


def _fatores_contextuais(briefing, *, origem: str, destino: str, nivel_origem: str):
    situacao = briefing.conteudo.situacao_mercadologica
    fatores: dict[str, tuple[float, str]] = {}
    notoriedade = _nivel(situacao.get("notoriedade") or situacao.get("nivel_notoriedade"))
    if notoriedade is not None:
        favorecidos = {"notoriedade", "construir alcance", "ampliar cobertura", "acelerar construção de alcance"}
        valor = 100.0 - notoriedade if _texto(destino) in favorecidos else notoriedade
        fatores["situacao_mercadologica"] = (valor, f"notoriedade declarada influencia {destino}")
    pressao = _nivel(situacao.get("intensidade_competitiva"))
    if pressao is not None:
        favorecidos = {"gerar frequência", "sustentar continuidade", "produzir impacto"}
        valor = pressao if _texto(destino) in favorecidos else 55.0
        fatores["situacao_competitiva"] = (valor, f"pressão competitiva {_texto(situacao.get('intensidade_competitiva'))}")
    if briefing.conteudo.publicos or briefing.conteudo.segmentos:
        valor = 80.0 if _texto(destino) in {"alcançar públicos prioritários", "aumentar afinidade"} else 60.0
        fatores["publico"] = (valor, "público ou segmento declarado")
    if briefing.conteudo.pracas:
        valor = 80.0 if _texto(destino) in {"ampliar cobertura", "ampliar presença territorial"} else 60.0
        fatores["praca"] = (valor, "praça declarada")
    if briefing.conteudo.jornadas:
        favorecidos = {"gerar frequência", "sustentar continuidade", "acompanhar etapas da jornada"}
        valor = 85.0 if _texto(destino) in favorecidos or _texto(origem) == "lembrança" else 60.0
        fatores["jornada"] = (valor, "jornada declarada")
    curto = _periodo_curto(briefing.conteudo.periodo)
    if curto is not None:
        favorecidos = {"acelerar construção de alcance", "favorecer resposta", "gerar tráfego"}
        fatores["periodo"] = (80.0 if curto and _texto(destino) in favorecidos else 60.0, "período declarado")
    natureza_verba = _texto(briefing.conteudo.verba.get("natureza"))
    if natureza_verba and natureza_verba != "ainda não definido":
        fatores["verba"] = (60.0, "verba disponível, sem inferir viabilidade")
    return fatores


def _compor(forca_padrao, prioridade, fatores, penalizacoes, config):
    entradas = {"forca_padrao": (forca_padrao, "força padrão versionada")}
    if prioridade is not None:
        entradas["prioridade_declarada"] = (prioridade, "prioridade declarada")
    entradas.update(fatores)
    pesos = config["pesos"]
    total = sum(pesos[nome] for nome in entradas)
    contribuicoes = tuple(ContribuicaoRelacao(
        dimensao=nome, valor=valor, peso=pesos[nome] / total,
        contribuicao=valor * pesos[nome] / total, explicacao=explicacao,
    ) for nome, (valor, explicacao) in entradas.items())
    bruto = sum(item.contribuicao for item in contribuicoes)
    desconto = sum(item.valor for item in penalizacoes)
    return round(max(config["escala"][0] + 1.0, min(config["escala"][1], bruto - desconto)), 2), contribuicoes


def _confianca(briefing, fatores) -> tuple[Confianca, str]:
    if briefing.conteudo.fontes:
        return Confianca.ALTA if len(fatores) >= 5 else Confianca.MEDIA, "fontes declaradas e contexto disponível"
    return Confianca.BAIXA, "fontes ausentes reduzem confiança, sem zerar a pontuação"


def _ordenar(avaliacoes, config):
    ordenadas = sorted(avaliacoes, key=lambda item: (-item["pontuacao"], _texto(item["destino"])))
    ordem = 0
    referencia = None
    for indice, item in enumerate(ordenadas, 1):
        empate = referencia is not None and abs(referencia - item["pontuacao"]) <= config["tolerancia_empate"]
        if not empate:
            ordem = indice
            referencia = item["pontuacao"]
        item["ordem"] = ordem
        item["empate"] = empate or (
            indice < len(ordenadas)
            and abs(item["pontuacao"] - ordenadas[indice]["pontuacao"]) <= config["tolerancia_empate"]
        )
    return ordenadas


def aplicar_pontuacao(contrato, briefing, catalogo):
    config = catalogo.configuracao_pontuacao
    avaliacoes = []
    for relacao in contrato.relacoes_estrategicas:
        if relacao.destino_nivel == "COMUNICACAO":
            forca = config["forca_padrao_marketing_comunicacao"]
            prioridade = _prioridade_declarada(briefing, relacao.origem, "MARKETING", config)
        else:
            chave = f"{_texto(relacao.origem)}|{_texto(relacao.destino)}"
            forca = config["forca_padrao_comunicacao_midia"].get(chave, config["forca_padrao_comunicacao_midia_default"])
            prioridade = _prioridade_declarada(briefing, relacao.origem, "COMUNICACAO", config)
        fatores = _fatores_contextuais(briefing, origem=relacao.origem, destino=relacao.destino, nivel_origem=relacao.origem_nivel)
        penalizacoes = ()
        if _restricao_orcamentaria(briefing):
            penalizacoes = (PenalizacaoRelacao(dimensao="restricao_orcamentaria", valor=config["penalizacao_restricao_orcamentaria"], explicacao="verba rígida ou restrição orçamentária declarada; objetivo preservado"),)
        pontuacao, contribuicoes = _compor(forca, prioridade, fatores, penalizacoes, config)
        confianca, motivo_confianca = _confianca(briefing, fatores)
        avaliacoes.append({"relacao": relacao, "destino": relacao.destino, "forca": forca, "pontuacao": pontuacao, "contribuicoes": contribuicoes, "penalizacoes": penalizacoes, "confianca": confianca, "motivo_confianca": motivo_confianca})

    atualizadas = []
    for nivel in ("COMUNICACAO", "MIDIA"):
        grupo = _ordenar([item for item in avaliacoes if item["relacao"].destino_nivel == nivel], config)
        for item in grupo:
            relacao = item["relacao"]
            aumentam = [c.dimensao for c in item["contribuicoes"] if c.valor >= 65]
            reduzem = [p.dimensao for p in item["penalizacoes"]]
            explicacao = f"Pontuação {item['pontuacao']:.2f}; fatores que aumentaram: {', '.join(aumentam) or 'nenhum acima do limiar'}; fatores que reduziram: {', '.join(reduzem) or 'nenhum'}; ordem contextual {item['ordem']}."
            condicao = "EMPATE_TECNICO" if item["empate"] else ("PRIORITARIA" if item["ordem"] == 1 else "COMPLEMENTAR")
            efeito = config["efeitos_arquitetura"].get(_texto(relacao.destino), "orientar a comparação de alternativas na arquitetura posterior")
            atualizadas.append(relacao.model_copy(update={"estado": "PONTUADA", "forca_padrao": item["forca"], "pontuacao_contextual": item["pontuacao"], "ordem_contextual": item["ordem"], "condicao": condicao, "contribuicoes": item["contribuicoes"], "penalizacoes": item["penalizacoes"], "confianca": item["confianca"], "explicacao_decisoria": explicacao + " Confiança: " + item["motivo_confianca"] + ".", "efeito_etapa_seguinte": efeito}))

    relacoes = tuple(sorted(atualizadas, key=lambda item: (0 if item.destino_nivel == "COMUNICACAO" else 1, item.ordem_contextual, _texto(item.destino))))
    por_midia = {item.destino: item for item in relacoes if item.destino_nivel == "MIDIA"}
    derivados_ordenados = sorted(contrato.objetivos_midia_derivados, key=lambda item: (por_midia[item.categoria].ordem_contextual, -por_midia[item.categoria].pontuacao_contextual, _texto(item.categoria)))
    total = sum(por_midia[item.categoria].pontuacao_contextual for item in derivados_ordenados) or 1.0
    derivados = tuple(item.model_copy(update={
        "ordem": por_midia[item.categoria].ordem_contextual,
        "pontuacao_contextual": por_midia[item.categoria].pontuacao_contextual,
        "prioridade_calculada": next(nome for minimo, nome in config["faixas_prioridade_calculada"] if por_midia[item.categoria].pontuacao_contextual >= minimo),
        "peso_calculado": round(por_midia[item.categoria].pontuacao_contextual / total, 6),
        "peso_efetivo": round(por_midia[item.categoria].pontuacao_contextual / total, 6),
        "intensidade_requerida": None,
        "efeito_na_arquitetura": por_midia[item.categoria].efeito_etapa_seguinte,
        "confianca": por_midia[item.categoria].confianca,
        "explicacao_peso": f"Peso normalizado da pontuação contextual {por_midia[item.categoria].pontuacao_contextual:.2f} na composição {config['codigo']}@{config['versao']}; intensidade quantitativa e meta permanecem pendentes.",
    }) for item in derivados_ordenados)

    pontuacao_comunicacao = {}
    for item in relacoes:
        if item.destino_nivel == "COMUNICACAO":
            pontuacao_comunicacao[item.destino] = max(pontuacao_comunicacao.get(item.destino, 0.0), item.pontuacao_contextual)
    marketing = [item for item in contrato.objetivos_declarados if item.nivel == "MARKETING"]
    comunicacao = [item for item in contrato.objetivos_declarados if item.nivel == "COMUNICACAO"]
    comunicacao.sort(key=lambda item: (-pontuacao_comunicacao.get(item.categoria, 1.0), _texto(item.categoria)))
    declarados = tuple(marketing + [item.model_copy(update={"pontuacao_contextual": pontuacao_comunicacao.get(item.categoria), "ordem_contextual": indice, "prioridade_calculada": next((nome for minimo, nome in config["faixas_prioridade_calculada"] if pontuacao_comunicacao.get(item.categoria, 1.0) >= minimo), "MUITO_BAIXA"), "explicacao_decisoria": f"Ordem calculada pela maior relação Marketing–Comunicação na composição {config['codigo']}@{config['versao']}."}) for indice, item in enumerate(comunicacao, 1)])
    criterios = tuple(item.model_copy(update={"prioridade": next((objetivo.prioridade_calculada for objetivo in derivados if objetivo.categoria in item.criterio), item.prioridade)}) for item in contrato.criterios_arquitetura)
    referencias = contrato.referencias_bibliotecas + (ReferenciaBibliotecaAplicada(biblioteca=17, codigo=config["codigo"], versao=config["versao"]),)
    return contrato.model_copy(update={"objetivos_declarados": declarados, "objetivos_midia_derivados": derivados, "relacoes_estrategicas": relacoes, "criterios_arquitetura": criterios, "versao_composicao": config["versao"], "referencias_bibliotecas": referencias})
