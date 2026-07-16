# SDM — Linguagem da Interface

Versão: 1.0

Este documento define a terminologia oficial utilizada na interface do SDM.

Objetivo:

- Tornar a interface intuitiva para profissionais de mídia.
- Evitar exposição de termos técnicos internos.
- Manter consistência entre todas as telas.

---

# Princípios

A interface deve utilizar a linguagem do mercado.

O código utiliza a linguagem técnica.

Os dois vocabulários não precisam ser iguais.

---

# Terminologia Oficial

| Código | Interface |
|---------|-----------|
| Briefing | Campanha |
| Workflow | Progresso da Campanha |
| Projeto | Campanha |
| PlanoEstrategico | Plano de Mídia |
| PlanoItem | Recomendação |
| InventoryEngine | — |
| AllocationEngine | — |
| ForecastEngine | — |
| RecommendationService | Recomendações |
| KPI | Indicador |
| Objetivo | Objetivo da Campanha |
| Inventário | Canal de Mídia |
| Ambiente | Ambiente |
| Plataforma | Plataforma |
| Audiência | Público |
| Cenário | Simulação |
| Dashboard | Painel Executivo |
| Exportação | Relatórios |

---

# Verbos

Não utilizar:

- Executar Engine
- Gerar Allocation
- Processar Workflow

Utilizar:

- Criar Campanha
- Continuar Planejamento
- Gerar Plano
- Simular Cenário
- Projetar Resultados
- Abrir Painel
- Exportar Relatório

---

# Botões

Preferir:

Nova Campanha

Continuar Campanha

Gerar Plano

Gerar Projeção

Abrir Painel Executivo

Exportar Relatório

Evitar:

Novo Briefing

Executar Forecast

Abrir Dashboard

---

# Mensagens

Ruim

"Nenhum briefing encontrado."

Bom

"Nenhuma campanha encontrada."

---

Ruim

"Workflow concluído."

Bom

"Planejamento concluído."

---

Ruim

"Forecast disponível."

Bom

"Projeção de resultados disponível."

---

# Princípio Geral

O usuário nunca deve precisar conhecer a arquitetura do SDM.

A interface comunica o negócio.

O código comunica a implementação.