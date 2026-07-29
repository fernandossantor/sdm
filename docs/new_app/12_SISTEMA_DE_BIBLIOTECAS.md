# Sistema de Bibliotecas do MediAd Planner

**Documento:** `12_SISTEMA_DE_BIBLIOTECAS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

O Sistema de Bibliotecas organiza objetos, relações, conhecimentos, problemas, regras e modelos reutilizáveis, versionados e rastreáveis que sustentam o planejamento de mídia no MediAd Planner.

As bibliotecas descrevem o domínio, preservam conhecimento técnico, estruturam problemas decisórios e disponibilizam referências operacionais. Os motores especialistas consultam essas estruturas, processam relações, selecionam procedimentos e produzem recomendações explicáveis. Os usuários permanecem responsáveis pelas decisões e os projetos preservam as versões efetivamente utilizadas.

O MediAd Planner é uma plataforma de inteligência de mídia baseada em sistemas especialistas, composta por ontologias, bibliotecas de conhecimento, catálogos, relações, motores de inferência e modelos reutilizáveis para apoiar o planejamento, a simulação, a comparação e a otimização de arquiteturas de mídia.

O sistema não acompanha campanhas em execução nem armazena resultados realizados como função central desta arquitetura.

---

## 2. Posição na arquitetura

```text
Briefing
    ↓
Tradução Estratégica
    ↓
Arquitetura de Mídia
    ↓
Catálogos e Bibliotecas
    ↓
Relações, parâmetros e problemas técnicos
    ↓
Motores especialistas
    ↓
Simulação, comparação, otimização e explicação
    ↓
Artefatos do projeto e Plano Consolidado
```

As bibliotecas são transversais ao Briefing, à Tradução Estratégica, à Arquitetura de Mídia, às Simulações, à Comparação, à Otimização e ao Plano Consolidado.

Os motores não incorporam de forma rígida todo o conhecimento do domínio. Eles consultam bibliotecas versionadas para identificar objetos, restrições, conhecimentos aplicáveis, problemas técnicos e procedimentos possíveis.

---

## 3. Distinções fundamentais

### 3.1 Catálogo

Vocabulário controlado utilizado para classificar objetos, como tecnologia, canal, ambiente, formato, modalidade de compra, tipo de objetivo, tipo de resultado, família de indicador, etapa de jornada, necessidade, função, ponto de contato, território, unidade métrica, família de conhecimento e categoria de problema.

### 3.2 Biblioteca

Coleção de objetos reutilizáveis e contextualizados, como inventários, públicos, jornadas, objetivos, resultados, indicadores, necessidades comunicacionais, funções, pontos de contato, conhecimentos técnicos, problemas, custos, regras e modelos.

### 3.3 Relação de conhecimento

Vínculo contextual entre objetos. Deve admitir, quando aplicável, fonte, versão, território, período, intensidade, prioridade, obrigatoriedade, confiança e condições de validade.

Exemplos:

- objetivo associado a resultado pretendido;
- resultado associado a indicador;
- jornada composta por etapas;
- etapa associada a necessidade comunicacional;
- combinação etapa–necessidade associada a função;
- função associada a ponto de contato;
- ponto de contato associado a tipologia de inventário;
- indicador compatível com inventário;
- público compatível com propriedades de inventário;
- problema técnico associado a conhecimentos aplicáveis;
- problema técnico associado a procedimentos possíveis;
- regra associada a objeto, contexto ou procedimento;
- modelo reutilizável composto por objetos e relações versionados.

### 3.4 Parâmetro

Valor utilizado por regra, fórmula, procedimento ou motor, como peso, limite, tolerância, frequência desejada, fator de overlap, coeficiente de equivalência ou nível mínimo de confiança.

O parâmetro não deve ser confundido com o conhecimento que explica seu significado, com o indicador que recebe seu valor ou com a regra que determina sua aplicação.

### 3.5 Objeto de Conhecimento Técnico

Unidade reutilizável da Biblioteca 17 que reúne conceito, definição, lógica, fórmulas, regras operacionais, condições de validade, limitações, interpretações, aplicações e referências sobre determinado conhecimento do planejamento de mídia.

### 3.6 Problema Técnico

Situação decisória, analítica, comparativa, econômica, operacional ou de validação que exige resposta fundamentada em conhecimento técnico.

Um problema técnico é definido pelo objetivo decisório, e não por uma fórmula, indicador ou algoritmo específico. Pode utilizar vários Objetos de Conhecimento Técnico e admitir diferentes procedimentos de resolução.

### 3.7 Procedimento de resolução

Caminho estruturado para resolver um problema técnico, composto por pré-condições, entradas, conhecimentos aplicados, cálculos, regras, validações, saídas e critérios de interpretação.

### 3.8 Instância de projeto

Cópia contextual e versionada de um objeto, relação, parâmetro, problema, procedimento ou modelo utilizada em um planejamento específico.

---

## 4. Camadas do Sistema de Bibliotecas

O Sistema de Bibliotecas organiza-se em quatro camadas funcionais.

### 4.1 Camada ontológica — descrição do domínio

Define quais objetos existem e como se relacionam no universo do planejamento de mídia:

1. Biblioteca 13 — Inventários de Mídia;
2. Biblioteca 14 — Públicos e Segmentos;
3. Biblioteca 15 — Objetivos, Resultados e KPIs;
4. Biblioteca 16 — Jornadas, Necessidades, Funções e Pontos de Contato.

### 4.2 Camada epistemológica — conhecimento do domínio

Formaliza o que o sistema sabe sobre planejamento de mídia:

5. Biblioteca 17 — Conhecimento Técnico.

### 4.3 Camada heurística — organização do raciocínio

Formaliza quais problemas os motores precisam resolver e como o conhecimento pode ser mobilizado:

6. Biblioteca 18 — Problemas Técnicos de Planejamento de Mídia.

### 4.4 Camada operacional — aplicação contextual

Organiza condições comerciais, regras transversais e estruturas reutilizáveis:

7. Biblioteca 19 — Custos e Condições Comerciais;
8. Biblioteca 20 — Regras, Restrições e Referências Metodológicas;
9. Biblioteca 21 — Modelos e Componentes Reutilizáveis.

---

## 5. Sequência documental

```text
12_SISTEMA_DE_BIBLIOTECAS.md
13_BIBLIOTECA_DE_INVENTARIOS.md
14_BIBLIOTECA_DE_PUBLICOS_E_SEGMENTOS.md
15_BIBLIOTECA_DE_OBJETIVOS_RESULTADOS_E_KPIS.md
16_BIBLIOTECA_DE_JORNADAS_NECESSIDADES_FUNCOES_E_PONTOS_DE_CONTATO.md
17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md
18_BIBLIOTECA_DE_PROBLEMAS_TECNICOS_DE_PLANEJAMENTO_DE_MIDIA.md
19_BIBLIOTECA_DE_CUSTOS_E_CONDICOES_COMERCIAIS.md
20_BIBLIOTECA_DE_REGRAS_RESTRICOES_E_REFERENCIAS_METODOLOGICAS.md
21_BIBLIOTECA_DE_MODELOS_E_COMPONENTES_REUTILIZAVEIS.md
```

Cada núcleo possui entidades próprias. Não deve existir uma tabela genérica única para todas as bibliotecas.

---

## 6. Cadeia estratégica canônica

```text
Objetivo declarado
    ↓
Classificação e validação
    ↓
Objetivo de marketing
    ↓
Objetivo de comunicação
    ↓
Objetivo de mídia
    ↓
Resultado pretendido
    ↓
Indicadores prioritários
    ↓
Jornada
    ↓
Etapa
    ↓
Necessidade comunicacional
    ↓
Função comunicacional da mídia
    ↓
Ponto de contato
    ↓
Tipologia da Biblioteca de Inventários
    ↓
Inventários compatíveis
    ↓
Problemas técnicos a resolver
    ↓
Conhecimentos e procedimentos aplicáveis
    ↓
Arquiteturas candidatas
```

A seleção não começa pelo meio ou inventário.

O ponto de contato é uma categoria de mídia. Formatos, peças, ambientes, plataformas, programas, posicionamentos e unidades comerciais pertencem ao desdobramento tipológico da Biblioteca de Inventários.

A Biblioteca 17 não determina sozinha a decisão. Ela fornece conhecimentos. A Biblioteca 18 organiza os problemas decisórios e relaciona cada problema aos conhecimentos e procedimentos possíveis. Os motores executam essa combinação no contexto do projeto.

---

## 7. Responsabilidades das bibliotecas

### 7.1 Biblioteca 13 — Inventários de Mídia

Define a materialização tipológica e operacional dos pontos de contato em tecnologias, canais, ambientes, estruturas, formatos, meios, plataformas, programas, modelos comerciais, modalidades, unidades e inventários.

Declara também capacidades analíticas, cobertura, segmentações, propriedades editoriais, contextuais e operacionais.

### 7.2 Biblioteca 14 — Públicos e Segmentos

Define públicos, segmentos, universos, características, interesses, comportamentos, territórios e contextos relevantes.

A jornada aplicada a um público, a prioridade estratégica e os pontos de contato selecionados são relações contextuais do planejamento, e não atributos permanentes do público.

### 7.3 Biblioteca 15 — Objetivos, Resultados e KPIs

Define objetivos de marketing, comunicação e mídia; resultados pretendidos; indicadores; famílias; possibilidade de metas; requisitos; estados de operacionalização; e relações objetivo–resultado–indicador.

Um indicador torna-se KPI quando recebe prioridade decisória em um planejamento específico.

### 7.4 Biblioteca 16 — Jornadas, Necessidades, Funções e Pontos de Contato

Define:

- modelos de jornada;
- etapas de cada jornada;
- necessidades comunicacionais relacionadas às etapas;
- funções relacionadas simultaneamente à etapa e à necessidade;
- pontos de contato entendidos como categorias de mídia;
- relações função–ponto de contato.

Não cadastra formatos nem inventários.

### 7.5 Biblioteca 17 — Conhecimento Técnico

Organiza conhecimentos técnicos reutilizáveis do domínio do planejamento de mídia, incluindo:

- conceitos e definições;
- modelos matemáticos;
- fórmulas principais e derivadas;
- equivalências e conversões;
- entradas e saídas;
- pré-condições;
- regras operacionais;
- limitações e exceções;
- condições de comparabilidade;
- interpretações;
- aplicações;
- referências e versões.

A Biblioteca 17 descreve o que o especialista sabe. Não organiza objetivos, resultados ou KPIs, que pertencem à Biblioteca 15, nem decide qual problema deve ser resolvido.

### 7.6 Biblioteca 18 — Problemas Técnicos de Planejamento de Mídia

Organiza situações decisórias que os motores especialistas podem resolver.

Cada problema deve declarar, no mínimo:

- objetivo decisório;
- contexto e gatilho;
- entradas e saídas;
- pré-condições e restrições;
- conhecimentos técnicos aplicáveis;
- procedimentos possíveis;
- critérios de escolha entre procedimentos;
- nível de automação;
- exigências de explicabilidade;
- estados de confiança e conclusão.

A Biblioteca 18 descreve como o especialista mobiliza conhecimento para resolver problemas. Os problemas são estáveis; os conhecimentos, fórmulas e algoritmos utilizados podem evoluir.

### 7.7 Biblioteca 19 — Custos e Condições Comerciais

Organiza preços, unidades comerciais, tabelas, descontos, bonificações, comissões, fees, pacotes, patrocínios, custos de tecnologia, produção e dados, vigências, moedas, impostos, condições de pagamento, disponibilidade e demais estruturas comerciais.

Ela fornece dados e condições aos cálculos descritos na Biblioteca 17 e aos problemas econômicos organizados na Biblioteca 18.

### 7.8 Biblioteca 20 — Regras, Restrições e Referências Metodológicas

Organiza regras transversais de elegibilidade, exclusão, governança, conformidade, proteção de marca, território, público, disponibilidade, mínimos de investimento e limites operacionais, além de referências metodológicas gerais.

Regras internas de cálculo ou de aplicação de um conhecimento específico permanecem na Biblioteca 17. Regras transversais a vários objetos, problemas ou procedimentos pertencem à Biblioteca 20.

### 7.9 Biblioteca 21 — Modelos e Componentes Reutilizáveis

Organiza estruturas compostas e versionadas que podem ser reutilizadas como ponto de partida, tais como:

- arquiteturas de referência;
- modelos de flight;
- matrizes de pesos;
- cenários padrão;
- configurações de jornada;
- combinações de pontos de contato;
- estratégias de lançamento, sustentação e continuidade;
- componentes de simulação;
- modelos de relatório e plano.

Modelos são referências ajustáveis, não prescrições universais.

### 7.10 Planejamento

O projeto armazena instâncias selecionadas, prioridades, KPIs efetivos, metas, valores projetados, parâmetros, ajustes, justificativas e snapshots.

---

## 8. Relação entre conhecimento, problema e motor

```text
Objeto de Conhecimento Técnico
    ↓ participa de
Problema Técnico
    ↓ admite
Procedimentos de resolução
    ↓ são selecionados e executados por
Motores especialistas
    ↓ produzem
Resposta, justificativa, confiança e rastreabilidade
```

Os motores não acessam fórmulas isoladas como primeira operação. Eles identificam o problema técnico, consultam os conhecimentos e procedimentos relacionados, verificam as pré-condições e selecionam a alternativa aplicável ao contexto.

A relação entre problemas e conhecimentos é N:N:

- um problema pode utilizar vários conhecimentos;
- um conhecimento pode participar de vários problemas;
- cada vínculo deve preservar papel, obrigatoriedade, prioridade, contexto e confiança.

---

## 9. Quatro famílias de indicadores

A Biblioteca 15 define:

1. Planejamento e pressão de mídia;
2. Entrega;
3. Eficiência;
4. Resposta.

Um indicador torna-se KPI quando recebe prioridade decisória em um planejamento específico.

Um inventário não possui KPI permanente; declara compatibilidade e capacidade de projeção ou mensuração posterior.

Conhecimentos sobre cálculo, interpretação e limitações dos indicadores pertencem à Biblioteca 17. Problemas que utilizam esses indicadores pertencem à Biblioteca 18.

---

## 10. Dimensões compartilhadas

Devem existir catálogos compartilhados e relações N:N para:

- objetivos;
- resultados;
- indicadores;
- famílias de indicadores;
- jornadas;
- etapas;
- necessidades comunicacionais;
- funções comunicacionais;
- pontos de contato;
- interesses;
- comportamentos;
- contextos de contato;
- territórios;
- temas editoriais;
- tipologias de inventário;
- famílias de conhecimento;
- objetos de conhecimento técnico;
- categorias de problema;
- problemas técnicos;
- procedimentos de resolução;
- regras e restrições;
- modelos reutilizáveis.

Cada vínculo preserva atributos próprios.

---

## 11. Separações ontológicas e funcionais obrigatórias

```text
Jornada ≠ tipo de cliente ou setor
Etapa ≠ objetivo
Necessidade ≠ função
Função ≠ propriedade essencial do meio
Ponto de contato = categoria de mídia
Ponto de contato ≠ formato ou peça
Inventário ≠ ponto de contato
Indicador ≠ KPI permanente
Meta ≠ objeto da biblioteca
Conhecimento técnico ≠ indicador
Conhecimento técnico ≠ problema técnico
Problema técnico ≠ procedimento
Problema técnico ≠ motor
Fórmula ≠ problema
Algoritmo ≠ objetivo decisório
Custo calculado ≠ condição comercial cadastrada
Regra interna de conhecimento ≠ regra transversal
Modelo reutilizável ≠ decisão automática
```

---

## 12. Qualificações da Arquitetura

A Arquitetura integra, no mínimo:

- objetivo–resultado;
- resultado–indicador;
- indicador–inventário;
- etapa–necessidade–função;
- função–ponto de contato;
- ponto de contato–tipologia de inventário;
- público–inventário;
- território–cobertura;
- problema–conhecimento;
- problema–procedimento;
- procedimento–regra;
- custos, restrições e disponibilidade;
- modelo–componentes.

Nenhuma dessas relações determina isoladamente a seleção final.

---

## 13. Explicabilidade e rastreabilidade

Toda recomendação produzida pelos motores deve permitir recuperar:

```text
Problema identificado
    ↓
Dados e entradas utilizados
    ↓
Objetos de conhecimento consultados
    ↓
Procedimento selecionado
    ↓
Regras e restrições aplicadas
    ↓
Cálculos e transformações
    ↓
Alternativas avaliadas
    ↓
Resultado e nível de confiança
    ↓
Justificativa apresentada ao usuário
```

O sistema não deve apresentar uma recomendação como certeza quando faltarem dados, houver incompatibilidade metodológica ou a solução depender de proxy, hipótese ou julgamento humano.

---

## 14. Escopos, estados e proveniência

Objetos e relações podem possuir escopo global, de espaço de trabalho, de projeto ou pessoal/rascunho.

Estados editoriais recomendados:

```text
RASCUNHO
PROPOSTO
EM_REVISAO
VALIDADO
PUBLICADO
SUSPENSO
SUBSTITUIDO
ARQUIVADO
REJEITADO
```

Bibliotecas especializadas podem acrescentar estados próprios, desde que mapeáveis aos estados editoriais gerais.

Devem ser preservados fonte, autoria, método, data, validade, território, limitações, natureza do dado e nível de confiança.

---

## 15. Versionamento e snapshot

```text
Cadastro mestre
    ↓
Seleção no projeto
    ↓
Snapshot
    ↓
Ajustes locais
    ↓
Uso nos motores
    ↓
Registro da decisão
```

Alterações futuras no cadastro mestre não modificam retroativamente planejamentos anteriores.

Problemas, conhecimentos, procedimentos, regras e modelos devem possuir versões independentes. A atualização de um conhecimento ou procedimento não substitui automaticamente a versão utilizada em um projeto anterior.

---

## 16. Princípio consolidado

> As bibliotecas ontológicas descrevem os objetos do domínio; a Biblioteca 17 formaliza o que o especialista sabe; a Biblioteca 18 organiza os problemas que esse conhecimento pode resolver; e as bibliotecas operacionais fornecem custos, regras e modelos para aplicação contextual. Os motores especialistas identificam problemas, selecionam conhecimentos e procedimentos, verificam restrições e produzem alternativas justificadas, rastreáveis e versionadas para o planejamento de mídia.
