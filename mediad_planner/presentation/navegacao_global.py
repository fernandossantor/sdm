from dataclasses import dataclass

import streamlit as st

from mediad_planner.application.dto.espaco_trabalho import (
    EspacoTrabalhoCampanhaResumo,
)
from mediad_planner.application.dto.diagnostico_fundacao import (
    DiagnosticoFundacao,
)


@dataclass(frozen=True, slots=True)
class AcaoNavegacao:
    pagina_global: str | None = None
    modulo_campanha: str | None = None
    fechar_campanha: bool = False


PAGINAS_GLOBAIS = (
    ("CAMPANHAS", "Campanhas"),
    ("BIBLIOTECAS", "Bibliotecas"),
    ("GUIA_DE_USO", "Guia de uso e glossário"),
    ("ADMINISTRACAO", "Administração"),
)


def apresentar_navegacao_global(
    pagina_global_ativa: str,
    resumo_campanha: EspacoTrabalhoCampanhaResumo | None,
    modulo_campanha_ativo: str | None,
    diagnostico: DiagnosticoFundacao,
) -> AcaoNavegacao:
    with st.sidebar:
        st.header("MediAd Planner")
        for codigo, rotulo in PAGINAS_GLOBAIS:
            if st.button(
                rotulo,
                key=f"pagina-global-{codigo}",
                use_container_width=True,
            ):
                return AcaoNavegacao(pagina_global=codigo)
            if pagina_global_ativa == codigo:
                st.caption("Página atual")

        if resumo_campanha is not None:
            st.divider()
            campanha = resumo_campanha.campanha
            st.subheader("Campanha ativa")
            st.write(f"[{campanha.codigo}] {campanha.nome}")
            for modulo in resumo_campanha.modulos:
                if st.button(
                    modulo.rotulo,
                    key=f"modulo-campanha-{modulo.codigo}",
                    disabled=not modulo.disponivel,
                    use_container_width=True,
                ):
                    return AcaoNavegacao(
                        pagina_global="CAMPANHA",
                        modulo_campanha=modulo.codigo,
                    )
                if (
                    pagina_global_ativa == "CAMPANHA"
                    and modulo.codigo == modulo_campanha_ativo
                ):
                    st.caption("Tela atual")
                if modulo.motivo_bloqueio:
                    st.caption(modulo.motivo_bloqueio)
            if st.button(
                "Fechar Campanha ativa",
                key="fechar-campanha-ativa",
                use_container_width=True,
            ):
                return AcaoNavegacao(fechar_campanha=True)

        st.divider()
        if diagnostico.backend_operacional:
            st.caption("Sistema: operacional")
            st.caption("Backend e interface conectados")
        else:
            st.caption("Sistema: atenção necessária")
            st.caption("Consulte Administração para detalhes.")
    return AcaoNavegacao()
