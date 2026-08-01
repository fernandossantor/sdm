from pathlib import Path

from streamlit.testing.v1 import AppTest

from presentation.campaign_state import iniciar_nova_campanha

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


def test_nova_campanha_limpa_selecao_e_mantem_modo_de_criacao():
    estado = {
        "campanha_id": "campanha-existente",
        "campanha_codigo": "MP-001",
        "campanha_nome": "Existente",
        "campanha_anunciante": "Anunciante",
        "campanha_marca": "Marca",
        "campanha_produto": "Produto",
        "campanha_planejador": "Planejador",
        "campanha_etapa": "ABERTURA",
        "briefing_id": "briefing-existente",
        "espaco_id": "espaco-preservado",
    }

    iniciar_nova_campanha(estado)

    assert estado["campanha_em_criacao"] is True
    assert estado["espaco_id"] == "espaco-preservado"
    assert "campanha_id" not in estado
    assert "briefing_id" not in estado
