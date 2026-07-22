import streamlit as st
import json


def render(service, tipo, titulo):
    with st.expander(f"{titulo} salvos", expanded=False):
        registros = service.listar(tipo, st.session_state.get("projeto_id"))
        if not registros:
            st.info(f"Nenhum {titulo.lower()} salvo.")
            return
        for registro in reversed(registros):
            nome = st.text_input(
                "Nome", registro["nome"], key=f"nome_artefato_{registro['id']}"
            )
            a, b, c = st.columns([1, 1, 1])
            if a.button("Atualizar", key=f"atualizar_artefato_{registro['id']}"):
                service.renomear(registro["id"], nome)
                st.rerun()
            if b.button("Visualizar", key=f"ver_artefato_{registro['id']}"):
                st.session_state["artefato_visualizado"] = registro
            if c.button("Excluir", key=f"excluir_artefato_{registro['id']}"):
                service.excluir(registro["id"])
                st.rerun()
        visualizado = st.session_state.get("artefato_visualizado")
        if visualizado and visualizado.get("tipo") == tipo:
            conteudo = st.text_area(
                "Dados do artefato",
                value=json.dumps(
                    visualizado.get("dados") or {}, ensure_ascii=False, indent=2
                ),
                height=280,
                key=f"dados_artefato_{visualizado['id']}",
            )
            if st.button("Salvar alterações nos dados", key=f"salvar_dados_{visualizado['id']}"):
                try:
                    dados = json.loads(conteudo)
                    service.atualizar_dados(visualizado["id"], dados)
                except json.JSONDecodeError:
                    st.error("Os dados devem permanecer em formato JSON válido.")
                else:
                    st.success("Artefato atualizado.")
