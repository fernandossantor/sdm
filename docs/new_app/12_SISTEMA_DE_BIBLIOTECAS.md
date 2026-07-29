# Sistema de Bibliotecas do MediAd Planner

**Documento:** `12_SISTEMA_DE_BIBLIOTECAS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

O Sistema de Bibliotecas organiza conhecimentos reutilizáveis, versionados e rastreáveis que sustentam o planejamento de mídia no MediAd Planner.

As bibliotecas fornecem referências estruturadas; os motores processam relações; os usuários tomam decisões; os projetos preservam as versões efetivamente utilizadas.

O sistema não acompanha campanhas em execução nem armazena resultados realizados.

---

## 2. Posição na arquitetura

```text
Catálogos
    ↓
Bibliotecas
    ↓
Relações e parâmetros
    ↓
Motores de planejamento
    ↓
Artefatos do projeto
```

As bibliotecas são transversais ao Briefing, à Tradução Estratégica, à Arquitetura de Mídia, às Simulações, à Comparação, à Otimização e ao Plano Consolidado.

---

## 3. Distinções fundamentais

### 3.1 Catálogo

Vocabulário controlado utilizado para classificar objetos, como tecnologia, canal, ambiente, formato, modalidade de compra, tipo de objetivo, tipo de resultado, família de indicador, etapa de jornada, necessidade, função, ponto de contato, território e unidade métrica.

### 3.2 Biblioteca

Coleção de objetos reutilizáveis e contextualizados, como inventários, públicos, jornadas, objetivos, resultados, indicadores, necessidades comunicacionais, funções, pontos de contato, parâmetros, fórmulas, custos, regras e modelos.

### 3.3 Relação de conhecimento

Vínculo contextual entre objetos. Deve admitir, quando aplicável, fonte, versão, território, período, intensidade, prioridade e confiança.

Exemplos:

- objetivo associado a resultado pretendido;
- resultado associado a indicador;
- jornada composta por etapas;
- etapa associada a necessidade comunicacional;
- combinação etapa–necessidade associada a função;
- função associada a ponto de contato;
- ponto de contato associado a tipologia de inventário;
- indicador compatível com inventário;
- público compatível com propriedades de inventário.

### 3.4 Parâmetro

Valor utilizado por regra, fórmula ou motor, como peso, limite, tolerância, frequência desejada, fator de overlap ou coeficiente de equivalência.

### 3.5 Instância de projeto

Cópia contextual e versionada de um objeto da biblioteca utilizada em um planejamento específico.

---

## 4. Núcleos do Sistema de Bibliotecas

1. Biblioteca de Inventários de Mídia;
2. Biblioteca de Públicos e Segmentos;
3. Biblioteca de Objetivos, Resultados e KPIs;
4. Biblioteca de Jornadas, Necessidades, Funções e Pontos de Contato;
5. Biblioteca de Parâmetros, Métricas e Fórmulas;
6. Biblioteca de Custos e Condições Comerciais;
7. Biblioteca de Regras, Restrições e Referências Metodológicas;
8. Biblioteca de Modelos e Componentes Reutilizáveis.

Sequência documental:

```text
12_SISTEMA_DE_BIBLIOTECAS.md
13_BIBLIOTECA_DE_INVENTARIOS.md
14_BIBLIOTECA_DE_PUBLICOS_E_SEGMENTOS.md
15_BIBLIOTECA_DE_OBJETIVOS_RESULTADOS_E_KPIS.md
16_BIBLIOTECA_DE_JORNADAS_NECESSIDADES_FUNCOES_E_PONTOS_DE_CONTATO.md
17_BIBLIOTECA_DE_PARAMETROS_METRICAS_E_FORMULAS.md
18_BIBLIOTECA_DE_CUSTOS_E_CONDICOES_COMERCIAIS.md
19_BIBLIOTECA_DE_REGRAS_E_REFERENCIAS.md
20_BIBLIOTECA_DE_MODELOS_REUTILIZAVEIS.md
```

Cada núcleo possui entidades próprias. Não deve existir uma tabela genérica única para todas as bibliotecas.

---

## 5. Cadeia estratégica canônica

```text
Objetivo
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
Arquiteturas candidatas
```

A seleção não começa pelo meio ou inventário.

O ponto de contato é uma categoria de mídia. Formatos, peças, ambientes, plataformas, programas, posicionamentos e unidades comerciais pertencem ao desdobramento tipológico da Biblioteca de Inventários.

---

## 6. Responsabilidades das bibliotecas

### 6.1 Objetivos, Resultados e KPIs

Define objetivos, resultados pretendidos, indicadores, famílias, possibilidade de metas, requisitos e relações objetivo–resultado–indicador.

### 6.2 Jornadas, Necessidades, Funções e Pontos de Contato

Define:

- modelos de jornada;
- etapas de cada jornada;
- necessidades comunicacionais relacionadas às etapas;
- funções relacionadas simultaneamente à etapa e à necessidade;
- pontos de contato entendidos como categorias de mídia;
- relações função–ponto de contato.

Não cadastra formatos nem inventários.

### 6.3 Inventários

Define a materialização tipológica e operacional dos pontos de contato em tecnologias, canais, ambientes, estruturas, formatos, meios, plataformas, programas, modelos comerciais, modalidades, unidades e inventários.

Declara também capacidades analíticas, cobertura, segmentações, propriedades editoriais e contextuais.

### 6.4 Públicos e Segmentos

Define públicos, segmentos, universos, características, interesses, comportamentos, territórios e contextos relevantes.

A jornada aplicada a um público é contextual ao planejamento, não atributo fixo desse público.

### 6.5 Parâmetros, Métricas e Fórmulas

Define métricas, unidades, fórmulas, conversões, dependências, benchmarks e parâmetros de cálculo.

### 6.6 Planejamento

Armazena instâncias selecionadas, prioridades, KPIs efetivos, metas, valores projetados, ajustes e snapshots.

---

## 7. Quatro famílias de indicadores

A Biblioteca 15 define:

1. Planejamento e pressão de mídia;
2. Entrega;
3. Eficiência;
4. Resposta.

Um indicador torna-se KPI quando recebe prioridade decisória em um planejamento específico.

Um inventário não possui KPI permanente; declara compatibilidade e capacidade de projeção ou mensuração posterior.

---

## 8. Dimensões compartilhadas

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
- tipologias de inventário.

Cada vínculo preserva atributos próprios.

---

## 9. Separações ontológicas obrigatórias

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
```

---

## 10. Qualificações da Arquitetura

A Arquitetura integra, no mínimo:

- objetivo–resultado;
- indicador–inventário;
- etapa–necessidade–função;
- função–ponto de contato;
- ponto de contato–tipologia de inventário;
- público–inventário;
- território–cobertura;
- restrições, custos e disponibilidade.

Nenhuma dessas relações determina isoladamente a seleção final.

---

## 11. Escopos, estados e proveniência

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

Devem ser preservados fonte, autoria, método, data, validade, território, limitações, natureza do dado e nível de confiança.

---

## 12. Versionamento e snapshot

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
```

Alterações futuras no cadastro mestre não modificam retroativamente planejamentos anteriores.

---

## 13. Princípio consolidado

> As bibliotecas descrevem objetos e relações reutilizáveis. A estratégia progride de objetivos e resultados para indicadores, jornadas, etapas, necessidades, funções e pontos de contato. Os pontos de contato são mídias; sua materialização em formatos e inventários pertence à Biblioteca de Inventários. A Arquitetura combina essas estruturas com públicos, restrições e capacidades para produzir alternativas justificadas.