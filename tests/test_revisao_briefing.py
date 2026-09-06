from dataclasses import asdict, replace
from decimal import Decimal
from uuid import UUID

from mediad_planner.application.dto.condicoes_declaradas import SalvarRestricaoEntrada
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    ObjetivoComunicacaoDeclarado, ObjetivoMarketingDeclarado, ObjetivosDeclarados,
)
from mediad_planner.domain.briefing.praca_universo import EstruturaTerritorialPopulacional
from mediad_planner.domain.briefing.revisao import avaliar_briefing
from mediad_planner.domain.briefing.situacao_mercadologica import (
    EscopoSituacaoMercadologica, NaturezaRegistroSituacao,
    RegistroSituacaoMercadologica, SituacaoMercadologicaCompetitiva,
)
from test_briefing_dominio import briefing
from test_jornada import _com_publico, _jornada, _etapa
from test_periodo_verba import _preparar, _entrada
from test_praca_universo_dominio import _praca, _universo
from test_publicos import _preparar as preparar_publicos, _entrada as entrada_publico


def test_rascunho_apresenta_lacunas_sem_alterar_estado_ou_declaracoes():
    original = briefing()
    antes = asdict(original)
    apontamentos = avaliar_briefing(original)
    assert len(apontamentos) == 10
    assert {item.subetapa for item in apontamentos} == {
        "Situação mercadológica e competitiva", "Objetivos declarados",
        "Praça e universo", "Segmentos e públicos", "Período e verba",
        "Prioridades, restrições e pretensões",
    }
    assert all(item.referencia_normativa.startswith("02_BRIEFING.md §") for item in apontamentos)
    assert asdict(original) == antes
    assert original.estado.value == "RASCUNHO"
    resumo = resumir_briefing(original)
    assert [asdict(item) for item in resumo.apontamentos_revisao] == [
        asdict(item) for item in apontamentos
    ]


def test_fontes_e_periodos_identificam_registro_e_desaparecem_apos_complemento():
    registro = RegistroSituacaoMercadologica(
        UUID(int=40), EscopoSituacaoMercadologica.MERCADO, None,
        "Participação", None, NaturezaRegistroSituacao.QUANTITATIVO,
        Decimal("0"), "%", None, None, None, None,
    )
    original = replace(briefing(), situacao_mercadologica=SituacaoMercadologicaCompetitiva((registro,)))
    apontamentos = [item for item in avaliar_briefing(original) if item.id_entidade == registro.id_registro]
    assert len(apontamentos) == 2
    assert all("Participação" in item.mensagem for item in apontamentos)
    completo = replace(original, situacao_mercadologica=SituacaoMercadologicaCompetitiva((
        replace(registro, fonte="Pesquisa", periodo_referencia="2026"),
    )))
    assert not any(item.subetapa == "Situação mercadológica e competitiva" for item in avaliar_briefing(completo))
    assert original.situacao_mercadologica.registros[0].valor_quantitativo == 0


def test_relacao_entre_objetivos_e_avaliada_sem_inferir_compatibilidade():
    marketing = ObjetivoMarketingDeclarado(UUID(int=41), None, "Crescimento", (), 3, 3, None)
    comunicacao = ObjetivoComunicacaoDeclarado(UUID(int=42), None, "Notoriedade", (), 3, 3, None)
    original = replace(briefing(), objetivos_declarados=ObjetivosDeclarados((marketing,), (comunicacao,)))
    assert any(item.id_entidade == comunicacao.id_objetivo for item in avaliar_briefing(original))
    relacionado = replace(comunicacao, ids_objetivos_marketing_relacionados=(marketing.id_objetivo,))
    completo = replace(original, objetivos_declarados=ObjetivosDeclarados((marketing,), (relacionado,)))
    assert not any(item.subetapa == "Objetivos declarados" for item in avaliar_briefing(completo))


def test_praca_sem_universo_e_fontes_populacionais():
    praca = _praca()
    original = replace(briefing(), estrutura_territorial_populacional=EstruturaTerritorialPopulacional((praca,), ()))
    assert any(item.id_entidade == praca.id_praca and "sem universo" in item.mensagem for item in avaliar_briefing(original))
    universo = _universo()
    com_universo = replace(original, estrutura_territorial_populacional=EstruturaTerritorialPopulacional((praca,), (universo,)))
    territoriais = [item for item in avaliar_briefing(com_universo) if item.subetapa == "Praça e universo"]
    assert len(territoriais) == 2
    assert all(item.id_entidade == universo.id_universo for item in territoriais)
    completo = replace(com_universo, estrutura_territorial_populacional=EstruturaTerritorialPopulacional(
        (praca,), (replace(universo, fonte="Pesquisa", data_referencia="2026"),),
    ))
    assert not any(item.subetapa == "Praça e universo" for item in avaliar_briefing(completo))


def test_jornada_sem_aplicabilidade_presumida_e_etapa_sem_objetivo():
    ambiente, campanha, publico = _com_publico()
    original = ambiente.briefings.abrir_briefing(campanha)
    assert any(item.id_entidade == publico and "verificar se" in item.mensagem for item in original.apontamentos_revisao)
    atualizado = ambiente.briefings.adicionar_jornada(campanha, _jornada(publico))
    assert not any(item.id_entidade == publico and item.subetapa == "Jornada" for item in atualizado.apontamentos_revisao)
    atualizado = ambiente.briefings.adicionar_etapa_jornada(campanha, atualizado.jornadas[0].id_jornada, _etapa(publico))
    assert any(item.id_entidade == atualizado.jornadas[0].etapas[0].id_etapa for item in atualizado.apontamentos_revisao)


def test_revisao_reutiliza_alertas_locais_e_recalcula_apos_edicao():
    ambiente, campanha = _preparar()
    alterado = ambiente.briefings.definir_periodo_verba(campanha, _entrada(valor_total="100"))
    assert any("Parcela comprometida superior" in item.mensagem for item in alterado.apontamentos_revisao)
    antes = ambiente.briefings.abrir_briefing(campanha)
    assert antes == ambiente.briefings.abrir_briefing(campanha)
    corrigido = ambiente.briefings.definir_periodo_verba(campanha, _entrada())
    assert not any(item.subetapa == "Período e verba" for item in corrigido.apontamentos_revisao)
    restrito = ambiente.briefings.salvar_restricao(campanha, SalvarRestricaoEntrada(
        "LEGAL", "Vedação declarada", None, 5, 5, "Jurídico", None, None, None,
    ))
    alertas = [item for item in restrito.apontamentos_revisao if item.id_entidade == restrito.restricoes[0].id_restricao]
    assert len(alertas) == 3
    assert all("Vedação declarada" in item.mensagem for item in alertas)
    assert not any("Nenhuma restrição" in item.mensagem for item in restrito.apontamentos_revisao)


def test_zero_e_verba_explicitamente_nao_definida_nao_sao_ausencia():
    ambiente, campanha = _preparar()
    for valor, natureza in (("0", "ESTIMADO"), (None, "AINDA_NAO_DEFINIDO")):
        resumo = ambiente.briefings.definir_periodo_verba(campanha, _entrada(
            valor_total=valor, natureza_limite=natureza, valor_minimo=None,
            valor_maximo=None, parcela_comprometida=None,
        ))
        assert not any(item.subetapa == "Período e verba" for item in resumo.apontamentos_revisao)


def test_prioridade_ausente_depende_de_multiplos_publicos():
    ambiente, campanha, segmentos, pracas = preparar_publicos()
    primeiro = entrada_publico((segmentos[0],), (pracas[0],), prioridade=None)
    resumo = ambiente.briefings.adicionar_publico(campanha, primeiro)
    assert not any("prioridade não informada" in item.mensagem for item in resumo.apontamentos_revisao)
    segundo = entrada_publico((segmentos[1],), (pracas[1],), nome="Outro público", prioridade=None)
    resumo = ambiente.briefings.adicionar_publico(campanha, segundo)
    assert len([item for item in resumo.apontamentos_revisao if "prioridade não informada" in item.mensagem]) == 2
    resumo = ambiente.briefings.remover_publico(campanha, resumo.publicos[-1].id_publico)
    assert not any("prioridade não informada" in item.mensagem for item in resumo.apontamentos_revisao)
