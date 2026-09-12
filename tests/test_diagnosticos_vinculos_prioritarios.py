from dataclasses import asdict, replace

import pytest

from mediad_planner.application.dto.objetivos_declarados import DefinirVinculosObjetivoEntrada
from mediad_planner.domain.briefing.revisao import avaliar_briefing
from test_vinculos_objetivos import _dominio_objetivos, _ambiente_vinculos, PUBLICO, PRACA
from test_publicos import _entrada


def _alertas(itens):
    return [a for a in itens if "prioritário (prioridade" in a.mensagem]


@pytest.mark.parametrize("grupo", ("marketing", "comunicacao"))
@pytest.mark.parametrize("prioridade", (1, 2, 3, 4, 5))
@pytest.mark.parametrize("publicos,pracas", (((), ()), ((PUBLICO,), ()), ((), (PRACA,)), ((PUBLICO,), (PRACA,))))
def test_objetivos_avaliam_cada_vinculo_sem_alterar_declaracoes(grupo, prioridade, publicos, pracas):
    original = _dominio_objetivos()
    objetivo = replace(getattr(original.objetivos_declarados, grupo)[0],
        prioridade_declarada=prioridade, ids_publicos_relacionados=publicos,
        ids_pracas_relacionadas=pracas)
    original = replace(original, objetivos_declarados=replace(original.objetivos_declarados,
        **{grupo: (objetivo,)}))
    antes = asdict(original)
    alertas = [a for a in _alertas(avaliar_briefing(original)) if a.id_entidade == objetivo.id_objetivo]
    esperados = [] if prioridade < 4 else [
        rotulo for ids, rotulo in ((publicos, "público"), (pracas, "praça")) if not ids
    ]
    assert len(alertas) == len(esperados)
    for alerta, rotulo in zip(alertas, esperados):
        assert f"sem {rotulo} relacionado." in alerta.mensagem
        assert objetivo.objetivo in alerta.mensagem
        assert alerta.subetapa == "Objetivos declarados"
        assert alerta.referencia_normativa == "02_BRIEFING.md § 13.3"
    assert asdict(original) == antes


@pytest.mark.parametrize("prioridade", (None, 1, 2, 3, 4, 5))
@pytest.mark.parametrize("vinculo", (None, "marketing", "comunicacao", "ambos", "so_praca"))
def test_publico_exige_vinculo_explicito_com_qualquer_objetivo(prioridade, vinculo):
    original = _dominio_objetivos()
    estrutura = original.estrutura_territorial_populacional
    original = replace(original, estrutura_territorial_populacional=replace(estrutura,
        publicos=(replace(estrutura.publicos[0], prioridade=prioridade),)))
    objetivos = original.objetivos_declarados
    for grupo in ("marketing", "comunicacao"):
        objetivo = replace(getattr(objetivos, grupo)[0], prioridade_declarada=1,
            ids_publicos_relacionados=(PUBLICO,) if vinculo in (grupo, "ambos") else (),
            ids_pracas_relacionadas=(PRACA,))
        objetivos = replace(objetivos, **{grupo: (objetivo,)})
    original = replace(original, objetivos_declarados=objetivos)
    antes = asdict(original)
    alertas = _alertas(avaliar_briefing(original))
    esperado = prioridade in (4, 5) and vinculo in (None, "so_praca")
    assert len(alertas) == int(esperado)
    if esperado:
        assert alertas[0].id_entidade == PUBLICO
        assert alertas[0].subetapa == "Segmentos e públicos"
        assert alertas[0].referencia_normativa == "02_BRIEFING.md § 13.3"
        assert "sem objetivo relacionado." in alertas[0].mensagem
    assert asdict(original) == antes


@pytest.mark.parametrize("grupo", ("marketing", "comunicacao"))
def test_aplicacao_recalcula_apos_vinculos_prioridade_e_remocao(grupo):
    ambiente, campanha = _ambiente_vinculos()
    resumo = ambiente.briefings.abrir_briefing(campanha)
    objetivo = getattr(resumo, f"objetivos_{grupo}")[0]
    publico, outro_publico = resumo.publicos
    vinculos = DefinirVinculosObjetivoEntrada(objetivo.id_objetivo,
        (publico.id_publico,), (resumo.pracas[0].id_praca,))
    resumo = ambiente.briefings.definir_vinculos_objetivo(campanha, vinculos)
    assert not any(a.id_entidade in (objetivo.id_objetivo, publico.id_publico) for a in _alertas(resumo.apontamentos_revisao))
    # Nomes iguais não substituem identidades distintas.
    assert any(a.id_entidade == outro_publico.id_publico for a in _alertas(resumo.apontamentos_revisao))
    resumo = ambiente.briefings.definir_vinculos_objetivo(campanha,
        DefinirVinculosObjetivoEntrada(objetivo.id_objetivo, (), ()))
    assert sum(a.id_entidade == objetivo.id_objetivo for a in _alertas(resumo.apontamentos_revisao)) == 2
    for prioridade, quantidade in ((3, 0), (4, 1), (5, 1), (None, 0)):
        resumo = ambiente.briefings.editar_publico(campanha, publico.id_publico,
            _entrada(publico.ids_segmentos_origem, publico.ids_pracas, prioridade=prioridade))
        assert sum(a.id_entidade == publico.id_publico for a in _alertas(resumo.apontamentos_revisao)) == quantidade
    ambiente.briefings.definir_vinculos_objetivo(campanha, vinculos)
    if grupo == "marketing":
        ambiente.briefings.remover_objetivo_comunicacao(campanha, resumo.objetivos_comunicacao[0].id_objetivo)
    resumo = getattr(ambiente.briefings, f"remover_objetivo_{grupo}")(campanha, objetivo.id_objetivo)
    resumo = ambiente.briefings.editar_publico(campanha, publico.id_publico,
        _entrada(publico.ids_segmentos_origem, publico.ids_pracas, prioridade=4))
    assert any(a.id_entidade == publico.id_publico for a in _alertas(resumo.apontamentos_revisao))
    assert not any(a.id_entidade == objetivo.id_objetivo for a in _alertas(resumo.apontamentos_revisao))
    assert ambiente.briefings.abrir_briefing(campanha) == resumo
