import ast
from pathlib import Path


ARQUIVOS = tuple(
    Path("mediad_planner/presentation") / nome
    for nome in (
        "streamlit_app.py",
        "espaco_trabalho.py",
        "visao_geral_campanha.py",
        "campanhas.py",
        "briefings.py",
    )
)


def test_telas_respeitam_fronteiras_e_contem_contrato_visual() -> None:
    fontes = ARQUIVOS + (
        Path("mediad_planner/application/use_cases/espaco_trabalho.py"),
        Path("mediad_planner/presentation/navegacao_global.py"),
        Path("mediad_planner/presentation/administracao.py"),
    )
    conteudo = "\n".join(item.read_text(encoding="utf-8") for item in fontes)
    for caminho in ARQUIVOS:
        arvore = ast.parse(caminho.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if isinstance(no, ast.ImportFrom) and no.module:
                assert not no.module.startswith(
                    (
                        "mediad_planner.domain",
                        "mediad_planner.engines",
                        "mediad_planner.infrastructure",
                    )
                )
    for texto in (
        "Espaço de trabalho",
        "Visão geral da Campanha",
        "Tradução Estratégica",
        "Arquitetura de Mídia",
        "Plano Consolidado",
        "Campanha ativa",
        "Fechar Campanha ativa",
        "Progresso metodológico",
        "Briefing ainda não iniciado.",
        "Inicie o Briefing para continuar.",
        "Conclua o Briefing para continuar.",
        "Selecione o cenário de Simulação que será consolidado.",
    ):
        assert texto in conteudo


def test_apresentacao_nao_decide_disponibilidade_nem_salva_dtos_na_sessao() -> None:
    streamlit = ARQUIVOS[0].read_text(encoding="utf-8")
    roteador = ARQUIVOS[1].read_text(encoding="utf-8")
    assert "etapa_atual ==" not in roteador
    assert "situacao ==" not in roteador
    assert "session_state[CHAVE_CAMPANHA_ATIVA] = str" in streamlit
    assert "session_state[CHAVE_MODULO_ATIVO]" in streamlit
    assert "session_state[CHAVE_CAMPANHA_ATIVA] = resumo" not in streamlit
