import ast
from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).resolve().parents[1]
APRESENTACAO = RAIZ / "mediad_planner/presentation"


def _conteudo(aplicativo: AppTest) -> str:
    return " ".join(
        item.value
        for grupo in (
            aplicativo.header,
            aplicativo.subheader,
            aplicativo.markdown,
            aplicativo.caption,
            aplicativo.info,
        )
        for item in grupo
    )


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


def test_barra_global_aparece_sem_campanha_ativa() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py")).run(timeout=5)

    assert not aplicativo.exception
    rotulos = {botao.label for botao in aplicativo.button}
    assert {
        "Campanhas",
        "Bibliotecas",
        "Guia de uso e glossário",
        "Administração",
    } <= rotulos
    assert "Campanha ativa" not in _conteudo(aplicativo)
    assert any(item.value == "Campanhas" for item in aplicativo.header)


def test_paginas_globais_renderizam_conteudo_provisorio_exclusivo() -> None:
    expectativas = {
        "BIBLIOTECAS": "Bibliotecas configuráveis",
        "GUIA_DE_USO": "Guia de uso e glossário",
        "ADMINISTRACAO": "Administração",
    }
    for pagina, titulo in expectativas.items():
        aplicativo = AppTest.from_file(str(RAIZ / "app.py"))
        aplicativo.session_state["pagina_global_ativa"] = pagina
        aplicativo.run(timeout=5)
        assert not aplicativo.exception
        assert titulo in _conteudo(aplicativo)
        assert {botao.label for botao in aplicativo.button} >= {
            "Campanhas",
            "Bibliotecas",
            "Guia de uso e glossário",
            "Administração",
        }


def test_campanha_ativa_e_preservada_e_fechada_somente_por_acao_explicita() -> None:
    aplicativo = AppTest.from_file(str(RAIZ / "app.py")).run(timeout=5)
    campos = {item.label: item for item in aplicativo.text_input}
    campos["Nome da Campanha"].set_value("Campanha Persistente")
    campos["Anunciante"].set_value("Anunciante")
    campos["Planejador Responsável"].set_value("Planejadora")
    next(
        item for item in aplicativo.button
        if item.label == "Salvar como Rascunho"
    ).click()
    aplicativo.run(timeout=5)
    assert "Campanha ativa" in _conteudo(aplicativo)

    next(
        item for item in aplicativo.button if item.label == "Bibliotecas"
    ).click()
    _preservar_formulario(aplicativo)
    aplicativo.run(timeout=5)
    assert "Bibliotecas configuráveis" in _conteudo(aplicativo)
    assert "Campanha ativa" in _conteudo(aplicativo)

    next(
        item for item in aplicativo.button
        if item.label == "Visão geral da Campanha"
    ).click()
    _preservar_formulario(aplicativo)
    aplicativo.run(timeout=5)
    assert any(
        item.value == "Visão geral da Campanha"
        for item in aplicativo.header
    )

    next(
        item for item in aplicativo.button
        if item.label == "Fechar Campanha ativa"
    ).click()
    _preservar_formulario(aplicativo)
    aplicativo.run(timeout=5)
    assert "Campanha ativa" not in _conteudo(aplicativo)
    assert any(item.value == "Campanhas" for item in aplicativo.header)
    assert "Campanha Persistente" in _conteudo(aplicativo)


def test_fronteiras_e_coordenacao_ficam_fora_da_tela_de_campanhas() -> None:
    arquivos = tuple(
        APRESENTACAO / nome
        for nome in (
            "navegacao_global.py",
            "bibliotecas.py",
            "guia_de_uso.py",
            "administracao.py",
        )
    )
    for caminho in arquivos:
        arvore = ast.parse(caminho.read_text(encoding="utf-8"))
        importacoes = tuple(
            no.module
            for no in ast.walk(arvore)
            if isinstance(no, ast.ImportFrom) and no.module
        )
        assert not any(
            modulo.startswith(
                (
                    "mediad_planner.domain",
                    "mediad_planner.engines",
                    "mediad_planner.infrastructure",
                )
            )
            for modulo in importacoes
        )

    campanhas = (APRESENTACAO / "campanhas.py").read_text(encoding="utf-8")
    assert "AplicacaoBriefings" not in campanhas
    assert "abrir_briefing" not in campanhas
    assert "AplicacaoEspacoTrabalho" in campanhas
