# Status da Arquitetura e Próximos Passos

## Objetivo

Este documento registra o estado atual da arquitetura conceitual do MediAd Planner e orienta a continuidade do desenvolvimento sem perda de contexto.

## Situação atual

A arquitetura conceitual encontra-se estabilizada e contida dentro da proposta funcional do MediAd Planner.

O refinamento realizado em 29/07/2026 confirmou que não são necessárias novas bibliotecas, telas ou motores para incorporar as práticas observadas em materiais teóricos, guias técnicos, mídia kits, tabelas comerciais e propostas multiplataforma.

O projeto permanece definido como plataforma de inteligência de mídia baseada em sistemas especialistas, composta por:

- ontologias do domínio;
- catálogos controlados;
- bibliotecas de conhecimento;
- biblioteca de problemas técnicos;
- motores especialistas;
- configurações e modelos reutilizáveis leves;
- mecanismos de inferência, rastreabilidade e explicabilidade.

---

## Bibliotecas principais da versão 1.0

### Consolidadas

- 12 — Sistema de Bibliotecas;
- 13 — Inventários de Mídia;
- 14 — Públicos e Segmentos;
- 15 — Objetivos, Resultados e KPIs;
- 16 — Jornadas, Necessidades, Funções e Pontos de Contato.

### Em finalização

- 17 — Conhecimento Técnico;
- 17A — Inventário Preliminar de Conhecimentos Técnicos;
- 17B — Protocolo de Formalização;
- 17C — Núcleo 1: Universo e Audiência;
- 17D — Núcleo 2: Alcance e Frequência;
- 17E — Núcleo 3: GRP e Equivalências Multimídia;
- 17F — Contrato Mínimo de Mensuração;
- 18 — Problemas Técnicos de Planejamento de Mídia;
- 18A — Primeiro Núcleo de Problemas Técnicos;
- 18B — Casos de Validação do Primeiro Núcleo.

### Estruturas incorporadas

As antigas propostas de Bibliotecas 19, 20 e 21 não serão implementadas como bibliotecas autônomas na versão 1.0.

Seus conteúdos foram redistribuídos conforme o documento:

`12A_CONSOLIDACAO_DAS_BIBLIOTECAS_OPERACIONAIS.md`

A distribuição consolidada é:

```text
custos e condições comerciais
→ Biblioteca 13 + Biblioteca 17 + Biblioteca 18

regras, restrições e referências metodológicas
→ bibliotecas correspondentes + Biblioteca 17 + Biblioteca 18

modelos e componentes reutilizáveis
→ simulações, cenários, cronograma, motores e artefatos de saída
```

Nenhum conteúdo essencial foi descartado. Foram eliminadas apenas estruturas autônomas cuja necessidade ainda não foi demonstrada.

---

## Princípio de granularidade

A arquitetura deve permanecer composta por poucas bibliotecas estáveis.

Um objeto somente deve ser separado quando houver diferença relevante de:

- fórmula;
- significado;
- universo;
- validade;
- interpretação;
- metodologia;
- versionamento;
- execução independente;
- decisão explícita do usuário.

Sinônimos, exemplos, mensagens, pequenos ajustes, exceções e classificações devem permanecer como campos, estados ou variantes internas.

A implementação deve seguir o princípio:

> rigor metodológico interno sem burocratização da experiência do usuário.

---

## Refinamentos concluídos

### Biblioteca 13 — Inventários

A cadeia consolidada é:

```text
proprietário ou grupo
→ veículo ou plataforma
→ propriedade
→ ambiente
→ inventário
→ formato compatível
→ disponibilização
→ produto comercial
→ oferta comercial
```

A Biblioteca 13 admite inventários hierárquicos, circuitos, redes e produtos compostos. Custos e condições comerciais acompanham produtos, ofertas e disponibilidades, sem biblioteca paralela.

### Mapa de Veiculação

A cadeia operacional consolidada é:

```text
Plano Consolidado
→ inventários e produtos aprovados
→ condições negociadas
→ linhas de programação
→ ocorrências
→ Mapa de Veiculação
→ autorização ou PI
→ checking e pós-compra
```

Não foi criado módulo autônomo de PI.

### Biblioteca 17 — Conhecimento Técnico

Os três primeiros núcleos foram formalizados:

- Universo e Audiência;
- Alcance e Frequência;
- GRP e Equivalências Multimídia.

O Contrato Mínimo de Mensuração harmoniza os seguintes metadados internos:

```text
unidade_de_observacao
universo_de_referencia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

Esses campos não constituem novas telas ou cadastros obrigatórios. Devem ser herdados ou calculados sempre que possível.

### Biblioteca 18 — Problemas Técnicos

Foi formalizado o primeiro núcleo executável, cobrindo:

```text
validar a base
→ calcular ou recuperar audiência
→ calcular impactos
→ estimar alcance e frequência
→ calcular pressão
→ validar comparabilidade
→ interpretar o resultado
```

Os casos de validação abrangem televisão, rádio, digital, OOH/DOOH, mídia impressa, cinema e combinações multimídia.

### Consolidação operacional

Os conteúdos antes atribuídos às Bibliotecas 19, 20 e 21 foram incorporados à arquitetura existente:

- preços, descontos, vigências e disponibilidade acompanham inventários e ofertas;
- fórmulas econômicas e regras metodológicas permanecem na Biblioteca 17;
- problemas de orçamento, eficiência e bloqueio permanecem na Biblioteca 18;
- templates, cenários, flights e matrizes de pesos permanecem configurações dos módulos e motores;
- referências são metadados dos objetos e permanecem consolidadas no documento 22.

---

## Princípios consolidados

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

```text
unidade de compra
≠
unidade de entrega
≠
unidade de mensuração
```

```text
custo cadastrado
≠
custo calculado
≠
custo projetado
```

```text
regra técnica
não exige
biblioteca autônoma de regras
```

```text
modelo reutilizável
=
configuração de objetos existentes
```

---

## Próxima etapa ativa

Finalizar as Bibliotecas 17 e 18 sem ampliar o escopo:

1. harmonizar definitivamente nomes de campos, estados e qualificadores;
2. vincular os conhecimentos da Biblioteca 17 aos indicadores da Biblioteca 15;
3. vincular os conhecimentos aos problemas da Biblioteca 18;
4. revisar redundâncias e converter objetos excessivos em atributos ou variantes;
5. limitar a Biblioteca 18 aos problemas efetivamente necessários aos motores;
6. declarar as Bibliotecas 17 e 18 formalizadas para a versão 1.0.

## Sequência posterior

1. especificar os motores especialistas;
2. revisar a arquitetura completa para eliminação de redundâncias;
3. declarar a arquitetura funcional congelada na versão 1.0;
4. decidir o que exige YAML, JSON ou banco;
5. modelar o banco definitivo;
6. implementar inferência, explicabilidade e rastreabilidade.

## Limites da próxima fase

Não devem ser criados, sem necessidade comprovada:

- novas bibliotecas;
- motores separados por meio ou formato;
- telas gerais de regras;
- cadastros obrigatórios de templates;
- entidades próprias para cada exceção metodológica;
- campos técnicos visíveis na jornada principal do usuário.

## Observação

A proposta funcional permanece madura e com escopo estável. O trabalho atual é de consolidação semântica, metodológica e operacional. A próxima expansão permitida é a especificação dos motores especialistas, e não a criação de novas camadas conceituais.