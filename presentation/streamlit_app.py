"""Casca Streamlit da nova aplicação, sem regras de domínio."""

from pathlib import Path
from uuid import UUID, uuid4

import streamlit as st

from application.dto import (
    AbrirCampanhaEntrada,
    CorrigirCampanhaEntrada,
    IniciarBriefingEntrada,
)
from components import auth_gate, workspace_gate
from presentation.composition import (
    AuthService,
    autenticacao_habilitada,
    bind_authenticated_client,
    campanhas_do_espaco,
    caso_de_uso_correcao_campanha,
    briefing_da_campanha,
    casos_de_uso_campanha,
)
from presentation.campaign_state import iniciar_nova_campanha
from presentation.navigation import ETAPAS_FUTURAS, NAVEGACAO_INICIAL

MARCA = Path(__file__).parents[1] / "assets" / "Marca.png"


def _aplicar_estilo() -> None:
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light dark;
        }
        .mp-eyebrow {
            color: #ffc29f; font-size: .78rem; font-weight: 700;
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
            label="Cadastrar uma campanha",
            icon=":material/arrow_forward:",
        )
    with coluna_briefing:
        st.markdown("#### 02 · Briefing de mídia")
        st.write("Demandas, limites, prioridades e informações disponíveis.")
        st.page_link(
            PAGINAS[2],
            label="Iniciar um briefing",
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
    if not _contexto_operacional_pronto():
        st.info("Entre e selecione um espaço de trabalho para criar campanhas.")
        return
    try:
        campanhas = campanhas_do_espaco(st.session_state)
    except Exception as exc:
        st.error(f"Não foi possível carregar as campanhas: {exc}")
        return
    if campanhas and not st.session_state.get("campanha_em_criacao"):
        ids = [str(item["id"]) for item in campanhas]
        atual = st.session_state.get("campanha_id")
        indice = ids.index(atual) if atual in ids else 0
        selecionada = st.selectbox(
            "Campanha para continuar",
            campanhas,
            index=indice,
            format_func=lambda item: "{} · {}".format(item["codigo"], item["nome"]),
        )
        if str(selecionada["id"]) != st.session_state.get("campanha_id"):
            for chave, campo in (
                ("campanha_id", "id"),
                ("campanha_codigo", "codigo"),
                ("campanha_nome", "nome"),
                ("campanha_anunciante", "nome_anunciante_atual"),
                ("campanha_marca", "nome_marca_atual"),
                ("campanha_produto", "nome_produto_servico_atual"),
                ("campanha_planejador", "identificacao_planejador_atual"),
                ("campanha_etapa", "etapa_atual"),
                ("campanha_anunciante_id", "anunciante_id"),
                ("campanha_marca_id", "marca_id"),
                ("campanha_produto_id", "produto_servico_id"),
                ("campanha_observacao", "observacao_inicial"),
            ):
                st.session_state[chave] = selecionada.get(campo)
            st.session_state["briefing_id"] = briefing_da_campanha(
                st.session_state, selecionada["id"]
            )
            st.rerun()
    if st.session_state.get("campanha_id"):
        st.success(
            f"Campanha {st.session_state['campanha_codigo']} criada e preservada."
        )
        st.write(st.session_state["campanha_nome"])
        if st.button("Editar campanha"):
            st.session_state["campanha_em_edicao"] = True
        if st.session_state.get("campanha_em_edicao"):
            with st.form("edicao_campanha"):
                esquerda, direita = st.columns(2)
                with esquerda:
                    nome_editado = st.text_input(
                        "Nome da campanha",
                        value=st.session_state.get("campanha_nome", ""),
                        key="edicao_campanha_nome",
                    )
                    anunciante_editado = st.text_input(
                        "Anunciante",
                        value=st.session_state.get("campanha_anunciante", ""),
                        key="edicao_campanha_anunciante",
                    )
                    marca_editada = st.text_input(
                        "Marca (opcional)",
                        value=st.session_state.get("campanha_marca") or "",
                        key="edicao_campanha_marca",
                    )
                with direita:
                    produto_editado = st.text_input(
                        "Produto ou serviço (opcional)",
                        value=st.session_state.get("campanha_produto") or "",
                        key="edicao_campanha_produto",
                    )
                    planejador_nome = (
                        st.session_state.get("auth_nome")
                        or st.session_state.get("auth_email", "")
                    )
                    st.text_input(
                        "Planejador responsável",
                        value=planejador_nome,
                        disabled=True,
                        key="edicao_campanha_planejador",
                    )
                    observacao_editada = st.text_area(
                        "Observação inicial (opcional)",
                        value=st.session_state.get("campanha_observacao") or "",
                        key="edicao_campanha_observacao",
                    )
                motivo = st.text_input(
                    "Motivo da correção",
                    key="edicao_campanha_motivo",
                )
                salvar_edicao = st.form_submit_button(
                    "Salvar correções", type="primary"
                )
            if salvar_edicao:
                try:
                    anunciante_anterior = st.session_state.get(
                        "campanha_anunciante"
                    )
                    marca_anterior = st.session_state.get("campanha_marca")
                    produto_anterior = st.session_state.get("campanha_produto")
                    entrada = CorrigirCampanhaEntrada(
                        campanha_id=UUID(st.session_state["campanha_id"]),
                        nome=nome_editado,
                        anunciante_id=(
                            UUID(st.session_state["campanha_anunciante_id"])
                            if anunciante_editado == anunciante_anterior
                            else uuid4()
                        ),
                        nome_anunciante=anunciante_editado,
                        marca_id=(
                            UUID(st.session_state["campanha_marca_id"])
                            if marca_editada
                            and marca_editada == (marca_anterior or "")
                            and st.session_state.get("campanha_marca_id")
                            else (uuid4() if marca_editada.strip() else None)
                        ),
                        nome_marca=marca_editada.strip() or None,
                        produto_servico_id=(
                            UUID(st.session_state["campanha_produto_id"])
                            if produto_editado
                            and produto_editado == (produto_anterior or "")
                            and st.session_state.get("campanha_produto_id")
                            else (uuid4() if produto_editado.strip() else None)
                        ),
                        nome_produto_servico=produto_editado.strip() or None,
                        planejador_responsavel_id=UUID(
                            st.session_state["auth_user_id"]
                        ),
                        identificacao_planejador=planejador_nome,
                        alterado_por=UUID(st.session_state["auth_user_id"]),
                        motivo=motivo,
                        observacao_inicial=observacao_editada.strip() or None,
                    )
                    caso_de_uso_correcao_campanha(
                        st.session_state
                    ).executar(entrada)
                except Exception as exc:
                    st.error(f"Não foi possível corrigir a campanha: {exc}")
                else:
                    st.session_state["campanha_nome"] = nome_editado.strip()
                    st.session_state["campanha_anunciante"] = (
                        anunciante_editado.strip()
                    )
                    st.session_state["campanha_marca"] = (
                        marca_editada.strip() or None
                    )
                    st.session_state["campanha_produto"] = (
                        produto_editado.strip() or None
                    )
                    st.session_state["campanha_planejador"] = planejador_nome
                    st.session_state["campanha_observacao"] = (
                        observacao_editada.strip() or None
                    )
                    st.session_state.pop("campanha_em_edicao", None)
                    st.success("Correções salvas com rastreabilidade.")
                    st.rerun()
            if st.button("Cancelar edição"):
                st.session_state.pop("campanha_em_edicao", None)
                st.rerun()
        if st.button("Nova campanha"):
            iniciar_nova_campanha(st.session_state)
            st.rerun()
        if st.session_state.get("briefing_id"):
            st.page_link(
                PAGINAS[2],
                label="Continuar para o briefing",
                icon=":material/arrow_forward:",
            )
        if not st.session_state.get("briefing_id") and st.button(
            "Iniciar briefing", type="primary"
        ):
            try:
                _, iniciar = casos_de_uso_campanha(st.session_state)
                saida = iniciar.executar(
                    IniciarBriefingEntrada(
                        campanha_id=UUID(st.session_state["campanha_id"]),
                        usuario_id=UUID(st.session_state["auth_user_id"]),
                    )
                )
            except Exception as exc:
                st.error(f"Não foi possível iniciar o briefing: {exc}")
            else:
                st.session_state["briefing_id"] = str(saida.briefing.id)
                st.session_state["campanha_etapa"] = saida.campanha.etapa_atual.value
                st.success("Briefing iniciado.")
        return
    if st.session_state.get("campanha_em_criacao"):
        st.info("Criando uma nova campanha. As campanhas existentes foram preservadas.")
        if st.button("Cancelar nova campanha"):
            st.session_state.pop("campanha_em_criacao", None)
            st.rerun()
    st.subheader("Informações da abertura")
    with st.form("abertura_campanha"):
        esquerda, direita = st.columns(2)
        with esquerda:
            nome = st.text_input("Nome da campanha")
            anunciante = st.text_input("Anunciante")
            marca = st.text_input("Marca (opcional)")
        with direita:
            produto = st.text_input("Produto ou serviço (opcional)")
            st.text_input(
                "Planejador responsável",
                value=(
                    st.session_state.get("espaco_planejador_padrao_nome")
                    or st.session_state.get("auth_email", "")
                ),
                disabled=True,
            )
            observacao = st.text_area("Observação inicial (opcional)")
        criar = st.form_submit_button("Criar campanha", type="primary")
    if criar:
        try:
            usuario_id = UUID(st.session_state["auth_user_id"])
            planejador_id = UUID(
                st.session_state.get("espaco_planejador_padrao_id")
                or st.session_state["auth_user_id"]
            )
            abrir, _ = casos_de_uso_campanha(st.session_state)
            saida = abrir.executar(
                AbrirCampanhaEntrada(
                    nome=nome,
                    anunciante_id=uuid4(),
                    nome_anunciante=anunciante,
                    marca_id=uuid4() if marca.strip() else None,
                    nome_marca=marca.strip() or None,
                    produto_servico_id=uuid4() if produto.strip() else None,
                    nome_produto_servico=produto.strip() or None,
                    planejador_responsavel_id=planejador_id,
                    identificacao_planejador=(
                        st.session_state.get("espaco_planejador_padrao_nome")
                        or st.session_state.get("auth_email")
                        or str(planejador_id)
                    ),
                    criado_por=usuario_id,
                    observacao_inicial=observacao.strip() or None,
                )
            )
        except Exception as exc:
            st.error(f"Não foi possível criar a campanha: {exc}")
        else:
            st.session_state["campanha_id"] = str(saida.campanha.id)
            st.session_state["campanha_codigo"] = saida.campanha.codigo
            st.session_state["campanha_nome"] = saida.campanha.nome
            st.session_state["campanha_anunciante"] = (
                saida.campanha.snapshot.nome_anunciante
            )
            st.session_state["campanha_anunciante_id"] = str(
                saida.campanha.anunciante_id
            )
            st.session_state["campanha_marca"] = saida.campanha.snapshot.nome_marca
            st.session_state["campanha_marca_id"] = (
                str(saida.campanha.marca_id) if saida.campanha.marca_id else None
            )
            st.session_state["campanha_produto"] = (
                saida.campanha.snapshot.nome_produto_servico
            )
            st.session_state["campanha_produto_id"] = (
                str(saida.campanha.produto_servico_id)
                if saida.campanha.produto_servico_id
                else None
            )
            st.session_state["campanha_planejador"] = (
                saida.campanha.snapshot.identificacao_planejador
            )
            st.session_state["campanha_observacao"] = (
                saida.campanha.observacao_inicial
            )
            st.session_state["campanha_etapa"] = saida.campanha.etapa_atual.value
            st.session_state.pop("campanha_em_criacao", None)
            st.rerun()


def pagina_briefing() -> None:
    _cabecalho(
        "Etapa 02",
        "Briefing de mídia",
        "Estruture progressivamente as demandas da campanha, preservando "
        "ausências, restrições e contradições.",
    )
    try:
        campanhas = campanhas_do_espaco(st.session_state)
    except Exception as exc:
        st.error(f"Não foi possível carregar as campanhas: {exc}")
        return
    if campanhas:
        ids = [str(item["id"]) for item in campanhas]
        atual = st.session_state.get("campanha_id")
        indice = ids.index(atual) if atual in ids else 0
        selecionada = st.selectbox(
            "Briefing da campanha",
            campanhas,
            index=indice,
            format_func=lambda item: "{} · {}".format(item["codigo"], item["nome"]),
            key="briefing_campanha_selecionada",
        )
        if str(selecionada["id"]) != st.session_state.get("campanha_id"):
            for chave, campo in (
                ("campanha_id", "id"),
                ("campanha_codigo", "codigo"),
                ("campanha_nome", "nome"),
                ("campanha_anunciante", "nome_anunciante_atual"),
                ("campanha_marca", "nome_marca_atual"),
                ("campanha_produto", "nome_produto_servico_atual"),
                ("campanha_planejador", "identificacao_planejador_atual"),
                ("campanha_etapa", "etapa_atual"),
                ("campanha_anunciante_id", "anunciante_id"),
                ("campanha_marca_id", "marca_id"),
                ("campanha_produto_id", "produto_servico_id"),
                ("campanha_observacao", "observacao_inicial"),
            ):
                st.session_state[chave] = selecionada.get(campo)
            st.session_state["briefing_id"] = briefing_da_campanha(
                st.session_state, selecionada["id"]
            )
            st.rerun()
    if not st.session_state.get("campanha_id"):
        st.warning("Crie uma campanha antes de abrir o Briefing.")
        return
    st.subheader("1. Contexto herdado da Campanha")
    st.caption(
        "Estas informações são um snapshot administrativo e não podem ser "
        "redefinidas no Briefing."
    )
    contexto = {
        "Código": st.session_state.get("campanha_codigo", "—"),
        "Campanha": st.session_state.get("campanha_nome", "—"),
        "Anunciante": st.session_state.get("campanha_anunciante", "—"),
        "Marca": st.session_state.get("campanha_marca") or "Não informado",
        "Produto ou serviço": st.session_state.get("campanha_produto")
        or "Não informado",
        "Planejador responsável": st.session_state.get("campanha_planejador", "—"),
    }
    colunas = st.columns(3)
    for indice, (rotulo, valor) in enumerate(contexto.items()):
        with colunas[indice % 3]:
            st.text_input(rotulo, value=valor, disabled=True)
    if not st.session_state.get("briefing_id"):
        st.warning("Crie uma campanha e inicie o briefing na etapa anterior.")
        return
    st.success(
        f"Briefing {st.session_state['briefing_id']} vinculado à campanha "
        f"{st.session_state['campanha_codigo']}."
    )
    st.page_link(
        PAGINAS[3],
        label="Continuar para Tradução estratégica",
        icon=":material/arrow_forward:",
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


def pagina_traducao():
    _cabecalho(
        "Etapa 03",
        "Tradução estratégica",
        "Transforme o briefing em problemas, objetivos e critérios de decisão.",
    )
    if not st.session_state.get("campanha_id") or not st.session_state.get(
        "briefing_id"
    ):
        st.warning("Selecione uma campanha com briefing iniciado antes de continuar.")
        return
    st.success(
        "Campanha {} pronta para a tradução estratégica.".format(
            st.session_state.get("campanha_codigo", "—")
        )
    )
    st.info("Esta etapa será construída progressivamente a partir do briefing salvo.")


PAGINAS = (
    st.Page(
        pagina_inicio,
        title=NAVEGACAO_INICIAL[0].titulo,
        icon="🏠",
        default=True,
    ),
    st.Page(pagina_campanha, title=NAVEGACAO_INICIAL[1].titulo, icon="📁"),
    st.Page(pagina_briefing, title=NAVEGACAO_INICIAL[2].titulo, icon="📋"),
    st.Page(pagina_traducao, title="Tradução estratégica", icon="🧭"),
)


def _contexto_operacional_pronto() -> bool:
    return bool(
        st.session_state.get("auth_user_id")
        and st.session_state.get("auth_access_token")
        and st.session_state.get("espaco_id")
    )


def executar() -> None:
    st.set_page_config(
        page_title="MediAd Planner",
        page_icon="📐",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _aplicar_estilo()
    navegacao = st.navigation(list(PAGINAS), position="hidden")
    if autenticacao_habilitada():
        if not auth_gate.render():
            return
        bind_authenticated_client(st.session_state["auth_access_token"])
        if not workspace_gate.render():
            return
    with st.sidebar:
        if MARCA.exists():
            st.image(MARCA, width=220)
        st.caption("Planejamento inteligente de mídia")
        st.divider()
        st.caption("FLUXO INICIAL")
        for pagina in PAGINAS:
            st.page_link(pagina, label=pagina.title, icon=pagina.icon)
        st.divider()
        if autenticacao_habilitada():
            st.caption(st.session_state.get("auth_email", ""))
            if st.button("Sair"):
                AuthService().sair(st.session_state)
                st.rerun()
            st.divider()
        st.caption("Nova arquitetura · Fundação em construção")
    navegacao.run()
