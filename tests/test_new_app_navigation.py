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


def test_identidade_visual_usa_novos_ativos():
    interface = Path("presentation/streamlit_app.py").read_text()
    login = Path("components/auth_gate.py").read_text()
    assert Path("assets/favicon2.png").is_file()
    assert Path("assets/Marca_nova.png").is_file()
    assert "page_icon=PAGE_ICON" in interface
    assert 'assets" / "Marca_nova.png"' in interface
    assert 'assets" / "Marca_nova.png"' in login
    assert 'ASSETS_DIR / "favicon2.png"' in Path(
        "components/page_config.py"
    ).read_text()
    assert 'data-testid="stSidebar"' in login
    assert "st.columns([1.25, 1, 1.25])" in login


def test_fluxo_distingue_primeiro_preenchimento_de_edicao():
    interface = Path("presentation/streamlit_app.py").read_text()
    assert '"Preencher briefing"' in interface
    assert '"Editar briefing"' in interface
    assert "briefing_vazio" in interface
    assert 'label="Continuar para o briefing"' in interface
    assert '"Completude do preenchimento"' in interface
    assert '"Enviar para revisão"' not in interface
    assert '"Concluir briefing"' in interface


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
