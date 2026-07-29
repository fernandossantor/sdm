# Status da Arquitetura e Próximos Passos

## Objetivo

Este documento registra o estado atual da arquitetura conceitual do MediAd Planner e orienta a continuidade do desenvolvimento sem perda de contexto.

## Situação atual

A arquitetura conceitual encontra-se estabilizada, contida dentro da proposta funcional e formalizada para a versão 1.0.

O MediAd Planner permanece definido como plataforma de inteligência de mídia baseada em sistemas especialistas, composta por:

- ontologias do domínio;
- catálogos controlados;
- bibliotecas de conhecimento;
- biblioteca de problemas técnicos;
- motores especialistas;
- configurações e modelos reutilizáveis leves;
- mecanismos de inferência, rastreabilidade e explicabilidade.

Não são necessárias novas bibliotecas para a versão 1.0.

---

## Bibliotecas principais da versão 1.0

### Consolidadas

- 12 — Sistema de Bibliotecas;
- 13 — Inventários de Mídia;
- 14 — Públicos e Segmentos;
- 15 — Objetivos, Resultados e KPIs;
- 16 — Jornadas, Necessidades, Funções e Pontos de Contato;
- 17 — Conhecimento Técnico;
- 18 — Problemas Técnicos de Planejamento de Mídia.

### Documentos complementares das Bibliotecas 17 e 18

- 17A — Inventário Preliminar de Conhecimentos Técnicos;
- 17B — Protocolo de Formalização;
- 17C — Núcleo 1: Universo e Audiência;
- 17D — Núcleo 2: Alcance e Frequência;
- 17E — Núcleo 3: GRP e Equivalências Multimídia;
- 17F — Contrato Mínimo de Mensuração;
- 18A — Primeiro Núcleo de Problemas Técnicos;
- 18B — Casos de Validação do Primeiro Núcleo;
- 17G/18C — Finalização das Bibliotecas 17 e 18.

O documento `17G_18C_FINALIZACAO_DAS_BIBLIOTECAS_17_E_18.md` encerra formalmente o escopo conceitual das duas bibliotecas para a versão 1.0.

---

## Estruturas incorporadas

As antigas propostas de Bibliotecas 19, 20 e 21 não serão implementadas como bibliotecas autônomas.

A distribuição consolidada é:

```text
custos e condições comerciais
→ Biblioteca 13 + Biblioteca 17 + Biblioteca 18

regras, restrições e referências metodológicas
→ bibliotecas correspondentes + Biblioteca 17 + Biblioteca 18

modelos e componentes reutilizáveis
→ simulações, cenários, cronograma, motores e artefatos de saída
```

Nenhum conteúdo essencial foi descartado. Foram eliminadas apenas estruturas autônomas cuja necessidade não foi demonstrada.

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

Sinônimos, exemplos, mensagens, pequenos ajustes, exceções e classificações devem permanecer como campos, estados, variantes, parâmetros ou relações internas.

> Rigor metodológico interno sem burocratização da experiência do usuário.

---

## Biblioteca 17 — estado consolidado

A Biblioteca 17 cobre os conhecimentos necessários para:

```text
calcular
transformar
validar
comparar
interpretar
explicar
```

Os núcleos formalizados são:

- Universo e Audiência;
- Alcance e Frequência;
- GRP e Equivalências Multimídia;
- Contrato Mínimo de Mensuração.

Os seguintes metadados são transversais:

```text
unidade_de_observacao
universo_de_referencia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

Esses campos devem ser herdados ou calculados sempre que possível e não constituem novas telas ou cadastros obrigatórios.

Novos conhecimentos somente serão incorporados quando exigidos por um motor, indicador ou caso de uso comprovado.

---

## Biblioteca 18 — estado consolidado

A Biblioteca 18 organiza perguntas técnicas orientadas à decisão.

Suas famílias estáveis são:

```text
ESTRATEGIA
DIMENSIONAMENTO_E_PROJECAO
COMPARACAO
SELECAO_E_COMPOSICAO
ECONOMIA_E_ORCAMENTO
TEMPO_E_OPERACAO
VALIDACAO
EXPLICACAO_E_DIAGNOSTICO
```

O núcleo inicial cobre:

```text
validar base e dados
→ calcular ou recuperar audiência
→ calcular impactos
→ estimar alcance e frequência
→ calcular pressão
→ validar comparabilidade
→ interpretar e explicar
```

Problemas próximos devem ser tratados primeiro como variantes, subproblemas ou procedimentos internos.

---

## Estados harmonizados

### Validação

```text
VALIDO
VALIDO_COM_ALERTA
INVALIDO
INDETERMINADO
```

### Comparabilidade

```text
COMPARAVEL_DIRETAMENTE
COMPARAVEL_APOS_CONVERSAO
COMPARAVEL_COM_RESSALVA
NAO_COMPARAVEL
DADOS_INSUFICIENTES
```

### Resultado de problema

```text
CONCLUIDO
CONCLUIDO_COM_RESSALVA
PARCIAL
NAO_APLICAVEL
NAO_CALCULADO_DADO_AUSENTE
NAO_CALCULADO_DADO_INVALIDO
BLOQUEADO_INCOMPATIBILIDADE
INDETERMINADO
```

### Deduplicação

```text
DEDUPLICADO
PARCIALMENTE_DEDUPLICADO
NAO_DEDUPLICADO
NAO_APLICAVEL
INDETERMINADO
```

### Equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

Não devem ser criados novos estados apenas para adaptar textos de interface.

---

## Relações mínimas para implementação

```text
indicador_da_biblioteca_15
↔ objeto_de_conhecimento_da_biblioteca_17
```

```text
problema_da_biblioteca_18
↔ objeto_de_conhecimento_da_biblioteca_17
```

```text
problema_da_biblioteca_18
↔ procedimento_de_resolucao
```

Essas relações são suficientes para iniciar a especificação dos motores.

---

## Próxima etapa ativa

Especificar os motores especialistas sem reabrir a arquitetura conceitual.

A especificação deve definir:

1. finalidade de cada motor;
2. problemas da Biblioteca 18 atendidos;
3. conhecimentos da Biblioteca 17 consultados;
4. entradas, saídas e pré-condições;
5. procedimentos e critérios de escolha;
6. tratamento de confiança, ausência e incompatibilidade;
7. necessidade de intervenção humana;
8. explicabilidade e rastreabilidade;
9. reutilização de funções comuns;
10. limites para evitar motores excessivamente especializados.

---

## Sequência posterior

1. especificar os motores especialistas;
2. revisar a arquitetura completa para eliminação final de redundâncias;
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
- campos técnicos visíveis na jornada principal do usuário;
- duplicações de fórmulas entre motores e Biblioteca 17;
- duplicações de problemas entre motores e Biblioteca 18.

## Observação

As Bibliotecas 17 e 18 estão formalizadas para a versão 1.0. A próxima expansão permitida é a especificação dos motores especialistas, e não a criação de novas camadas conceituais.