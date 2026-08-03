import ast
from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).parents[1]
ARQUIVO = RAIZ / "mediad_planner/presentation/praca_universo.py"


def _preservar_estado_do_formulario(app: AppTest) -> None:
    for chave in (
        "campanha-nome",
        "campanha-anunciante",
        "campanha-marca",
        "campanha-produto-servico",
        "campanha-planejador",
        "campanha-equipe",
        "campanha-observacao",
    ):
        app.session_state[chave] = ""


def test_apresentacao_respeita_fronteiras_e_conteudo() -> None:
    fonte = ARQUIVO.read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    importacoes = {
        no.module
        for no in ast.walk(arvore)
        if isinstance(no, ast.ImportFrom) and no.module
    }
    proibidos = (
        "mediad_planner.domain",
        "mediad_planner.infrastructure",
        "mediad_planner.engines",
        "mediad_planner.composition",
    )
    assert not any(item.startswith(proibidos) for item in importacoes)
    for texto in (
        "Praça e universo", "Praças", "Universos", "Tipo territorial",
        "Nome da Praça", "Código oficial (opcional)",
        "População territorial de referência (opcional)", "Nome do Universo",
        "Definição", "Praças relacionadas", "Remover Praça",
        "Remover Universo", "Praças salvas (", "Universos salvos (",
        "Praça territorial não é Praça do composto de Marketing",
        "Universo não é audiência, segmento ou público-alvo",
    ):
        assert texto in fonte
    assert ".lower(" not in fonte
    assert "slug" not in fonte.casefold()


def test_expanders_recolhidos_e_catalogos_vem_da_aplicacao() -> None:
    fonte = ARQUIVO.read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    expanders = [
        no for no in ast.walk(arvore)
        if isinstance(no, ast.Call)
        and isinstance(no.func, ast.Attribute)
        and no.func.attr == "expander"
    ]
    assert len(expanders) == 2
    for chamada in expanders:
        expanded = next(
            item for item in chamada.keywords if item.arg == "expanded"
        )
        assert isinstance(expanded.value, ast.Constant)
        assert expanded.value.value is False
    assert "aplicacao.listar_tipos_praca()" in fonte
    assert "aplicacao.listar_unidades_populacionais()" in fonte
    assert "ERROS_CONTROLADOS" in fonte


def test_app_abre_e_exibe_terceira_subetapa_sem_excecoes() -> None:
    app = AppTest.from_file(str(RAIZ / "app.py")).run(timeout=3)
    campos = {item.label: item for item in app.text_input}
    campos["Nome da Campanha"].set_value("Territorial")
    campos["Anunciante"].set_value("Anunciante")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(
        item for item in app.button
        if item.label == "Criar Campanha e iniciar Briefing"
    ).click()
    app.run(timeout=3)
    next(item for item in app.button if item.label == "Continuar no Briefing").click()
    _preservar_estado_do_formulario(app)
    app.run(timeout=3)
    assert "Praça e universo" in app.radio[0].options
    app.radio[0].set_value("Praça e universo")
    app.run(timeout=3)
    assert not app.exception
    assert any(item.value == "Praça e universo" for item in app.subheader)
    assert {item.label for item in app.tabs} >= {"Praças", "Universos"}
    assert any(item.label == "Campanhas" for item in app.button)

    next(
        item for item in app.text_input if item.label == "Nome da Praça"
    ).set_value("São Borja")
    next(
        item
        for item in app.text_input
        if item.label == "População territorial de referência (opcional)"
    ).set_value("60000.5")
    next(
        item for item in app.selectbox if item.key == "unidade_praca"
    ).set_value("Pessoas")
    next(item for item in app.button if item.label == "Adicionar Praça").click()
    app.run(timeout=3)
    assert any(item.label == "Praças salvas (1)" for item in app.expander)

    next(
        item for item in app.text_input if item.label == "Nome do Universo"
    ).set_value("Moradores adultos")
    next(
        item for item in app.text_area if item.label == "Definição"
    ).set_value("Pessoas com 18 anos ou mais residentes na praça.")
    relacao = next(
        item for item in app.multiselect if item.label == "Praças relacionadas"
    )
    relacao.set_value([relacao.options[0]])
    next(item for item in app.button if item.label == "Adicionar Universo").click()
    app.run(timeout=3)
    assert any(item.label == "Universos salvos (1)" for item in app.expander)
    conteudo = " ".join(item.value for item in app.markdown)
    assert "São Borja" in conteudo
    assert "60000.5 Pessoas" in conteudo

    next(item for item in app.button if item.label == "Remover Universo").click()
    app.run(timeout=3)
    assert any(item.label == "Universos salvos (0)" for item in app.expander)
    next(item for item in app.button if item.label == "Remover Praça").click()
    app.run(timeout=3)
    assert any(item.label == "Praças salvas (0)" for item in app.expander)
    assert not app.exception
