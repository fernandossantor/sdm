"""Casca Streamlit da nova aplicação, sem regras de domínio."""

from pathlib import Path

import streamlit as st

from presentation.navigation import ETAPAS_FUTURAS, NAVEGACAO_INICIAL

MARCA = Path(__file__).parents[1] / "assets" / "Marca.png"


def _aplicar_estilo() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #f7f8fa; }
        [data-testid="stSidebar"] { background: #101d2f; }
        [data-testid="stSidebar"] * { color: #f5f7fa; }
        .mp-eyebrow {
            color: #b25f32; font-size: .78rem; font-weight: 700;
            letter-spacing: .09em; text-transform: uppercase;
        }
        .mp-hero {
            background: linear-gradient(125deg, #10233c, #1d4860);
            border-radius: 18px; color: white; margin-bottom: 1.5rem;
            padding: 2rem 2.2rem;
        }
        .mp-hero h1 { color: white; margin: .25rem 0 .6rem; }
        .mp-hero p { color: #dbe7ec; margin: 0; max-width: 48rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _cabecalho(sobretitulo: str, titulo: str, descricao: str) -> None:
    st.markdown(
        f"""
        <section class="mp-hero">
          <div class="mp-eyebrow">{sobretitulo}</div>
          <h1>{titulo}</h1>
          <p>{descricao}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def pagina_inicio() -> None:
    _cabecalho(
        "MediAd Planner",
        "Planejamento de mídia com decisões explicáveis",
        "Uma jornada progressiva da abertura da campanha ao acompanhamento "
        "de resultados, sustentada por contratos e motores especialistas.",
    )
    st.subheader("Comece pelo contexto")
    st.write(
        "A nova experiência inicia com a identificação da campanha e avança "
        "para um briefing estruturado. Nenhum cálculo é executado nesta etapa."
    )
    coluna_campanha, coluna_briefing = st.columns(2)
    with coluna_campanha:
        st.markdown("#### 01 · Abertura da campanha")
        st.write("Identidade, responsáveis, vínculos e contexto inicial.")
        st.page_link(
            PAGINAS[1],
            label="Revisar abertura",
            icon=":material/arrow_forward:",
        )
    with coluna_briefing:
        st.markdown("#### 02 · Briefing de mídia")
        st.write("Demandas, limites, prioridades e informações disponíveis.")
        st.page_link(
            PAGINAS[2],
            label="Conhecer o briefing",
            icon=":material/arrow_forward:",
        )
    st.divider()
    st.caption("Próximas etapas do fluxo")
    st.write("  →  ".join(ETAPAS_FUTURAS))


def pagina_campanha() -> None:
    _cabecalho(
        "Etapa 01",
        "Abertura da campanha",
        "Crie o contexto inicial do planejamento antes de qualquer decisão "
        "estratégica ou cálculo.",
    )
    st.info(
        "Esta fatia apresenta o contrato da etapa. A gravação será habilitada "
        "quando autorização e persistência canônicas estiverem conectadas.",
        icon="ℹ️",
    )
    st.subheader("Informações da abertura")
    esquerda, direita = st.columns(2)
    with esquerda:
        st.text_input("Nome da campanha", disabled=True)
        st.text_input("Anunciante", disabled=True)
        st.text_input("Marca (opcional)", disabled=True)
    with direita:
        st.text_input("Produto ou serviço (opcional)", disabled=True)
        st.text_input("Planejador responsável", disabled=True)
        st.text_area("Observação inicial (opcional)", disabled=True)
    st.button(
        "Criar campanha",
        type="primary",
        disabled=True,
        help="Disponível após a conexão da camada de persistência.",
    )


def pagina_briefing() -> None:
    _cabecalho(
        "Etapa 02",
        "Briefing de mídia",
        "Estruture progressivamente as demandas da campanha, preservando "
        "ausências, restrições e contradições.",
    )
    st.warning(
        "O briefing será habilitado após a criação de uma campanha.",
        icon="⚠️",
    )
    secoes = (
        ("1", "Contexto e situação"),
        ("2", "Objetivos e resultados"),
        ("3", "Públicos e praças"),
        ("4", "Período, verba e restrições"),
        ("5", "Prioridades e informações disponíveis"),
    )
    for numero, titulo in secoes:
        with st.expander(f"{numero}. {titulo}"):
            st.caption("Seção prevista no fluxo progressivo do briefing.")


PAGINAS = (
    st.Page(
        pagina_inicio,
        title=NAVEGACAO_INICIAL[0].titulo,
        icon="🏠",
        default=True,
    ),
    st.Page(pagina_campanha, title=NAVEGACAO_INICIAL[1].titulo, icon="📁"),
    st.Page(pagina_briefing, title=NAVEGACAO_INICIAL[2].titulo, icon="📋"),
)


def executar() -> None:
    st.set_page_config(
        page_title="MediAd Planner",
        page_icon="📐",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _aplicar_estilo()
    with st.sidebar:
        if MARCA.exists():
            st.image(MARCA, width=220)
        st.caption("Planejamento inteligente de mídia")
        st.divider()
        st.caption("FLUXO INICIAL")
        for pagina in PAGINAS:
            st.page_link(pagina, label=pagina.title, icon=pagina.icon)
        st.divider()
        st.caption("Nova arquitetura · Fundação em construção")
    st.navigation(list(PAGINAS), position="hidden").run()
