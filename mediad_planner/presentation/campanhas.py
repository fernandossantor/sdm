import streamlit as st

from mediad_planner.application.dto.campanha import (
    CampanhaResumo,
    CriarCampanhaEntrada,
)
from mediad_planner.application.services.aplicacao_campanhas import (
    AplicacaoCampanhas,
)
from mediad_planner.composition.campanhas import (
    construir_aplicacao_campanhas_em_memoria,
)


@st.cache_resource
def _obter_aplicacao() -> AplicacaoCampanhas:
    return construir_aplicacao_campanhas_em_memoria()


def _rotulo_situacao(valor: str) -> str:
    rotulos = {
        "RASCUNHO": "Rascunho",
        "EM_ANDAMENTO": "Em andamento",
        "CONCLUIDA": "Concluída",
        "CANCELADA": "Cancelada",
        "ARQUIVADA": "Arquivada",
    }
    return rotulos[valor]


def _rotulo_etapa(valor: str) -> str:
    rotulos = {
        "ABERTURA": "Abertura",
        "BRIEFING": "Briefing",
        "TRADUCAO_ESTRATEGICA": "Tradução Estratégica",
        "ARQUITETURA_DE_MIDIA": "Arquitetura de Mídia",
        "SIMULACAO": "Simulação",
        "CONSOLIDACAO_DO_PLANO": "Consolidação do Plano",
        "VALIDACAO_E_APROVACAO": "Validação e Aprovação",
        "ACOMPANHAMENTO_E_RESULTADOS": "Acompanhamento e Resultados",
    }
    return rotulos[valor]


def _criar_entrada(
    nome: str,
    anunciante: str,
    marca: str,
    produto_servico: str,
    planejador: str,
    equipe: str,
    observacao: str,
    iniciar_briefing: bool,
) -> CriarCampanhaEntrada:
    return CriarCampanhaEntrada(
        nome=nome,
        nome_anunciante=anunciante,
        nome_marca=marca or None,
        nome_produto_servico=produto_servico or None,
        nome_planejador_responsavel=planejador,
        nomes_equipe=tuple(equipe.splitlines()),
        observacao_inicial=observacao or None,
        iniciar_briefing=iniciar_briefing,
    )


def _apresentar_campanha(
    aplicacao: AplicacaoCampanhas,
    campanha: CampanhaResumo,
) -> None:
    with st.container(border=True):
        st.subheader(campanha.identificacao_completa)
        codigo, situacao, etapa = st.columns(3)
        codigo.write(f"**Código:** {campanha.codigo}")
        situacao.write(f"**Situação:** {_rotulo_situacao(campanha.situacao)}")
        etapa.write(f"**Etapa Atual:** {_rotulo_etapa(campanha.etapa_atual)}")
        st.write(f"**Nome:** {campanha.nome}")
        st.write(f"**Anunciante:** {campanha.anunciante}")
        if campanha.marca:
            st.write(f"**Marca:** {campanha.marca}")
        if campanha.produto_servico:
            st.write(f"**Produto ou Serviço:** {campanha.produto_servico}")
        st.write(f"**Planejador:** {campanha.planejador_responsavel}")
        st.write(f"**Criada em:** {campanha.criado_em:%d/%m/%Y %H:%M %Z}")
        if campanha.situacao == "RASCUNHO" and campanha.etapa_atual == "ABERTURA":
            if st.button("Iniciar Briefing", key=f"briefing-{campanha.id_campanha}"):
                try:
                    aplicacao.iniciar_briefing(campanha.id_campanha)
                except (LookupError, PermissionError, ValueError) as erro:
                    st.error(str(erro))
                else:
                    st.rerun()


def apresentar_campanhas() -> None:
    aplicacao = _obter_aplicacao()
    st.header("Campanhas")
    st.warning(
        "Persistência temporária em memória. As Campanhas desta etapa são "
        "perdidas quando o servidor é reiniciado."
    )

    with st.form("abertura-campanha", clear_on_submit=True):
        st.subheader("Identificação")
        nome = st.text_input("Nome")
        anunciante = st.text_input("Anunciante")
        marca = st.text_input("Marca opcional")
        produto_servico = st.text_input("Produto ou Serviço opcional")

        st.subheader("Responsáveis")
        planejador = st.text_input("Planejador Responsável")
        equipe = st.text_area("Equipe da Campanha", help="Um nome por linha.")

        st.subheader("Organização")
        observacao = st.text_area("Observação Inicial")

        cancelar = st.form_submit_button("Cancelar")
        salvar = st.form_submit_button("Salvar como Rascunho")
        criar_e_iniciar = st.form_submit_button(
            "Criar Campanha e iniciar Briefing"
        )

    if salvar or criar_e_iniciar:
        entrada = _criar_entrada(
            nome=nome,
            anunciante=anunciante,
            marca=marca,
            produto_servico=produto_servico,
            planejador=planejador,
            equipe=equipe,
            observacao=observacao,
            iniciar_briefing=criar_e_iniciar,
        )
        try:
            criada = aplicacao.criar_campanha(entrada)
        except (PermissionError, ValueError) as erro:
            st.error(str(erro))
        else:
            st.success(f"Campanha {criada.codigo} criada com sucesso.")
    elif cancelar:
        st.info("Abertura cancelada. Nenhuma Campanha foi criada.")

    st.subheader("Campanhas desta execução")
    try:
        campanhas = aplicacao.listar_campanhas()
    except PermissionError as erro:
        st.error(str(erro))
        return
    if not campanhas:
        st.info("Nenhuma Campanha criada nesta execução.")
        return
    for campanha in campanhas:
        _apresentar_campanha(aplicacao, campanha)
