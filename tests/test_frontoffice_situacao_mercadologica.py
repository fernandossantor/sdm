import ast
from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).resolve().parents[1]
APRESENTACAO = RAIZ / "mediad_planner/presentation/briefings.py"


def _preservar_formulario(aplicativo: AppTest) -> None:
    for chave in (
        "campanha-nome",
        "campanha-anunciante",
        "campanha-marca",
        "campanha-produto-servico",
        "campanha-planejador",
        "campanha-equipe",
        "campanha-observacao",
    ):
        aplicativo.session_state[chave] = ""


def test_frontoffice_nao_importa_camadas_proibidas() -> None:
    arvore = ast.parse(APRESENTACAO.read_text(encoding="utf-8"))
    proibidos = (
        "mediad_planner.domain",
        "mediad_planner.engines",
        "mediad_planner.infrastructure",
    )
    for no in ast.walk(arvore):
        if isinstance(no, ast.ImportFrom):
            assert not (no.module or "").startswith(proibidos)
        if isinstance(no, ast.Import):
            for alias in no.names:
                assert not alias.name.startswith(proibidos)


def test_interface_contem_formulario_e_separacao_epistemologica() -> None:
    conteudo = APRESENTACAO.read_text(encoding="utf-8")
    textos = (
        "Situação mercadológica e competitiva", "Anunciante", "Mercado",
        "Categoria", "Concorrência", "Outro aspecto",
        "Nome do aspecto observado",
        "Concorrente relacionado", "Quantitativo", "Qualitativo", "Valor de",
        "Unidade de medida", "Descrição de", "Fonte dos dados (opcional)",
        "Período de referência (opcional)",
        "Observação complementar (opcional)", "Adicionar registro", "Registros salvos",
        "Remover registro",
    )
    for texto in textos:
        assert texto in conteudo
    assert "declarações sem produzir interpretação estratégica" in conteudo
    assert "listar_aspectos_situacao" in conteudo
    assert ".codigo" in conteudo
    assert "lower()" not in conteudo
    assert "replace(" not in conteudo
    assert "Participação de mercado" not in conteudo
    for antigo in ("Dimensão", "Outra dimensão", "Informe a dimensão"):
        assert antigo not in conteudo
    for proibido in (
        "objetivo de mídia", "KPI", "recomendação de meio", "seleção de canal",
        "alcance calculado", "frequência calculada", "executar_motor", "SQL",
    ):
        assert proibido not in conteudo


def test_apptest_salva_registro_quantitativo() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py")).run(timeout=5)
    campos = {campo.label: campo for campo in aplicativo.text_input}
    campos["Nome da Campanha"].set_value("Campanha Situação")
    campos["Anunciante"].set_value("Anunciante Situação")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(
        botao for botao in aplicativo.button
        if botao.label == "Criar Campanha e iniciar Briefing"
    ).click()
    aplicativo.run(timeout=5)
    next(
        item for item in aplicativo.button
        if item.label == "Continuar no Briefing"
    ).click()
    _preservar_formulario(aplicativo)
    aplicativo.run(timeout=5)

    next(
        item for item in aplicativo.selectbox if item.label == "Aspecto observado"
    ).select("Participação de mercado")
    aplicativo.run(timeout=5)
    campos = {campo.label: campo for campo in aplicativo.text_input}
    campos["Valor de “Participação de mercado”"].set_value("12.5")
    campos["Unidade de medida"].set_value("%")
    campos["Fonte dos dados (opcional)"].set_value("Instituto")
    campos["Período de referência (opcional)"].set_value("2026")
    next(
        botao for botao in aplicativo.button
        if botao.label == "Adicionar registro"
    ).click()
    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    texto = " ".join(item.value for item in aplicativo.markdown)
    assert "Participação de mercado" in texto
    assert "12.5" in texto
    assert "Em preenchimento" in texto

    aplicativo.run(timeout=5)
    texto = " ".join(item.value for item in aplicativo.markdown)
    assert "Participação de mercado" in texto

    next(
        item for item in aplicativo.selectbox if item.label == "Escopo"
    ).select("Mercado")
    aplicativo.run(timeout=5)
    next(
        item for item in aplicativo.selectbox if item.label == "Aspecto observado"
    ).select("Tendência de desempenho do mercado")
    next(
        item for item in aplicativo.selectbox if item.label == "Natureza"
    ).select("Qualitativo")
    aplicativo.run(timeout=5)
    next(
        item
        for item in aplicativo.text_area
        if item.label == "Descrição de “Tendência de desempenho do mercado”"
    ).set_value("Crescimento moderado no período observado.")
    next(
        botao for botao in aplicativo.button
        if botao.label == "Adicionar registro"
    ).click()
    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    texto = " ".join(item.value for item in aplicativo.markdown)
    assert "Tendência de desempenho do mercado" in texto
    assert "Crescimento moderado no período observado." in texto


def test_apptest_aspecto_personalizado_nao_salva_controle_visual() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py")).run(timeout=5)
    campos = {campo.label: campo for campo in aplicativo.text_input}
    campos["Nome da Campanha"].set_value("Campanha Personalizada")
    campos["Anunciante"].set_value("Anunciante")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(
        botao for botao in aplicativo.button
        if botao.label == "Criar Campanha e iniciar Briefing"
    ).click()
    aplicativo.run(timeout=5)
    next(
        item for item in aplicativo.button
        if item.label == "Continuar no Briefing"
    ).click()
    _preservar_formulario(aplicativo)
    aplicativo.run(timeout=5)
    next(
        item for item in aplicativo.selectbox if item.label == "Aspecto observado"
    ).select("Outro aspecto")
    aplicativo.run(timeout=5)

    next(
        botao for botao in aplicativo.button
        if botao.label == "Adicionar registro"
    ).click()
    aplicativo.run(timeout=5)
    assert any(
        erro.value == "Informe o nome do aspecto observado"
        for erro in aplicativo.error
    )
    assert not any(
        botao.label == "Remover registro" for botao in aplicativo.button
    )

    campos = {campo.label: campo for campo in aplicativo.text_input}
    campos["Nome do aspecto observado"].set_value(
        "Índice de disponibilidade local"
    )
    aplicativo.run(timeout=5)
    campos = {campo.label: campo for campo in aplicativo.text_input}
    campos["Valor de “Índice de disponibilidade local”"].set_value("7.5")
    campos["Unidade de medida"].set_value("índice")
    next(
        botao for botao in aplicativo.button
        if botao.label == "Adicionar registro"
    ).click()
    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    texto = " ".join(item.value for item in aplicativo.markdown)
    assert "Índice de disponibilidade local" in texto
    assert "7.5 índice" in texto
