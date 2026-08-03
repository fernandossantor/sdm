from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    RegistroSituacaoResumo,
)
from mediad_planner.application.dto.objetivos_declarados import (
    ObjetivoComunicacaoResumo,
    ObjetivoMarketingResumo,
)
from mediad_planner.application.dto.praca_universo import PracaResumo, UniversoResumo
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    listar_dimensoes_composto_marketing,
)
from mediad_planner.domain.briefing.praca_universo import (
    listar_tipos_praca_territorial,
    listar_unidades_populacionais,
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
    rotulos_tipos = {
        definicao.codigo: definicao.rotulo
        for definicao in listar_tipos_praca_territorial()
    }
    rotulos_unidades = {
        definicao.codigo: definicao.rotulo
        for definicao in listar_unidades_populacionais()
    }
    pracas = tuple(
        PracaResumo(
            id_praca=item.id_praca,
            tipo=item.tipo.value,
            rotulo_tipo=rotulos_tipos[item.tipo],
            nome=item.nome,
            codigo_oficial=item.codigo_oficial,
            abrangencia=item.abrangencia,
            valor_populacao_referencia=(
                format(item.valor_populacao_referencia, "f")
                if item.valor_populacao_referencia is not None else None
            ),
            codigo_unidade_populacional=item.codigo_unidade_populacional,
            unidade_populacional=(
                rotulos_unidades[item.codigo_unidade_populacional]
                if item.codigo_unidade_populacional is not None
                else item.unidade_populacional
            ),
            fonte=item.fonte,
            data_referencia=item.data_referencia,
            observacao=item.observacao,
        )
        for item in briefing.estrutura_territorial_populacional.pracas
    )
    pracas_por_id = {item.id_praca: item for item in pracas}
    universos = tuple(
        UniversoResumo(
            id_universo=item.id_universo,
            nome=item.nome,
            definicao=item.definicao,
            ids_pracas=item.ids_pracas,
            rotulos_pracas=tuple(
                _rotulo_praca(pracas_por_id[id_praca])
                for id_praca in item.ids_pracas
            ),
            valor_populacional=(
                format(item.valor_populacional, "f")
                if item.valor_populacional is not None else None
            ),
            codigo_unidade=item.codigo_unidade,
            unidade=(
                rotulos_unidades[item.codigo_unidade]
                if item.codigo_unidade is not None
                else item.unidade
            ),
            fonte=item.fonte,
            data_referencia=item.data_referencia,
            criterios_inclusao=item.criterios_inclusao,
            criterios_exclusao=item.criterios_exclusao,
            observacao=item.observacao,
        )
        for item in briefing.estrutura_territorial_populacional.universos
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
        pracas=pracas,
        universos=universos,
    )


def _rotulo_praca(praca: PracaResumo) -> str:
    rotulo = f"[{praca.rotulo_tipo}] {praca.nome}"
    if praca.codigo_oficial:
        rotulo += f" — {praca.codigo_oficial}"
    return rotulo
