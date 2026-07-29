# Sistema de Bibliotecas do MediAd Planner

**Documento:** `12_SISTEMA_DE_BIBLIOTECAS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

O Sistema de Bibliotecas organiza os conhecimentos reutilizáveis que sustentam o planejamento de mídia no MediAd Planner.

Seu objetivo é evitar que cada projeto reconstrua do zero conceitos, parâmetros, referências, classificações, inventários, públicos, objetivos, resultados, indicadores, métricas, custos e modelos de planejamento.

As bibliotecas não substituem o julgamento do planejador. Elas fornecem objetos estruturados, versionados e rastreáveis para apoiar:

- o Briefing;
- a Tradução Estratégica;
- a Arquitetura de Mídia;
- as Simulações;
- a Comparação de Cenários;
- a Otimização;
- o Plano Consolidado;
- o Cronograma;
- o Mapa de Veiculação.

```text
Base de conhecimento fornece referências.
Motores processam relações.
Usuários tomam decisões.
Planos preservam as versões utilizadas.
```

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

O Sistema de Bibliotecas é transversal a todos os ambientes do aplicativo. Ele não constitui uma etapa isolada do planejamento.

Seus objetos são consultados, selecionados, adaptados e instanciados ao longo do fluxo.

---

## 3. Distinções fundamentais

### 3.1 Catálogo

Catálogo é um vocabulário controlado utilizado para classificar objetos.

Exemplos:

- tecnologia;
- canal;
- ambiente;
- formato;
- modalidade de compra;
- unidade comercial;
- tipo de objetivo;
- tipo de resultado;
- família de indicador;
- etapa de jornada;
- interesse;
- comportamento;
- tipo territorial;
- unidade métrica.

### 3.2 Biblioteca

Biblioteca é uma coleção de objetos reutilizáveis e contextualizados.

Exemplos:

- inventários;
- públicos;
- universos;
- modelos de jornada;
- objetivos;
- resultados pretendidos;
- indicadores;
- parâmetros;
- fórmulas;
- regras;
- benchmarks;
- modelos de arquitetura.

Bibliotecas podem possuir versões, fontes, escopos, validade, autoria, confiança e relações com outros objetos.

### 3.3 Relação de conhecimento

Relação de conhecimento conecta dois ou mais objetos.

Exemplos:

- objetivo associado a resultado pretendido;
- resultado associado a indicador;
- indicador compatível com inventário;
- interesse do público compatível com proposta editorial;
- comportamento do público compatível com contexto de contato;
- território do público sobreposto à cobertura do veículo;
- afinidade observada entre público e veículo ou programa;
- ponto de contato atendido por meio;
- formato compatível com ambiente;
- unidade compatível com modalidade de compra.

Relações não devem ser tratadas automaticamente como verdades universais. Quando necessário, devem admitir contexto, fonte, versão, território, período e nível de confiança.

### 3.4 Parâmetro

Parâmetro é um valor utilizado por regras, fórmulas ou motores.

Exemplos:

- peso de aderência;
- limite de saturação;
- frequência desejada;
- faixa de confiança;
- coeficiente de equivalência;
- tolerância de orçamento;
- fator de sobreposição.

### 3.5 Instância de projeto

Uma instância de projeto é a cópia contextual de um objeto da biblioteca utilizada em um planejamento específico.

```text
Objeto da biblioteca
        ↓
Seleção
        ↓
Instância no projeto
        ↓
Adaptação contextual
        ↓
Uso no planejamento
```

A instância pode manter vínculo com a origem, mas deve preservar os dados efetivamente utilizados no projeto.

---

## 4. Núcleos do Sistema de Bibliotecas

O sistema será composto pelos seguintes núcleos:

1. Biblioteca de Inventários de Mídia;
2. Biblioteca de Públicos e Segmentos;
3. Biblioteca de Objetivos, Resultados e KPIs;
4. Biblioteca de Jornadas, Pontos de Contato e Funções;
5. Biblioteca de Parâmetros, Métricas e Fórmulas;
6. Biblioteca de Custos e Condições Comerciais;
7. Biblioteca de Regras, Restrições e Referências Metodológicas;
8. Biblioteca de Modelos e Componentes Reutilizáveis.

Sequência documental:

```text
12_SISTEMA_DE_BIBLIOTECAS.md
        ↓
13_BIBLIOTECA_DE_INVENTARIOS.md
        ↓
14_BIBLIOTECA_DE_PUBLICOS_E_SEGMENTOS.md
        ↓
15_BIBLIOTECA_DE_OBJETIVOS_RESULTADOS_E_KPIS.md
        ↓
16_BIBLIOTECA_DE_JORNADAS_PONTOS_DE_CONTATO_E_FUNCOES.md
        ↓
17_BIBLIOTECA_DE_PARAMETROS_METRICAS_E_FORMULAS.md
        ↓
18_BIBLIOTECA_DE_CUSTOS_E_CONDICOES_COMERCIAIS.md
        ↓
19_BIBLIOTECA_DE_REGRAS_E_REFERENCIAS.md
        ↓
20_BIBLIOTECA_DE_MODELOS_REUTILIZAVEIS.md
```

Cada núcleo possuirá entidades próprias. Não será criada uma tabela genérica única para todos os tipos de biblioteca.

---

## 5. Dependência entre objetivos, indicadores e inventários

A relação metodológica central passa a ser:

```text
Biblioteca de Objetivos, Resultados e KPIs
        ↓
Define objetivos, resultados e indicadores possíveis
        ↓
Biblioteca de Inventários
        ↓
Declara capacidades analíticas e compatibilidades
        ↓
Arquitetura de Mídia
        ↓
Relaciona prioridades e capacidades
        ↓
Simulações
        ↓
Plano Consolidado
```

A seleção de mídia não deve depender apenas de associações diretas entre objetivo e inventário.

Cadeia canônica:

```text
Objetivo
    ↓
Resultado pretendido
    ↓
Indicadores prioritários
    ↓
Inventários compatíveis
    ↓
Arquiteturas candidatas
```

Um inventário não possui KPI permanente. Ele possui capacidades de suportar, projetar ou permitir mensurar determinados indicadores.

Um indicador torna-se KPI apenas quando recebe prioridade decisória em um planejamento específico.

---

## 6. Responsabilidades de cada biblioteca

### 6.1 Biblioteca de Objetivos, Resultados e KPIs

Define:

- objetivos;
- resultados pretendidos;
- indicadores;
- quatro famílias de indicadores;
- relações objetivo–resultado;
- relações resultado–indicador;
- possibilidade de definição de metas;
- requisitos gerais;
- possibilidades de projeção e mensuração posterior.

### 6.2 Biblioteca de Inventários

Declara:

- estrutura operacional;
- propriedades editoriais e contextuais;
- cobertura territorial;
- segmentações disponíveis;
- indicadores compatíveis;
- indicadores projetáveis;
- indicadores posteriormente mensuráveis;
- requisitos e fontes de dados;
- limitações e confiança.

### 6.3 Biblioteca de Parâmetros, Métricas e Fórmulas

Define:

- métricas básicas e derivadas;
- unidades;
- fórmulas;
- conversões;
- dependências;
- parâmetros de cálculo;
- benchmarks numéricos.

### 6.4 Planejamento

Armazena:

- indicadores selecionados;
- KPIs efetivos;
- metas;
- valores projetados;
- ajustes do planejador;
- snapshots das versões utilizadas.

Resultados realizados de campanhas não pertencem ao escopo do MediAd Planner.

---

## 7. Quatro famílias compartilhadas de indicadores

O catálogo canônico deve reconhecer:

1. Planejamento e pressão de mídia;
2. Entrega;
3. Eficiência;
4. Resposta.

Essas famílias são definidas pela Biblioteca 15 e reutilizadas pelas demais bibliotecas e motores.

---

## 8. Princípio das dimensões compartilhadas

Públicos, inventários e indicadores precisam ser descritos por dimensões comparáveis para que a Arquitetura de Mídia calcule suas relações.

Devem existir catálogos compartilhados, associados por relações N:N:

- interesses;
- comportamentos;
- contextos de consumo e contato;
- etapas da jornada;
- pontos de contato;
- funções de mídia;
- variáveis demográficas;
- territórios e praças;
- temas e gêneros editoriais;
- objetivos;
- resultados pretendidos;
- indicadores;
- famílias de indicadores.

Cada vínculo deve registrar atributos próprios, como intensidade, relevância, origem, fonte, validade e confiança.

---

## 9. Separação entre públicos e audiência

A Biblioteca de Públicos e Segmentos define quem se pretende alcançar e onde esse público se encontra.

Ela não armazena como atributos permanentes do público:

- audiência;
- alcance;
- cobertura;
- frequência;
- impactos;
- afinidade medida.

Essas variáveis dependem da relação entre público, veículo ou inventário, praça, período, fonte e metodologia.

```text
Público
+
Veículo, programa ou inventário
+
Praça
+
Período
+
Fonte e metodologia
=
Evidência, estimativa ou resultado de mídia
```

Audiência e cobertura podem ser fornecidas por veículos, programas, redes, plataformas, disponibilizações ou inventários em contextos definidos. Alcance e frequência são metas ou resultados projetados de veiculações, cenários ou planos.

Afinidade observada é uma relação medida entre público e mídia, não atributo isolado de qualquer biblioteca.

---

## 10. Qualificação público–inventário e indicador–inventário

A Arquitetura de Mídia deve integrar duas qualificações complementares.

### 10.1 Qualificação público–inventário

```text
Biblioteca de Públicos
↔
Biblioteca de Inventários
```

Compara:

- demografia;
- interesses;
- comportamentos;
- jornada;
- pontos de contato;
- territórios;
- proposta editorial;
- contextos de contato;
- segmentações;
- cobertura territorial.

### 10.2 Qualificação indicador–inventário

```text
Biblioteca de Objetivos, Resultados e KPIs
↔
Biblioteca de Inventários
```

Compara:

- indicadores prioritários;
- compatibilidade do inventário;
- capacidade de projeção;
- possibilidade de mensuração posterior;
- requisitos de dados;
- fontes disponíveis;
- limitações;
- confiança.

As duas qualificações compõem o cálculo dinâmico de adequação e não constituem motores concorrentes.

---

## 11. Escopos

Todo objeto reutilizável deve possuir escopo explícito:

- global;
- espaço de trabalho;
- projeto;
- pessoal ou rascunho.

Itens pessoais não participam dos motores compartilhados até serem promovidos.

---

## 12. Estados editoriais

Estados recomendados:

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

O estado editorial deve permanecer separado do estado operacional.

---

## 13. Inclusão de informações

Toda inclusão deve declarar, no mínimo:

- tipo de objeto;
- nome ou título;
- escopo;
- autor;
- estado editorial;
- fonte, quando aplicável;
- data da fonte;
- território ou praça, quando aplicável;
- período de validade, quando aplicável;
- unidade, quando aplicável;
- natureza do dado;
- nível de confiança;
- restrições de uso;
- observações metodológicas.

---

## 14. Natureza dos dados

Categorias recomendadas:

- observado;
- declarado;
- fornecido comercialmente;
- benchmark;
- estimado;
- calculado;
- convertido;
- modelado;
- inferido;
- recomendado;
- padrão do sistema;
- não disponível.

A natureza do dado deve acompanhar o valor até seu uso em uma simulação ou plano.

---

## 15. Proveniência, confiança e snapshot

Cada objeto, relação ou versão deve poder registrar:

- fonte original;
- responsável pela coleta;
- método de coleta;
- data de obtenção;
- documento de suporte;
- transformações realizadas;
- unidade original;
- território;
- período;
- limitações;
- nível de confiança.

Ao selecionar um item reutilizável, o projeto deve guardar uma fotografia versionada das informações utilizadas.

Alterações futuras no cadastro mestre não devem modificar retroativamente planejamentos anteriores.

---

## 16. Princípio consolidado

> As bibliotecas descrevem objetos, relações e capacidades reutilizáveis. A Biblioteca de Objetivos, Resultados e KPIs define o que pode ser pretendido e observado; a Biblioteca de Inventários declara quais indicadores cada oportunidade de mídia suporta; a Biblioteca de Parâmetros, Métricas e Fórmulas define como os cálculos são realizados; e a Arquitetura de Mídia conecta essas informações ao Briefing e à Tradução Estratégica. O MediAd Planner planeja e projeta, mas não acompanha resultados realizados de campanhas.