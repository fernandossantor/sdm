# MODELO DE PLANEJAMENTO CROSS MEDIA
## Fundamentos Arquiteturais e Modelo Conceitual do MediAd Planner

**Versão:** 1.0
**Status:** Documento Canônico
**Localização:** `docs/MODELO_PLANEJAMENTO_CROSS_MEDIA.md`

---

# 1. Finalidade

Este documento estabelece os fundamentos conceituais, epistemológicos e arquiteturais do MediAd Planner.

Enquanto o Plano Mestre descreve os módulos, funcionalidades e componentes do sistema, este documento define a lógica de construção do conhecimento que sustenta o processo de planejamento.

Seu objetivo é garantir que toda evolução do sistema preserve uma arquitetura coerente, rastreável e fundamentada na teoria do planejamento de marketing, comunicação e mídia.

---

# 2. Natureza do MediAd Planner

O MediAd Planner não é um software destinado apenas ao preenchimento de formulários, nem um gerador automático de planos de mídia.

Também não é um sistema especialista que substitui o planejador.

Sua finalidade é representar formalmente o processo de construção do planejamento cross media, organizando informações, verificando sua coerência, estruturando decisões e permitindo sua simulação.

O sistema modela o raciocínio do planejamento, tornando explícitas as relações entre informações, decisões e resultados.

---

# 3. Fundamentos Epistemológicos

O planejamento é entendido como um processo progressivo de construção do conhecimento.

Cada etapa possui uma finalidade própria.

Nenhuma etapa substitui outra.

Cada etapa prepara a seguinte.

O conhecimento produzido em cada fase reduz gradativamente o espaço de possibilidades até a consolidação do plano.

O sistema, portanto, não parte diretamente da escolha de meios, veículos ou formatos.

Parte da compreensão estruturada do problema.

---

# 4. Princípios Arquiteturais

## 4.1 Construção Progressiva

O planejamento é desenvolvido por sucessivas etapas de formalização do problema.

Cada etapa reduz o espaço de possibilidades da etapa seguinte.

Nenhuma etapa elimina a necessidade da próxima.

---

## 4.2 Não Antecipação das Decisões

Cada etapa possui competência própria.

Uma etapa jamais executa decisões pertencentes à etapa seguinte.

Exemplos:

O Briefing não escolhe meios.

A Tradução Estratégica não seleciona veículos.

A Arquitetura de Mídia não define automaticamente o plano final.

A Simulação não determina a melhor alternativa.

Cada etapa apenas organiza, qualifica e restringe as decisões posteriores.

---

## 4.3 Representação antes da Solução

Toda decisão deve ser precedida pela representação adequada do problema.

O sistema primeiro:

- registra;
- estrutura;
- relaciona;
- verifica coerência;

para somente depois:

- interpretar;
- decidir;
- simular;
- comparar.

---

## 4.4 Coerência

As etapas verificam coerência.

Não produzem automaticamente soluções.

A função do sistema é identificar relações compatíveis, incompatíveis ou insuficientemente fundamentadas.

Exemplo:

Objetivo de Marketing

↓

Objetivo de Comunicação

↓

Intenção de Mídia

A coerência entre esses elementos pode ser avaliada antes da elaboração do plano.

---

## 4.5 Ontologia Disciplinar

Os conceitos utilizados pelo sistema não são definidos pelo software.

São definidos pela literatura consolidada das áreas de:

- Marketing;
- Comunicação;
- Planejamento de Mídia;
- Pesquisa;
- Administração;
- Economia;
- Estatística;
- disciplinas correlatas.

Toda classificação adotada deve possuir fundamentação conceitual explícita.

---

## 4.6 Parametrização

Sempre que possível, as informações deverão ser representadas por parâmetros estruturados.

A ordem de preferência será:

1. Seleção única;

2. Seleção múltipla;

3. Escalas de intensidade;

4. Valores quantitativos;

5. Texto livre.

O texto será utilizado apenas quando a informação não puder ser parametrizada adequadamente.

---

## 4.7 Relações Conceituais

Os parâmetros não constituem campos isolados.

Eles representam entidades relacionadas.

O significado de um parâmetro decorre tanto de sua definição quanto das relações que estabelece com os demais.

---

# 5. Modelo de Construção do Planejamento

O planejamento é representado como uma sequência de transformações sucessivas.

Campanha

↓

Briefing

↓

Tradução Estratégica

↓

Arquitetura de Mídia

↓

Ambiente de Simulação

↓

Consolidação do Plano

↓

Validação

↓

Resultados

Cada etapa transforma conhecimento recebido na etapa anterior.

Nenhuma etapa reinicia o processo.

---

# 6. Modelo de Conhecimento

O sistema opera sobre uma rede conceitual.

As informações deixam de existir como campos independentes e passam a integrar um conjunto de relações.

Exemplos:

Marketing

↓

Objetivos de Marketing

↓

Objetivos de Comunicação

↓

Intenções de Mídia

↓

Objetivos de Mídia

↓

KPIs

Outro exemplo:

Mercado

↓

Concorrência

↓

Posicionamento Competitivo

↓

Pressão Competitiva

↓

Necessidades Estratégicas

Outro exemplo:

Praça

↓

Universo

↓

Público

↓

Segmento

↓

População

↓

Cobertura

↓

Alcance

As decisões decorrem dessas relações.

Não de campos isolados.

---

# 7. Modelo Conceitual

O MediAd Planner representa conhecimento em três níveis.

## Nível Descritivo

Descreve a realidade.

Exemplos:

mercado;

marca;

concorrência;

público;

praça;

restrições.

Não existem decisões.

---

## Nível Interpretativo

Transforma descrições em implicações para o planejamento.

Exemplos:

priorização;

objetivos de mídia;

pressão necessária;

papéis estratégicos;

arquitetura.

Ainda não existe plano.

---

## Nível Decisório

Constrói alternativas.

Simula.

Compara.

Consolida.

Produz o plano.

---

# 8. Critérios de Coerência

O sistema deverá verificar relações entre parâmetros.

Exemplos:

Objetivos de Marketing × Objetivos de Comunicação.

Objetivos de Comunicação × Intenções de Mídia.

Mercado × Posição Competitiva.

Praça × Universo × Segmento.

Orçamento × Objetivos.

Período × Objetivos.

A identificação de inconsistências não representa decisão automática.

Representa apoio ao planejador.

---

# 9. Regras Arquiteturais

Toda informação deve possuir significado conceitual.

Toda informação pertence a apenas uma etapa do processo.

Toda decisão deve ser justificável pelos parâmetros anteriores.

Nenhuma etapa poderá executar responsabilidades pertencentes às etapas seguintes.

Sempre que possível deverão ser utilizados parâmetros estruturados.

Todo parâmetro deverá integrar uma rede de relações.

Toda classificação deverá possuir fundamentação teórica.

Todo resultado deverá ser rastreável até os parâmetros que o originaram.

---

# 10. Evolução do Sistema

Novas funcionalidades somente deverão ser incorporadas quando respeitarem integralmente os princípios estabelecidos neste documento.

Antes da inclusão de qualquer novo componente deverão ser respondidas as seguintes perguntas:

1. Em qual etapa do processo ele pertence?

2. Ele descreve ou decide?

3. Qual conhecimento transforma?

4. Quais parâmetros utiliza?

5. Quais relações estabelece?

6. Em quais fundamentos teóricos se apoia?

Caso essas questões não possam ser respondidas de forma consistente, o componente deverá ser revisto antes de sua implementação.

---

# 11. Princípio Geral

O MediAd Planner não modela campanhas.

Modela o processo de construção do conhecimento necessário para planejar campanhas.

Seu objetivo não é substituir o planejador.

Seu objetivo é tornar explícito, estruturado, rastreável, coerente e simulável o raciocínio do planejamento cross media.

---

# 12. Ontologia Conceitual

O MediAd Planner representa o planejamento cross media como uma rede de conceitos relacionados.

Cada conceito possui identidade própria, atributos específicos e relações explícitas com outros conceitos.

O sistema não trata essas entidades como simples tabelas ou formulários, mas como componentes de uma ontologia disciplinar fundamentada na literatura de Marketing, Comunicação, Planejamento de Mídia, Pesquisa e Administração.

A ontologia organiza-se em quatro grandes domínios.

---

## 12.1 Domínio Estratégico

Representa os elementos responsáveis pela definição do problema de marketing.

Entidades principais:

- Campanha
- Mercado
- Categoria
- Marca
- Produto
- Concorrente
- Objetivo de Marketing
- Objetivo de Comunicação
- Indicadores Competitivos
- Restrições
- Prioridades

Esse domínio responde principalmente à pergunta:

> "Qual problema precisa ser resolvido?"

---

## 12.2 Domínio Mercadológico

Representa os elementos que descrevem a realidade observável.

Entidades principais:

- Praça
- Universo
- Público
- Segmento
- Jornada
- Período
- Verba
- Mercado
- Participação
- Pressão Competitiva

Esse domínio descreve o contexto no qual a campanha será desenvolvida.

Não existem decisões.

Existem descrições estruturadas.

---

## 12.3 Domínio do Planejamento

Representa a transformação do conhecimento descritivo em decisões de mídia.

Entidades principais:

- Intenção de Mídia
- Objetivos de Mídia
- Estratégias
- Papéis Estratégicos
- Arquitetura de Mídia
- Canais
- Inventários
- Veículos
- Formatos
- Distribuição Temporal
- Distribuição Territorial

Esse domínio transforma necessidades estratégicas em alternativas de planejamento.

## 12.4 Domínio da Avaliação

Representa a mensuração das alternativas.

Entidades principais:

- Indicadores
- KPIs
- Simulações
- Cenários
- Resultados
- Comparações
- Recomendações
- Histórico

Esse domínio permite avaliar diferentes soluções antes de sua consolidação.

---

## 12.5 Natureza das Relações

As relações entre entidades podem assumir diferentes naturezas.

### Hierárquicas

Exemplo:

Campanha

↓

Briefing

↓

Tradução Estratégica

↓

Plano

---

### Compositivas

Exemplo:

Público

↓

Segmentos

↓

Subsegmentos

---

### Dependência

Exemplo:

Objetivos de Comunicação

dependem dos

Objetivos de Marketing.

---

### Influência

Exemplo:

Mercado

influencia

Objetivos de Marketing.

Mas não os determina.

---

### Consistência

Exemplo:

Objetivos de Marketing

↓

Objetivos de Comunicação

↓

Objetivos de Mídia

↓

KPIs

Essas relações permitem verificar coerência sem impor soluções.

---

## 12.6 Princípio Ontológico

Nenhum conceito existe isoladamente.

O significado de qualquer entidade decorre simultaneamente de:

- sua definição;
- seus atributos;
- suas relações;
- sua posição no processo de planejamento.

Assim, alterar qualquer conceito implica alterar a rede conceitual à qual pertence.

---

# 13. Grafo Conceitual do MediAd Planner

O MediAd Planner representa o planejamento como um grafo dirigido de construção do conhecimento.

Cada nó representa uma entidade conceitual.

Cada aresta representa uma relação de dependência, influência ou transformação.

O fluxo geral do conhecimento pode ser representado da seguinte forma.

```

```text
Mercado
        │
        ▼
Categoria
        │
        ▼
Marca
        │
        ▼
Produto
        │
        ▼
Campanha
        │
        ▼
Briefing
        │
        ▼
Objetivos de Marketing
        │
        ▼
Objetivos de Comunicação
        │
        ▼
Intenções de Mídia
        │
        ▼
Objetivos de Mídia
        │
        ▼
Estratégias
        │
        ▼
Arquitetura de Mídia
        │
        ▼
Plano
        │
        ▼
Simulações
        │
        ▼
Resultados
```

13.1 Grafo Mercadológico

Praça
   │
   ▼
Universo
   │
   ▼
Público
   │
   ▼
Segmentos
   │
   ▼
População

13.2 Grafo Competitivo

Mercado
    │
    ▼
Concorrentes
    │
    ▼
Indicadores Competitivos
    │
    ▼
Marca

13.3 Grafo Estratégico

Objetivos de Marketing
          │
          ▼
Objetivos de Comunicação
          │
          ▼
Intenções de Mídia
          │
          ▼
Objetivos de Mídia

13.4 Grafo Operacional

Arquitetura
      │
      ▼
Canais
      │
      ▼
Inventários
      │
      ▼
Veículos
      │
      ▼
Formatos

13.5 Grafo de Avaliação

Plano
   │
   ▼
KPIs
   │
   ▼
Simulações
   │
   ▼
Comparações
   │
   ▼
Resultados

13.6 Princípio do Grafo

Todo elemento existente no MediAd Planner deverá pertencer a pelo menos um grafo conceitual.

Nenhuma entidade poderá existir sem relações explícitas.

Todo novo parâmetro deverá responder, antes de sua implementação:

A qual conceito pertence?
Em qual grafo está inserido?
Com quais entidades se relaciona?
Quais decisões influencia?
Quais decisões dependem dele?

Caso essas relações não possam ser claramente identificadas, o parâmetro não deverá ser incorporado ao sistema.

13.7 Princípio Geral da Ontologia

O conhecimento produzido pelo MediAd Planner não é organizado em formulários, mas em uma rede de conceitos interdependentes.

Os formulários constituem apenas a interface de entrada.

A arquitetura real do sistema é dada pela ontologia conceitual e pelos grafos que representam as relações entre seus elementos.


---

### Há um último passo que considero importante

Depois desses capítulos, eu acrescentaria um **Apêndice A – Glossário Canônico**. Ele conteria, em ordem alfabética, a definição oficial de cada conceito (por exemplo, *Campanha*, *Mercado*, *Intenção de Mídia*, *Papel Estratégico*, *KPIs*, *Universo*, *Segmento*). Esse glossário passaria a ser a única referência autorizada para a nomenclatura do sistema.

Com isso, o MediAd Planner deixaria de ser apenas um software de planejamento e passaria a possuir um **modelo formal de conhecimento**, no qual a documentação, a implementação em Python, o banco de dados e a interface compartilham exatamente o mesmo vocabulário e a mesma estrutura conceitual. Na minha avaliação, esse é um diferencial metodológico muito significativo do projeto.
