"""Casca Streamlit da nova aplicação, sem regras de domínio."""

from pathlib import Path
from uuid import UUID, uuid4

import streamlit as st

from application.dto import (
    AbrirCampanhaEntrada,
    CorrigirCampanhaEntrada,
    CriarVersaoBriefingEntrada,
    EditarBriefingEntrada,
    IniciarBriefingEntrada,
    TransicionarBriefingEntrada,
)
from domain.briefing import ConteudoBriefing, EstadoBriefing, avaliar_briefing
from components import auth_gate, workspace_gate
from components.page_config import PAGE_ICON
from presentation.composition import (
    AuthService,
    autenticacao_habilitada,
    bind_authenticated_client,
    campanhas_do_espaco,
    caso_de_uso_correcao_campanha,
    briefing_da_campanha,
    briefing_atual,
    casos_de_uso_briefing,
    casos_de_uso_campanha,
    versoes_briefing,
)
from presentation.campaign_state import iniciar_nova_campanha
from presentation.navigation import ETAPAS_FUTURAS, NAVEGACAO_INICIAL

MARCA = Path(__file__).parents[1] / "assets" / "Marca_nova.png"


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
    if MARCA.exists():
        st.image(MARCA, width=220)
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
                st.session_state["briefing_recém_criado"] = True
                st.rerun()
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
    try:
        briefing = briefing_atual(st.session_state, st.session_state["briefing_id"])
        historico = versoes_briefing(
            st.session_state, st.session_state["campanha_id"]
        )
    except Exception as exc:
        st.error(f"Não foi possível carregar o conteúdo do briefing: {exc}")
        return
    if briefing is None:
        st.error("O briefing selecionado não foi encontrado.")
        return
    st.caption(
        f"Versão {briefing.versao} · {briefing.estado.value.replace('_', ' ').title()}"
    )
    if st.session_state.pop("briefing_recém_criado", False):
        st.success("Briefing criado. Inicie agora o primeiro preenchimento.")
    pode_editar = briefing.estado in {
        EstadoBriefing.RASCUNHO, EstadoBriefing.EM_PREENCHIMENTO
    }
    briefing_vazio = briefing.conteudo == ConteudoBriefing()
    acao_editar, acao_criar = st.columns(2)
    with acao_editar:
        rotulo_edicao = (
            "Preencher briefing"
            if briefing.estado is EstadoBriefing.RASCUNHO and briefing_vazio
            else "Editar briefing"
        )
        if st.button(rotulo_edicao, disabled=not pode_editar, type="primary"):
            st.session_state["briefing_em_edicao"] = True
    with acao_criar:
        if st.button("Criar nova versão", disabled=briefing_vazio):
            st.session_state["briefing_em_edicao"] = True
            st.session_state["briefing_nova_versao"] = True
    if briefing_vazio:
        st.info(
            "Este Briefing ainda não foi preenchido. Use Preencher briefing "
            "para registrar sua primeira versão de conteúdo."
        )
    if not pode_editar:
        st.info(
            "Esta versão não admite sobrescrita. Use Criar nova versão para "
            "preservar o histórico."
        )
    if historico:
        with st.expander("Histórico de versões"):
            st.dataframe(historico, hide_index=True, use_container_width=True)
    conteudo = briefing.conteudo
    avaliacao = avaliar_briefing(conteudo)
    st.subheader("Avaliação do Briefing")
    st.progress(avaliacao.percentual_completude / 100)
    st.caption(f"{avaliacao.percentual_completude}% dos critérios mínimos atendidos")
    if avaliacao.pendencias:
        with st.expander(
            f"Pendências para revisão ({len(avaliacao.pendencias)})",
            expanded=True,
        ):
            for pendencia in avaliacao.pendencias:
                st.warning(pendencia)
    else:
        st.success("Briefing apto para ser enviado à revisão.")
    for alerta in avaliacao.alertas:
        st.info(alerta)
    if briefing.estado is EstadoBriefing.EM_PREENCHIMENTO:
        with st.form("enviar_briefing_revisao"):
            motivo_revisao = st.text_input("Motivo do envio à revisão")
            enviar_revisao = st.form_submit_button(
                "Enviar para revisão",
                type="primary",
                disabled=not avaliacao.apto_para_revisao,
            )
        if enviar_revisao:
            try:
                _, _, revisar, _ = casos_de_uso_briefing(st.session_state)
                revisar.executar(TransicionarBriefingEntrada(
                    briefing_id=briefing.id,
                    usuario_id=UUID(st.session_state["auth_user_id"]),
                    motivo=motivo_revisao,
                ))
            except Exception as exc:
                st.error(f"Não foi possível enviar à revisão: {exc}")
            else:
                st.success("Briefing enviado para revisão.")
                st.rerun()
    elif briefing.estado is EstadoBriefing.EM_REVISAO:
        with st.form("concluir_briefing"):
            reconhecidos = ()
            if avaliacao.alertas:
                reconhecer = st.checkbox(
                    "Li e reconheço todos os alertas apresentados"
                )
                if reconhecer:
                    reconhecidos = avaliacao.alertas
            motivo_conclusao = st.text_input("Motivo da conclusão")
            concluir = st.form_submit_button(
                "Concluir briefing",
                type="primary",
                disabled=bool(avaliacao.alertas) and not reconhecidos,
            )
        if concluir:
            try:
                _, _, _, concluir_caso = casos_de_uso_briefing(
                    st.session_state
                )
                concluir_caso.executar(TransicionarBriefingEntrada(
                    briefing_id=briefing.id,
                    usuario_id=UUID(st.session_state["auth_user_id"]),
                    motivo=motivo_conclusao,
                    alertas_reconhecidos=reconhecidos,
                ))
            except Exception as exc:
                st.error(f"Não foi possível concluir o briefing: {exc}")
            else:
                st.session_state["campanha_etapa"] = "TRADUCAO_ESTRATEGICA"
                st.success("Briefing concluído. Tradução Estratégica liberada.")
                st.rerun()
    elif briefing.estado is EstadoBriefing.CONCLUIDO:
        st.success("Briefing concluído e preservado.")
        st.page_link(
            PAGINAS[3],
            label="Continuar para Tradução estratégica",
            icon=":material/arrow_forward:",
        )
    with st.expander("Resumo do conteúdo salvo", expanded=False):
        st.json(conteudo.model_dump(mode="json"), expanded=False)
    if st.session_state.get("briefing_em_edicao"):
        with st.form("conteudo_briefing"):
            abas = st.tabs([
                "Situação", "Objetivos", "Praça e públicos",
                "Jornada", "Período e verba", "Restrições e pretensões",
            ])
            with abas[0]:
                situacao = st.text_area(
                    "Situação mercadológica e competitiva",
                    value=conteudo.situacao_mercadologica.get("descricao", ""),
                )
            with abas[1]:
                marketing = st.multiselect(
                    "Objetivos de marketing declarados",
                    ["Branding", "Posicionamento", "Segmentação", "Diferenciação",
                     "Crescimento", "Participação de mercado", "Fidelização",
                     "Penetração", "Desenvolvimento de produto", "Diversificação"],
                    default=[i.get("categoria") for i in conteudo.objetivos_marketing],
                )
                comunicacao = st.multiselect(
                    "Objetivos de comunicação declarados",
                    ["notoriedade", "conhecimento", "lembrança", "compreensão",
                     "imagem", "diferenciação percebida", "persuasão", "preferência",
                     "consideração", "engajamento", "experimentação", "ação",
                     "relacionamento", "fidelização", "recomendação"],
                    default=[i.get("categoria") for i in conteudo.objetivos_comunicacao],
                )
                relacao_objetivos = st.text_area(
                    "Relação entre objetivos de marketing e comunicação",
                    value="\n".join(
                        i.get("descricao", "")
                        for i in conteudo.relacoes_objetivos
                    ),
                )
            with abas[2]:
                pracas = st.text_input(
                    "Praças (separadas por ponto e vírgula)",
                    value="; ".join(i.get("nome", "") for i in conteudo.pracas),
                )
                universos = st.text_input(
                    "Universos de referência (separados por ponto e vírgula)",
                    value="; ".join(i.get("nome", "") for i in conteudo.universos),
                )
                criterios_segmentacao = st.multiselect(
                    "Critérios de segmentação",
                    ["geográfica", "demográfica", "socioeconômica",
                     "psicográfica", "comportamental", "consumo",
                     "relacionamento com a categoria",
                     "relacionamento com a marca", "jornada", "intenção",
                     "contexto"],
                    default=list(conteudo.criterios_segmentacao),
                )
                segmentos = st.text_input(
                    "Segmentos (separados por ponto e vírgula)",
                    value="; ".join(i.get("nome", "") for i in conteudo.segmentos),
                )
                publicos = st.text_input(
                    "Públicos declarados (separados por ponto e vírgula)",
                    value="; ".join(i.get("nome", "") for i in conteudo.publicos),
                )
            with abas[3]:
                jornada_aplicavel = st.checkbox(
                    "A jornada é aplicável a esta campanha",
                    value=conteudo.jornada_aplicavel is not False,
                )
                jornada = st.text_area(
                    "Jornadas e etapas declaradas",
                    value="\n".join(i.get("descricao", "") for i in conteudo.jornadas),
                )
            with abas[4]:
                inicio = st.text_input(
                    "Data inicial pretendida", value=conteudo.periodo.get("inicio", "")
                )
                fim = st.text_input(
                    "Data final pretendida", value=conteudo.periodo.get("fim", "")
                )
                valor = st.number_input(
                    "Verba total", min_value=0.0,
                    value=float(conteudo.verba.get("valor_total") or 0),
                )
                natureza = st.selectbox(
                    "Natureza do limite", ["rígido", "flexível", "estimado",
                    "ainda não definido"],
                    index=["rígido", "flexível", "estimado", "ainda não definido"].index(
                        conteudo.verba.get("natureza", "ainda não definido")
                    ),
                )
            with abas[5]:
                prioridades = st.text_area(
                    "Prioridades declaradas (uma por linha)",
                    value="\n".join(
                        i.get("descricao", "") for i in conteudo.prioridades
                    ),
                )
                restricoes = st.text_area(
                    "Restrições declaradas (uma por linha)",
                    value="\n".join(i.get("descricao", "") for i in conteudo.restricoes),
                )
                pretensoes = st.text_area(
                    "Pretensões declaradas (uma por linha)",
                    value="\n".join(i.get("categoria", "") for i in conteudo.pretensoes),
                )
                sem_restricoes = st.checkbox(
                    "Declaro que não há restrições conhecidas",
                    value=conteudo.sem_restricoes_declaradas,
                    disabled=bool(restricoes.strip()),
                )
                fontes = st.text_area(
                    "Fontes e períodos de referência (uma por linha)",
                    value="\n".join(
                        i.get("descricao", "") for i in conteudo.fontes
                    ),
                )
            motivo = st.text_input("Motivo da alteração")
            salvar = st.form_submit_button(
                "Criar versão" if st.session_state.get("briefing_nova_versao")
                else "Salvar edição", type="primary"
            )
        if salvar:
            def itens(texto):
                return tuple(item.strip() for item in texto.split(";") if item.strip())
            novo = ConteudoBriefing(
                situacao_mercadologica={"descricao": situacao.strip()},
                objetivos_marketing=tuple({"categoria": i} for i in marketing),
                objetivos_comunicacao=tuple({"categoria": i} for i in comunicacao),
                relacoes_objetivos=tuple(
                    {"descricao": i.strip()}
                    for i in relacao_objetivos.splitlines() if i.strip()
                ),
                pracas=tuple({"nome": i} for i in itens(pracas)),
                universos=tuple({"nome": i} for i in itens(universos)),
                criterios_segmentacao=tuple(criterios_segmentacao),
                segmentos=tuple({"nome": i} for i in itens(segmentos)),
                publicos=tuple({"nome": i} for i in itens(publicos)),
                jornadas=tuple({"descricao": i.strip()} for i in jornada.splitlines() if i.strip()),
                jornada_aplicavel=jornada_aplicavel,
                periodo={"inicio": inicio.strip(), "fim": fim.strip()},
                verba={"valor_total": valor, "moeda": "BRL", "natureza": natureza},
                prioridades=tuple(
                    {"descricao": i.strip()}
                    for i in prioridades.splitlines() if i.strip()
                ),
                restricoes=tuple({"descricao": i.strip()} for i in restricoes.splitlines() if i.strip()),
                sem_restricoes_declaradas=sem_restricoes,
                pretensoes=tuple({"categoria": i.strip()} for i in pretensoes.splitlines() if i.strip()),
                fontes=tuple(
                    {"descricao": i.strip()}
                    for i in fontes.splitlines() if i.strip()
                ),
            )
            try:
                editar, versionar, _, _ = casos_de_uso_briefing(
                    st.session_state
                )
                usuario_id = UUID(st.session_state["auth_user_id"])
                if st.session_state.get("briefing_nova_versao"):
                    salvo = versionar.executar(CriarVersaoBriefingEntrada(
                        briefing_id_origem=briefing.id, usuario_id=usuario_id,
                        conteudo=novo, motivo=motivo,
                    ))
                    st.session_state["briefing_id"] = str(salvo.id)
                else:
                    editar.executar(EditarBriefingEntrada(
                        briefing_id=briefing.id, usuario_id=usuario_id,
                        conteudo=novo, motivo=motivo,
                    ))
            except Exception as exc:
                st.error(f"Não foi possível salvar o briefing: {exc}")
            else:
                st.session_state.pop("briefing_em_edicao", None)
                st.session_state.pop("briefing_nova_versao", None)
                st.success("Briefing salvo com rastreabilidade.")
                st.rerun()


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
        page_icon=PAGE_ICON,
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
