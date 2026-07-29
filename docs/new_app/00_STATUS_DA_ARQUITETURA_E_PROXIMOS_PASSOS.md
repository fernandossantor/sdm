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
- 17E — Núcleo 3: GRP e Equivalências Multimídia;
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

Foram estruturados conceito de universo, identidade de universo, audiência percentual, participação de audiência, impactos e cálculos correspondentes.

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

As noções de alcance líquido, acumulado, incremental, distribuição de frequência, frequência eficiente e saturação permanecem como qualificadores ou tópicos relacionados até que uma necessidade operacional exija separação.

### Núcleo 3 — GRP e equivalências multimídia

Formalizado no documento:

```text
17E_NUCLEO_3_GRP_E_EQUIVALENCIAS_MULTIMIDIA.md
```

Foram adotados quatro objetos principais:

```text
KT_CONCEITO_GRP
KT_CALCULO_GRP
KT_CONVERSAO_GRP_IMPACTOS
KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA
```

O cálculo de GRP reúne como variantes internas:

```text
GRP por audiência percentual e inserções
GRP por soma da programação
GRP por alcance percentual e frequência média
GRP por exposições brutas e universo
```

A comparação entre mídias passa a utilizar o conceito de pontos de pressão qualificados.

A regra de equivalência classifica cada conversão como:

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

A equivalência multimídia é uma equivalência de escala e pressão. Ela não transforma contatos de naturezas diferentes em experiências idênticas.

O sistema deverá preservar simultaneamente:

```text
metrica_original
valor_original
pontos_de_pressao_convertidos
estado_de_equivalencia
qualificador_da_exposicao
universo
ressalvas
confianca
```

Foram estabelecidas alternativas condicionadas para:

- televisão linear;
- rádio;
- digital display, social e vídeo online;
- CTV, OTT e streaming;
- OOH e DOOH;
- cinema;
- jornal e revista;
- mídia própria, e-mail e CRM;
- eventos, PDV e no media.

As diferenças entre mídias permanecem como variantes internas da regra de equivalência, sem criação de objetos separados para cada meio.

## Princípios consolidados de comparação multimídia

```text
mesma forma algébrica
não implica
mesmo significado de exposição
```

```text
comparar pressão
≠
somar alcance
≠
deduplicar pessoas
```

A conversão para pontos de pressão somente será permitida quando houver:

- definição de exposição;
- valor bruto;
- universo compatível;
- unidade populacional identificada;
- target, praça e período;
- fonte e metodologia;
- qualificador da exposição;
- estado de equivalência e confiança.

Impressão, oportunidade de ver, circulação, fluxo, entrega, presença e interação não são sinônimos.

## Próxima etapa ativa

Revisar conjuntamente os Núcleos 1, 2 e 3 para:

1. detectar duplicidades e decomposição excessiva;
2. harmonizar nomenclaturas, estados e campos;
3. criar um pequeno conjunto de casos válidos, inválidos e condicionados;
4. verificar se os objetos formalizados são suficientes para os primeiros problemas da Biblioteca 18;
5. evitar antecipar objetos que ainda não tenham uso demonstrado.

## Sequência posterior

1. relacionar os conhecimentos aos indicadores da Biblioteca 15;
2. relacionar os conhecimentos aos problemas da Biblioteca 18;
3. avaliar quais elementos realmente exigem representação estruturada em YAML, JSON ou banco de dados;
4. revisar a necessidade de existência autônoma das Bibliotecas 19, 20 e 21;
5. especificar os motores especialistas;
6. modelar o banco de dados definitivo;
7. definir a arquitetura de inferência e explicabilidade.

## Observação

A fase de reorganização conceitual está encerrada. O projeto entrou na fase de formalização do conhecimento, sob o princípio de que a arquitetura deve ser suficientemente rigorosa para ser explicável e suficientemente simples para ser implementável e mantida.
