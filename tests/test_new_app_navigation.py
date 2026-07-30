from pathlib import Path

from streamlit.testing.v1 import AppTest

from presentation.navigation import ETAPAS_FUTURAS, NAVEGACAO_INICIAL


def test_navegacao_inicial_e_progressiva():
    assert [item.chave for item in NAVEGACAO_INICIAL] == [
        "inicio",
        "campanha",
        "briefing",
    ]
    assert [item.etapa for item in NAVEGACAO_INICIAL] == [None, 1, 2]
    assert len(ETAPAS_FUTURAS) == 6


def test_nova_entrada_nao_importa_navegacao_ou_servicos_legados():
    entrada = Path("app.py").read_text()
    interface = Path("presentation/streamlit_app.py").read_text()
    codigo = entrada + interface
    assert '"pages/' not in codigo
    assert "application.services" not in codigo
    assert "infrastructure.database" not in codigo


def test_streamlit_inicializa_sem_erro():
    app = AppTest.from_file("app.py").run(timeout=10)
    assert not app.exception
    assert any(
        "Planejamento de mídia com decisões explicáveis" in item.value
        for item in app.markdown
    )
