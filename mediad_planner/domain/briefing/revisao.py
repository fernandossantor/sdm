"""Avaliação parcial e somente de leitura, conforme 02_BRIEFING, §§ 7–20.

Os apontamentos não certificam suficiência nem autorizam conclusão. Regras
interpretativas e reconhecimento de pendências ainda não integram esta entrega.
"""

from dataclasses import dataclass
from uuid import UUID

from mediad_planner.domain.briefing.entidades import Briefing


@dataclass(frozen=True, slots=True)
class ApontamentoRevisao:
    subetapa: str
    mensagem: str
    referencia_normativa: str
    id_entidade: UUID | None = None


def avaliar_briefing(briefing: Briefing) -> tuple[ApontamentoRevisao, ...]:
    apontamentos: list[ApontamentoRevisao] = []

    def registrar(subetapa, mensagem, secao, id_entidade=None):
        apontamentos.append(ApontamentoRevisao(
            subetapa, mensagem, f"02_BRIEFING.md § {secao}", id_entidade,
        ))

    situacao = "Situação mercadológica e competitiva"
    registros = briefing.situacao_mercadologica.registros
    if not registros:
        registrar(situacao, "Situação mercadológica e competitiva ainda não registrada.", "20")
    for item in registros:
        if not item.fonte:
            registrar(situacao, f"{item.aspecto}: fonte não informada.", "7.5", item.id_registro)
        if not item.periodo_referencia:
            registrar(situacao, f"{item.aspecto}: período de referência não informado.", "7.5", item.id_registro)

    objetivos = briefing.objetivos_declarados
    if not objetivos.marketing:
        registrar("Objetivos declarados", "Nenhum objetivo de marketing registrado.", "20")
    if not objetivos.comunicacao:
        registrar("Objetivos declarados", "Nenhum objetivo de comunicação registrado.", "20")
    for item in objetivos.comunicacao:
        if not item.ids_objetivos_marketing_relacionados:
            registrar("Objetivos declarados", f"{item.objetivo}: sem relação explícita com objetivo de marketing.", "8.4", item.id_objetivo)

    estrutura = briefing.estrutura_territorial_populacional
    if not estrutura.pracas:
        registrar("Praça e universo", "Nenhuma praça registrada.", "20")
    if not estrutura.universos:
        registrar("Praça e universo", "Nenhum universo registrado.", "20")
    pracas_com_universo = {id_praca for item in estrutura.universos for id_praca in item.ids_pracas}
    for item in estrutura.pracas:
        if item.id_praca not in pracas_com_universo:
            registrar("Praça e universo", f"{item.nome}: praça sem universo correspondente.", "9.7", item.id_praca)
        if item.valor_populacao_referencia is not None:
            if not item.fonte:
                registrar("Praça e universo", f"{item.nome}: população de referência sem fonte.", "20", item.id_praca)
            if not item.data_referencia:
                registrar("Praça e universo", f"{item.nome}: população sem data de referência.", "16", item.id_praca)
    for item in estrutura.universos:
        if not item.fonte:
            registrar("Praça e universo", f"{item.nome}: universo sem fonte.", "9.7", item.id_universo)
        if item.valor_populacional is not None and not item.data_referencia:
            registrar("Praça e universo", f"{item.nome}: população sem data de referência.", "16", item.id_universo)
    if not estrutura.publicos:
        registrar("Segmentos e públicos", "Nenhum público registrado com vínculo a segmento e universo.", "20")
    for item in estrutura.segmentos:
        if item.tamanho_estimado is not None:
            if not item.fonte:
                registrar("Segmentos e públicos", f"{item.definicao}: tamanho estimado sem fonte.", "20", item.id_segmento)
            if not item.data_referencia:
                registrar("Segmentos e públicos", f"{item.definicao}: tamanho estimado sem data de referência.", "16", item.id_segmento)
    for item in estrutura.publicos:
        if len(estrutura.publicos) > 1 and item.prioridade is None:
            registrar("Segmentos e públicos", f"{item.nome or 'Público'}: prioridade não informada entre múltiplos públicos.", "9.7", item.id_publico)

    publicos_com_jornada = {id_publico for item in briefing.jornadas for id_publico in item.ids_publicos}
    for item in estrutura.publicos:
        if item.id_publico not in publicos_com_jornada and item.jornada_aplicavel is not False:
            motivo = (
                "jornada declarada aplicável, mas ainda sem vínculo."
                if item.jornada_aplicavel is True
                else "sem jornada vinculada; verificar se a jornada é aplicável."
            )
            registrar("Jornada", f"{item.nome or 'Público'}: {motivo}", "10.4", item.id_publico)
    for jornada in briefing.jornadas:
        for etapa in jornada.etapas:
            if not etapa.ids_objetivos_comunicacao:
                registrar("Jornada", f"{jornada.nome}, etapa {etapa.categoria.value.lower()}: sem relação com objetivo de comunicação.", "10.4", etapa.id_etapa)

    if briefing.contexto_periodo_verba is None:
        registrar("Período e verba", "Período pretendido ainda não registrado.", "20")
        registrar("Período e verba", "Informe a verba ou declare explicitamente que ainda não está definida.", "20")
    else:
        for mensagem in briefing.contexto_periodo_verba.diagnosticos():
            registrar("Período e verba", mensagem, "11–12")

    condicoes = "Prioridades, restrições e pretensões"
    if not briefing.restricoes and not briefing.restricoes_inexistentes_declaradas:
        registrar(condicoes, "Nenhuma restrição registrada; a ausência de registros não declara inexistência de restrições.", "20")
    for item in briefing.restricoes:
        for mensagem in item.diagnosticos():
            registrar(condicoes, f"{item.descricao}: {mensagem}", "14.4", item.id_restricao)
    if not briefing.pretensoes:
        registrar(condicoes, "Nenhuma pretensão declarada registrada.", "20")
    return tuple(apontamentos)
