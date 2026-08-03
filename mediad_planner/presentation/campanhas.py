import streamlit as st
from uuid import UUID

from mediad_planner.application.dto.campanha import (
    CampanhaResumo,
    CriarCampanhaEntrada,
)
from mediad_planner.application.services.aplicacao_campanhas import (
    AplicacaoCampanhas,
)
from mediad_planner.application.services.aplicacao_espaco_trabalho import (
    AplicacaoEspacoTrabalho,
)


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
    campanha: CampanhaResumo,
) -> UUID | None:
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
        if st.button(
            "Abrir espaço de trabalho",
            key=f"abrir-{campanha.id_campanha}",
        ):
            return campanha.id_campanha
    return None


def apresentar_campanhas(
    aplicacao: AplicacaoCampanhas,
    aplicacao_espaco_trabalho: AplicacaoEspacoTrabalho,
) -> UUID | None:
    st.header("Campanhas")
    st.warning(
        "Persistência temporária em memória. As Campanhas desta etapa são "
        "perdidas quando o servidor é reiniciado."
    )

    with st.form("abertura-campanha", clear_on_submit=True):
        st.subheader("Identificação")
        nome = st.text_input(
            "Nome da Campanha",
            key="campanha-nome",
            help=(
                "Use um nome que permita identificar esta iniciativa no "
                "histórico de planejamento."
            ),
            placeholder="Ex.: Lançamento Linha Verão 2027",
        )
        anunciante = st.text_input("Anunciante", key="campanha-anunciante")
        marca = st.text_input("Marca (opcional)", key="campanha-marca")
        produto_servico = st.text_input(
            "Produto ou Serviço (opcional)",
            key="campanha-produto-servico",
        )

        st.subheader("Responsáveis")
        planejador = st.text_input(
            "Planejador Responsável",
            key="campanha-planejador",
            help=(
                "Nesta versão temporária, informe o nome do responsável. "
                "Quando a autenticação for integrada, este campo será "
                "preenchido pelo usuário conectado."
            ),
        )
        equipe = st.text_area(
            "Equipe da Campanha (opcional)",
            key="campanha-equipe",
            help=(
                "Informe um nome por linha. A seleção de membros cadastrados "
                "será integrada ao cadastro de usuários do espaço de trabalho."
            ),
        )

        st.subheader("Organização")
        observacao = st.text_area(
            "Observação inicial (opcional)",
            key="campanha-observacao",
            help=(
                "Registre informações administrativas ou de organização da "
                "abertura. "
                "Dados mercadológicos e estratégicos devem ser informados no Briefing."
            ),
            placeholder=(
                "Ex.: demanda recebida pela diretoria; responsáveis ainda "
                "em "
                "definição."
            ),
        )

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
            if criar_e_iniciar:
                try:
                    aplicacao_espaco_trabalho.preparar_briefing(
                        criada.id_campanha
                    )
                except (LookupError, PermissionError, ValueError) as erro:
                    st.error(
                        "A Campanha foi criada, mas não foi possível "
                        f"preparar o Briefing: {erro}"
                    )
                else:
                    return criada.id_campanha
            else:
                return criada.id_campanha
    elif cancelar:
        st.info("Abertura cancelada. Nenhuma Campanha foi criada.")

    st.subheader("Campanhas desta execução")
    try:
        campanhas = aplicacao.listar_campanhas()
    except PermissionError as erro:
        st.error(str(erro))
        return None
    if not campanhas:
        st.info("Nenhuma Campanha criada nesta execução.")
        return None
    for campanha in campanhas:
        selecionada = _apresentar_campanha(campanha)
        if selecionada is not None:
            return selecionada
    return None
