import pandas as pd
import streamlit as st
from components.formatters import numero_ptbr


def render(plano):
    if not plano.cronograma:
        st.info("Defina as datas do briefing para gerar a linha do tempo semanal.")
        return
    quadro = pd.DataFrame(plano.cronograma)
    fixas = [c for c in ("Inventário", "Unidade", "Total") if c in quadro.columns]
    semanas = [c for c in quadro.columns if c not in fixas]
    if not semanas:
        st.dataframe(quadro, hide_index=True, width="stretch")
        return

    st.caption(
        "A intensidade da cor representa a pressão relativa de cada inventário; "
        "os valores absolutos permanecem visíveis nas células."
    )
    exibicao = quadro.set_index(fixas[0]) if fixas else quadro
    subconjunto = [c for c in semanas if c in exibicao.columns]
    st.dataframe(
        exibicao.style.background_gradient(cmap="Blues", subset=subconjunto, axis=1)
        .format({c: "{:.0f}" for c in subconjunto}),
        width="stretch",
    )

    pressao = quadro[semanas].apply(pd.to_numeric, errors="coerce").fillna(0).sum()
    st.markdown("#### Pressão total por semana")
    st.bar_chart(pressao, color="#2563EB")
    st.caption(
        f"Flight {plano.tipo_flight.title()} · frequência combinada "
        f"{numero_ptbr(plano.frequencia_alvo, 2)} · GRP {numero_ptbr(plano.grp, 2)}"
    )
