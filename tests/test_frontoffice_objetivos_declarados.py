import ast
from pathlib import Path
from uuid import UUID

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).resolve().parents[1]
OBJETIVOS = RAIZ / "mediad_planner/presentation/objetivos_declarados.py"
BRIEFINGS = RAIZ / "mediad_planner/presentation/briefings.py"
PROIBIDOS = (
    "mediad_planner.domain",
    "mediad_planner.engines",
    "mediad_planner.infrastructure",
)


def importacoes(caminho: Path) -> tuple[str, ...]:
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    encontrados = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            encontrados.extend(item.name for item in no.names)
        elif isinstance(no, ast.ImportFrom):
            encontrados.append(("." * no.level) + (no.module or ""))
    return tuple(encontrados)


def test_frontoffice_respeita_fronteiras() -> None:
    for caminho in (OBJETIVOS, BRIEFINGS):
        for modulo in importacoes(caminho):
            assert not modulo.startswith(PROIBIDOS)


def test_interface_contem_fluxo_e_mensagens_obrigatorias() -> None:
    conteudo = OBJETIVOS.read_text(encoding="utf-8")
    controlador = BRIEFINGS.read_text(encoding="utf-8")
    esperados = (
        "Objetivos declarados",
        "Marketing",
        "Comunicação",
        "Objetivo de Marketing",
        "Outro objetivo",
        "Informe o Objetivo de Marketing",
        "Dimensões do composto relacionadas (opcional)",
        "Praça (distribuição)",
        "Prioridade declarada",
        "Intensidade declarada",
        "Justificativa do Objetivo de Marketing (opcional)",
        "Adicionar Objetivo de Marketing",
        "Objetivo de Comunicação",
        "Informe o Objetivo de Comunicação",
        "Objetivos de Marketing relacionados (opcional)",
        "Justificativa do Objetivo de Comunicação (opcional)",
        "Adicionar Objetivo de Comunicação",
        "Remover Objetivo de Marketing",
        "Remover Objetivo de Comunicação",
        "Elas não são pesos calculados pelos motores.",
    )
    for texto in esperados:
        assert texto in conteudo
    assert "Subetapa em preenchimento" in controlador
    assert "Situação mercadológica e competitiva" in controlador


def test_catalogos_e_identidades_nao_sao_recriados_na_apresentacao() -> None:
    conteudo = OBJETIVOS.read_text(encoding="utf-8")
    minusculo = conteudo.lower()

    assert "listar_objetivos_marketing" in conteudo
    assert "listar_objetivos_comunicacao" in conteudo
    assert "listar_dimensoes_composto_marketing" in conteudo
    assert "objetivo.rotulos_dimensoes_composto" in conteudo
    assert "options=opcoes_marketing" in conteudo
    assert "ids_objetivos_marketing_relacionados=tuple(relacionados)" in conteudo
    assert "item.objetivo: item.id_objetivo" not in conteudo
    assert ".codigo" in conteudo
    assert ".id_objetivo" in conteudo
    assert ".lower(" not in conteudo
    assert ".replace(" not in conteudo
    for termo in (
        "objetivo de mídia calculado",
        "peso estratégico",
        "score",
        "kpi",
        "recomendação de meio",
        "seleção de canal",
        "executar_motor",
        "sql",
    ):
        assert termo not in minusculo


def _criar_briefing(aplicativo: AppTest) -> None:
    aplicativo.run(timeout=5)
    campos = {item.label: item for item in aplicativo.text_input}
    campos["Nome da Campanha"].set_value("Campanha Objetivos")
    campos["Anunciante"].set_value("Anunciante")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(
        item
        for item in aplicativo.button
        if item.label == "Criar Campanha e iniciar Briefing"
    ).click()
    aplicativo.run(timeout=5)


def test_apptest_fluxo_marketing_e_comunicacao_vinculados() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py"))
    _criar_briefing(aplicativo)
    aplicativo.radio[0].set_value("Objetivos declarados")
    aplicativo.run(timeout=5)

    seletores = {item.label: item for item in aplicativo.selectbox}
    seletores["Objetivo de Marketing"].set_value("Crescimento")
    seletores["Prioridade declarada"].set_value("5 — Muito alta")
    next(
        item
        for item in aplicativo.selectbox
        if item.label == "Intensidade declarada"
    ).set_value("4 — Alta")
    next(
        item
        for item in aplicativo.multiselect
        if item.label == "Dimensões do composto relacionadas (opcional)"
    ).set_value(["Produto", "Praça (distribuição)"])
    next(
        item
        for item in aplicativo.text_area
        if item.label == "Justificativa do Objetivo de Marketing (opcional)"
    ).set_value("Crescer de forma sustentável")
    next(
        item
        for item in aplicativo.button
        if item.label == "Adicionar Objetivo de Marketing"
    ).click()
    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    conteudo = " ".join(item.value for item in aplicativo.markdown)
    assert "Crescimento" in conteudo
    assert any(
        "2. Objetivos declarados" in item.value
        and "Em preenchimento" in item.value
        for item in aplicativo.markdown
    )

    objetivo_marketing = next(
        item
        for item in aplicativo.selectbox
        if item.label == "Objetivo de Marketing"
    )
    objetivo_marketing.set_value("Outro objetivo")
    aplicativo.run(timeout=5)
    next(
        item
        for item in aplicativo.text_input
        if item.label == "Informe o Objetivo de Marketing"
    ).set_value("Crescimento")
    next(
        item
        for item in aplicativo.button
        if item.label == "Adicionar Objetivo de Marketing"
    ).click()
    aplicativo.run(timeout=5)

    comunicacao = next(
        item
        for item in aplicativo.selectbox
        if item.label == "Objetivo de Comunicação"
    )
    comunicacao.set_value("Notoriedade")
    relacionados = next(
        item
        for item in aplicativo.multiselect
        if item.label == "Objetivos de Marketing relacionados (opcional)"
    )
    ids_marketing = [
        UUID(item.key.removeprefix("remover_marketing_"))
        for item in aplicativo.button
        if item.label == "Remover Objetivo de Marketing"
    ]
    assert relacionados.options == [
        "1. Crescimento — prioridade 3",
        "2. Crescimento — prioridade 3",
    ]
    relacionados.set_value(ids_marketing)
    next(
        item
        for item in aplicativo.text_area
        if item.label == "Justificativa do Objetivo de Comunicação (opcional)"
    ).set_value("Ampliar reconhecimento")
    next(
        item
        for item in aplicativo.button
        if item.label == "Adicionar Objetivo de Comunicação"
    ).click()
    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    conteudo = " ".join(item.value for item in aplicativo.markdown)
    assert "Notoriedade" in conteudo
    assert "Objetivos de Marketing relacionados: 1. Crescimento, 2. Crescimento" in conteudo


def test_apptest_objetivo_personalizado_exige_nome() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py"))
    _criar_briefing(aplicativo)
    aplicativo.radio[0].set_value("Objetivos declarados")
    aplicativo.run(timeout=5)
    objetivo = next(
        item
        for item in aplicativo.selectbox
        if item.label == "Objetivo de Marketing"
    )
    objetivo.set_value("Outro objetivo")
    aplicativo.run(timeout=5)
    next(
        item
        for item in aplicativo.button
        if item.label == "Adicionar Objetivo de Marketing"
    ).click()
    aplicativo.run(timeout=5)

    assert any(
        item.value == "Informe o Objetivo de Marketing"
        for item in aplicativo.error
    )
    assert not aplicativo.exception
