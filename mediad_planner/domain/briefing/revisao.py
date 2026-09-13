"""Avaliação parcial e somente de leitura, conforme 02_BRIEFING, §§ 7–20.

Os apontamentos não certificam suficiência nem autorizam conclusão. Regras
interpretativas e reconhecimento de pendências ainda não integram esta entrega.
"""

from dataclasses import dataclass
from uuid import UUID

from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.condicoes_declaradas import (
    ROTULOS_PRETENSOES, TipoEntidadePrioridade,
)


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
    for itens, rotulo in (
        (objetivos.marketing, "Objetivos de Marketing"),
        (objetivos.comunicacao, "Objetivos de Comunicação"),
    ):
        _avaliar_prioridades_declaradas(tuple(
            (item.id_objetivo, item.objetivo, item.prioridade_declarada, item.justificativa)
            for item in itens
        ), rotulo, "Objetivos declarados", registrar)
    if not objetivos.marketing:
        registrar("Objetivos declarados", "Nenhum objetivo de marketing registrado.", "20")
    if not objetivos.comunicacao:
        registrar("Objetivos declarados", "Nenhum objetivo de comunicação registrado.", "20")
    for item in objetivos.comunicacao:
        if not item.ids_objetivos_marketing_relacionados:
            registrar("Objetivos declarados", f"{item.objetivo}: sem relação explícita com objetivo de marketing.", "8.4", item.id_objetivo)

    estrutura = briefing.estrutura_territorial_populacional
    objetivos_combinados = objetivos.marketing + objetivos.comunicacao
    publicos_com_objetivo = {
        id_publico
        for item in objetivos_combinados
        for id_publico in item.ids_publicos_relacionados
    }
    for item in objetivos_combinados:
        if item.prioridade_declarada in (4, 5):
            for referencias, rotulo in (
                (item.ids_publicos_relacionados, "público"),
                (item.ids_pracas_relacionadas, "praça"),
            ):
                if not referencias:
                    registrar(
                        "Objetivos declarados",
                        f"{item.objetivo}: objetivo prioritário "
                        f"(prioridade {item.prioridade_declarada}) sem {rotulo} relacionado.",
                        "13.3", item.id_objetivo,
                    )
    for item in estrutura.publicos:
        if item.prioridade in (4, 5) and item.id_publico not in publicos_com_objetivo:
            registrar(
                "Segmentos e públicos",
                f"{item.nome or 'Público'}: público prioritário "
                f"(prioridade {item.prioridade}) sem objetivo relacionado.",
                "13.3", item.id_publico,
            )
    _avaliar_prioridades_declaradas(tuple(
        (item.id_publico, item.nome or "Público", item.prioridade, item.justificativa)
        for item in estrutura.publicos
    ), "Públicos", "Segmentos e públicos", registrar)
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
        prioritarias = tuple(etapa for etapa in jornada.etapas if etapa.prioridade == 5)
        if len(prioritarias) > 1 and any(etapa.ordem is None for etapa in prioritarias):
            registrar(
                "Jornada",
                f"{jornada.nome}: há múltiplas etapas de máxima prioridade (5) "
                "sem ordenação explícita para todas elas.",
                "10.4", jornada.id_jornada,
            )
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
    _avaliar_prioridades_declaradas(tuple(
        (item.id_restricao, item.descricao, item.prioridade, item.justificativa)
        for item in briefing.restricoes
    ), "Restrições", condicoes, registrar)
    _avaliar_prioridades_declaradas(tuple(
        (item.id_pretensao, item.descricao_controlada or ROTULOS_PRETENSOES[item.categoria],
         item.prioridade, item.justificativa)
        for item in briefing.pretensoes
    ), "Pretensões", condicoes, registrar)
    prioridades = briefing.prioridades_contextuais
    if len(prioridades) > 1 and len({item.prioridade for item in prioridades}) == 1:
        registrar(
            condicoes,
            "Todas as prioridades contextuais estão marcadas com o mesmo valor; "
            "a escala não distingue a importância declarada desses itens.",
            "13.3",
        )
    maximas = tuple(item for item in prioridades if item.prioridade == 5)
    if len(maximas) > 1:
        rotulos = {
            (TipoEntidadePrioridade.PRACA, item.id_praca): f"Praça {item.nome}"
            for item in estrutura.pracas
        }
        rotulos.update({
            (TipoEntidadePrioridade.SEGMENTO, item.id_segmento): f"Segmento {item.definicao}"
            for item in estrutura.segmentos
        })
        rotulos[(TipoEntidadePrioridade.PERIODO, None)] = "Período pretendido"
        for item in maximas:
            if not item.justificativa:
                registrar(
                    condicoes,
                    f"{rotulos[(item.tipo_entidade, item.id_entidade)]}: "
                    "prioridade máxima sem justificativa entre múltiplas prioridades máximas.",
                    "13.3", item.id_prioridade,
                )
    if not briefing.restricoes and not briefing.restricoes_inexistentes_declaradas:
        registrar(condicoes, "Nenhuma restrição registrada; a ausência de registros não declara inexistência de restrições.", "20")
    for item in briefing.restricoes:
        for mensagem in item.diagnosticos():
            registrar(condicoes, f"{item.descricao}: {mensagem}", "14.4", item.id_restricao)
    if not briefing.pretensoes:
        registrar(condicoes, "Nenhuma pretensão declarada registrada.", "20")
    return tuple(apontamentos)


def _avaliar_prioridades_declaradas(itens, rotulo, subetapa, registrar):
    """Compara um conjunto declarado; ausência não é valor da escala."""
    if len(itens) > 1 and all(item[2] is not None for item in itens):
        if len({item[2] for item in itens}) == 1:
            registrar(
                subetapa,
                f"{rotulo}: todos os itens estão marcados com o mesmo valor de prioridade; "
                "a escala não distingue a importância declarada desses itens.",
                "13.3",
            )
    maximas = tuple(item for item in itens if item[2] == 5)
    if len(maximas) > 1:
        for id_entidade, nome, _, justificativa in maximas:
            if not justificativa:
                registrar(
                    subetapa,
                    f"{rotulo} — {nome}: prioridade máxima sem justificativa "
                    "entre múltiplas prioridades máximas.",
                    "13.3", id_entidade,
                )
