import ast
from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).resolve().parents[1]
ARQUIVOS_APRESENTACAO = (
    RAIZ / "mediad_planner/presentation/campanhas.py",
    RAIZ / "mediad_planner/presentation/briefings.py",
    RAIZ / "mediad_planner/presentation/streamlit_app.py",
)
CAMADAS_PROIBIDAS = (
    "mediad_planner.domain",
    "mediad_planner.engines",
    "mediad_planner.infrastructure",
)


def modulos_importados(caminho: Path) -> tuple[str, ...]:
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    modulos: list[str] = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            modulos.extend(alias.name for alias in no.names)
        elif isinstance(no, ast.ImportFrom):
            prefixo = "." * no.level
            modulos.append(prefixo + (no.module or ""))
    return tuple(modulos)


def test_frontoffice_respeita_fronteiras_de_camadas() -> None:
    for caminho in ARQUIVOS_APRESENTACAO:
        importacoes = modulos_importados(caminho)

        for modulo in importacoes:
            assert not modulo.startswith(CAMADAS_PROIBIDAS)


def test_cache_existe_somente_no_controlador_principal() -> None:
    campanhas = ARQUIVOS_APRESENTACAO[0].read_text(encoding="utf-8")
    briefings = ARQUIVOS_APRESENTACAO[1].read_text(encoding="utf-8")
    controlador = ARQUIVOS_APRESENTACAO[2].read_text(encoding="utf-8")

    assert "st.cache_resource" not in campanhas
    assert "st.cache_resource" not in briefings
    assert controlador.count("@st.cache_resource") == 1
    assert "construir_ambiente_aplicacao_em_memoria" in controlador
    assert "_obter_ambiente" in controlador


def test_navegacao_e_contexto_estao_presentes() -> None:
    campanhas = ARQUIVOS_APRESENTACAO[0].read_text(encoding="utf-8")
    briefings = ARQUIVOS_APRESENTACAO[1].read_text(encoding="utf-8")
    controlador = ARQUIVOS_APRESENTACAO[2].read_text(encoding="utf-8")

    assert "Abrir Briefing" in campanhas
    assert "Voltar às Campanhas" in briefings
    assert "id_campanha_briefing_ativa" in controlador
    assert "Estes dados são herdados da Campanha" in briefings
    assert "não são redefinidos no Briefing." in briefings
    assert "A estrutura do Briefing está disponível." in briefings

    subetapas = (
        "1. Situação mercadológica e competitiva",
        "2. Objetivos declarados",
        "3. Praça e universo",
        "4. Segmentos e públicos",
        "5. Jornada",
        "6. Período e verba",
        "7. Prioridades, restrições e pretensões",
        "8. Revisão do Briefing",
    )
    for subetapa in subetapas:
        assert subetapa in briefings


def test_frontoffice_nao_antecipa_conteudo_metodologico() -> None:
    conteudo = "\n".join(
        caminho.read_text(encoding="utf-8") for caminho in ARQUIVOS_APRESENTACAO
    ).lower()
    termos_proibidos = (
        "objetivo de mídia",
        "kpi",
        "alcance",
        "frequência",
        "flight",
        "meios",
        "canais",
        "inventários",
        "distribuição de verba",
        "executar_motor",
        "sql",
    )

    for termo in termos_proibidos:
        assert termo not in conteudo


def test_app_renderiza_sem_excecoes() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py"))

    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    assert any(titulo.value == "Campanhas" for titulo in aplicativo.header)


def test_fluxo_minimo_abre_briefing() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py"))
    aplicativo.run(timeout=5)

    campos = {campo.label: campo for campo in aplicativo.text_input}
    campos["Nome"].set_value("Campanha AppTest")
    campos["Anunciante"].set_value("Anunciante AppTest")
    campos["Planejador Responsável"].set_value("Planejadora AppTest")
    botao = next(
        item
        for item in aplicativo.button
        if item.label == "Criar Campanha e iniciar Briefing"
    )
    botao.click()

    aplicativo.run(timeout=5)

    assert not aplicativo.exception
    conteudo = " ".join(
        item.value
        for grupo in (
            aplicativo.title,
            aplicativo.header,
            aplicativo.subheader,
            aplicativo.markdown,
        )
        for item in grupo
    )
    assert "Briefing de Mídia" in conteudo
    assert "Campanha AppTest" in conteudo
    metricas = {
        metrica.label: str(metrica.value) for metrica in aplicativo.metric
    }
    assert metricas["Versão"] == "1"
    assert metricas["Estado"] == "Rascunho"
