import streamlit as st


def render(

    estado

):

    st.subheader("Workflow oficial")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Etapas",

        f"{estado.concluidas}/{estado.total}"

    )

    c2.metric(

        "Progresso",

        f"{estado.percentual}%"

    )

    c3.metric(

        "Próxima",

        estado.proxima_etapa

    )

    st.progress(

        estado.percentual / 100

    )

    etapas = [
        ("Briefing", "pages/00_Briefing.py", "briefing", "📋"),
        ("Papéis de mídia", "pages/03_MCP_Papeis.py", "mcp_papeis", "🧩"),
        ("Planejamento", "pages/05_Planejamento.py", "planejamento", "🧠"),
        ("Diagnóstico", "pages/09_Diagnostico.py", "diagnostico", "🩺"),
        ("Forecast", "pages/06_Forecast.py", "forecast", "📈"),
        ("Painel Executivo", "pages/07_Dashboard.py", "dashboard", "📊"),
        ("Relatórios", "pages/08_Exportacao.py", "exportacao", "📄"),
    ]

    status = [getattr(estado, chave) for _, _, chave, _ in etapas]
    for inicio in range(0, len(etapas), 3):
        colunas = st.columns(3)
        for coluna, indice in zip(colunas, range(inicio, min(inicio + 3, len(etapas)))):
            nome, pagina, _, icone = etapas[indice]
            concluida = status[indice]
            liberada = indice == 0 or all(status[:indice])
            marcador = "✅" if concluida else ("➡️" if liberada else "🔒")
            with coluna:
                st.page_link(
                    pagina,
                    label=f"{marcador} {nome}",
                    icon=icone,
                    disabled=not liberada,
                    width="stretch",
                )

    proxima = next(
        (
            (nome, pagina, icone)
            for indice, (nome, pagina, _, icone) in enumerate(etapas)
            if not status[indice] and (indice == 0 or all(status[:indice]))
        ),
        None,
    )
    if proxima:
        nome, pagina, icone = proxima
        st.page_link(
            pagina,
            label=f"Continuar: {nome}",
            icon=icone,
            width="stretch",
        )
