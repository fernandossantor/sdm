import ast
from pathlib import Path
from uuid import UUID

import pytest

from mediad_planner.application.dto.briefing import RegistroSituacaoResumo
from mediad_planner.presentation import briefings
from mediad_planner.presentation.briefings import _possui_texto


RAIZ = Path(__file__).resolve().parents[1]
APRESENTACAO = RAIZ / "mediad_planner/presentation"


@pytest.mark.parametrize(
    ("valor", "esperado"),
    (
        (None, False),
        ("", False),
        ("   ", False),
        ("IBGE", True),
    ),
)
def test_possui_texto_omite_somente_atributos_sem_conteudo(
    valor: str | None,
    esperado: bool,
) -> None:
    assert _possui_texto(valor) is esperado


def test_briefing_recolhe_detalhes_e_preserva_formulario() -> None:
    fonte = (APRESENTACAO / "briefings.py").read_text(encoding="utf-8")
    for rotulo in (
        "Contexto herdado da Campanha",
        "Estrutura do Briefing",
        "Registros salvos (",
    ):
        assert rotulo in fonte
    assert fonte.count("expanded=False") >= 3
    assert (
        "A estrutura do Briefing está disponível. O conteúdo metodológico "
        "será implementado incrementalmente."
    ) not in fonte
    for campo in (
        "Fonte dos dados (opcional)",
        "Período de referência (opcional)",
        "Observação complementar (opcional)",
        "Unidade de medida",
    ):
        assert campo in fonte
    assert "Nenhum registro salvo nesta subetapa." in fonte
    assert "registro.unidade.strip()" in fonte


def _registro(**valores: str | None) -> RegistroSituacaoResumo:
    return RegistroSituacaoResumo(
        id_registro=UUID(int=1),
        escopo="MERCADO",
        codigo_aspecto=None,
        aspecto="Participação de mercado",
        entidade_referencia=valores.get("entidade_referencia"),
        natureza="QUANTITATIVO",
        valor_quantitativo="25",
        unidade=valores.get("unidade"),
        valor_qualitativo=valores.get("valor_qualitativo"),
        fonte=valores.get("fonte"),
        periodo_referencia=valores.get("periodo_referencia"),
        observacao=valores.get("observacao"),
    )


def test_registro_salvo_omite_vazios_e_preserva_preenchidos(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    escritos: list[object] = []
    monkeypatch.setattr(briefings.st, "write", escritos.append)

    briefings._detalhar_registro(
        _registro(
            unidade="   ",
            fonte=" ",
            periodo_referencia="",
            observacao=None,
        )
    )
    vazio = " ".join(str(item) for item in escritos)
    assert "Fonte dos dados:" not in vazio
    assert "Período de referência:" not in vazio
    assert "Observação:" not in vazio
    assert "None" not in vazio

    escritos.clear()
    briefings._detalhar_registro(
        _registro(
            unidade=" % ",
            fonte="Pesquisa interna",
            periodo_referencia="2025",
            observacao="Mercado nacional",
        )
    )
    completo = " ".join(str(item) for item in escritos)
    assert "25 %" in completo
    assert "Fonte dos dados: Pesquisa interna" in completo
    assert "Período de referência: 2025" in completo
    assert "Observação: Mercado nacional" in completo


def test_diagnostico_e_obtido_uma_vez_e_recebido_pelas_telas() -> None:
    caminhos = {
        nome: APRESENTACAO / nome
        for nome in (
            "streamlit_app.py",
            "navegacao_global.py",
            "administracao.py",
        )
    }
    arvores = {
        nome: ast.parse(caminho.read_text(encoding="utf-8"))
        for nome, caminho in caminhos.items()
    }
    chamadas = {
        nome: tuple(
            no
            for no in ast.walk(arvore)
            if isinstance(no, ast.Call)
            and isinstance(no.func, ast.Name)
            and no.func.id == "obter_diagnostico_fundacao"
        )
        for nome, arvore in arvores.items()
    }
    assert len(chamadas["streamlit_app.py"]) == 1
    assert chamadas["navegacao_global.py"] == ()
    assert chamadas["administracao.py"] == ()

    navegacao = caminhos["navegacao_global.py"].read_text(encoding="utf-8")
    assert "Sistema: operacional" in navegacao
    assert "Backend e interface conectados" in navegacao
    assert "st.metric" not in navegacao

    administracao = caminhos["administracao.py"].read_text(encoding="utf-8")
    assert "Diagnóstico do sistema" in administracao
    assert "Detalhes técnicos do sistema" in administracao
    assert "expanded=False" in administracao
    assert "Versão do contrato" in administracao
    assert "Motores previstos" in administracao
