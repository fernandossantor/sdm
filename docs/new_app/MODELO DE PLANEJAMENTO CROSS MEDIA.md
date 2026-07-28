# MODELO DE PLANEJAMENTO CROSS MEDIA
## Fundamentos Arquiteturais e Modelo Conceitual do MediAd Planner

**Versão:** 1.2  
**Status:** Documento Canônico  
**Localização:** `docs/new_app/MODELO DE PLANEJAMENTO CROSS MEDIA.md`

---

# 1. Finalidade

Este documento estabelece os fundamentos conceituais, epistemológicos e arquiteturais do MediAd Planner.

Enquanto o Plano Mestre descreve os módulos, funcionalidades e componentes do sistema, este documento define a lógica de construção do conhecimento que sustenta o processo de planejamento cross media.

Seu objetivo é garantir que toda evolução do sistema preserve uma arquitetura coerente, rastreável e fundamentada na teoria do planejamento de marketing, comunicação e mídia.

Este documento possui caráter canônico. Todas as especificações de etapas, modelos de domínio, estruturas de dados, motores de cálculo, interfaces e relatórios devem ser compatíveis com os princípios aqui estabelecidos.

---

# 2. Natureza do MediAd Planner

O MediAd Planner não é apenas um software de preenchimento de formulários nem um gerador automático de planos de mídia.

Também não é um sistema especialista destinado a substituir o planejador.

Sua finalidade é representar formalmente o processo de construção do planejamento cross media, organizando informações, verificando coerência, estruturando interpretações, apoiando decisões e permitindo simulações comparáveis.

O sistema modela o raciocínio do planejamento, tornando explícitas as relações entre informações, interpretações, decisões, avaliações e resultados.

O MediAd Planner não transforma dados diretamente em planos. Ele representa uma sequência disciplinar de transformações de conhecimento, na qual cada etapa recebe um objeto estruturado, realiza uma operação epistemológica própria e produz um novo objeto de conhecimento.

---

# 3. Fundamentos Epistemológicos

O planejamento é entendido como um processo progressivo de construção do conhecimento.

Cada etapa possui finalidade própria, transforma o conhecimento recebido e prepara a etapa seguinte.

Nenhuma etapa substitui outra e nenhuma deve antecipar interpretações ou decisões cuja competência pertença a uma fase posterior.

O conhecimento produzido em cada etapa reduz gradativamente o espaço de possibilidades até a consolidação do plano, sem transformar essa redução em automatismo decisório.

O sistema, portanto, não parte diretamente da escolha de meios, canais, veículos ou formatos. Parte da organização estruturada das circunstâncias concretas que motivam e condicionam o planejamento.

A distinção entre descrição, interpretação, decisão, avaliação e execução é indispensável para a arquitetura do sistema.

Um fato, uma circunstância, uma intenção declarada ou uma restrição não constituem, por si mesmos, um problema de mídia. O problema é uma interpretação disciplinar construída a partir desses elementos. Por essa razão, o Briefing organiza o contexto, enquanto a Tradução Estratégica realiza a primeira interpretação desse contexto.

---

# 4. Princípios Arquiteturais

## 4.1 Construção Progressiva

O planejamento é desenvolvido por sucessivas etapas de transformação do conhecimento.

Cada etapa recebe um objeto de conhecimento, realiza uma operação específica e produz um novo objeto, que se torna a matéria-prima canônica da etapa seguinte.

A progressão não elimina alternativas automaticamente. Ela organiza, qualifica e restringe o espaço de possibilidades com base em relações conceituais explícitas.

## 4.2 Não Antecipação das Competências

Cada etapa possui competência epistemológica própria.

Uma etapa não deve executar interpretações, decisões ou avaliações pertencentes às etapas seguintes.

Exemplos:

- a Campanha não interpreta o contexto;
- o Briefing não define o problema de mídia;
- o Briefing não escolhe meios, canais, veículos ou formatos;
- a Tradução Estratégica não seleciona veículos nem consolida o plano;
- a Arquitetura de Mídia não define automaticamente o plano final;
- a Simulação não determina, por si só, a melhor alternativa;
- a Consolidação não deve ocultar as alternativas e justificativas que a antecederam.

Critério prático:

> Esta informação registra, descreve, interpreta, decide, avalia ou executa?

A resposta deve determinar a etapa competente e a natureza do objeto ao qual a informação pertence.

## 4.3 Representação antes da Interpretação

Toda interpretação deve ser precedida por uma representação adequada do contexto.

O fluxo epistemológico fundamental é:

```text
Registrar
    ↓
Descrever e estruturar
    ↓
Interpretar
    ↓
Decidir
    ↓
Simular e avaliar
    ↓
Consolidar e executar
```

O sistema primeiro registra, estrutura, relaciona e verifica coerência. Somente depois interpreta, decide, simula, compara, consolida e acompanha.

## 4.4 Princípio da Transformação do Conhecimento

O MediAd Planner representa o planejamento cross media como uma sequência disciplinar de transformações de conhecimento.

Cada etapa:

1. recebe um objeto de conhecimento;
2. realiza uma operação epistemológica própria;
3. produz um novo objeto de conhecimento;
4. preserva a rastreabilidade entre origem, transformação e resultado.

O sistema não transmite apenas dados entre etapas. Transmite conhecimento progressivamente estruturado.

## 4.5 Objetos de Conhecimento

Um objeto de conhecimento é uma unidade estruturada e versionável que representa o resultado cognitivo produzido por uma etapa do planejamento.

Cada objeto deve possuir:

- identidade própria;
- origem explícita;
- conteúdo estruturado;
- relações conceituais;
- autoria e responsabilidade;
- estado e versão;
- critérios de completude;
- critérios de coerência;
- histórico de alterações;
- vínculo com os objetos antecedentes e subsequentes.

Os objetos de conhecimento são entidades de primeira ordem no sistema. Não devem ser reduzidos a conjuntos de campos de interface ou a simples registros de banco de dados.

## 4.6 Coerência sem Automatismo

As etapas podem verificar coerência, mas não devem produzir automaticamente soluções que ultrapassem sua competência.

A função do sistema é identificar relações:

- compatíveis;
- incompatíveis;
- insuficientes;
- contraditórias;
- não fundamentadas;
- dependentes de justificativa adicional.

Exemplo:

```text
Objetivo de Marketing
          ↓
Objetivo de Comunicação
          ↓
Intenção de Mídia
```

A coerência entre esses elementos pode ser avaliada antes da elaboração do plano.

A identificação de incoerência não substitui o julgamento do planejador. Ela cria uma exigência de revisão, justificativa ou aprofundamento.

## 4.7 Ontologia Disciplinar

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

## 4.8 Parametrização

Sempre que possível, as informações devem ser representadas por parâmetros estruturados.

A ordem preferencial é:

1. seleção única;
2. seleção múltipla;
3. escala de intensidade;
4. valor quantitativo;
5. texto livre.

O texto livre deve ser empregado quando a informação não puder ser adequadamente parametrizada, quando for necessária justificativa ou quando houver conteúdo contextual que não possa ser reduzido sem perda de significado.

## 4.9 Relações Conceituais

Os parâmetros não constituem campos isolados.

Eles representam entidades, propriedades ou relações de uma ontologia disciplinar.

O significado de um parâmetro decorre de:

- sua definição;
- seus atributos;
- suas relações;
- sua posição no processo;
- sua função no objeto de conhecimento ao qual pertence.

## 4.10 Rastreabilidade Integral

Toda interpretação, decisão, cálculo, recomendação e resultado deve ser rastreável até os elementos que o fundamentaram.

A rastreabilidade deve permitir reconstruir:

- quais informações estavam disponíveis;
- quais relações foram consideradas;
- quais interpretações foram formuladas;
- quais decisões foram tomadas;
- quais alternativas foram descartadas;
- quais parâmetros foram utilizados;
- quais resultados foram comparados;
- quem realizou ou aprovou cada transformação.

---

# 5. Modelo de Construção do Planejamento

O planejamento é representado como uma sequência de etapas e objetos de conhecimento.

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

O fluxo acima não deve ser compreendido apenas como uma sequência de telas ou módulos.

Cada transição representa uma transformação metodológica controlada:

```text
Etapa anterior
      ↓
Objeto de conhecimento de entrada
      ↓
Operação epistemológica específica
      ↓
Objeto de conhecimento de saída
      ↓
Etapa seguinte
```

Cada etapa transforma o conhecimento recebido da anterior.

Nenhuma etapa reinicia o processo, apaga sua origem ou substitui a responsabilidade metodológica das demais.

O objeto produzido por uma etapa constitui a entrada canônica da etapa seguinte, mas não impede consultas aos objetos anteriores. A etapa seguinte deve preservar a referência explícita aos fundamentos que recebeu.

---

# 6. Transformações Epistemológicas do Planejamento

## 6.1 Princípio Geral

Cada etapa do MediAd Planner produz um tipo distinto de conhecimento.

A diferença entre as etapas não é apenas funcional. É epistemológica.

Uma etapa pode registrar, descrever, interpretar, decidir, avaliar ou executar. Essas operações não são equivalentes e não devem ser misturadas.

## 6.2 Tipos de Objetos Produzidos

| Etapa | Objeto produzido | Natureza epistemológica | Função principal |
|---|---|---|---|
| Campanha | Objeto Administrativo | Identitária e organizacional | Define o que será planejado, sua autoria, responsabilidades, escopo administrativo, estado e histórico. |
| Briefing | Objeto Contextual Estruturado | Descritiva | Organiza fatos, circunstâncias, intenções declaradas, anseios, limites, recursos, restrições e demais elementos concretos conhecidos, sem convertê-los em diagnóstico ou solução. |
| Tradução Estratégica | Objeto Interpretativo | Interpretativa | Constrói a primeira leitura disciplinar do contexto, formulando problemas, oportunidades, tensões, prioridades, hipóteses e implicações estratégicas. |
| Arquitetura de Mídia | Objeto Decisório | Decisória | Estrutura decisões de mídia coerentes com a interpretação estratégica, definindo objetivos, papéis, relações, critérios e alternativas de arquitetura. |
| Ambiente de Simulação | Objeto Avaliativo | Avaliativa | Testa alternativas, calcula consequências, compara cenários, explicita trade-offs e produz evidências para decisão. |
| Consolidação do Plano | Objeto Executável | Prescritiva e operacional | Formaliza a alternativa selecionada, sua distribuição, parâmetros, cronograma, orçamento e condições de implementação. |
| Validação e Aprovação | Objeto de Validação | Deliberativa | Registra análise, ajustes, justificativas, aprovações, rejeições e responsabilidades. |
| Acompanhamento e Resultados | Objeto de Evidência | Empírica e avaliativa | Registra execução, desempenho, desvios, aprendizados e retroalimentação do conhecimento. |

## 6.3 Campanha como Objeto Administrativo

A Campanha constitui a entidade raiz do processo.

Ela responde principalmente:

> O que será planejado, por quem, para quem e em qual condição administrativa?

A Campanha define identidade, vínculo com o anunciante, responsáveis, permissões, estado, histórico e relação com os demais objetos.

Ela não contém, por si só, interpretação estratégica ou decisão de mídia.

## 6.4 Briefing como Objeto Contextual Estruturado

O Briefing organiza o contexto concreto recebido do demandante e das fontes disponíveis.

Ele reúne:

- circunstâncias;
- fatos;
- histórico;
- características do anunciante, marca, produto ou serviço;
- mercado e concorrência conhecidos;
- intenções declaradas;
- objetivos declarados;
- anseios e expectativas;
- públicos conhecidos ou presumidos;
- praça e período;
- verba e recursos;
- limitações;
- restrições;
- premissas;
- incertezas;
- lacunas de informação.

O Briefing pode verificar coerência interna entre elementos declarados, mas não deve formular o problema de mídia como se ele fosse um dado recebido.

O problema é uma interpretação. Portanto, pertence à Tradução Estratégica.

## 6.5 Tradução Estratégica como Objeto Interpretativo

A Tradução Estratégica pergunta:

> O que o contexto estruturado significa para o planejamento?

É nessa etapa que podem ser formulados:

- problemas;
- oportunidades;
- tensões;
- contradições;
- prioridades;
- hipóteses;
- necessidades estratégicas;
- implicações para comunicação e mídia.

Um mesmo Objeto Contextual Estruturado pode admitir interpretações diferentes, desde que justificáveis e rastreáveis.

A Tradução Estratégica não é mera transcrição do Briefing. É a primeira transformação disciplinar do contexto em sentido estratégico.

## 6.6 Arquitetura de Mídia como Objeto Decisório

A Arquitetura de Mídia transforma a interpretação estratégica em uma estrutura de decisões.

Ela define, entre outros elementos:

- objetivos de mídia;
- prioridades;
- critérios de alcance, frequência, continuidade e pressão;
- papéis estratégicos dos canais;
- relações de complementaridade;
- funções territoriais e temporais;
- critérios de seleção;
- alternativas de composição.

A arquitetura não deve confundir decisão estrutural com consolidação operacional do plano.

## 6.7 Simulação como Objeto Avaliativo

A Simulação não cria fatos nem encerra a decisão.

Ela avalia alternativas por meio de parâmetros, modelos, indicadores e cenários.

Sua função é explicitar consequências, restrições, riscos, eficiências, perdas e ganhos relativos.

Uma simulação pode recomendar, mas não deve ocultar os critérios da recomendação nem substituir a deliberação do planejador.

## 6.8 Consolidação como Objeto Executável

A Consolidação transforma uma alternativa escolhida em plano implementável.

Ela deve preservar:

- a interpretação que fundamentou a escolha;
- a arquitetura da qual o plano deriva;
- as alternativas comparadas;
- os parâmetros utilizados;
- as justificativas da decisão;
- as aprovações realizadas.

O plano executável é o resultado final de uma cadeia de transformações, não um documento isolado.

## 6.9 Verdadeiro Núcleo do Projeto

O verdadeiro núcleo do MediAd Planner não é o formulário, o banco de dados, o algoritmo, a tela ou o relatório.

É a representação formal do processo pelo qual o conhecimento do planejamento é construído, transformado, validado e convertido em ação.

O princípio central pode ser expresso da seguinte forma:

> Cada etapa produz um objeto de conhecimento que se torna a matéria-prima da etapa seguinte.

Consequentemente:

- o sistema não organiza apenas informações;
- não oferece apenas cálculos;
- não produz apenas documentos;
- não recomenda apenas canais;
- não simula apenas resultados.

O sistema representa o raciocínio do planejador como uma cadeia explícita, estruturada, rastreável e auditável de transformações de conhecimento.

---

# 7. Modelo de Conhecimento

O MediAd Planner opera sobre duas camadas complementares:

1. ontologia do domínio;
2. ontologia do processo de construção do conhecimento.

## 7.1 Ontologia do Domínio

Representa aquilo sobre o que o sistema pensa.

Inclui conceitos de Marketing, Comunicação, Mídia, Pesquisa, Mercado, Públicos, Canais, Indicadores, Orçamento e Avaliação.

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

## 7.2 Ontologia do Processo de Conhecimento

Representa como o sistema constrói o pensamento do planejamento.

Inclui:

- etapas;
- objetos de conhecimento;
- transformações;
- estados;
- versões;
- validações;
- autoria;
- dependências;
- rastreabilidade;
- critérios de coerência e completude.

Exemplo:

```text
Objeto Administrativo
          ↓
Objeto Contextual Estruturado
          ↓
Objeto Interpretativo
          ↓
Objeto Decisório
          ↓
Objeto Avaliativo
          ↓
Objeto Executável
```

## 7.3 Integração entre as Duas Camadas

As duas ontologias não existem separadamente na implementação.

Cada objeto de conhecimento contém entidades da ontologia do domínio e registra as transformações realizadas sobre elas.

Exemplo:

```text
Objetivo de Marketing declarado
          pertence ao
Objeto Contextual Estruturado
          ↓ interpretado como
Implicação estratégica
          pertence ao
Objeto Interpretativo
          ↓ convertido em
Objetivo de Mídia
          pertence ao
Objeto Decisório
```

As decisões decorrem das relações entre conceitos e das transformações realizadas, não de campos isolados.

---

# 8. Níveis do Modelo Conceitual

O MediAd Planner representa o conhecimento em cinco níveis complementares.

## 8.1 Nível Administrativo

Define identidade, responsabilidade, estado, versão, autoria, permissões e histórico do processo.

Exemplos:

- campanha;
- anunciante;
- responsável;
- equipe;
- versão;
- status;
- aprovação.

## 8.2 Nível Descritivo

Descreve e estrutura a realidade conhecida, as circunstâncias, as intenções declaradas e os limites do planejamento.

Exemplos:

- mercado;
- marca;
- concorrência;
- público;
- praça;
- período;
- verba;
- objetivos declarados;
- anseios;
- restrições;
- premissas;
- lacunas.

Nesse nível não existem problemas de mídia formulados nem decisões de mídia.

## 8.3 Nível Interpretativo

Transforma descrições em implicações para o planejamento.

Exemplos:

- problema;
- oportunidade;
- tensão;
- prioridade;
- hipótese;
- necessidade estratégica;
- implicação de comunicação;
- implicação de mídia.

Nesse nível ainda não existe arquitetura consolidada nem plano executável.

## 8.4 Nível Decisório

Converte interpretações em alternativas estruturadas de mídia.

Exemplos:

- objetivos de mídia;
- papéis estratégicos;
- critérios de alcance e frequência;
- arquitetura de mídia;
- distribuição territorial;
- distribuição temporal;
- alternativas de plano.

## 8.5 Nível Avaliativo e Executivo

Avalia alternativas, consolida decisões e acompanha a execução.

Exemplos:

- simulações;
- cenários;
- comparações;
- recomendações;
- plano consolidado;
- aprovação;
- execução;
- resultados;
- aprendizados.

Todas as decisões devem permanecer rastreáveis até os elementos administrativos, descritivos e interpretativos que as fundamentaram.

---

# 9. Critérios de Coerência

O sistema deve verificar coerência tanto dentro de um objeto de conhecimento quanto entre objetos sucessivos.

## 9.1 Coerência Interna

Exemplos:

- objetivos declarados × expectativas;
- verba × abrangência declarada;
- período × resultados esperados;
- público declarado × praça;
- restrições × intenções;
- marca × produto ou serviço;
- mercado × posição competitiva informada.

## 9.2 Coerência entre Objetos

Exemplos:

- contexto estruturado × interpretação estratégica;
- Objetivos de Marketing × Objetivos de Comunicação;
- Objetivos de Comunicação × Intenções de Mídia;
- Intenções de Mídia × Objetivos de Mídia;
- Objetivos de Mídia × KPIs;
- Mercado × Posição Competitiva;
- Praça × Universo × Público × Segmento;
- Orçamento × Objetivos;
- Período × Objetivos;
- Restrições × Arquitetura de Mídia;
- Arquitetura × Canais × Inventários;
- Alternativa de plano × resultados simulados;
- plano consolidado × decisão aprovada.

## 9.3 Estados de Coerência

Uma relação pode ser classificada como:

- coerente;
- parcialmente coerente;
- incoerente;
- insuficientemente fundamentada;
- dependente de justificativa;
- não avaliável por ausência de informação.

A identificação de inconsistências não representa decisão automática. Representa apoio ao planejador e exigência de tratamento explícito.

---

# 10. Regras Arquiteturais

1. Toda informação deve possuir significado conceitual.
2. Toda informação deve pertencer a uma etapa e a um objeto de conhecimento definidos.
3. Nenhuma etapa pode executar responsabilidades epistemológicas pertencentes às etapas seguintes.
4. O Briefing organiza o contexto; não define o problema de mídia.
5. O problema é uma interpretação e pertence à Tradução Estratégica.
6. Toda decisão deve ser justificável pelos objetos anteriores.
7. Todo resultado deve ser rastreável até os elementos que o originaram.
8. Toda classificação deve possuir fundamentação teórica.
9. Sempre que possível, devem ser utilizados parâmetros estruturados.
10. Todo parâmetro deve integrar uma rede de relações.
11. Todo objeto de conhecimento deve possuir identidade, versão, estado, autoria e histórico.
12. A interface não deve determinar a ontologia; deve apenas representá-la.
13. O banco de dados não deve inventar conceitos; deve implementar o modelo conceitual.
14. Regras de cálculo devem permanecer separadas das definições conceituais.
15. Inferências do sistema devem ser explicáveis e auditáveis.
16. Recomendações não podem ocultar critérios, pesos, restrições ou alternativas.
17. Uma alteração conceitual deve ser avaliada em toda a rede de dependências.
18. A saída de cada etapa deve ser formalizada como objeto de conhecimento consumível pela etapa seguinte.
19. Objetos anteriores não devem ser sobrescritos por objetos posteriores.
20. A consolidação deve preservar a cadeia completa de origem, transformação e decisão.

---

# 11. Evolução do Sistema

Novas funcionalidades somente devem ser incorporadas quando respeitarem integralmente os princípios estabelecidos neste documento.

Antes da inclusão de qualquer novo componente, devem ser respondidas as seguintes perguntas:

1. Em qual etapa do processo ele pertence?
2. A qual objeto de conhecimento ele pertence?
3. Ele registra, descreve, interpreta, decide, calcula, avalia, consolida ou acompanha?
4. Qual conhecimento recebe?
5. Qual transformação realiza?
6. Qual conhecimento produz?
7. Quais parâmetros utiliza?
8. Com quais entidades se relaciona?
9. Quais decisões influencia?
10. Quais decisões dependem dele?
11. Em quais fundamentos teóricos se apoia?
12. Como sua atuação será rastreada e explicada?
13. Qual é seu estado, versão e autoria?
14. Quais critérios de completude e coerência se aplicam?

Caso essas questões não possam ser respondidas de forma consistente, o componente deve ser revisto antes de sua implementação.

---

# 12. Princípio Geral

O MediAd Planner não modela apenas campanhas.

Modela o processo de construção do conhecimento necessário para planejar campanhas.

Seu objetivo não é substituir o planejador, mas tornar explícito, estruturado, rastreável, coerente, simulável e auditável o raciocínio do planejamento cross media.

O sistema deve preservar a diferença entre:

- o que foi declarado;
- o que foi observado;
- o que foi interpretado;
- o que foi decidido;
- o que foi calculado;
- o que foi aprovado;
- o que foi executado;
- o que foi efetivamente observado como resultado.

Essa separação é condição para a integridade metodológica do projeto.

---

# 13. Ontologia Conceitual

O MediAd Planner representa o planejamento cross media por meio de duas ontologias interdependentes:

1. a ontologia do domínio disciplinar;
2. a ontologia do processo de construção do conhecimento.

## 13.1 Ontologia do Domínio Disciplinar

Representa os conceitos de Marketing, Comunicação, Mídia, Pesquisa, Mercado e Avaliação utilizados no planejamento.

Cada conceito possui identidade própria, atributos específicos e relações explícitas com outros conceitos.

O sistema não trata essas entidades como simples tabelas ou formulários, mas como componentes de uma ontologia fundamentada na literatura disciplinar.

### 13.1.1 Domínio Estratégico

Representa os elementos relacionados às intenções organizacionais e à interpretação estratégica.

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
- Problema;
- Oportunidade;
- Hipótese;
- Prioridade;
- Necessidade Estratégica.

Esse domínio responde, em etapas diferentes, às perguntas:

> Quais intenções e circunstâncias foram declaradas?

> Que interpretação estratégica pode ser construída a partir delas?

A primeira pergunta pertence ao Briefing. A segunda pertence à Tradução Estratégica.

### 13.1.2 Domínio Mercadológico e Contextual

Representa os elementos que descrevem a realidade conhecida na qual a campanha será desenvolvida.

Entidades principais:

- Praça;
- Universo;
- Público;
- Segmento;
- Jornada;
- Período;
- Verba;
- Recursos;
- Mercado;
- Participação;
- Pressão Competitiva;
- Restrição;
- Premissa;
- Anseio;
- Expectativa;
- Histórico;
- Evidência;
- Lacuna de Informação.

Nesse domínio existem descrições estruturadas, não decisões de mídia.

### 13.1.3 Domínio do Planejamento

Representa a transformação do conhecimento interpretativo em alternativas de mídia.

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
- Alternativa de Plano;
- Plano.

### 13.1.4 Domínio da Avaliação

Representa a mensuração, comparação, validação e aprendizagem.

Entidades principais:

- Indicador;
- KPI;
- Parâmetro;
- Simulação;
- Cenário;
- Resultado;
- Comparação;
- Recomendação;
- Validação;
- Aprovação;
- Execução;
- Desvio;
- Aprendizado;
- Histórico de Resultado.

## 13.2 Ontologia do Processo de Conhecimento

Representa as entidades necessárias para formalizar a construção progressiva do planejamento.

Entidades principais:

- Etapa;
- Objeto de Conhecimento;
- Transformação;
- Entrada;
- Saída;
- Estado;
- Versão;
- Autor;
- Responsável;
- Validação;
- Aprovação;
- Justificativa;
- Regra de Coerência;
- Critério de Completude;
- Dependência;
- Histórico;
- Evidência de Origem.

## 13.3 Tipos Canônicos de Objeto de Conhecimento

O sistema reconhece, no mínimo, os seguintes tipos:

- Objeto Administrativo;
- Objeto Contextual Estruturado;
- Objeto Interpretativo;
- Objeto Decisório;
- Objeto Avaliativo;
- Objeto Executável;
- Objeto de Validação;
- Objeto de Evidência.

Cada documento específico de etapa deve definir:

- qual objeto recebe;
- qual objeto produz;
- quais conceitos contém;
- quais transformações realiza;
- quais validações exige;
- quais estados admite;
- quais relações preserva.

## 13.4 Natureza das Relações

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
Arquitetura de Mídia
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

Indica que uma etapa converte um objeto de entrada em uma nova representação do conhecimento.

```text
Objeto Contextual Estruturado
          ↓ interpretação
Objeto Interpretativo
```

### Proveniência

Indica a origem de um elemento ou decisão.

```text
Decisão de mídia
      deriva de
Interpretação Estratégica
      fundamentada em
Contexto Estruturado
```

### Versionamento

Indica continuidade histórica sem apagamento das versões anteriores.

```text
Objeto v1
    ↓ revisão
Objeto v2
    ↓ aprovação
Objeto v3
```

## 13.5 Princípio Ontológico

Nenhum conceito ou objeto de conhecimento existe isoladamente.

O significado de qualquer entidade decorre simultaneamente de:

- sua definição;
- seus atributos;
- suas relações;
- sua posição no processo de planejamento;
- sua função no fluxo de transformação do conhecimento;
- sua origem;
- seu estado;
- sua versão.

Alterar um conceito implica avaliar os efeitos da mudança em toda a rede conceitual e documental à qual ele pertence.

---

# 14. Grafo Conceitual do MediAd Planner

O MediAd Planner representa o planejamento como um grafo dirigido de construção do conhecimento.

Cada nó pode representar:

- uma entidade conceitual;
- um objeto de conhecimento;
- uma etapa;
- uma decisão;
- uma evidência;
- uma versão.

Cada aresta representa uma relação de fluxo, composição, dependência, influência, consistência, transformação, proveniência ou versionamento.

## 14.1 Grafo Geral das Etapas

```text
Mercado e Contexto
        ↓
Campanha
        ↓
Briefing
        ↓
Tradução Estratégica
        ↓
Objetivos e Arquitetura de Mídia
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

## 14.2 Grafo das Transformações Epistemológicas

```text
Campanha
    ↓ produz
Objeto Administrativo
    ↓ fundamenta
Briefing
    ↓ produz
Objeto Contextual Estruturado
    ↓ interpretado pela
Tradução Estratégica
    ↓ produz
Objeto Interpretativo
    ↓ convertido pela
Arquitetura de Mídia
    ↓ produz
Objeto Decisório
    ↓ avaliado no
Ambiente de Simulação
    ↓ produz
Objeto Avaliativo
    ↓ selecionado e formalizado na
Consolidação do Plano
    ↓ produz
Objeto Executável
    ↓ deliberado na
Validação e Aprovação
    ↓ produz
Objeto de Validação
    ↓ observado no
Acompanhamento e Resultados
    ↓ produz
Objeto de Evidência
```

Esse grafo explicita a diferença epistemológica entre as etapas e constitui o eixo central da arquitetura do sistema.

## 14.3 Grafo Mercadológico

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

## 14.4 Grafo Competitivo

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

Esse grafo representa o ambiente competitivo e suas possíveis implicações.

## 14.5 Grafo Estratégico

```text
Objetivos de Marketing declarados
          ↓ coerência
Objetivos de Comunicação declarados
          ↓ interpretação
Problemas e Oportunidades
          ↓ tradução
Intenções de Mídia
          ↓ decisão
Objetivos de Mídia
          ↓ avaliação
KPIs
```

Esse grafo constitui a principal cadeia de coerência estratégica do planejamento.

## 14.6 Grafo Operacional

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

## 14.7 Grafo de Avaliação

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

## 14.8 Grafo de Rastreabilidade

```text
Fato ou intenção declarada
          ↓ origem
Objeto Contextual Estruturado
          ↓ interpretação justificada
Objeto Interpretativo
          ↓ decisão fundamentada
Objeto Decisório
          ↓ resultado simulado
Objeto Avaliativo
          ↓ escolha aprovada
Objeto Executável
          ↓ execução observada
Objeto de Evidência
```

Esse grafo permite reconstruir o raciocínio completo do planejamento.

## 14.9 Regras do Grafo

Todo elemento existente no MediAd Planner deve pertencer a pelo menos um grafo conceitual.

Nenhuma entidade pode existir sem relações explícitas.

Todo novo parâmetro, entidade ou objeto deve responder, antes de sua implementação:

1. A qual conceito pertence?
2. Em qual objeto de conhecimento está contido?
3. Em qual grafo está inserido?
4. Com quais entidades se relaciona?
5. Qual é a natureza de cada relação?
6. Qual é sua origem?
7. Quais transformações o afetam?
8. Quais decisões influencia?
9. Quais decisões dependem dele?
10. Quais resultados podem ser rastreados até ele?
11. Como será versionado?
12. Como será validado?

Caso essas relações não possam ser claramente identificadas, o elemento não deve ser incorporado ao sistema.

## 14.10 Princípio Geral da Ontologia e do Grafo

O conhecimento produzido pelo MediAd Planner não é organizado em formulários, mas em uma rede de conceitos, objetos e transformações interdependentes.

Os formulários constituem apenas interfaces de entrada, consulta e edição.

A arquitetura real do sistema é dada:

- pela ontologia do domínio;
- pela ontologia do processo de conhecimento;
- pelos objetos de conhecimento;
- pelas transformações epistemológicas;
- pelos grafos que representam suas relações.

A implementação em banco de dados, código, motores, interface e relatórios deve preservar esse mesmo vocabulário e essas mesmas relações.

---

# 15. Controle do Documento

Este documento é canônico e deve orientar:

- a evolução do Plano Mestre;
- a elaboração das especificações de cada etapa;
- a modelagem do domínio;
- a modelagem dos objetos de conhecimento;
- a estrutura do banco de dados;
- as regras dos motores;
- a construção das interfaces;
- os testes de coerência;
- os testes de rastreabilidade;
- o versionamento dos objetos;
- a documentação das transformações;
- a rastreabilidade das decisões.

Alterações conceituais relevantes devem ser registradas formalmente e avaliadas quanto aos seus efeitos sobre os demais documentos canônicos do MediAd Planner.

## 15.1 Registro da Versão 1.2

A versão 1.2 consolida as seguintes decisões arquiteturais:

- formalização do conceito de Objeto de Conhecimento;
- definição de cada etapa como produtora de um objeto estruturado;
- distinção epistemológica entre registro, descrição, interpretação, decisão, avaliação e execução;
- definição do Briefing como produtor do Objeto Contextual Estruturado;
- reserva da formulação do problema à Tradução Estratégica;
- definição da Tradução Estratégica como produtora do Objeto Interpretativo;
- diferenciação entre ontologia do domínio e ontologia do processo de construção do conhecimento;
- criação do Grafo das Transformações Epistemológicas;
- ampliação das regras de rastreabilidade, proveniência e versionamento;
- consolidação da transformação do conhecimento como núcleo arquitetural do MediAd Planner.
