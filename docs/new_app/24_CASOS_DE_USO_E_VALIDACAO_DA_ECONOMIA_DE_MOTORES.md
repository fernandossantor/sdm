# Casos de Uso e Validação da Economia de Motores

**Documento:** `24_CASOS_DE_USO_E_VALIDACAO_DA_ECONOMIA_DE_MOTORES.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Natureza:** Validação arquitetural por casos de uso  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

Este documento testa a proposta de motores especialistas contra casos de uso reais do MediAd Planner antes da especificação individual de cada componente.

A validação procura responder simultaneamente:

1. quantos motores são realmente necessários;
2. quais responsabilidades possuem fronteira própria;
3. quais funções devem permanecer procedimentos internos;
4. como evitar motores excessivamente amplos, lentos ou difíceis de compreender;
5. como manter a jornada do usuário simples mesmo quando a lógica interna for complexa.

O critério principal não é distribuir uniformemente funções entre componentes. É preservar poucas responsabilidades decisórias claras, acionadas somente quando necessárias.

---

## 2. Premissas de teste

Os casos foram avaliados segundo as seguintes premissas:

- nem todo fluxo precisa executar todos os motores;
- uma função matemática, validação ou cálculo não justifica motor próprio;
- um motor pode possuir modos de execução, desde que compartilhem o mesmo objeto decisório;
- procedimentos especializados podem ser carregados sob demanda;
- o usuário não deve escolher manualmente qual motor executar;
- a interface deve apresentar tarefas e decisões, não a arquitetura técnica interna;
- resultados parciais devem ser reutilizados, evitando recomputação integral;
- a ausência de dados deve reduzir a profundidade da resposta, não bloquear desnecessariamente o fluxo inteiro.

---

## 3. Critérios de validação dos casos

Cada caso foi examinado por cinco perguntas:

```text
qual decisão precisa ser produzida?
quais entradas são realmente necessárias?
qual responsabilidade especialista é acionada?
o resultado pode ser reutilizado por outros fluxos?
a separação em novo motor melhora ou piora a experiência?
```

Um motor foi considerado excessivamente pesado quando acumulava responsabilidades com ciclos de execução, entradas ou saídas claramente distintos.

Uma separação foi considerada excessiva quando criava passagem técnica entre componentes sem representar uma nova decisão para o usuário.

---

## 4. Caso 1 — Planejamento guiado a partir de briefing

### Situação

O usuário informa objetivo, público, praça, período, verba, restrições e prioridades. Espera receber alternativas iniciais de arquitetura de mídia.

### Fluxo necessário

```text
briefing
→ tradução das prioridades
→ geração de arquiteturas candidatas
→ simulação preliminar das alternativas viáveis
→ apresentação das opções
```

### Constatações

A tradução estratégica possui saída própria e reutilizável: o contrato estratégico. Alterações de inventário, preço ou programação não exigem necessariamente refazer toda a tradução.

A geração de arquiteturas e a avaliação inicial das alternativas pertencem ao mesmo objeto decisório: escolher e aperfeiçoar uma configuração de mídia coerente com o contrato estratégico.

Separar geração e avaliação em dois motores obriga uma troca artificial:

```text
gerar candidatos
→ simular
→ devolver a outro motor
→ avaliar
→ solicitar novos candidatos
```

Esse ciclo seria frequente e aumentaria acoplamento, latência e dificuldade de explicação.

### Resultado

- Motor de Tradução Estratégica: necessário.
- Motor de Decisão de Arquitetura e Cenários: necessário.
- Motor de Simulação: necessário como serviço especialista independente chamado sob demanda.
- Motores separados de composição e avaliação: desnecessários.

---

## 5. Caso 2 — Simular uma arquitetura já definida pelo usuário

### Situação

O usuário já selecionou meios, inventários, quantidades, praça, período e custos. Deseja apenas projetar alcance, frequência, pressão, investimento e eficiência.

### Fluxo necessário

```text
arquitetura informada
→ validação técnica
→ cálculos aplicáveis
→ resultado da simulação
```

### Constatações

Não é necessário executar tradução estratégica nem gerar alternativas.

O caso demonstra que a simulação possui ciclo independente, entradas próprias e utilidade direta. Portanto, não deve ser incorporada ao motor decisório de arquitetura.

Entretanto, alcance, frequência, custos, GRP, overlap, saturação e cronograma não exigem motores distintos. São procedimentos selecionados conforme os componentes e dados presentes no cenário.

### Resultado

- confirma a autonomia do Motor de Simulação;
- rejeita motores separados de cobertura, pressão, custos ou meio;
- exige execução modular interna e apenas dos procedimentos aplicáveis.

---

## 6. Caso 3 — Comparar dois cenários construídos manualmente

### Situação

O usuário possui dois ou mais cenários simulados e deseja compreender qual atende melhor às prioridades do projeto.

### Fluxo necessário

```text
cenários simulados
+ contrato estratégico, quando disponível
→ validação de comparabilidade
→ análise de trade-offs
→ ordenação condicionada
→ justificativa
```

### Constatações

Comparar cenários e gerar arquiteturas são modos de uma mesma responsabilidade: decidir sobre configurações de mídia.

Ambos utilizam:

- contrato estratégico;
- pesos e restrições;
- inventários e papéis;
- resultados de simulação;
- critérios de dominância e compensação;
- justificativas para aceitação ou rejeição.

A diferença é o ponto de entrada:

```text
GERAR
recebe espaço de alternativas

AVALIAR
recebe alternativas já existentes
```

Não há necessidade de dois motores autônomos.

### Resultado

O antigo Motor de Composição e o antigo Motor de Avaliação devem ser fundidos no:

```text
Motor de Decisão de Arquitetura e Cenários
```

---

## 7. Caso 4 — Ajustar o plano para caber no orçamento

### Situação

O cenário desejado excede a verba disponível. O usuário quer alternativas para reduzir o investimento com menor perda estratégica possível.

### Fluxo necessário

```text
cenário atual
+ limite orçamentário
+ prioridades preservadas
→ identificar componentes ajustáveis
→ gerar poucas variações plausíveis
→ simular apenas as variações alteradas
→ comparar perdas e ganhos
→ sugerir ajustes
```

### Constatações

A otimização não constitui responsabilidade independente. Ela combina geração, avaliação e chamadas iterativas ao Motor de Simulação.

Criar um Motor de Otimização separado duplicaria:

- critérios do motor decisório;
- pesos estratégicos;
- regras de elegibilidade;
- comparação de cenários;
- explicação dos trade-offs.

### Resultado

O ajuste orçamentário será um modo do Motor de Decisão:

```text
SUGERIR_AJUSTES
```

A busca deve trabalhar com limites explícitos e número controlado de alternativas, evitando combinações exaustivas que prejudiquem desempenho e compreensão.

---

## 8. Caso 5 — Explorar uma melhor configuração

### Situação

O usuário solicita que o sistema procure uma configuração melhor dentro de um conjunto permitido de meios, inventários, períodos e limites.

### Fluxo necessário

```text
espaço de alternativas delimitado
→ geração controlada de candidatos
→ filtragem prévia
→ simulação progressiva
→ eliminação de dominados
→ apresentação de finalistas
```

### Risco identificado

Uma busca combinatória irrestrita tornaria o motor pesado e produziria quantidade excessiva de cenários, prejudicando:

- tempo de resposta;
- rastreabilidade;
- legibilidade das recomendações;
- capacidade de decisão do usuário.

### Controles obrigatórios

- limites de quantidade por componente;
- filtros de elegibilidade antes da simulação;
- número máximo de candidatos intermediários;
- eliminação precoce de alternativas inviáveis ou dominadas;
- simulação em níveis de precisão;
- interrupção quando ganhos marginais forem irrelevantes;
- apresentação de poucas alternativas finais.

### Resultado

`BUSCAR_MELHOR_CONFIGURACAO` permanece modo avançado do Motor de Decisão, não motor autônomo e não operação padrão da interface.

---

## 9. Caso 6 — Briefing incompleto ou contraditório

### Situação

Há ausência de verba, público impreciso, objetivos conflitantes ou prazo incompatível.

### Fluxo necessário

```text
briefing parcial
→ identificar lacunas relevantes
→ produzir tradução provisória quando possível
→ marcar incertezas
→ solicitar apenas dados que alteram a decisão
```

### Constatações

Validação não é uma etapa isolada nem um motor. Cada responsabilidade valida aquilo que precisa consumir.

Um Motor de Validação central criaria um bloqueio geral e tenderia a exigir completude excessiva antes de qualquer auxílio.

### Resultado

- validação permanece transversal;
- o Motor de Tradução retorna contrato definitivo, provisório ou insuficiente;
- perguntas ao usuário devem ser priorizadas pelo impacto decisório;
- campos ausentes sem relevância imediata não devem interromper o fluxo.

---

## 10. Caso 7 — Alteração localizada de preço ou disponibilidade

### Situação

Um inventário deixa de estar disponível ou recebe nova condição comercial depois que os cenários foram construídos.

### Fluxo necessário

```text
alteração localizada
→ invalidar apenas resultados dependentes
→ recalcular custos e entregas afetadas
→ reavaliar os cenários relacionados
```

### Constatações

A arquitetura não deve reexecutar automaticamente todos os motores.

O contrato estratégico permanece válido. A simulação deve recalcular somente o cenário ou componente afetado. O motor decisório reavalia apenas as alternativas alteradas.

### Resultado

É obrigatório implementar:

- dependências explícitas entre resultados;
- cache ou snapshot das execuções;
- reexecução incremental;
- invalidação seletiva.

Esses mecanismos são responsabilidades da aplicação e da execução técnica, não novos motores.

---

## 11. Caso 8 — Uso didático com intervenção do aluno

### Situação

O aluno precisa compreender por que determinada arquitetura foi proposta, alterar parâmetros e comparar suas decisões com as sugestões do sistema.

### Constatações

A usabilidade exige que os motores não funcionem como caixas pretas nem como assistentes que substituem todas as escolhas.

A interface deve permitir:

- aceitar ou rejeitar sugestões;
- fixar componentes do cenário;
- alterar parâmetros autorizados;
- executar novamente apenas a etapa afetada;
- visualizar justificativas em camadas;
- comparar resultado original e ajustado.

### Resultado

Explicação permanece contrato obrigatório das saídas. Não haverá Motor de Explicação separado.

A complexidade técnica deve aparecer progressivamente:

```text
resultado principal
→ justificativa resumida
→ alertas e trade-offs
→ memória técnica detalhada
```

---

## 12. Caso 9 — Cálculo técnico isolado

### Situação

O usuário deseja calcular ou verificar apenas CPM, CPP, GRP, frequência, investimento líquido ou outro indicador.

### Constatações

O cálculo utiliza objetos da Biblioteca 17 e procedimentos do Motor de Simulação, mas não justifica motor próprio nem passagem pelo planejamento completo.

### Resultado

O Motor de Simulação deverá admitir operações pontuais, além de simulações completas:

```text
CALCULAR_INDICADOR
VALIDAR_CALCULO
SIMULAR_COMPONENTE
SIMULAR_CENARIO
```

A interface pode oferecer calculadoras ou verificações contextuais sem expor um novo motor ao usuário.

---

## 13. Caso 10 — Gerar Plano Consolidado e Mapa de Veiculação

### Situação

O usuário aprova um cenário e deseja os artefatos finais.

### Constatações

A geração documental não decide, não compara e não calcula uma nova arquitetura. Ela organiza dados já aprovados.

### Resultado

Relatórios, plano e mapa permanecem serviços de composição documental. Não justificam Motor de Consolidação.

---

## 14. Resultado geral dos casos de uso

Os casos confirmam três responsabilidades especialistas autônomas.

### 14.1 Motor de Tradução Estratégica

Produz o contrato estratégico que orienta as demais decisões.

### 14.2 Motor de Decisão de Arquitetura e Cenários

Reúne, como modos de uma mesma responsabilidade:

```text
GERAR_ARQUITETURAS
AVALIAR_CENARIOS
COMPARAR_CENARIOS
SUGERIR_AJUSTES
BUSCAR_MELHOR_CONFIGURACAO
```

Ele decide sobre configurações de mídia, mas não executa internamente todos os cálculos técnicos. Solicita simulações ao motor correspondente.

### 14.3 Motor de Simulação Técnica e Econômica

Executa cálculos, projeções e validações técnicas de componentes e cenários.

Modos iniciais:

```text
CALCULAR_INDICADOR
SIMULAR_COMPONENTE
SIMULAR_CENARIO
RECALCULAR_DEPENDENCIAS
```

---

## 15. Arquitetura consolidada de três motores

```text
Motor de Tradução Estratégica
responde:
o que deve ser priorizado?

        ↓

Motor de Decisão de Arquitetura e Cenários
responde:
quais configurações são coerentes e preferíveis?

        ↕ solicita projeções

Motor de Simulação Técnica e Econômica
responde:
o que cada configuração entrega, custa e exige?
```

A relação entre Decisão e Simulação pode ser iterativa, mas deve ser controlada pela camada de aplicação.

---

## 16. Como evitar motores pesados

A economia de motores não significa concentrar toda a lógica em classes monolíticas.

Cada motor será uma fronteira decisória estável composta por procedimentos internos pequenos e substituíveis.

```text
motor
→ seleciona procedimento
→ carrega apenas conhecimentos aplicáveis
→ executa funções especializadas
→ compõe uma saída única
```

### 16.1 Procedimentos sob demanda

O Motor de Simulação não deve calcular todos os indicadores em toda execução. Deve identificar quais resultados são necessários ao caso e quais dados estão disponíveis.

Exemplo:

```text
cenário somente digital
→ não carregar procedimentos de GRP televisivo

cenário sem estimativa de deduplicação
→ não executar alcance cross-media como valor certificado
```

### 16.2 Execução progressiva

Recomenda-se três níveis:

```text
PREVIA
cálculos mínimos para filtrar alternativas

PADRAO
projeções necessárias à decisão

DETALHADA
análises adicionais solicitadas pelo usuário
```

A execução detalhada não deve ser o padrão.

### 16.3 Saídas enxutas

Cada motor deve possuir uma saída principal, acompanhada de metadados técnicos.

A interface não deve reproduzir todos os campos do contrato interno. Deve mostrar:

- decisão ou resultado central;
- principais razões;
- alertas relevantes;
- confiança;
- opção de aprofundamento.

### 16.4 Limites de processamento

A busca e comparação devem possuir limites configuráveis para:

- candidatos gerados;
- cenários simultaneamente simulados;
- iterações de aperfeiçoamento;
- profundidade de combinações;
- tolerância de ganho marginal;
- tempo máximo de execução.

### 16.5 Reexecução incremental

Alterações locais não devem reiniciar o planejamento inteiro.

```text
mudou objetivo ou público prioritário
→ refazer tradução e dependências

mudou inventário ou papel
→ refazer decisão e simulação relacionadas

mudou quantidade ou preço
→ refazer simulação e avaliação afetadas

mudou somente texto do plano
→ não refazer motores
```

---

## 17. Regras de usabilidade

1. O usuário nunca escolhe o motor; escolhe a tarefa.
2. A jornada principal não apresenta nomes técnicos de procedimentos.
3. O sistema solicita somente dados que alteram a decisão atual.
4. Resultados preliminares devem ser possíveis com indicação de confiança.
5. Análises avançadas permanecem opcionais.
6. O número de alternativas apresentadas deve ser pequeno e justificável.
7. A explicação deve começar pela diferença prática, não pela fórmula.
8. Alterações devem indicar quais resultados precisam ser recalculados.
9. A decisão final permanece humana.
10. A arquitetura interna não deve determinar a quantidade de telas.

---

## 18. Componentes que continuam não sendo motores

```text
validação
→ regras e serviço transversal

explicação
→ contrato das saídas e compositor compartilhado

orquestração
→ serviço de aplicação

persistência e cache
→ infraestrutura

relatórios e exportações
→ composição documental

cálculos individuais
→ procedimentos do Motor de Simulação

seleção, comparação e otimização
→ modos do Motor de Decisão
```

---

## 19. Decisão arquitetural

A proposta anterior de quatro motores foi reduzida para três após os casos de uso demonstrarem que composição e avaliação operam sobre o mesmo objeto decisório e formam um ciclo recorrente.

A versão 1.0 deverá especificar apenas:

1. Motor de Tradução Estratégica;
2. Motor de Decisão de Arquitetura e Cenários;
3. Motor de Simulação Técnica e Econômica.

Não devem ser criados novos motores sem caso de uso que demonstre simultaneamente:

- decisão autônoma;
- entradas e saídas próprias;
- reutilização independente;
- benefício real de separação;
- ausência de duplicação relevante.

---

## 20. Próxima etapa

Especificar primeiro os contratos comuns dos três motores e, somente depois, cada responsabilidade individual.

A especificação deve começar por:

1. comando recebido;
2. contexto mínimo;
3. problemas técnicos acionáveis;
4. procedimentos selecionáveis;
5. saída principal;
6. alertas, confiança e rastreabilidade;
7. níveis de execução;
8. dependências que exigem reexecução.

Não devem ser criadas classes, tabelas ou telas definitivas antes dessa definição.

---

## 21. Princípio consolidado

> Poucos motores não significam motores monolíticos. O MediAd Planner terá três fronteiras decisórias estáveis, internamente compostas por procedimentos pequenos e carregados sob demanda. A arquitetura deve economizar componentes sem concentrar processamento desnecessário, e preservar rigor técnico sem expor complexidade ao usuário.