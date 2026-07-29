# Consolidação das Bibliotecas Operacionais

**Documento:** `12A_CONSOLIDACAO_DAS_BIBLIOTECAS_OPERACIONAIS.md`  
**Documento principal:** `12_SISTEMA_DE_BIBLIOTECAS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Decisão arquitetural consolidada  
**Última revisão:** 29/07/2026  
**Natureza:** Adendo normativo de simplificação

---

## 1. Decisão

As estruturas anteriormente previstas como Bibliotecas 19, 20 e 21 não serão implementadas como bibliotecas autônomas na versão 1.0 do MediAd Planner.

Seus conteúdos serão absorvidos pelas bibliotecas e módulos já existentes, preservando rigor técnico sem criar novos cadastros, telas, fluxos ou entidades quando não houver decisão independente do usuário.

A arquitetura funcional passa a operar com seis bibliotecas principais:

```text
13 — Inventários de Mídia
14 — Públicos e Segmentos
15 — Objetivos, Resultados e KPIs
16 — Jornadas, Necessidades, Funções e Pontos de Contato
17 — Conhecimento Técnico
18 — Problemas Técnicos de Planejamento de Mídia
```

Custos, regras e modelos reutilizáveis permanecem no sistema como atributos, relações, parâmetros, procedimentos, configurações ou artefatos, e não como novas bibliotecas.

---

## 2. Critério de incorporação

Um conteúdo somente deve gerar objeto autônomo quando possuir simultaneamente:

- identidade própria relevante para o planejamento;
- ciclo de vida ou versionamento independente;
- uso em mais de um contexto;
- necessidade de consulta, seleção ou decisão explícita;
- impossibilidade de representação adequada como atributo, relação, parâmetro, regra ou componente interno.

Quando essas condições não forem atendidas, o conteúdo deve permanecer incorporado ao objeto ou procedimento que efetivamente o utiliza.

---

## 3. Incorporação da antiga Biblioteca 19 — Custos e Condições Comerciais

### 3.1 Destino principal: Biblioteca 13

Permanecem associados ao inventário, produto comercial, oferta comercial ou disponibilidade:

```text
unidade_comercial
modelo_de_compra
preco_de_tabela
preco_negociado
desconto
bonificacao
vigencia
moeda
impostos
condicao_de_pagamento
quantidade_minima
investimento_minimo
disponibilidade
politica_de_cancelamento
entregas_incluidas
custos_de_producao
custos_de_tecnologia
custos_de_dados
direitos_e_licencas
```

Esses elementos não constituem uma biblioteca paralela. São propriedades comerciais da oferta ou componentes de custo relacionados ao inventário.

### 3.2 Destino metodológico: Biblioteca 17

Fórmulas, conceitos e regras de cálculo permanecem como conhecimento técnico, incluindo:

- investimento bruto;
- investimento líquido;
- comissão de agência;
- custos adicionais;
- CPM, CPC, CPA, CPP e demais métricas de eficiência;
- tratamento de desconto, bonificação e impostos;
- distinção entre custo cadastrado, custo calculado e custo projetado.

### 3.3 Destino decisório: Biblioteca 18

Os problemas econômicos permanecem como problemas técnicos, por exemplo:

```text
VALIDAR_VIABILIDADE_ORCAMENTARIA
DISTRIBUIR_ORCAMENTO
CALCULAR_INVESTIMENTO_BRUTO
CALCULAR_INVESTIMENTO_LIQUIDO
CALCULAR_COMISSAO_DE_AGENCIA
AVALIAR_EFICIENCIA_DE_CUSTO
COMPARAR_CUSTOS
OTIMIZAR_DISTRIBUICAO_DE_RECURSOS
```

### 3.4 Interface

O usuário deve visualizar apenas os valores necessários à decisão. Detalhes avançados aparecem sob demanda, especialmente em ofertas comerciais compostas ou negociações específicas.

---

## 4. Incorporação da antiga Biblioteca 20 — Regras, Restrições e Referências Metodológicas

### 4.1 Destino principal: Biblioteca 17

Regras técnicas relacionadas a cálculo, interpretação, validade, comparabilidade, conversão e uso de indicadores permanecem vinculadas ao conhecimento que fundamentam.

Exemplos:

- identidade de universo;
- identidade temporal e territorial;
- compatibilidade de unidades;
- condições de deduplicação;
- limites de equivalência multimídia;
- critérios de uso de proxies;
- regras de arredondamento;
- tratamento de zero e ausência;
- critérios de confiança.

### 4.2 Destino decisório: Biblioteca 18

Restrições aplicadas à resolução de problemas permanecem como:

```text
pre_condicoes
restricoes
bloqueios
criterios_de_escolha
criterios_de_conclusao
tratamento_de_incerteza
estados_de_resultado
mensagens_explicativas
```

Não será criado cadastro separado de regras quando a regra só existir para autorizar, condicionar ou bloquear um problema específico.

### 4.3 Destino ontológico ou operacional

Regras próprias de um objeto permanecem no próprio objeto:

- elegibilidade de inventário na Biblioteca 13;
- restrições de público na Biblioteca 14;
- requisitos de indicador na Biblioteca 15;
- compatibilidade de ponto de contato na Biblioteca 16.

Regras institucionais de acesso, governança e permissões permanecem nos documentos e componentes próprios da plataforma, sem constituir biblioteca de planejamento.

### 4.4 Referências metodológicas

Fontes, autores, documentos técnicos, datas, territórios, versões e níveis de confiança permanecem como metadados dos objetos de conhecimento, problemas, procedimentos e relações.

O referencial consolidado permanece no documento:

`22_REFERENCIAL_CONCEITUAL_TECNICO_E_MERCADOLOGICO_DO_MEDIAD_PLANNER.md`

---

## 5. Incorporação da antiga Biblioteca 21 — Modelos e Componentes Reutilizáveis

### 5.1 Princípio

Modelos reutilizáveis não constituem nova ontologia. São configurações versionadas de objetos e parâmetros já existentes.

### 5.2 Destinos

```text
arquiteturas de referência
→ Arquitetura de Mídia e Simulações

cenários padrão
→ Biblioteca de Cenários e Otimização

modelos de flight
→ cronograma, flight e Mapa de Veiculação

matrizes de pesos
→ parâmetros dos motores especialistas

combinações de canais e pontos de contato
→ Biblioteca 16 + Arquitetura de Mídia

componentes de cálculo
→ Biblioteca 17 + procedimentos dos motores

modelos de relatório e plano
→ artefatos de saída e Plano Consolidado
```

### 5.3 Persistência

Quando reutilizáveis, esses modelos podem ser armazenados como:

- configuração salva;
- cenário-base;
- template;
- snapshot;
- conjunto de parâmetros;
- composição de objetos existentes.

Não devem exigir tabelas ou interfaces próprias antes que a implementação demonstre uso recorrente e necessidade de gestão independente.

---

## 6. Distribuição consolidada de responsabilidades

| Conteúdo | Destino |
|---|---|
| preço, desconto, vigência e disponibilidade | Biblioteca 13 |
| fórmulas e conceitos econômicos | Biblioteca 17 |
| decisões de orçamento e eficiência | Biblioteca 18 |
| regras de validade de cálculo | Biblioteca 17 |
| bloqueios e critérios de resolução | Biblioteca 18 |
| restrições próprias de inventário, público, KPI ou ponto de contato | Biblioteca correspondente |
| cenários, flights e arquiteturas reutilizáveis | módulos existentes como configurações |
| matrizes, parâmetros e componentes de cálculo | motores e procedimentos |
| modelos de relatório | artefatos de saída |

---

## 7. Regras de contenção de escopo

Para preservar a usabilidade, ficam vedadas na versão 1.0:

- criação de uma tela geral de regras;
- criação de uma biblioteca isolada de preços;
- criação de cadastro obrigatório de modelos reutilizáveis;
- exposição de metadados técnicos em telas principais;
- duplicação de campos já pertencentes a inventários, conhecimentos ou problemas;
- transformação de toda exceção metodológica em objeto autônomo;
- criação de motores diferentes apenas por meio, formato ou indicador.

A interface deve priorizar:

```text
contexto
→ decisão
→ entradas essenciais
→ recomendação
→ justificativa resumida
```

Rastreabilidade, memória de cálculo e detalhes metodológicos permanecem disponíveis em camadas de explicação, auditoria ou configuração avançada.

---

## 8. Consequência para o banco de dados

A modelagem definitiva não deverá criar, por padrão, tabelas centrais denominadas `biblioteca_19`, `biblioteca_20` ou `biblioteca_21`.

Os dados deverão ser distribuídos conforme a responsabilidade funcional:

- atributos comerciais nas entidades de inventário, produto, oferta ou disponibilidade;
- conhecimentos e regras técnicas nas entidades da Biblioteca 17;
- restrições e procedimentos nas entidades da Biblioteca 18;
- templates e cenários em estruturas leves de configuração, somente quando necessários;
- snapshots e parâmetros nas instâncias dos projetos.

A normalização deve evitar duplicação, mas não deve fragmentar a experiência do usuário nem criar uma entidade para cada variação de campo.

---

## 9. Estado arquitetural

Com esta decisão:

- as Bibliotecas 19, 20 e 21 deixam de ser pendências arquiteturais;
- nenhum conteúdo essencial é descartado;
- a arquitetura permanece extensível;
- o número de bibliotecas principais é reduzido;
- custos, regras e modelos ficam próximos dos objetos e decisões que os utilizam;
- a implementação poderá avançar sem criar estruturas especulativas.

---

## 10. Princípio consolidado

> Custos devem acompanhar as ofertas e os cálculos que os utilizam; regras devem acompanhar os conhecimentos, objetos e problemas que condicionam; modelos reutilizáveis devem permanecer configurações dos módulos e motores existentes. O MediAd Planner não criará bibliotecas autônomas quando atributos, relações, parâmetros e procedimentos forem suficientes.