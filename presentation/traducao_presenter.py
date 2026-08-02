"""Presenter do apoio decisório da Tradução Estratégica persistida."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


AJUDAS = {
    "prioridade_declarada": "Importância informada no briefing; orienta a tradução, mas não é o resultado calculado.",
    "forca_padrao": "Referência inicial da relação, fornecida pela biblioteca versionada.",
    "pontuacao_contextual": "Adequação calculada pelo motor com os fatores disponíveis no contexto.",
    "peso_calculado": "Participação relativa produzida pelo motor antes de qualquer revisão humana.",
    "peso_ajustado": "Valor proposto pelo planejador; quando ausente, o calculado permanece válido.",
    "peso_efetivo": "Valor realmente utilizado: o ajustado, quando autorizado, ou o calculado.",
    "confianca": "Qualidade das fontes e suficiência do contexto; não substitui a pontuação.",
    "condicao": "Papel do resultado na decisão: prioritário, complementar ou empate técnico.",
    "restricao": "Limite declarado que a decisão posterior deve respeitar.",
    "tensao": "Conflito que exige conciliação ou escolha consciente do planejador.",
    "efeito_arquitetura": "Decisão que o futuro Motor de Arquitetura deverá considerar, sem escolher canais aqui.",
}


@dataclass(frozen=True, slots=True)
class ItemContexto:
    titulo: str
    valor: str
    explicacao: str
    origem: str = "Informado pelo usuário"


@dataclass(frozen=True, slots=True)
class ObjetivoDecisorio:
    nivel: str
    nome: str
    prioridade: str
    peso_efetivo: str
    ordem: str
    origem_peso: str
    forca_padrao: str
    pontuacao_contextual: str
    peso_calculado: str
    peso_ajustado: str
    fatores_positivos: tuple[str, ...]
    fatores_negativos: tuple[str, ...]
    confianca: str
    condicao: str
    empate_tecnico: bool
    efeito_arquitetura: str
    explicacao: str


@dataclass(frozen=True, slots=True)
class SinteseDecisoria:
    principal: str
    secundarias: tuple[str, ...]
    tensao: str
    confianca: str


@dataclass(frozen=True, slots=True)
class ConsequenciasPlanejamento:
    priorizar: tuple[str, ...]
    obrigatorias: tuple[str, ...]
    complementares: tuple[str, ...]
    tensoes: tuple[str, ...]
    dados_faltantes: tuple[str, ...]
    nao_concluido: tuple[str, ...]
    decisoes_humanas: tuple[str, ...]


def _texto_lista(itens, campo: str, vazio: str = "Não informado") -> str:
    valores = [str(item.get(campo, "")).strip() for item in itens]
    return ", ".join(item for item in valores if item) or vazio


def _dinheiro(verba: dict[str, Any]) -> str:
    valor = verba.get("valor_total")
    if valor in (None, "") or verba.get("natureza") == "ainda não definido":
        return "Pendente"
    moeda = verba.get("moeda") or "BRL"
    return f"{moeda} {Decimal(str(valor)):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _periodo(periodo: dict[str, Any]) -> str:
    inicio, fim = periodo.get("inicio"), periodo.get("fim")
    return f"{inicio} a {fim}" if inicio and fim else "Pendente"


def apresentar_contexto(briefing) -> tuple[ItemContexto, ...]:
    conteudo = briefing.conteudo
    situacao = "; ".join(
        f"{str(chave).replace('_', ' ').title()}: {valor}"
        for chave, valor in conteudo.situacao_mercadologica.items()
        if valor not in (None, "")
    ) or "Não informada"
    restricoes = _texto_lista(conteudo.restricoes, "categoria", "Nenhuma declarada")
    if conteudo.sem_restricoes_declaradas:
        restricoes = "Nenhuma restrição declarada"
    return (
        ItemContexto("Objetivos de Marketing", _texto_lista(conteudo.objetivos_marketing, "categoria"), "Resultados de negócio pretendidos; orientam quais mudanças de comunicação devem receber prioridade."),
        ItemContexto("Objetivos de Comunicação", _texto_lista(conteudo.objetivos_comunicacao, "categoria"), "Mudanças esperadas na relação com o público; originam os objetivos de mídia."),
        ItemContexto("Situação mercadológica", situacao, "Condições da marca, mercado e concorrência que podem elevar ou reduzir adequações."),
        ItemContexto("Público prioritário", _texto_lista(conteudo.publicos, "nome"), "Grupo que deve orientar alcance, afinidade e seletividade."),
        ItemContexto("Praça", _texto_lista(conteudo.pracas, "nome"), "Território no qual cobertura e presença precisam ser avaliadas."),
        ItemContexto("Período", _periodo(conteudo.periodo), "Horizonte disponível; pode influenciar velocidade e continuidade necessárias."),
        ItemContexto("Verba", _dinheiro(conteudo.verba), "Limite financeiro informado; condiciona prioridades sem provar viabilidade."),
        ItemContexto("Prioridades declaradas", _texto_lista(conteudo.prioridades, "nivel"), AJUDAS["prioridade_declarada"]),
        ItemContexto("Restrições", restricoes, AJUDAS["restricao"]),
    )


def formatar_peso(valor: float | None) -> str:
    return "Pendente" if valor is None else f"{valor * 100:.1f}%".replace(".", ",")


def formatar_pontuacao(valor: float | None) -> str:
    return "Pendente" if valor is None else f"{valor:.1f}/100".replace(".", ",")


def _origem_peso(objetivo) -> str:
    if getattr(objetivo, "peso_ajustado", None) is not None:
        return "Ajustado pelo planejador; calculado preservado"
    if getattr(objetivo, "peso_calculado", None) is not None:
        return "Calculado pelo motor"
    return "Não produzido neste nível do contrato"


def _relacao_por_destino(contrato, nivel: str) -> dict[str, Any]:
    relacoes = [
        item for item in contrato.relacoes_estrategicas
        if item.destino_nivel == nivel
    ]
    resultado = {}
    for item in relacoes:
        atual = resultado.get(item.destino)
        if atual is None or (item.pontuacao_contextual or -1) > (atual.pontuacao_contextual or -1):
            resultado[item.destino] = item
    return resultado


def _objetivo_apresentado(nivel: str, objetivo, relacao=None) -> ObjetivoDecisorio:
    peso_efetivo = getattr(objetivo, "peso_efetivo", None)
    peso_calculado = getattr(objetivo, "peso_calculado", None)
    peso_ajustado = getattr(objetivo, "peso_ajustado", None)
    condicao = getattr(relacao, "condicao", None) or "Não determinada"
    positivos = tuple(item.explicacao for item in getattr(relacao, "contribuicoes", ()))
    negativos = tuple(item.explicacao for item in getattr(relacao, "penalizacoes", ()))
    confianca = getattr(objetivo, "confianca", None) or getattr(relacao, "confianca", None)
    efeito = getattr(objetivo, "efeito_na_arquitetura", None) or getattr(relacao, "efeito_etapa_seguinte", None)
    explicacao = getattr(objetivo, "explicacao_peso", None) or getattr(relacao, "explicacao_decisoria", None)
    return ObjetivoDecisorio(
        nivel=nivel,
        nome=objetivo.categoria,
        prioridade=(getattr(objetivo, "prioridade_calculada", None) or "Pendente").replace("_", " ").title(),
        peso_efetivo=formatar_peso(peso_efetivo),
        ordem=str(getattr(objetivo, "ordem", None) or getattr(objetivo, "ordem_contextual", None) or "Pendente"),
        origem_peso=_origem_peso(objetivo),
        forca_padrao=formatar_pontuacao(getattr(relacao, "forca_padrao", None)),
        pontuacao_contextual=formatar_pontuacao(getattr(objetivo, "pontuacao_contextual", None) or getattr(relacao, "pontuacao_contextual", None)),
        peso_calculado=formatar_peso(peso_calculado),
        peso_ajustado=formatar_peso(peso_ajustado),
        fatores_positivos=positivos or ("Nenhum fator favorável detalhado nesta versão.",),
        fatores_negativos=negativos or ("Nenhuma penalização aplicada.",),
        confianca=(confianca.value.title() if confianca else "Pendente"),
        condicao=condicao.replace("_", " ").title(),
        empate_tecnico=condicao == "EMPATE_TECNICO",
        efeito_arquitetura=efeito or "Efeito ainda não determinado para a Arquitetura de Mídia.",
        explicacao=explicacao or "Esta versão não registrou explicação decisória detalhada.",
    )


def apresentar_objetivos(contrato):
    relacoes_comunicacao = _relacao_por_destino(contrato, "COMUNICACAO")
    relacoes_midia = _relacao_por_destino(contrato, "MIDIA")
    comunicacao = tuple(
        _objetivo_apresentado("Comunicação", item, relacoes_comunicacao.get(item.categoria))
        for item in contrato.objetivos_declarados if item.nivel == "COMUNICACAO"
    )
    midia = tuple(
        _objetivo_apresentado("Mídia", item, relacoes_midia.get(item.categoria))
        for item in contrato.objetivos_midia_derivados
    )
    return comunicacao, midia


def apresentar_sintese(contrato, midia: tuple[ObjetivoDecisorio, ...]) -> SinteseDecisoria:
    principal = midia[0].nome if midia else "Não determinada"
    secundarias = tuple(item.nome for item in midia[1:3])
    tensao = contrato.tensoes[0].tensao if contrato.tensoes else "Nenhuma tensão crítica identificada"
    return SinteseDecisoria(principal, secundarias, tensao, contrato.confianca.value.title())


def apresentar_consequencias(contrato, midia: tuple[ObjetivoDecisorio, ...]) -> ConsequenciasPlanejamento:
    obrigatorias = tuple(item.criterio for item in contrato.criterios_arquitetura if item.limita_decisoes)
    complementares = tuple(item.nome for item in midia if item.condicao == "Complementar")
    pendencias_mensuracao = tuple(
        f"{item.objetivo_midia}: {item.estado_mensuracao.replace('_', ' ').lower()}"
        for item in contrato.resultados_indicadores
        if "PENDENTE" in item.estado_mensuracao
    )
    intensidade_pendente = tuple(
        f"Intensidade quantitativa de {item.categoria}"
        for item in contrato.objetivos_midia_derivados
        if item.intensidade_requerida is None
    )
    decisoes = ["Confirmar ou revisar os objetivos efetivamente adotados, sempre com justificativa."]
    if any(item.empate_tecnico for item in midia):
        decisoes.append("Resolver conscientemente os empates técnicos quando a Arquitetura exigir escolha.")
    if contrato.lacunas:
        decisoes.append("Complementar os dados ausentes ou aceitar formalmente as ressalvas.")
    return ConsequenciasPlanejamento(
        priorizar=tuple(item.efeito_arquitetura for item in midia[:3]),
        obrigatorias=obrigatorias or ("Nenhuma condição obrigatória adicional registrada.",),
        complementares=complementares or ("Nenhum elemento classificado como complementar.",),
        tensoes=tuple(item.tensao for item in contrato.tensoes) or ("Nenhuma tensão crítica identificada.",),
        dados_faltantes=contrato.lacunas or ("Nenhuma lacuna adicional registrada.",),
        nao_concluido=pendencias_mensuracao + intensidade_pendente or ("Nenhuma pendência técnica registrada.",),
        decisoes_humanas=tuple(decisoes),
    )


def apresentar_revisao(contrato, categorias_propostas: tuple[str, ...]):
    efetivas = {
        item.categoria for item in contrato.objetivos_midia_derivados
        if not any(inter.objetivo_midia == item.categoria and inter.valor_efetivo == "REJEITADO" for inter in contrato.intervencoes_humanas)
    }
    propostas = set(categorias_propostas)
    linhas = []
    for item in contrato.objetivos_midia_derivados:
        antes = "Adotado" if item.categoria in efetivas else "Não adotado"
        depois = "Adotar" if item.categoria in propostas else "Não adotar"
        mantem = (item.categoria in efetivas) == (item.categoria in propostas)
        efeito = (
            "Preserva a orientação calculada"
            if mantem else "Altera o conjunto efetivo e gera nova versão"
        )
        linhas.append({"Objetivo": item.categoria, "Valor calculado": formatar_peso(item.peso_calculado), "Valor efetivo atual": formatar_peso(item.peso_efetivo), "Novo valor proposto": depois, "Efeito estimado": efeito})
    return tuple(linhas)
