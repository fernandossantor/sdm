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
- 18 — Problemas Técnicos de Planejamento de Mídia.

### Pendentes

- 19 — Custos e Condições Comerciais;
- 20 — Regras, Restrições e Referências Metodológicas;
- 21 — Modelos e Componentes Reutilizáveis.

## Decisões recentes

### Limite entre as Bibliotecas 14 e 16

A Biblioteca 14 define o público, seus critérios, características e contexto.

A Biblioteca 16 aplica jornadas, etapas, necessidades comunicacionais, funções e pontos de contato ao público em determinado planejamento.

Jornada, etapa, função e ponto de contato não são atributos permanentes do público.

### Granularidade da Biblioteca 17

Um domínio técnico não corresponde necessariamente a um único objeto.

Domínios como GRP, alcance, frequência ou CPM devem ser decompostos em objetos atômicos e relacionáveis, como:

- conceito;
- cálculo;
- conversão;
- validação;
- restrição;
- interpretação.

### Fronteiras da Biblioteca 17

- indicadores e KPIs permanecem na Biblioteca 15;
- conhecimento técnico pertence à Biblioteca 17;
- problemas a resolver pertencem à Biblioteca 18;
- valores e condições comerciais pertencem à Biblioteca 19;
- regras externas, institucionais e normativas pertencem à Biblioteca 20.

## Trabalho concluído no primeiro lote

Foi criado o documento:

```text
17C_NUCLEO_1_UNIVERSO_E_AUDIENCIA.md
```

O núcleo formaliza, em estado `EM_VALIDACAO`:

- `KT_CONCEITO_UNIVERSO`;
- `KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO`;
- `KT_CONCEITO_AUDIENCIA_PERCENTUAL`;
- `KT_CALCULO_AUDIENCIA_PERCENTUAL`;
- `KT_CONCEITO_PARTICIPACAO_AUDIENCIA`;
- `KT_CALCULO_PARTICIPACAO_AUDIENCIA`;
- `KT_CONCEITO_IMPACTOS`;
- `KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES`.

O núcleo também consolidou as seguintes distinções:

```text
audiência percentual ≠ participação de audiência
impactos ≠ alcance líquido
universo de pessoas ≠ universo de domicílios
universo total ≠ universo ligado ou ativo
igualdade numérica ≠ identidade metodológica
```

## Próxima etapa ativa

### Núcleo 2 — Alcance e frequência

Formalizar:

- `KT_CONCEITO_ALCANCE`;
- `KT_CALCULO_ALCANCE_PERCENTUAL`;
- `KT_CONCEITO_FREQUENCIA_MEDIA`;
- `KT_CALCULO_FREQUENCIA_POR_IMPACTOS_E_ALCANCE`;
- `KT_VALIDACAO_FREQUENCIA_MESMO_UNIVERSO`;
- `KT_INTERPRETACAO_FREQUENCIA_MEDIA`.

Esse núcleo deve preservar a distinção entre:

```text
alcance absoluto
alcance percentual
alcance líquido
alcance acumulado
alcance incremental
```

Também deve impedir que frequência média seja interpretada como distribuição de frequência ou frequência eficiente.

## Etapas posteriores do primeiro lote

### Núcleo 3 — GRP

- conceito de GRP;
- cálculo por audiência e inserções;
- cálculo por alcance e frequência;
- conversão de GRP em impactos;
- restrição de comparabilidade multimídia;
- interpretação de GRP.

### Validação transversal

Após os três núcleos:

1. produzir representação estruturada em YAML ou JSON;
2. definir casos válidos e inválidos;
3. relacionar objetos aos indicadores da Biblioteca 15;
4. relacionar objetos aos problemas da Biblioteca 18;
5. validar códigos de unidades, estados e severidades;
6. testar a conversão dos objetos em funções e regras executáveis.

## Sequência posterior

1. ampliar o inventário formalizado;
2. projetar as Bibliotecas 19, 20 e 21;
3. especificar os motores especialistas;
4. modelar o banco de dados definitivo;
5. definir a arquitetura de inferência e explicabilidade.

## Observação

A fase de reorganização conceitual está encerrada. O projeto entrou na fase de formalização do conhecimento e preparação da base executável dos motores especialistas. O Núcleo 1 representa a primeira aplicação integral do protocolo de formalização.