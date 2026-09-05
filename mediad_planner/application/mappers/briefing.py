from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    RegistroSituacaoResumo,
)
from mediad_planner.application.dto.objetivos_declarados import (
    ObjetivoComunicacaoResumo,
    ObjetivoMarketingResumo,
)
from mediad_planner.application.dto.praca_universo import PracaResumo, UniversoResumo
from mediad_planner.application.dto.segmentos import SegmentoResumo
from mediad_planner.application.dto.publicos import PublicoResumo
from mediad_planner.application.dto.jornada import EtapaJornadaResumo, JornadaResumo
from mediad_planner.domain.briefing.jornada import ROTULOS_ETAPAS
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    listar_dimensoes_composto_marketing,
)
from mediad_planner.domain.briefing.praca_universo import (
    listar_tipos_praca_territorial,
    listar_unidades_populacionais,
    listar_criterios_segmentacao,
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
    universos_por_id = {
        item.id_universo: item
        for item in briefing.estrutura_territorial_populacional.universos
    }
    rotulos_criterios = {
        item.codigo: item.rotulo for item in listar_criterios_segmentacao()
    }
    segmentos = tuple(
        SegmentoResumo(
            id_segmento=item.id_segmento,
            id_universo_origem=item.id_universo_origem,
            nome_universo_origem=universos_por_id[item.id_universo_origem].nome,
            ids_pracas=item.ids_pracas,
            rotulos_pracas=tuple(
                _rotulo_praca(pracas_por_id[id_praca])
                for id_praca in item.ids_pracas
            ),
            criterios_aplicados=tuple(
                criterio.value for criterio in item.criterios_aplicados
            ),
            rotulos_criterios=tuple(
                rotulos_criterios[criterio] for criterio in item.criterios_aplicados
            ),
            definicao=item.definicao,
            tamanho_estimado=(
                format(item.tamanho_estimado, "f")
                if item.tamanho_estimado is not None else None
            ),
            unidade=universos_por_id[item.id_universo_origem].unidade,
            fonte=item.fonte,
            data_referencia=item.data_referencia,
        )
        for item in briefing.estrutura_territorial_populacional.segmentos
    )
    segmentos_por_id = {
        item.id_segmento: item
        for item in briefing.estrutura_territorial_populacional.segmentos
    }
    publicos = tuple(
        PublicoResumo(
            id_publico=item.id_publico,
            nome=item.nome,
            ids_segmentos_origem=item.ids_segmentos_origem,
            definicoes_segmentos_origem=tuple(
                segmentos_por_id[id_segmento].definicao
                for id_segmento in item.ids_segmentos_origem
            ),
            ids_pracas=item.ids_pracas,
            rotulos_pracas=tuple(
                _rotulo_praca(pracas_por_id[id_praca])
                for id_praca in item.ids_pracas
            ),
            prioridade=item.prioridade,
            intensidade_importancia=item.intensidade_importancia,
            tamanho_estimado=(
                format(item.tamanho_estimado, "f")
                if item.tamanho_estimado is not None else None
            ),
            papel_declarado=item.papel_declarado,
            justificativa=item.justificativa,
        )
        for item in briefing.estrutura_territorial_populacional.publicos
    )
    nomes_publicos = {
        item.id_publico: item.nome or f"Público {str(item.id_publico)[:8]}"
        for item in briefing.estrutura_territorial_populacional.publicos
    }
    nomes_objetivos = {
        item.id_objetivo: item.objetivo
        for item in briefing.objetivos_declarados.comunicacao
    }
    jornadas = tuple(
        JornadaResumo(
            id_jornada=item.id_jornada,
            nome=item.nome,
            descricao=item.descricao,
            ids_publicos=item.ids_publicos,
            nomes_publicos=tuple(nomes_publicos[id_publico] for id_publico in item.ids_publicos),
            referencia_modelo=item.referencia_modelo,
            adaptada_localmente=item.adaptada_localmente,
            etapas=tuple(
                EtapaJornadaResumo(
                    id_etapa=etapa.id_etapa,
                    categoria=etapa.categoria.value,
                    rotulo_categoria=ROTULOS_ETAPAS[etapa.categoria],
                    ordem=etapa.ordem,
                    existe=etapa.existe,
                    relevancia=etapa.relevancia,
                    intensidade=etapa.intensidade,
                    prioridade=etapa.prioridade,
                    ids_publicos=etapa.ids_publicos,
                    nomes_publicos=tuple(nomes_publicos[id_publico] for id_publico in etapa.ids_publicos),
                    ids_objetivos_comunicacao=etapa.ids_objetivos_comunicacao,
                    nomes_objetivos_comunicacao=tuple(
                        nomes_objetivos[id_objetivo]
                        for id_objetivo in etapa.ids_objetivos_comunicacao
                    ),
                    situacao_atual=etapa.situacao_atual,
                    situacao_pretendida=etapa.situacao_pretendida,
                    observacao=etapa.observacao,
                )
                for etapa in sorted(
                    item.etapas,
                    key=lambda etapa: (etapa.ordem is None, etapa.ordem or 0),
                )
            ),
        )
        for item in briefing.jornadas
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
        criterios_segmentacao=tuple(
            item.value
            for item in (
                briefing.estrutura_territorial_populacional
                .criterios_segmentacao
            )
        ),
        segmentos=segmentos,
        publicos=publicos,
        jornadas=jornadas,
    )


def _rotulo_praca(praca: PracaResumo) -> str:
    rotulo = f"[{praca.rotulo_tipo}] {praca.nome}"
    if praca.codigo_oficial:
        rotulo += f" — {praca.codigo_oficial}"
    return rotulo
