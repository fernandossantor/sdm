from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    RegistroSituacaoResumo,
)
from mediad_planner.application.dto.objetivos_declarados import (
    ObjetivoComunicacaoResumo,
    ObjetivoMarketingResumo,
)
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    listar_dimensoes_composto_marketing,
)


def resumir_briefing(briefing: Briefing) -> BriefingResumo:
    contexto = briefing.contexto_herdado
    registros = tuple(
        RegistroSituacaoResumo(
            id_registro=registro.id_registro,
            escopo=registro.escopo.value,
            codigo_aspecto=registro.codigo_aspecto,
            aspecto=registro.aspecto,
            entidade_referencia=registro.entidade_referencia,
            natureza=registro.natureza.value,
            valor_quantitativo=(
                format(registro.valor_quantitativo, "f")
                if registro.valor_quantitativo is not None
                else None
            ),
            unidade=registro.unidade,
            valor_qualitativo=registro.valor_qualitativo,
            fonte=registro.fonte,
            periodo_referencia=registro.periodo_referencia,
            observacao=registro.observacao,
        )
        for registro in briefing.situacao_mercadologica.registros
    )
    rotulos_dimensoes = {
        definicao.codigo: definicao.rotulo
        for definicao in listar_dimensoes_composto_marketing()
    }
    objetivos_marketing = tuple(
        ObjetivoMarketingResumo(
            id_objetivo=item.id_objetivo,
            codigo_objetivo=item.codigo_objetivo,
            objetivo=item.objetivo,
            dimensoes_composto=tuple(
                dimensao.value for dimensao in item.dimensoes_composto
            ),
            rotulos_dimensoes_composto=tuple(
                rotulos_dimensoes[dimensao]
                for dimensao in item.dimensoes_composto
            ),
            prioridade_declarada=item.prioridade_declarada,
            intensidade_declarada=item.intensidade_declarada,
            justificativa=item.justificativa,
        )
        for item in briefing.objetivos_declarados.marketing
    )
    objetivos_comunicacao = tuple(
        ObjetivoComunicacaoResumo(
            id_objetivo=item.id_objetivo,
            codigo_objetivo=item.codigo_objetivo,
            objetivo=item.objetivo,
            ids_objetivos_marketing_relacionados=(
                item.ids_objetivos_marketing_relacionados
            ),
            prioridade_declarada=item.prioridade_declarada,
            intensidade_declarada=item.intensidade_declarada,
            justificativa=item.justificativa,
        )
        for item in briefing.objetivos_declarados.comunicacao
    )
    return BriefingResumo(
        id_briefing=briefing.id_briefing,
        id_campanha=briefing.id_campanha,
        numero_versao=briefing.numero_versao,
        estado=briefing.estado.value,
        codigo_campanha=contexto.codigo_campanha.valor,
        nome_campanha=contexto.nome_campanha,
        anunciante=contexto.anunciante.nome_snapshot,
        marca=contexto.marca.nome_snapshot if contexto.marca else None,
        produto_servico=(
            contexto.produto_servico.nome_snapshot
            if contexto.produto_servico
            else None
        ),
        planejador_responsavel=contexto.planejador_responsavel.nome_snapshot,
        equipe=tuple(item.nome_snapshot for item in contexto.equipe),
        criado_em=briefing.criado_em,
        atualizado_em=briefing.atualizado_em,
        registros_situacao=registros,
        objetivos_marketing=objetivos_marketing,
        objetivos_comunicacao=objetivos_comunicacao,
    )
