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
