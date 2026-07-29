# Biblioteca de Objetivos, Resultados e KPIs do MediAd Planner

**Documento:** `15_BIBLIOTECA_DE_OBJETIVOS_RESULTADOS_E_KPIS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Objetivos, Resultados e KPIs organiza os objetivos que podem orientar um plano de mídia, os resultados pretendidos associados a esses objetivos e os indicadores que podem receber metas, ser projetados nas simulações ou ser posteriormente mensurados por fontes externas ao MediAd Planner.

A Biblioteca responde, de forma estruturada, às seguintes questões:

```text
Para este objetivo,
quais resultados podem ser pretendidos?

Para este resultado,
quais indicadores são pertinentes?

Quais desses indicadores podem receber metas no plano?

Em quais mídias, formatos, modelos de compra e inventários
esses indicadores podem ser projetados ou posteriormente mensurados?
```

O MediAd Planner elabora planos de mídia. Não acompanha campanhas em execução e não armazena resultados realizados.

---

## 2. Limites

A Biblioteca deve:

- manter vocabulários controlados de objetivos, resultados e indicadores;
- organizar relações entre objetivos e resultados pretendidos;
- organizar relações entre resultados e indicadores possíveis;
- classificar indicadores em quatro famílias;
- declarar se um indicador pode receber meta;
- declarar se pode ser calculado, projetado ou apenas recomendado;
- registrar requisitos de dados;
- relacionar indicadores com meios, ambientes, formatos, modelos de compra, unidades e inventários;
- informar possibilidades e limites de mensuração posterior;
- preservar fontes, versões, validade e confiança.

A Biblioteca não deve:

- receber resultados realizados de campanhas;
- acompanhar veiculação;
- comparar planejado e realizado;
- emitir alertas de performance;
- calcular cumprimento de metas;
- otimizar campanha em curso;
- substituir plataformas de mídia, ad servers, analytics, pesquisas ou sistemas de atribuição.

---

## 3. Cadeia conceitual

```text
Objetivo
    ↓
Resultado pretendido
    ↓
Indicadores possíveis
    ↓
Indicadores compatíveis com os inventários
    ↓
Metas do planejamento
    ↓
Projeções das simulações
    ↓
Plano consolidado
```

A mensuração posterior pode ser recomendada no plano, mas ocorre fora do MediAd Planner.

---

## 4. Conceitos fundamentais

### 4.1 Objetivo

Objetivo é a direção estratégica do que o plano de mídia pretende produzir ou favorecer.

Exemplos:

- ampliar notoriedade;
- aumentar consideração;
- construir alcance;
- ampliar cobertura territorial;
- sustentar frequência;
- gerar tráfego;
- estimular resposta;
- apoiar conversões;
- reforçar presença de marca;
- sustentar lançamento;
- apoiar fidelização.

O objetivo pode ser qualitativo e não precisa conter um valor numérico.

### 4.2 Resultado pretendido

Resultado pretendido é a transformação esperada associada ao objetivo.

Exemplo:

```text
Objetivo:
ampliar notoriedade

Resultado pretendido:
aumentar o reconhecimento da marca entre o público prioritário
```

### 4.3 Indicador

Indicador é uma variável capaz de representar pressão, entrega, eficiência ou resposta relacionada ao plano.

Um indicador pode ser:

- fornecido como entrada;
- calculado;
- projetado;
- estimado por benchmark;
- recomendado para mensuração posterior;
- indisponível em determinado contexto.

### 4.4 Métrica

Métrica é uma medida operacional, observada, fornecida, estimada ou calculada.

Nem toda métrica é KPI.

### 4.5 KPI

KPI é um indicador selecionado como prioritário para avaliar um objetivo ou resultado dentro de um planejamento específico.

```text
Indicador = objeto reutilizável da biblioteca.
KPI = função prioritária assumida pelo indicador no projeto.
```

O mesmo indicador pode ser KPI em uma campanha e apenas métrica diagnóstica em outra.

### 4.6 Meta

Meta é o valor pretendido para um indicador em determinado contexto de planejamento.

Pode estar vinculada a:

- campanha;
- versão do planejamento;
- cenário;
- público;
- segmento;
- universo;
- praça;
- período;
- etapa da jornada;
- meio;
- canal;
- inventário.

A meta não pertence permanentemente ao indicador. A biblioteca pode conter referências e benchmarks, mas a meta efetiva pertence ao planejamento.

---

## 5. Quatro famílias de indicadores

### 5.1 Planejamento e pressão de mídia

Representam a intensidade, extensão, repetição, continuidade ou distribuição planejada da comunicação.

Exemplos:

- alcance;
- cobertura;
- frequência;
- impactos;
- audiência;
- GRP;
- TRP;
- continuidade;
- concentração temporal;
- distribuição temporal;
- presença territorial;
- cobertura territorial;
- participação de voz, quando aplicável.

Esses indicadores podem constituir metas centrais do plano.

Exemplos:

```text
Alcance planejado: 70% do universo prioritário
Frequência média planejada: 4 exposições
Cobertura territorial planejada: 90% das praças prioritárias
Pressão planejada: 280 GRP no período
```

### 5.2 Entrega

Representam o volume de exposição, presença, inserção ou disponibilização associado ao inventário e ao modelo de compra.

Exemplos:

- impressões;
- inserções;
- exibições;
- visualizações;
- faces;
- circuitos;
- espaços;
- sessões;
- tempo de exposição;
- ocupação;
- volume contratado;
- volume estimado de entrega.

### 5.3 Eficiência

Relacionam investimento, pressão, entrega ou resposta.

Exemplos:

- CPM;
- CPP;
- CPC;
- CPV;
- CPA;
- CPL;
- custo por alcance;
- custo por impacto;
- custo por ponto;
- custo por inserção;
- custo por período;
- ROAS projetado, quando houver parâmetros suficientes.

Indicadores de eficiência são geralmente derivados e dependem de métricas básicas e fórmulas definidas na Biblioteca de Parâmetros, Métricas e Fórmulas.

### 5.4 Resposta

Representam comportamentos ou efeitos observáveis do público.

Exemplos:

- cliques;
- CTR;
- visitas;
- sessões;
- downloads;
- cadastros;
- leads;
- conversões;
- compras;
- receita atribuída;
- taxa de conversão;
- share de busca;
- interações;
- respostas diretas.

Esses indicadores dependem de mecanismos de rastreamento, atribuição, pesquisa ou coleta externos ao MediAd Planner.

---

## 6. Capacidades do indicador

Cada indicador deverá declarar separadamente:

- pode receber meta;
- pode ser calculado no planejamento;
- pode ser projetado em simulação;
- pode ser estimado por benchmark;
- pode ser fornecido pelo veículo, plataforma ou fornecedor;
- pode ser posteriormente mensurado;
- exige fonte externa;
- exige mecanismo de rastreamento;
- exige pesquisa;
- exige atribuição;
- possui limitações conhecidas;
- grau de confiança possível.

Essas capacidades não são equivalentes.

```text
Pode receber meta
≠
Pode ser projetado
≠
Pode ser posteriormente mensurado
```

---

## 7. Requisitos de dados

Cada indicador deve declarar suas dependências.

Exemplos:

```text
Frequência
requer impactos e alcance,
ou dados equivalentes de audiência e exposição.

CTR
requer impressões e cliques.

GRP
requer audiência percentual e quantidade de inserções,
ou impactos e universo compatíveis.

CPA
requer investimento e conversões atribuídas.

ROAS
requer investimento e receita atribuída.

Cobertura territorial
requer territórios pretendidos e áreas atendidas.
```

A ausência de uma dependência deve impedir o cálculo ou reduzir explicitamente a confiança da projeção.

---

## 8. Relações de conhecimento

A Biblioteca deve manter relações N:N entre:

```text
Objetivos ↔ Resultados pretendidos
Resultados pretendidos ↔ Indicadores
Indicadores ↔ Famílias
Indicadores ↔ Etapas da jornada
Indicadores ↔ Funções de mídia
Indicadores ↔ Meios e canais
Indicadores ↔ Ambientes
Indicadores ↔ Formatos
Indicadores ↔ Modelos de compra
Indicadores ↔ Unidades de compra
Indicadores ↔ Inventários
```

Cada relação pode registrar:

- aplicabilidade;
- intensidade ou prioridade sugerida;
- condição;
- requisitos;
- restrições;
- fonte;
- validade;
- confiança;
- observações metodológicas.

---

## 9. Relação com a Biblioteca de Inventários

A Biblioteca 15 define os indicadores e suas propriedades gerais.

A Biblioteca de Inventários declara quais indicadores são compatíveis com cada oportunidade concreta de mídia.

```text
Biblioteca 15
Define o indicador
        ↓
Biblioteca 13
Declara a capacidade do inventário
        ↓
Arquitetura de Mídia
Relaciona prioridades e capacidades
```

O inventário não possui um KPI permanente. Ele possui capacidades analíticas.

Exemplo:

```text
Indicador: CTR

Inventário A:
compatível = sim
projetável = sim
mensurável posteriormente = sim

Inventário B:
compatível = não
```

O indicador se torna KPI apenas quando priorizado no planejamento.

---

## 10. Relação com a Biblioteca de Parâmetros, Métricas e Fórmulas

A Biblioteca 15 responde:

> O que deve ou pode ser observado para avaliar determinado objetivo ou resultado?

A Biblioteca de Parâmetros, Métricas e Fórmulas responde:

> Como o indicador é definido, calculado, convertido ou estimado?

Portanto, fórmulas, unidades, conversões, dependências matemáticas, valores paramétricos e benchmarks numéricos não devem ser duplicados neste documento.

---

## 11. Relação com a Arquitetura de Mídia

A Arquitetura de Mídia deve operar pela cadeia:

```text
Objetivos
    ↓
Resultados pretendidos
    ↓
Indicadores prioritários
    ↓
Inventários compatíveis
    ↓
Arquiteturas candidatas
```

A seleção de inventários não deve depender apenas de associações genéricas como “bom para branding” ou “bom para performance”. Deve considerar quais indicadores o inventário é capaz de suportar, projetar ou permitir mensurar.

---

## 12. Metas do planejamento

Uma meta deve registrar, no mínimo:

- indicador;
- valor ou faixa pretendida;
- unidade;
- direção desejada;
- contexto;
- público ou universo;
- praça;
- período;
- escopo;
- origem;
- responsável;
- grau de confiança;
- observações.

Tipos de direção:

- atingir;
- no mínimo;
- no máximo;
- manter;
- aumentar;
- reduzir;
- faixa desejada.

Metas podem incidir sobre as quatro famílias.

---

## 13. Natureza e confiança

Indicadores, relações e referências devem declarar sua natureza:

- observado;
- fornecido;
- calculado;
- projetado;
- estimado;
- modelado;
- benchmark;
- recomendado;
- não disponível.

O sistema deve distinguir claramente valor calculado, valor ajustado e valor efetivo utilizado na simulação.

---

## 14. Modelo lógico mínimo

Entidades conceituais recomendadas:

```text
objetivos
resultados_pretendidos
familias_indicadores
indicadores
objetivos_resultados
resultados_indicadores
indicadores_jornadas
indicadores_funcoes
indicadores_requisitos
indicadores_aplicabilidades
metas_planejamento
planejamentos_indicadores
```

As relações específicas com inventários pertencem à Biblioteca de Inventários, embora referenciem o catálogo canônico de indicadores.

---

## 15. Princípio consolidado

> A Biblioteca de Objetivos, Resultados e KPIs define o que o plano pretende produzir, quais resultados podem evidenciar esse propósito e quais indicadores podem receber metas, ser projetados ou ser recomendados para mensuração posterior. O MediAd Planner não acompanha campanhas nem armazena resultados realizados. Um indicador somente se torna KPI quando recebe prioridade decisória em um planejamento específico.