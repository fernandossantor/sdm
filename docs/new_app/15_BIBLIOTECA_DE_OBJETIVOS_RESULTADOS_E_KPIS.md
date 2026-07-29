# Biblioteca de Objetivos, Resultados e KPIs do MediAd Planner

**Documento:** `15_BIBLIOTECA_DE_OBJETIVOS_RESULTADOS_E_KPIS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Objetivos, Resultados e KPIs organiza os objetivos que podem orientar um plano de mídia, os resultados pretendidos associados a esses objetivos e os indicadores que podem receber metas, ser projetados nas simulações ou ser posteriormente mensurados por fontes externas ao MediAd Planner.

```text
Objetivo
    ↓
Resultado pretendido
    ↓
Indicadores possíveis
    ↓
Indicadores prioritários / KPIs do planejamento
```

O MediAd Planner elabora planos. Não acompanha campanhas em execução e não armazena resultados realizados.

---

## 2. Limites

A Biblioteca deve:

- manter vocabulários controlados de objetivos, resultados e indicadores;
- organizar relações objetivo–resultado;
- organizar relações resultado–indicador;
- classificar indicadores em quatro famílias;
- declarar se um indicador pode receber meta;
- declarar se pode ser projetado, calculado ou apenas recomendado;
- registrar requisitos de dados;
- informar possibilidades e limites de mensuração posterior;
- relacionar indicadores com tipologias e capacidades de inventário;
- preservar fontes, versões, validade e confiança.

A Biblioteca não deve:

- receber resultados realizados;
- acompanhar veiculação;
- comparar planejado e realizado;
- emitir alertas de performance;
- calcular cumprimento de metas;
- otimizar campanha em curso;
- substituir plataformas de mídia, ad servers, analytics ou pesquisas.

---

## 3. Conceitos fundamentais

### 3.1 Objetivo

Direção estratégica que expressa o que o planejamento de mídia pretende favorecer.

### 3.2 Resultado pretendido

Mudança, condição ou efeito esperado que torna o objetivo mais observável e operacionalizável.

### 3.3 Indicador

Variável capaz de representar uma dimensão relevante do planejamento, da entrega, da eficiência ou da resposta.

### 3.4 KPI

Indicador que recebeu prioridade decisória em um planejamento específico.

```text
Indicador da biblioteca
+
Prioridade no planejamento
=
KPI contextual
```

### 3.5 Meta

Valor pretendido atribuído a um indicador dentro de um planejamento, público, praça, período ou cenário determinado.

Metas pertencem às instâncias de projeto, não ao cadastro permanente da biblioteca.

---

## 4. Quatro famílias de indicadores

### 4.1 Planejamento e pressão de mídia

Exemplos:

- alcance;
- cobertura;
- frequência;
- audiência;
- impactos;
- GRP;
- TRP;
- continuidade;
- afinidade.

### 4.2 Entrega

Exemplos:

- impressões;
- inserções;
- exibições;
- visualizações;
- faces;
- ocupação;
- volume distribuído.

### 4.3 Eficiência

Exemplos:

- CPM;
- CPP;
- CPC;
- CPA;
- CPL;
- CPV;
- custo por alcance;
- custo por impacto.

### 4.4 Resposta

Exemplos:

- cliques;
- CTR;
- leads;
- conversões;
- downloads;
- compras;
- receita;
- ROAS.

A classificação deve distinguir indicador, unidade, fórmula e natureza do dado.

---

## 5. Relações objetivo–resultado–indicador

As relações não são universais nem exclusivas.

Um objetivo pode admitir vários resultados. Um resultado pode ser observado por vários indicadores. Um indicador pode servir a diferentes resultados.

Cada relação deve registrar:

- contexto de aplicação;
- prioridade sugerida;
- condição de uso;
- limitações;
- fonte;
- validade;
- confiança.

---

## 6. Capacidades do indicador

Cada indicador deve declarar, quando aplicável:

- família;
- definição;
- unidade;
- natureza;
- pode receber meta;
- pode ser projetado;
- pode ser calculado;
- pode ser estimado;
- pode ser posteriormente mensurado;
- requisitos de dados;
- dependências;
- limitações;
- grau de confiança.

Fórmulas e parâmetros detalhados pertencem à Biblioteca 17.

---

## 7. Relação com jornadas e estruturas comunicacionais

Objetivos, resultados e indicadores não determinam diretamente um inventário.

A Biblioteca 16 introduz a mediação estratégica:

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
Função comunicacional
    ↓
Ponto de contato
```

A jornada organiza estados de progressão. As necessidades pertencem às etapas. As funções respondem simultaneamente às etapas e necessidades. Os pontos de contato são categorias de mídia.

Os indicadores podem restringir ou priorizar pontos de contato e inventários, mas não substituem a interpretação da jornada.

---

## 8. Relação com a Biblioteca de Inventários

A Biblioteca de Inventários declara:

- indicadores compatíveis;
- indicadores projetáveis;
- indicadores calculáveis;
- indicadores posteriormente mensuráveis;
- requisitos de dados;
- fontes;
- limitações;
- confiança.

```text
Indicador prioritário
    ↔
Capacidade analítica do inventário
```

Um inventário não possui KPI permanente.

---

## 9. Metas e valores projetados

A Biblioteca oferece indicadores reutilizáveis. O planejamento define:

- indicador selecionado;
- prioridade;
- meta;
- público;
- praça;
- período;
- cenário;
- valor projetado;
- tolerância;
- fonte ou premissa;
- confiança.

Resultados realizados não pertencem ao MediAd Planner.

---

## 10. Modelo lógico mínimo

```text
objetivos
resultados_pretendidos
indicadores
familias_indicadores
objetivos_resultados
resultados_indicadores
indicadores_requisitos
indicadores_tipologias
indicadores_inventarios
planejamentos_indicadores
planejamentos_metas
```

As relações devem preservar contexto, fonte, validade e confiança.

---

## 11. Princípio consolidado

> A Biblioteca 15 define o que se pretende alcançar e o que pode ser observado. A Biblioteca 16 interpreta em quais jornadas, etapas, necessidades, funções e pontos de contato essa intenção se desdobra. A Biblioteca 13 declara quais inventários podem materializar esses pontos de contato e suportar os indicadores priorizados. Metas e KPIs são contextuais ao planejamento; resultados realizados permanecem fora do MediAd Planner.