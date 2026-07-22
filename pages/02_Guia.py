import streamlit as st


st.set_page_config(page_title="Guia de Uso — PlanOS", page_icon="📖", layout="wide")
st.title("📖 Guia de Uso do PlanOS")
st.caption("Plataforma Inteligente de Planejamento Híbrido de Mídia")

st.info(
    "Siga o workflow na ordem apresentada na barra lateral. Cada etapa usa "
    "informações produzidas e salvas nas etapas anteriores."
)

st.header("Fluxo recomendado")
etapas = [
    ("1. Projeto", "Crie ou selecione um projeto na página Início. O andamento será salvo progressivamente."),
    ("2. Briefing de Mídia", "Informe campanha, orçamento, período, públicos, KPIs, flight e dois valores entre alcance, frequência média e GRP."),
    ("3. Papéis dos Meios", "Escolha apenas os inventários pertinentes e classifique afinidade editorial, consumo e cobertura para esta campanha."),
    ("4. Plano de Mídia", "Selecione o briefing, revise as metas, confira os papéis e gere o plano."),
    ("5. Cronograma", "Após gerar, abra Cronograma de Inserções, ajuste as quantidades semanais de cada inventário e aplique as alterações."),
    ("6. Diagnóstico e projeções", "Selecione um plano salvo para produzir diagnóstico, forecast, painel, comparações, cenários e insights."),
    ("7. Relatório", "Salve o plano e confira todas as abas antes de gerar a exportação final."),
]
for titulo, texto in etapas:
    with st.expander(titulo, expanded=titulo.startswith("1.")):
        st.write(texto)

st.header("Como acrescentar informações")
st.markdown(
    """
- **Universos, Segmentos e Públicos:** use as páginas correspondentes da Base de Conhecimento.
- **Inventários:** em Cadastro de Inventários, selecione os itens existentes do catálogo ou escolha **Cadastrar outra opção…**. A opção criada passa a integrar o catálogo.
- **Meios:** ao cadastrar um novo meio, informe plataforma, empresa e, se disponível, o site.
- **Formatos:** novos formatos são vinculados ao ambiente selecionado.
- **Unidades de compra:** novas unidades são vinculadas à modalidade escolhida.
- **Preços:** mantenha preço bruto, desconto e vigência atualizados para que quantidade e entrega possam ser estimadas.
"""
)

st.header("Solução de problemas")
problemas = {
    "Não consigo avançar no workflow": "Volte à etapa indicada na mensagem, salve-a e confirme se existe um projeto ativo.",
    "O briefing não aparece": "Confirme se ele foi salvo no projeto correto. Use Briefings salvos para editar ou reabrir.",
    "Nenhum inventário entra no plano": "Abra Papéis dos Meios, selecione o briefing correto, escolha os inventários e clique em Aplicar papéis à campanha.",
    "Formato ou unidade não aparece": "Confira o ambiente ou a modalidade selecionada. Se a opção for válida e ainda não existir, use Cadastrar outra opção….",
    "Quantidade ou alcance está em branco": "Cadastre preço vigente e unidade de compra. O alcance só é estimado para unidades baseadas em impressões ou contatos.",
    "Alcance, frequência e GRP são inconsistentes": "Escolha qual indicador deve ser calculado e informe apenas os outros dois. GRP = alcance (%) × frequência média.",
    "Um registro não pode ser excluído": "Verifique se ele está sendo usado por briefing, público, inventário ou plano. Remova primeiro o vínculo dependente.",
    "O resultado salvo não foi atualizado": "Depois de editar o cronograma ou outra configuração, aplique a alteração e salve novamente o plano.",
}
for problema, solucao in problemas.items():
    with st.expander(problema):
        st.write(solucao)

st.divider()
st.caption(
    "Suporte e sugestões: Fernando Silva Santor — "
    "fernandosantor@unipampa.edu.br"
)
