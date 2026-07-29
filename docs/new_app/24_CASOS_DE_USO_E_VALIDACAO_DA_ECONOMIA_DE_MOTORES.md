# Casos de Uso e Validação da Economia de Motores

**Documento:** `24_CASOS_DE_USO_E_VALIDACAO_DA_ECONOMIA_DE_MOTORES.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Natureza:** Validação arquitetural por casos de uso e matriz de consumo  
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

## 20. Matriz de consumo e responsabilidade

### 20.1 Finalidade da matriz

Os motores não possuem cópias próprias dos campos, parâmetros ou objetos definidos nos documentos anteriores. Eles consomem snapshots e referências versionadas conforme a responsabilidade e o modo de execução.

A matriz utiliza as seguintes qualificações:

```text
P = consumo principal
C = consumo condicionado ao caso ou ao modo de execução
R = recebe ou reutiliza como resultado de outro motor ou serviço
— = não consome diretamente como responsabilidade de domínio
```

O consumo não significa que todo campo do documento seja carregado. Cada execução deve selecionar apenas os campos necessários ao problema identificado.

### 20.2 Documentos funcionais 01 a 11

| Documento | Conteúdo utilizado pelos motores | Tradução Estratégica | Decisão de Arquitetura e Cenários | Simulação Técnica e Econômica | Responsabilidade predominante |
|---|---|---:|---:|---:|---|
| 01 — Campanha | anunciante, marca, produto, identificação, vigência, estado e contexto da campanha | C | C | C | fornece identidade, escopo e snapshot; não contém raciocínio próprio do motor |
| 02 — Briefing | objetivos declarados, públicos, praças, período, verba, restrições, prioridades, concorrência e informações disponíveis | P | C | C | principal entrada da tradução; fornece limites aos demais motores |
| 03 — Tradução Estratégica | pesos, prioridades, relações, mínimos, penalizações, estados de completude e confiança | P | R | R | configurado e executado pelo Motor de Tradução; os demais recebem o contrato resultante |
| 04 — Arquitetura de Mídia | meios, pontos de contato, papéis, mix, praça, cronologia, elegibilidade, componentes fixos e ajustáveis | C | P | P | objeto decisório principal do Motor de Decisão e estrutura de entrada da simulação |
| 05 — Simulações | cenários, componentes, quantidades, parâmetros, modos, snapshots e resultados projetados | — | R | P | ambiente principal do Motor de Simulação; resultados retornam ao Motor de Decisão |
| 06 — Comparação de Cenários | critérios, pesos, tolerâncias, dominância, empate técnico, incomparabilidade e trade-offs | C | P | R | modo do Motor de Decisão; utiliza resultados produzidos pela simulação |
| 07 — Otimização de Cenários | limites de busca, componentes bloqueados, faixas ajustáveis, ganho marginal, iterações e objetivo do ajuste | C | P | R | modo avançado do Motor de Decisão, com chamadas controladas ao Motor de Simulação |
| 08 — Plano Consolidado de Mídia | cenário aprovado, justificativas, decisões finais, parâmetros preservados e referências às versões utilizadas | R | R | R | destino dos resultados aprovados; geração pertence a serviço documental, não a motor |
| 09 — Validação, aprovação e operacionalização previstas no fluxo | estados de decisão, bloqueios, aprovações, ressalvas e condições para avanço | C | C | C | condiciona execução e publicação; aprovação humana não é produzida pelos motores |
| 10 — Mapa de Veiculação | linhas aprovadas, produtos, ofertas, ocorrências, datas, quantidades e condições comerciais | — | R | R | recebe o cenário consolidado; composição operacional não constitui motor |
| 11 — Perfis de Acesso e Permissões | escopo de leitura, edição, execução, aprovação e alteração de parâmetros | C | C | C | controla autorização para executar ou alterar; não interfere no mérito técnico da recomendação |

### 20.3 Sistema de Bibliotecas 12 a 18B

| Documento ou biblioteca | Conteúdo utilizado pelos motores | Tradução Estratégica | Decisão de Arquitetura e Cenários | Simulação Técnica e Econômica | Responsabilidade predominante |
|---|---|---:|---:|---:|---|
| 12 — Sistema de Bibliotecas | contratos de uso, versionamento, relações, proveniência, estados e snapshots | P | P | P | contrato transversal de acesso e rastreabilidade |
| 12A — Consolidação das Bibliotecas Operacionais | localização de custos, regras e modelos reutilizáveis nas estruturas existentes | C | P | P | impede consultas a bibliotecas paralelas inexistentes |
| 13 — Inventários de Mídia | tipologias, veículos, plataformas, ambientes, formatos, disponibilidades, produtos, ofertas, unidades e condições comerciais | C | P | P | fornece alternativas ao Motor de Decisão e entradas operacionais ao Motor de Simulação |
| 14 — Públicos e Segmentos | universos, segmentos, características, interesses, comportamentos, territórios e contextos | P | P | P | orienta prioridades, elegibilidade e bases de mensuração |
| 15 — Objetivos, Resultados e KPIs | objetivos classificados, resultados pretendidos, indicadores, metas, prioridades e compatibilidades | P | P | P | define o que orientar, comparar, projetar e calcular |
| 16 — Jornadas, Necessidades, Funções e Pontos de Contato | etapas, necessidades, funções e relações com categorias de mídia | P | P | C | estrutura a passagem da intenção estratégica para alternativas de mídia |
| 17 — Conhecimento Técnico | conceitos, fórmulas, regras, técnicas, comparabilidade, interpretação, restrições e variantes | P | P | P | base de conhecimento compartilhada, consultada seletivamente |
| 17A — Inventário Preliminar | mapa de conhecimentos existentes, pendentes e prioritários | C | C | C | apoio à disponibilidade e cobertura do conhecimento; não é entrada de usuário |
| 17B — Protocolo de Formalização | estrutura, campos obrigatórios, versionamento e critérios de qualidade dos conhecimentos | C | C | P | contrato de leitura e execução dos objetos técnicos |
| 17C — Universo e Audiência | universo, audiência, impactos, unidades, bases e regras de validade | C | C | P | procedimentos acionados quando o cenário exige audiência ou impactos |
| 17D — Alcance e Frequência | alcance, frequência, deduplicação, acumulação e condições de cálculo | C | C | P | procedimentos acionados sob demanda na simulação |
| 17E — GRP e Equivalências Multimídia | GRP, TRP, pressão, conversões, equivalências e ressalvas multimídia | C | C | P | procedimentos condicionais; não universaliza métricas entre meios |
| 17F — Contrato Mínimo de Mensuração | unidade de observação, universo, natureza do valor, deduplicação, equivalência e confiança | P | P | P | metadados obrigatórios herdados ou calculados em todas as saídas mensuráveis |
| 18 — Problemas Técnicos | problemas, gatilhos, entradas, procedimentos possíveis, restrições, confiança e conclusão | P | P | P | permite que cada motor identifique o problema que lhe compete resolver |
| 18A — Primeiro Núcleo de Problemas Técnicos | validação de base, audiência, impactos, alcance, frequência, pressão, comparabilidade e interpretação | C | C | P | primeiro núcleo executável do Motor de Simulação e apoio às decisões dependentes |
| 18B — Casos de Validação | casos por meio, combinação, disponibilidade de dados e condição de mensuração | C | C | P | testes de seleção de procedimento, comportamento e saída dos motores |

### 20.4 Responsabilidade por grupos de campos configuráveis

| Grupo configurável | Motor responsável por interpretar ou decidir | Motor responsável por calcular ou projetar | Observação |
|---|---|---|---|
| objetivos, resultados e KPIs prioritários | Tradução Estratégica | Simulação, quando houver cálculo | a prioridade vem do contrato estratégico; a fórmula vem da Biblioteca 17 |
| públicos, segmentos e praças prioritárias | Tradução Estratégica | Simulação | o Motor de Decisão usa a prioridade para filtrar alternativas |
| jornadas, etapas, necessidades e funções | Tradução Estratégica | — | o Motor de Decisão converte essas relações em pontos de contato e inventários |
| pesos, mínimos, penalizações e tolerâncias estratégicas | Tradução Estratégica | — | são preservados no contrato e usados pelo Motor de Decisão |
| meios, pontos de contato, inventários e papéis | Decisão de Arquitetura e Cenários | Simulação | principal, complementar e apoio são decisões contextuais, não atributos permanentes do meio |
| componentes fixos, obrigatórios, proibidos ou ajustáveis | Decisão de Arquitetura e Cenários | Simulação | componentes bloqueados não participam de ajustes automáticos |
| verba total, tetos, pisos e distribuição | Decisão de Arquitetura e Cenários | Simulação | a decisão propõe distribuição; a simulação calcula custos e consequências |
| preços, descontos, comissões, fees e condições comerciais | — | Simulação | são obtidos de produtos e ofertas da Biblioteca 13 ou do snapshot do projeto |
| quantidades, inserções, faces, impressões e unidades comerciais | Decisão, quando selecionadas ou ajustadas | Simulação | a unidade de compra não deve ser confundida com unidade de entrega ou mensuração |
| cronograma, flight, continuidade, ondas e pulsação | Decisão de Arquitetura e Cenários | Simulação | o motor decisório escolhe a configuração; o motor técnico projeta efeitos e custos |
| overlap, deduplicação e alcance combinado | Decisão, para escolher hipótese ou parâmetro permitido | Simulação | ausência de deduplicação válida deve reduzir a confiança, não fabricar alcance líquido |
| frequência desejada, saturação e rendimento marginal | Decisão, para limites e preferências | Simulação | curvas e parâmetros são aplicados apenas quando compatíveis com o caso |
| critérios de comparação, dominância e empate técnico | Decisão de Arquitetura e Cenários | Simulação fornece valores comparáveis | cenários não comparáveis não entram em ordenação numérica comum |
| limites de candidatos, iterações e ganho marginal | Decisão de Arquitetura e Cenários | Simulação atende chamadas delimitadas | controle obrigatório para evitar busca combinatória excessiva |
| precisão, arredondamento, ausência e zero | — | Simulação | definidos pelos objetos de conhecimento e pelo contrato de mensuração |
| confiança, alertas, justificativas e rastreabilidade | todos | todos | cada motor responde apenas pela explicação de sua própria decisão ou cálculo |
| perfis, permissões e aprovação | serviços de aplicação e governança | — | autorizam ações, mas não alteram silenciosamente a lógica técnica |

### 20.5 Entradas por necessidade, não por disponibilidade

Um motor não deve consumir um campo apenas porque ele existe no snapshot. A seleção de entradas seguirá a sequência:

```text
comando do usuário
→ problema técnico identificado
→ saída necessária
→ procedimentos possíveis
→ campos obrigatórios e condicionais
→ carregamento seletivo
```

Consequências:

- o Motor de Tradução não consulta ofertas comerciais para classificar objetivos;
- o Motor de Decisão não recalcula internamente CPM, alcance ou GRP;
- o Motor de Simulação não redefine objetivos, públicos prioritários ou papéis estratégicos;
- nenhum motor carrega todas as bibliotecas em toda execução;
- campos configuráveis sem efeito no problema atual permanecem preservados, mas não processados.

### 20.6 Campos obrigatórios, condicionais e opcionais

Cada contrato de motor deverá classificar suas entradas como:

```text
OBRIGATORIA
necessária para produzir a saída solicitada

CONDICIONAL
necessária apenas quando determinado procedimento, meio ou indicador for acionado

OPCIONAL
melhora a precisão ou explicação, mas não bloqueia a execução

HERDADA
obtida do contrato, snapshot ou resultado anterior

PADRAO_CONFIGURAVEL
utiliza valor versionado quando não houver ajuste autorizado no projeto

NAO_PERTINENTE
não deve ser carregada por aquele motor ou modo
```

A ausência de uma entrada opcional não deve gerar bloqueio. A ausência de uma entrada obrigatória deve produzir estado próprio, pergunta priorizada ou resultado insuficiente, nunca zero artificial.

### 20.7 Regras contra duplicação e campos órfãos

1. Nenhum campo configurável será recadastrado dentro de um motor.
2. Todo campo que altera uma decisão deve possuir ao menos um consumidor declarado.
3. Campos destinados apenas a interface, auditoria ou composição documental não precisam ser consumidos por motores.
4. Um mesmo campo pode ser lido por vários motores, mas apenas um deles deve possuir responsabilidade primária pela sua interpretação decisória.
5. Resultados produzidos por um motor são recebidos pelos demais por contrato versionado, não por leitura direta de estruturas internas.
6. Fórmulas, regras e variantes permanecem na Biblioteca 17; os motores apenas selecionam e executam procedimentos.
7. Problemas e gatilhos permanecem na Biblioteca 18; os motores não mantêm catálogos paralelos de problemas.
8. Permissões controlam quem pode executar ou ajustar, mas não criam versões distintas da lógica técnica por perfil.

### 20.8 Reexecução por origem da alteração

| Alteração | Tradução Estratégica | Decisão de Arquitetura e Cenários | Simulação Técnica e Econômica |
|---|---:|---:|---:|
| objetivo, resultado ou KPI prioritário | refazer | invalidar dependentes | invalidar resultados dependentes |
| público, praça ou etapa prioritária | refazer | invalidar dependentes | recalcular bases afetadas |
| peso, mínimo ou restrição estratégica | refazer parcialmente | reavaliar | recalcular apenas se mudar a configuração |
| meio, inventário ou papel | preservar | refazer parcialmente | recalcular componentes afetados |
| quantidade, inserção ou distribuição temporal | preservar | reavaliar se necessário | recalcular |
| preço, desconto, comissão ou disponibilidade | preservar | reavaliar alternativas afetadas | recalcular custos e entregas afetadas |
| parâmetro de overlap, deduplicação ou saturação | preservar | reavaliar após nova projeção | recalcular procedimentos dependentes |
| critério de comparação ou tolerância | preservar | refazer avaliação | preservar simulações válidas |
| texto, nota ou formatação do plano | preservar | preservar | preservar |
| permissão ou aprovação | preservar resultados | preservar resultados | preservar resultados |

---

## 21. Próxima etapa

Especificar primeiro os contratos comuns dos três motores e, somente depois, cada responsabilidade individual.

A especificação deve começar por:

1. comando recebido;
2. contexto mínimo;
3. problemas técnicos acionáveis;
4. procedimentos selecionáveis;
5. saída principal;
6. alertas, confiança e rastreabilidade;
7. níveis de execução;
8. dependências que exigem reexecução;
9. entradas obrigatórias, condicionais, opcionais, herdadas e não pertinentes;
10. documentos e bibliotecas efetivamente consultados por modo de execução.

Não devem ser criadas classes, tabelas ou telas definitivas antes dessa definição.

---

## 22. Princípio consolidado

> Poucos motores não significam motores monolíticos. O MediAd Planner terá três fronteiras decisórias estáveis, internamente compostas por procedimentos pequenos e carregados sob demanda. Os motores utilizam os campos configuráveis e objetos definidos nos documentos 01 a 18B por contratos seletivos e versionados, sem recadastro, duplicação ou carregamento indiscriminado. A arquitetura deve economizar componentes sem concentrar processamento desnecessário, e preservar rigor técnico sem expor complexidade ao usuário.
