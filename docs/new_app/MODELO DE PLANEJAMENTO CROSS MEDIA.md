# MODELO DE PLANEJAMENTO CROSS MEDIA
## Fundamentos Arquiteturais e Modelo Conceitual do MediAd Planner

**Versão:** 1.1  
**Status:** Documento Canônico  
**Localização:** `docs/new_app/MODELO DE PLANEJAMENTO CROSS MEDIA.md`

---

# 1. Finalidade

Este documento estabelece os fundamentos conceituais, epistemológicos e arquiteturais do MediAd Planner.

Enquanto o Plano Mestre descreve os módulos, funcionalidades e componentes do sistema, este documento define a lógica de construção do conhecimento que sustenta o processo de planejamento.

Seu objetivo é garantir que toda evolução do sistema preserve uma arquitetura coerente, rastreável e fundamentada na teoria do planejamento de marketing, comunicação e mídia.

---

# 2. Natureza do MediAd Planner

O MediAd Planner não é apenas um software de preenchimento de formulários nem um gerador automático de planos de mídia.

Também não é um sistema especialista destinado a substituir o planejador.

Sua finalidade é representar formalmente o processo de construção do planejamento cross media, organizando informações, verificando coerência, estruturando decisões e permitindo simulações comparáveis.

O sistema modela o raciocínio do planejamento, tornando explícitas as relações entre informações, interpretações, decisões e resultados.

---

# 3. Fundamentos Epistemológicos

O planejamento é entendido como um processo progressivo de construção do conhecimento.

Cada etapa possui finalidade própria, transforma o conhecimento recebido e prepara a etapa seguinte.

Nenhuma etapa substitui outra e nenhuma deve antecipar decisões cuja competência pertença a uma fase posterior.

O conhecimento produzido em cada fase reduz gradativamente o espaço de possibilidades até a consolidação do plano.

O sistema, portanto, não parte diretamente da escolha de meios, veículos ou formatos. Parte da compreensão estruturada do problema.

---

# 4. Princípios Arquiteturais

## 4.1 Construção Progressiva

O planejamento é desenvolvido por sucessivas etapas de formalização do problema.

Cada etapa reduz o espaço de possibilidades da etapa seguinte, sem eliminar sua necessidade.

## 4.2 Não Antecipação das Decisões

Cada etapa possui competência própria.

Uma etapa não deve executar decisões pertencentes à etapa seguinte.

Exemplos:

- o Briefing não escolhe meios;
- a Tradução Estratégica não seleciona veículos;
- a Arquitetura de Mídia não define automaticamente o plano final;
- a Simulação não determina, por si só, a melhor alternativa.

Cada etapa organiza, qualifica e restringe as decisões posteriores.

Critério prático:

> Esta informação descreve, interpreta ou decide?

Se decide, deve estar situada na etapa competente para essa decisão.

## 4.3 Representação antes da Solução

Toda decisão deve ser precedida pela representação adequada do problema.

O fluxo obrigatório é:

```text
Representar
    ↓
Interpretar
    ↓
Decidir
    ↓
Simular
    ↓
Comparar
```

O sistema primeiro registra, estrutura, relaciona e verifica coerência. Somente depois interpreta, decide, simula e compara.

## 4.4 Coerência

As etapas verificam coerência, mas não produzem automaticamente soluções.

A função do sistema é identificar relações compatíveis, incompatíveis, insuficientes ou não fundamentadas.

Exemplo:

```text
Objetivo de Marketing
          ↓
Objetivo de Comunicação
          ↓
Intenção de Mídia
```

A coerência entre esses elementos pode ser avaliada antes da elaboração do plano.

## 4.5 Ontologia Disciplinar

Os conceitos utilizados pelo sistema não são definidos arbitrariamente pelo software.

São derivados da literatura consolidada das áreas de:

- Marketing;
- Comunicação;
- Planejamento de Mídia;
- Pesquisa;
- Administração;
- Economia;
- Estatística;
- disciplinas correlatas.

Toda classificação adotada deve possuir fundamentação conceitual explícita.

## 4.6 Parametrização

Sempre que possível, as informações devem ser representadas por parâmetros estruturados.

A ordem preferencial é:

1. seleção única;
2. seleção múltipla;
3. escala de intensidade;
4. valor quantitativo;
5. texto livre.

O texto livre deve ser empregado apenas quando a informação não puder ser adequadamente parametrizada ou quando for necessário complementar uma seleção estruturada.

## 4.7 Relações Conceituais

Os parâmetros não constituem campos isolados.

Eles representam entidades relacionadas.

O significado de um parâmetro decorre de sua definição, de seus atributos, das relações que estabelece e de sua posição no processo de planejamento.

---

# 5. Modelo de Construção do Planejamento

O planejamento é representado como uma sequência de transformações sucessivas:

```text
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
Validação e Aprovação
    ↓
Acompanhamento e Resultados
```

Cada etapa transforma o conhecimento recebido da anterior.

Nenhuma etapa reinicia o processo nem apaga sua origem.

---

# 6. Modelo de Conhecimento

O sistema opera sobre uma rede conceitual.

As informações deixam de existir como campos independentes e passam a integrar conjuntos de relações.

Exemplo estratégico:

```text
Objetivos de Marketing
          ↓
Objetivos de Comunicação
          ↓
Intenções de Mídia
          ↓
Objetivos de Mídia
          ↓
KPIs
```

Exemplo competitivo:

```text
Mercado
    ↓
Concorrência
    ↓
Posicionamento Competitivo
    ↓
Pressão Competitiva
    ↓
Necessidades Estratégicas
```

Exemplo territorial e populacional:

```text
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
```

As decisões decorrem dessas relações, não de campos isolados.

---

# 7. Níveis do Modelo Conceitual

O MediAd Planner representa o conhecimento em três níveis.

## 7.1 Nível Descritivo

Descreve a realidade observável.

Exemplos:

- mercado;
- marca;
- concorrência;
- público;
- praça;
- período;
- verba;
- restrições.

Nesse nível não existem decisões de mídia.

## 7.2 Nível Interpretativo

Transforma descrições em implicações para o planejamento.

Exemplos:

- priorização;
- objetivos de mídia;
- pressão necessária;
- papéis estratégicos;
- critérios de arquitetura.

Nesse nível ainda não existe plano consolidado.

## 7.3 Nível Decisório

Constrói alternativas, simula, compara, consolida e produz o plano.

As decisões devem permanecer rastreáveis até os elementos descritivos e interpretativos que as fundamentaram.

---

# 8. Critérios de Coerência

O sistema deve verificar relações entre parâmetros, incluindo:

- Objetivos de Marketing × Objetivos de Comunicação;
- Objetivos de Comunicação × Intenções de Mídia;
- Intenções de Mídia × Objetivos de Mídia;
- Objetivos de Mídia × KPIs;
- Mercado × Posição Competitiva;
- Praça × Universo × Público × Segmento;
- Orçamento × Objetivos;
- Período × Objetivos;
- Restrições × Arquitetura de Mídia;
- Arquitetura × Canais × Inventários.

A identificação de inconsistências não representa decisão automática. Representa apoio ao planejador.

---

# 9. Regras Arquiteturais

1. Toda informação deve possuir significado conceitual.
2. Toda informação deve pertencer a uma etapa definida do processo.
3. Nenhuma etapa pode executar responsabilidades pertencentes às etapas seguintes.
4. Toda decisão deve ser justificável pelos parâmetros anteriores.
5. Todo resultado deve ser rastreável até os parâmetros que o originaram.
6. Toda classificação deve possuir fundamentação teórica.
7. Sempre que possível, devem ser utilizados parâmetros estruturados.
8. Todo parâmetro deve integrar uma rede de relações.
9. A interface não deve determinar a ontologia; deve apenas representá-la.
10. O banco de dados não deve inventar conceitos; deve implementar o modelo conceitual.
11. Regras de cálculo devem permanecer separadas das definições conceituais.
12. Inferências do sistema devem ser explicáveis e auditáveis.

---

# 10. Evolução do Sistema

Novas funcionalidades somente devem ser incorporadas quando respeitarem integralmente os princípios estabelecidos neste documento.

Antes da inclusão de qualquer novo componente, devem ser respondidas as seguintes perguntas:

1. Em qual etapa do processo ele pertence?
2. Ele descreve, interpreta, decide, calcula ou compara?
3. Qual conhecimento recebe?
4. Qual conhecimento transforma ou produz?
5. Quais parâmetros utiliza?
6. Com quais entidades se relaciona?
7. Quais decisões influencia?
8. Em quais fundamentos teóricos se apoia?
9. Como sua atuação será rastreada e explicada?

Caso essas questões não possam ser respondidas de forma consistente, o componente deve ser revisto antes de sua implementação.

---

# 11. Princípio Geral

O MediAd Planner não modela apenas campanhas.

Modela o processo de construção do conhecimento necessário para planejar campanhas.

Seu objetivo não é substituir o planejador, mas tornar explícito, estruturado, rastreável, coerente e simulável o raciocínio do planejamento cross media.

---

# 12. Ontologia Conceitual

O MediAd Planner representa o planejamento cross media como uma rede de conceitos relacionados.

Cada conceito possui identidade própria, atributos específicos e relações explícitas com outros conceitos.

O sistema não trata essas entidades como simples tabelas ou formulários, mas como componentes de uma ontologia disciplinar fundamentada na literatura de Marketing, Comunicação, Planejamento de Mídia, Pesquisa e Administração.

A ontologia organiza-se em quatro grandes domínios.

## 12.1 Domínio Estratégico

Representa os elementos responsáveis pela definição do problema de marketing e comunicação.

Entidades principais:

- Campanha;
- Anunciante;
- Mercado;
- Categoria;
- Marca;
- Produto ou Serviço;
- Concorrente;
- Objetivo de Marketing;
- Objetivo de Comunicação;
- Indicador Competitivo;
- Restrição;
- Prioridade.

Esse domínio responde principalmente à pergunta:

> Qual problema precisa ser resolvido?

## 12.2 Domínio Mercadológico

Representa os elementos que descrevem a realidade observável na qual a campanha será desenvolvida.

Entidades principais:

- Praça;
- Universo;
- Público;
- Segmento;
- Jornada;
- Período;
- Verba;
- Mercado;
- Participação;
- Pressão Competitiva.

Nesse domínio existem descrições estruturadas, não decisões de mídia.

## 12.3 Domínio do Planejamento

Representa a transformação do conhecimento descritivo e interpretativo em alternativas de mídia.

Entidades principais:

- Intenção de Mídia;
- Objetivo de Mídia;
- Estratégia;
- Papel Estratégico;
- Arquitetura de Mídia;
- Canal;
- Inventário;
- Veículo;
- Formato;
- Distribuição Temporal;
- Distribuição Territorial;
- Plano.

## 12.4 Domínio da Avaliação

Representa a mensuração, comparação e validação das alternativas.

Entidades principais:

- Indicador;
- KPI;
- Parâmetro;
- Simulação;
- Cenário;
- Resultado;
- Comparação;
- Recomendação;
- Histórico;
- Aprovação.

## 12.5 Natureza das Relações

As relações entre entidades podem assumir diferentes naturezas.

### Hierarquia ou fluxo

Indica posição no processo metodológico.

```text
Campanha
    ↓
Briefing
    ↓
Tradução Estratégica
    ↓
Plano
```

### Composição

Indica que uma entidade contém ou agrega outras.

```text
Público
    └── Segmentos
            └── Subsegmentos
```

### Dependência

Indica que um elemento exige outro como fundamento.

```text
Objetivos de Comunicação
          dependem de
Objetivos de Marketing
```

### Influência

Indica que um elemento afeta outro sem determiná-lo automaticamente.

```text
Mercado
    influencia
Objetivos de Marketing
```

### Consistência

Indica que elementos devem ser avaliados conjuntamente.

```text
Objetivos de Marketing
          ↓
Objetivos de Comunicação
          ↓
Objetivos de Mídia
          ↓
KPIs
```

### Transformação

Indica que uma etapa converte entradas em uma nova representação do conhecimento.

```text
Briefing
    ↓
Tradução Estratégica
```

## 12.6 Princípio Ontológico

Nenhum conceito existe isoladamente.

O significado de qualquer entidade decorre simultaneamente de:

- sua definição;
- seus atributos;
- suas relações;
- sua posição no processo de planejamento;
- sua função no fluxo de transformação do conhecimento.

Alterar um conceito implica avaliar os efeitos da mudança em toda a rede conceitual à qual ele pertence.

---

# 13. Grafo Conceitual do MediAd Planner

O MediAd Planner representa o planejamento como um grafo dirigido de construção do conhecimento.

Cada nó representa uma entidade conceitual.

Cada aresta representa uma relação de fluxo, composição, dependência, influência, consistência ou transformação.

## 13.1 Fluxo Geral do Conhecimento

```text
Mercado e Contexto
        ↓
Campanha
        ↓
Briefing
        ↓
Tradução Estratégica
        ↓
Objetivos de Mídia
        ↓
Estratégias e Papéis Estratégicos
        ↓
Arquitetura de Mídia
        ↓
Alternativas de Plano
        ↓
Simulações
        ↓
Comparações
        ↓
Plano Consolidado
        ↓
Validação e Aprovação
        ↓
Acompanhamento e Resultados
```

O fluxo não significa causalidade automática. Cada transição representa uma transformação metodológica controlada.

## 13.2 Grafo Mercadológico

```text
Praça
    ↓
Universo
    ↓
Público
    ↓
Segmento
    ↓
População
```

Esse grafo estrutura a dimensão territorial e populacional do planejamento.

## 13.3 Grafo Competitivo

```text
Mercado
    ↓
Concorrentes
    ↓
Indicadores Competitivos
    ↓
Posicionamento da Marca
    ↓
Pressão Competitiva
```

Esse grafo representa o ambiente competitivo e suas implicações.

## 13.4 Grafo Estratégico

```text
Objetivos de Marketing
          ↓
Objetivos de Comunicação
          ↓
Intenções de Mídia
          ↓
Objetivos de Mídia
          ↓
KPIs
```

Esse grafo constitui a principal cadeia de coerência estratégica do planejamento.

## 13.5 Grafo Operacional

```text
Arquitetura de Mídia
          ↓
Canais
          ↓
Inventários
          ↓
Veículos
          ↓
Formatos
          ↓
Cronograma e Distribuição
```

Esse grafo representa as decisões de implementação.

## 13.6 Grafo de Avaliação

```text
Alternativa de Plano
          ↓
Parâmetros e KPIs
          ↓
Simulação
          ↓
Comparação
          ↓
Resultado
          ↓
Validação
```

Esse grafo representa a mensuração e a comparação das alternativas produzidas.

## 13.7 Regras do Grafo

Todo elemento existente no MediAd Planner deve pertencer a pelo menos um grafo conceitual.

Nenhuma entidade pode existir sem relações explícitas.

Todo novo parâmetro deve responder, antes de sua implementação:

1. A qual conceito pertence?
2. Em qual grafo está inserido?
3. Com quais entidades se relaciona?
4. Qual é a natureza de cada relação?
5. Quais decisões influencia?
6. Quais decisões dependem dele?
7. Quais resultados podem ser rastreados até ele?

Caso essas relações não possam ser claramente identificadas, o parâmetro não deve ser incorporado ao sistema.

## 13.8 Princípio Geral da Ontologia e do Grafo

O conhecimento produzido pelo MediAd Planner não é organizado em formulários, mas em uma rede de conceitos interdependentes.

Os formulários constituem apenas interfaces de entrada, consulta e edição.

A arquitetura real do sistema é dada pela ontologia conceitual e pelos grafos que representam as relações entre seus elementos.

A implementação em banco de dados, código, motores, interface e relatórios deve preservar esse mesmo vocabulário e essas mesmas relações.

---

# 14. Controle do Documento

Este documento é canônico e deve orientar:

- a evolução do Plano Mestre;
- a elaboração das especificações de cada etapa;
- a modelagem do domínio;
- a estrutura do banco de dados;
- as regras dos motores;
- a construção das interfaces;
- os testes de coerência;
- a rastreabilidade das decisões.

Alterações conceituais relevantes devem ser registradas formalmente e avaliadas quanto aos seus efeitos sobre os demais documentos canônicos do MediAd Planner.
