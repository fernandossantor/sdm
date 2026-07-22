import streamlit as st
from components.page_config import PAGE_ICON


st.set_page_config(page_title="Guia de Uso — PlanOS", page_icon=PAGE_ICON, layout="wide")
st.title("📖 Guia de Uso do PlanOS")
st.caption("Plataforma Inteligente de Planejamento Híbrido de Mídia")

st.info(
    "Siga o workflow na ordem apresentada na barra lateral. Cada etapa usa "
    "informações produzidas e salvas nas etapas anteriores."
)

st.header("Fluxo recomendado")
etapas = [
    ("1. Universo (quando necessário)", "Cadastre a praça e a população que servirão de base aos cálculos."),
    ("2. Segmento (quando necessário)", "Defina o recorte demográfico dentro do Universo."),
    ("3. Público (quando necessário)", "Combine Segmentos, interesses e etapa da jornada. Reutilize registros adequados já existentes."),
    ("4. Projeto", "Crie ou selecione um projeto na página Início. O código o acompanha por todo o processo."),
    ("5. Briefing de Mídia", "Informe campanha, orçamento, período, públicos, jornada, KPIs e metas globais."),
    ("6. Papéis dos Meios", "Escolha os inventários e avalie afinidade editorial, consumo e capacidade de cobertura."),
    ("7. Plano de Mídia", "Configure pesos, audiência, alcance, frequência, alcance incremental, saturação e premissas. Por padrão, as metas calculam a quantidade; também é possível fixar a compra e recalcular a entrega."),
    ("8. Cronograma", "Visualize flights e pressão semanal no calendário. A distribuição decorre das quantidades e do flight."),
    ("9. Diagnóstico e projeções", "Confira entrega, custos, retorno, limitações e confiança dos dados."),
    ("10. Relatório", "Salve o plano e confira as premissas e a auditoria antes da exportação."),
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
    "O resultado salvo não foi atualizado": "Depois de alterar premissas ou quantidades, gere e salve uma nova versão do plano. O cronograma é uma visualização calculada.",
    "Uma página posterior não abre": "Selecione Projeto, Briefing e Plano no contexto ativo da barra lateral. Registros já salvos não precisam ser refeitos.",
    "Não consigo gerar o plano": "Audiência, alcance e frequência são obrigatórios por inventário, e os pesos estratégicos devem somar 100%.",
    "O alcance combinado parece incorreto": "Revise o alcance incremental. Sem valor informado, o sistema usa estimativa por independência e registra essa premissa.",
}
for problema, solucao in problemas.items():
    with st.expander(problema):
        st.write(solucao)

st.header("Análises Avançadas")
analises = {
    "Comparação de Planos": "Compare duas versões salvas e defina pesos para alcance, frequência, conversões, ROI, jornada, saturação e custo. Não existe vencedor universal: a justificativa segue os critérios escolhidos.",
    "Simulação de Cenários": "Aplica perfis alternativos ao mesmo conjunto de inventários para observar mudanças de pressão e distribuição.",
    "Otimização de Verba": "Explora redistribuições com pisos, tetos, limites por ambiente e reserva para testes.",
    "Insights de Mídia": "Interpreta entrega, concentração, custos e projeções do plano selecionado.",
}
for nome, descricao in analises.items():
    with st.expander(nome):
        st.write(descricao)
st.info(
    "Para testar uma hipótese sem reconstruir tudo, duplique o registro, altere "
    "somente as premissas desejadas, gere e salve uma nova versão. Dados medidos, "
    "estimados e informados manualmente permanecem identificados."
)

st.divider()
st.caption(
    "Suporte e sugestões: Fernando Silva Santor — "
    "fernandosantor@unipampa.edu.br"
)
