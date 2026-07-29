# Status da Arquitetura e Próximos Passos

## Objetivo

Este documento registra o estado atual da arquitetura conceitual do MediAd Planner e orienta a continuidade do desenvolvimento sem perda de contexto.

## Situação atual

A arquitetura conceitual encontra-se estabilizada. O refinamento realizado em 29/07/2026 confirmou que não são necessárias novas bibliotecas, telas ou motores para incorporar as práticas observadas em materiais teóricos, guias técnicos, mídia kits, tabelas comerciais e propostas multiplataforma.

O projeto permanece definido como plataforma de inteligência de mídia baseada em sistemas especialistas, composta por:

- ontologias do domínio;
- catálogos controlados;
- bibliotecas de conhecimento;
- bibliotecas de problemas técnicos;
- motores especialistas;
- modelos reutilizáveis;
- mecanismos de inferência, rastreabilidade e explicabilidade.

---

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
- 17B — Protocolo de Formalização;
- 17C — Núcleo 1: Universo e Audiência;
- 17D — Núcleo 2: Alcance e Frequência;
- 17E — Núcleo 3: GRP e Equivalências Multimídia;
- 18 — Problemas Técnicos de Planejamento de Mídia.

### Pendentes de confirmação arquitetural

- 19 — Custos e Condições Comerciais;
- 20 — Regras, Restrições e Referências Metodológicas;
- 21 — Modelos e Componentes Reutilizáveis.

Essas estruturas somente permanecerão autônomas se a implementação demonstrar necessidade real.

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
- execução independente.

Sinônimos, exemplos, mensagens, pequenos ajustes e classificações devem permanecer como campos, estados ou variantes internas.

---

## Refinamentos concluídos em 29/07/2026

### Biblioteca 13 — Inventários

O documento `13_BIBLIOTECA_DE_INVENTARIOS.md` foi revisado para formalizar:

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

Foram consolidadas as separações entre:

- inventário, formato, especificação e experiência;
- produto comercial, pacote, cota, patrocínio e projeto;
- unidade de compra, entrega e mensuração;
- cobertura territorial, abrangência da programação e alcance;
- fluxo, OTS, contato ajustado e impactos;
- composição de audiência, penetração, afinidade e alcance no target;
- mídia, produção, direitos, tecnologia, dados e ativação.

A Biblioteca passa a admitir inventários hierárquicos, circuitos, redes e produtos compostos sem criar novas bibliotecas.

### Mapa de Veiculação

O documento `10_MAPA_DE_VEICULACAO.md` foi incrementado.

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

O Mapa permanece como saída operacional do Plano e passa a preservar:

- hierarquia do inventário;
- produtos e entregas compostas;
- condições negociadas além do desconto;
- modelos de remuneração;
- métricas nativas;
- natureza garantida, estimada, histórica ou potencial dos valores;
- tipologia de impactos;
- estados de equivalência e deduplicação;
- dados necessários à autorização, PI, checking e conciliação.

Não foi criado módulo autônomo de PI.

### Núcleo 2 — Alcance e Frequência

O documento `17D_NUCLEO_2_ALCANCE_E_FREQUENCIA.md` foi revisado.

Foram formalizados:

- estados de deduplicação;
- distinção entre cobertura e alcance;
- referência temporal obrigatória;
- limites da frequência média;
- incompatibilidade entre inserções, impressões, impacto e frequência;
- relação entre overlap, alcance, frequência e saturação.

A distribuição de frequência, frequência eficiente e saturação permanecem tópicos relacionados, não novos objetos.

### Núcleo 3 — GRP e Equivalências Multimídia

O documento `17E_NUCLEO_3_GRP_E_EQUIVALENCIAS_MULTIMIDIA.md` foi revisado.

A comparação passa a operar em quatro camadas:

```text
métrica nativa
→ oportunidade de exposição
→ contato qualificado
→ efeito ou resultado
```

Estados mantidos:

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

Os pontos de pressão foram definidos como índice analítico normalizado. Não equivalem automaticamente a GRP certificado, alcance deduplicado, pessoas únicas, atenção ou efeito.

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
cobertura territorial
≠
alcance de audiência
```

```text
fluxo
≠
OTS
≠
contato ajustado
≠
impacto validado
```

---

## Próxima etapa ativa

Revisar conjuntamente os Núcleos 1, 2 e 3 e sua integração com as Bibliotecas 13, 15 e 18 para:

1. harmonizar nomes de campos, estados e qualificadores;
2. revisar a tipologia de impactos no Núcleo 1;
3. validar casos de televisão, rádio, digital, OOH, impresso e cinema;
4. testar casos válidos, condicionados, inválidos e indeterminados;
5. verificar suficiência para os primeiros problemas técnicos da Biblioteca 18;
6. evitar antecipar objetos sem uso demonstrado.

## Sequência posterior

1. relacionar conhecimentos aos indicadores da Biblioteca 15;
2. relacionar conhecimentos aos problemas da Biblioteca 18;
3. decidir o que exige YAML, JSON ou banco;
4. revisar a autonomia das Bibliotecas 19, 20 e 21;
5. especificar os motores especialistas;
6. modelar o banco definitivo;
7. definir inferência e explicabilidade.

## Observação

A proposta funcional permanece madura e com escopo estável. O trabalho atual é de precisão semântica, metodológica e operacional, não de expansão da plataforma.