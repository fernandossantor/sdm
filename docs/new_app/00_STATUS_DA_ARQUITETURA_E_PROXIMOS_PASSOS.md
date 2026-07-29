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

## Próxima etapa ativa

Formalizar o primeiro lote de Objetos de Conhecimento Técnico.

### Núcleo 1 — Universo e audiência

- conceito de universo;
- validação de identidade de universo;
- conceito e cálculo de audiência percentual;
- conceito e cálculo de participação de audiência;
- conceito de impactos;
- cálculo de impactos por audiência e inserções.

### Núcleo 2 — Alcance e frequência

- conceito e cálculo de alcance;
- conceito de frequência média;
- cálculo da frequência por impactos e alcance;
- validação de identidade de universo;
- interpretação da frequência média.

### Núcleo 3 — GRP

- conceito de GRP;
- cálculo por audiência e inserções;
- cálculo por alcance e frequência;
- conversão de GRP em impactos;
- restrição de comparabilidade multimídia;
- interpretação de GRP.

## Sequência posterior

1. produzir fichas normativas do primeiro lote;
2. produzir representação estruturada em YAML ou JSON;
3. definir casos válidos e inválidos;
4. relacionar objetos aos indicadores da Biblioteca 15;
5. relacionar objetos aos problemas da Biblioteca 18;
6. ampliar o inventário formalizado;
7. projetar as Bibliotecas 19, 20 e 21;
8. especificar os motores especialistas;
9. modelar o banco de dados definitivo;
10. definir a arquitetura de inferência e explicabilidade.

## Observação

A fase de reorganização conceitual está encerrada. O projeto entrou na fase de formalização do conhecimento e preparação da base executável dos motores especialistas.