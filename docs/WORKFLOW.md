# Workflow Oficial

## Fluxo

Nova Campanha

↓

Planejamento

↓

Diagnóstico

↓

Forecast

↓

Painel Executivo

↓

Relatórios

---

## Estado

WorkflowState

representa o progresso da campanha.

---

## WorkflowService

Responsável por:

- estado atual;
- progresso;
- próxima etapa;
- validação de transições.

## Estado da versão 1.0

Os artefatos do workflow usam chaves canônicas no `st.session_state`:

- `briefing` ou `briefing_ref`;
- `plano`;
- `diagnostico`;
- `forecast`;
- `dashboard`;
- `exportacao`.

O `WorkflowService` registra conclusões, calcula o progresso e verifica os
pré-requisitos de cada etapa. Um briefing salvo no banco pode iniciar um novo
fluxo por meio de `briefing_ref`.

O estado dos cálculos permanece associado à sessão ativa do Streamlit. Histórico
e retomada persistente entre sessões pertencem ao SDM 1.1.

Análises avançadas e cadastros da base de conhecimento não contam como etapas
do workflow oficial.

---

## Princípios

O usuário sempre deve ser conduzido para a próxima ação.

Nunca deve ficar sem orientação.
