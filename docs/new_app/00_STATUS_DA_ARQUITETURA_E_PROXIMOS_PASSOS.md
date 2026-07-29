# Status da Arquitetura e Próximos Passos

## Objetivo

Este documento registra, de forma provisória, o estado atual da arquitetura conceitual do MediAd Planner para permitir a retomada do desenvolvimento sem perda de contexto.

## Situação atual

A arquitetura conceitual do MediAd Planner encontra-se estabilizada.

O projeto é definido como uma plataforma de inteligência de mídia baseada em sistemas especialistas, composta por:

- ontologias do domínio;
- catálogos controlados;
- bibliotecas de conhecimento;
- bibliotecas de problemas técnicos;
- motores especialistas;
- modelos reutilizáveis;
- mecanismos de inferência, rastreabilidade e explicabilidade.

## Bibliotecas

### Consolidadas

- 12 — Sistema de Bibliotecas;
- 13 — Inventários de Mídia;
- 14 — Públicos e Segmentos;
- 15 — Objetivos, Resultados e KPIs;
- 16 — Jornadas, Necessidades, Funções e Pontos de Contato.

### Em formalização progressiva

- 17 — Conhecimento Técnico;
- 17A — Inventário Preliminar de Conhecimentos Técnicos;
- 17B — Protocolo de Formalização dos Objetos de Conhecimento Técnico;
- 17C — Núcleo 1: Universo e Audiência;
- 17D — Núcleo 2: Alcance e Frequência;
- 18 — Problemas Técnicos de Planejamento de Mídia.

### Pendentes de confirmação arquitetural

- 19 — Custos e Condições Comerciais;
- 20 — Regras, Restrições e Referências Metodológicas;
- 21 — Modelos e Componentes Reutilizáveis.

Essas três estruturas somente deverão permanecer como bibliotecas autônomas se a implementação demonstrar que não podem funcionar de maneira sustentável como módulos internos ou entidades relacionadas às bibliotecas existentes.

## Decisões recentes

### Limite entre as Bibliotecas 14 e 16

A Biblioteca 14 define o público, seus critérios, características e contexto.

A Biblioteca 16 aplica jornadas, etapas, necessidades comunicacionais, funções e pontos de contato ao público em determinado planejamento.

Jornada, etapa, função e ponto de contato não são atributos permanentes do público.

### Granularidade mínima sustentável

A arquitetura deve evitar proliferação de bibliotecas, microdocumentos, microentidades e relações cuja manutenção seja mais onerosa do que o benefício metodológico ou computacional produzido.

As bibliotecas principais devem permanecer poucas, estáveis e delimitadas por responsabilidade. A granularidade necessária ao sistema deve ocorrer preferencialmente dentro delas, por meio de objetos, campos, variantes, regras e relações internas.

Um conhecimento somente deve ser separado em objetos distintos quando a diferença alterar de forma relevante pelo menos um destes elementos:

- fórmula ou direção do cálculo;
- significado das entradas ou da saída;
- universo ou denominador;
- condição de validade;
- interpretação do resultado;
- variante metodológica;
- versionamento independente;
- possibilidade real de substituição ou execução isolada.

Não justificam separação autônoma:

- sinônimos;
- diferenças apenas terminológicas;
- exemplos;
- mensagens explicativas;
- pequenas variações de arredondamento;
- classificações que possam ser campos ou estados;
- regras que só existam como parte inseparável de um cálculo.

O padrão preferencial será:

```text
uma biblioteca estável
    ↓
um domínio técnico coeso
    ↓
um pequeno conjunto de objetos principais
    ↓
componentes internos, variantes e regras
```

A decomposição em vários objetos será exceção justificada, não regra automática.

### Fronteiras da Biblioteca 17

- indicadores e KPIs permanecem na Biblioteca 15;
- conhecimento técnico pertence à Biblioteca 17;
- problemas a resolver pertencem à Biblioteca 18;
- valores e condições comerciais poderão pertencer à Biblioteca 19 ou a módulos internos, conforme validação futura;
- regras externas, institucionais e normativas poderão pertencer à Biblioteca 20 ou a um módulo de referências e restrições, conforme validação futura.

## Trabalho concluído

### Núcleo 1 — Universo e audiência

Formalizado no documento:

```text
17C_NUCLEO_1_UNIVERSO_E_AUDIENCIA.md
```

Foram estruturados:

- conceito de universo;
- validação de identidade de universo;
- conceito e cálculo de audiência percentual;
- conceito e cálculo de participação de audiência;
- conceito de impactos;
- cálculo de impactos por audiência e inserções.

A separação lógica desses componentes não implica a criação de novas bibliotecas nem exige que cada componente se torne uma tabela, classe ou arquivo próprio na implementação.

### Núcleo 2 — Alcance e frequência

Formalizado no documento:

```text
17D_NUCLEO_2_ALCANCE_E_FREQUENCIA.md
```

Foram adotados apenas quatro objetos principais:

```text
KT_CONCEITO_ALCANCE
KT_CALCULO_ALCANCE_PERCENTUAL
KT_CONCEITO_FREQUENCIA_MEDIA
KT_CALCULO_FREQUENCIA_MEDIA
```

As validações de universo, deduplicação, tratamento de zero, interpretação e mensagens permanecem integradas aos objetos ou reutilizam conhecimentos já formalizados no Núcleo 1.

As seguintes noções permanecem como qualificadores ou tópicos relacionados, sem objetos autônomos antecipados:

- alcance líquido;
- alcance acumulado;
- alcance incremental;
- alcance projetado e realizado;
- distribuição de frequência;
- frequência eficiente;
- frequência excessiva;
- saturação.

Elas somente serão separadas se os problemas técnicos ou a implementação exigirem cálculo, validade ou versionamento próprios.

## Próxima etapa ativa

### Núcleo 3 — GRP

O núcleo deverá ser formalizado em um único documento coeso.

A proposta inicial deve ser reduzida a um pequeno conjunto de objetos principais:

```text
KT_CONCEITO_GRP
KT_CALCULO_GRP
KT_CONVERSAO_GRP_IMPACTOS
KT_RESTRICAO_COMPARABILIDADE_GRP
```

O objeto `KT_CALCULO_GRP` poderá conter, como variantes internas:

```text
GRP por audiência percentual e inserções
GRP por alcance percentual e frequência média
soma de GRPs de uma programação
```

A interpretação de pressão, os alertas e as validações de universo permanecerão integrados, salvo necessidade concreta de execução independente.

## Sequência posterior

1. formalizar o Núcleo 3 — GRP com granularidade mínima sustentável;
2. revisar os três núcleos em conjunto para detectar duplicidades ou decomposição excessiva;
3. testar os objetos em casos válidos e inválidos;
4. relacionar os conhecimentos aos indicadores da Biblioteca 15;
5. relacionar os conhecimentos aos problemas da Biblioteca 18;
6. avaliar quais elementos realmente exigem representação estruturada em YAML, JSON ou banco de dados;
7. revisar a necessidade de existência autônoma das Bibliotecas 19, 20 e 21;
8. especificar os motores especialistas;
9. modelar o banco de dados definitivo;
10. definir a arquitetura de inferência e explicabilidade.

## Observação

A fase de reorganização conceitual está encerrada. O projeto entrou na fase de formalização do conhecimento, sob o princípio de que a arquitetura deve ser suficientemente rigorosa para ser explicável e suficientemente simples para ser implementável e mantida.