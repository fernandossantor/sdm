# Motor de Simulação Técnica e Econômica

**Documento:** `28_MOTOR_DE_SIMULACAO_TECNICA_E_ECONOMICA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Especificado para a versão 1.0  
**Natureza:** Contrato normativo individual de motor especialista  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

O Motor de Simulação Técnica e Econômica transforma uma arquitetura ou configuração de mídia em resultados quantitativos, temporais, territoriais, financeiros e de entrega, preservando validade, comparabilidade, confiança e rastreabilidade.

Sua pergunta central é:

> O que esta configuração pode entregar, custar e exigir, sob quais premissas e com qual grau de confiança?

O motor não decide os objetivos da campanha, não escolhe autonomamente a arquitetura preferida e não aprova o plano. Ele calcula, projeta, valida tecnicamente e devolve consequências mensuráveis para uso do planejador e do Motor de Decisão de Arquitetura e Cenários.

---

## 2. Resultado principal

O resultado principal é:

```text
resultado_de_simulacao_tecnica_e_economica
```

Conforme o modo, esse resultado poderá representar:

- um indicador isolado;
- um componente de mídia;
- uma arquitetura candidata;
- um cenário completo;
- um conjunto de dependências recalculadas.

A saída deve conservar, quando aplicável:

```text
identificacao e versao
arquitetura ou componente de origem
configuracao utilizada
metricas nativas
metricas equivalentes
resultados de audiencia e entrega
resultados temporais e territoriais
resultados economicos
resultados de performance
validacoes
alertas
restricoes
confianca
rastreabilidade
dependencias
politica de reexecucao
```

---

## 3. Modos de execução

### 3.1 `CALCULAR_INDICADOR`

Calcula ou valida um indicador pontual, sem exigir a execução do planejamento completo.

Exemplos:

- CPM;
- CPP;
- CPC;
- CPA;
- CTR;
- GRP;
- TRP;
- frequência média;
- investimento bruto;
- investimento líquido;
- comissão;
- ROAS;
- alcance estimado, quando houver base válida.

### 3.2 `SIMULAR_COMPONENTE`

Projeta um inventário, oferta, canal, veículo, praça, público, período ou linha de veiculação individual.

### 3.3 `SIMULAR_CENARIO`

Executa o conjunto de procedimentos necessários para produzir um Cenário Simulado de Mídia a partir de uma arquitetura e de suas configurações.

### 3.4 `RECALCULAR_DEPENDENCIAS`

Recalcula somente os resultados afetados por alteração localizada, preservando resultados ainda válidos.

### 3.5 `VALIDAR_CALCULO`

Reproduz ou verifica um cálculo, sua fórmula, unidades, entradas, arredondamento, versão e condições de validade.

Este modo não constitui motor separado.

---

## 4. Limites de responsabilidade

O motor deve:

- aplicar preços, quantidades, unidades e condições comerciais;
- calcular investimento bruto, líquido, comissão, fees e demais incidências configuradas;
- projetar audiência, impactos, alcance, frequência, cobertura e pressão quando houver procedimentos válidos;
- tratar overlap, deduplicação, saturação e rendimento marginal;
- aplicar cronograma, fases e flight operacional;
- projetar resultados por público, praça, período, meio, canal e inventário;
- calcular indicadores nativos e derivados;
- registrar equivalências apenas quando autorizadas pelos conhecimentos aplicáveis;
- distinguir valores informados, calculados, estimados, inferidos e ajustados;
- preservar confiança e condições de validade;
- devolver resultados comparáveis somente quando o contrato mínimo de mensuração for atendido.

O motor não deve:

- redefinir objetivos de Marketing, Comunicação ou Mídia;
- alterar prioridades estratégicas;
- escolher inventários por mérito estratégico sem solicitação do Motor de Decisão;
- atribuir automaticamente papéis principal, complementar ou apoio;
- ordenar cenários por aderência estratégica;
- otimizar autonomamente o mix;
- inventar preços, audiências, descontos, taxas ou coeficientes;
- fabricar alcance líquido quando não houver deduplicação válida;
- transformar ausência em zero;
- aprovar o plano ou consolidar documentos finais.

Pode sugerir inconsistências ou reclassificações, mas a decisão permanece fora do motor.

---

## 5. Entradas e fontes

### 5.1 Entradas principais

Conforme o modo, o motor pode consumir:

- arquitetura candidata ou cenário existente;
- componentes, inventários, ofertas e unidades de compra;
- quantidades, inserções, impressões, faces, diárias, pacotes ou demais volumes;
- preços de tabela e negociados;
- descontos, bonificações, comissão, fees e taxas;
- orçamento e limites financeiros;
- públicos, segmentos, universos e praças;
- período, fases, flight e distribuição temporal;
- dados de audiência e entrega;
- parâmetros de overlap, deduplicação, saturação e equivalência;
- taxas de performance e conversão;
- definição de conversão, receita e atribuição;
- indicadores requeridos;
- nível e limites de execução.

### 5.2 Documentos funcionais consumidos

| Documento | Consumo |
|---|---|
| 01 — Campanha | contexto, identidade, vigência, moeda e snapshot |
| 02 — Briefing | verba, prazo, praça, público, restrições e referências |
| 03 — Tradução Estratégica | recebe objetivos, pesos, mínimos e indicadores como contexto herdado; não os redefine |
| 04 — Arquitetura de Mídia | principal estrutura de entrada |
| 05 — Simulações | contrato funcional principal |
| 06 — Comparação de Cenários | fornece requisitos de comparabilidade e indicadores solicitados |
| 07 — Otimização | recebe variações delimitadas; não conduz a busca |
| 08 — Plano Consolidado | fornece o cenário aprovado somente como referência |
| 09 — Validação e aprovação | estados e bloqueios de governança |
| 10 — Mapa de Veiculação | pode fornecer linhas operacionais para recalcular custos e distribuição |
| 11 — Perfis e permissões | autoriza execução e alteração de parâmetros |

### 5.3 Bibliotecas consumidas

| Biblioteca | Uso principal |
|---|---|
| 12 e 12A | contratos, snapshots, proveniência, versionamento e localização correta dos dados |
| 13 — Inventários | produtos, ofertas, unidades, disponibilidade, preços, audiência, entrega e condições comerciais |
| 14 — Públicos | universos, segmentos, territórios e bases de cálculo |
| 15 — Objetivos, Resultados e KPIs | definição e metadados dos indicadores requeridos |
| 16 — Jornadas e Pontos de Contato | contexto condicional para decomposição de resultados |
| 17 — Conhecimento Técnico | fórmulas, regras, variantes, arredondamentos, equivalências e validade |
| 17C | universo, audiência e impactos |
| 17D | alcance, frequência, acumulação e deduplicação |
| 17E | GRP, TRP, pressão e equivalências multimídia |
| 17F | contrato mínimo de mensuração |
| 18 — Problemas Técnicos | gatilhos e problemas acionáveis |
| 18A | primeiro núcleo de problemas de cálculo e interpretação |
| 18B | casos de validação por meio e disponibilidade de dados |

Nenhuma fórmula será codificada como regra fixa do motor quando já existir como objeto versionado da Biblioteca 17.

---

## 6. Classificação das entradas

### 6.1 Obrigatórias

Dependem da saída solicitada. Exemplos:

- valor e unidade necessários ao indicador;
- universo para percentual de audiência ou alcance;
- quantidade e preço para investimento;
- arquitetura e componentes para cenário completo;
- período para cálculo temporal;
- definição de conversão para CPA ou ROAS.

### 6.2 Condicionais

Exigidas apenas quando o procedimento correspondente for acionado:

- deduplicação para alcance líquido combinado;
- audiência no target para TRP;
- curva de frequência para saturação detalhada;
- receita para ROAS;
- modelo de atribuição para contribuição financeira;
- praça e cobertura para distribuição territorial;
- lote mínimo e indivisibilidade para arredondamento comercial.

### 6.3 Opcionais

Aprimoram precisão ou explicação:

- benchmark;
- intervalo de confiança;
- distribuição de audiência por faixa;
- sazonalidade histórica;
- volatilidade de preço;
- sensibilidade de taxas.

### 6.4 Herdadas

Podem vir do contrato estratégico, da arquitetura, do cenário, do snapshot ou de resultado anterior.

### 6.5 Padrões configuráveis

Só podem ser aplicados quando:

- houver objeto versionado;
- o uso for permitido para o caso;
- a origem for registrada;
- a confiança for ajustada adequadamente.

### 6.6 Não pertinentes

Campos sem efeito no cálculo solicitado não devem ser carregados.

---

## 7. Processo interno canônico

```text
receber comando
→ identificar o objeto a simular
→ resolver somente o contexto necessário
→ identificar problemas técnicos aplicáveis
→ verificar dados e unidades
→ selecionar conhecimentos e procedimentos
→ ordenar dependências de cálculo
→ executar procedimentos nativos
→ executar equivalências autorizadas
→ compor resultados por componente
→ agregar somente resultados compatíveis
→ aplicar validações, confiança e alertas
→ registrar rastreabilidade
→ declarar dependências e invalidações
```

A execução deve ser orientada por grafo de dependências, não por uma sequência fixa que calcule tudo em todos os casos.

---

## 8. Famílias de procedimentos internos

As famílias abaixo não constituem motores autônomos.

### 8.1 Universo, audiência e impactos

Inclui:

- validação de universo;
- audiência absoluta e percentual;
- audiência no target;
- impactos brutos;
- impactos por compra;
- afinidade e índices relacionados, quando definidos.

### 8.2 Alcance, cobertura e frequência

Inclui:

- alcance por componente;
- acumulação;
- deduplicação;
- frequência média;
- frequência por período;
- alcance incremental;
- estados de alcance bruto, líquido, estimado ou não disponível.

### 8.3 Pressão, GRP e TRP

Inclui:

- GRP e TRP;
- pressão por período;
- curvas de pressão;
- intensidade e concentração temporal;
- equivalências permitidas e suas ressalvas.

### 8.4 Economia e condições comerciais

Inclui:

- preço de tabela;
- preço negociado;
- desconto;
- bonificação;
- investimento bruto;
- investimento líquido;
- comissão;
- fee e taxas;
- custo de operação;
- custos não midiáticos;
- custo total;
- saldos e excedentes.

A regra padrão de comissão 80/20 permanece parametrizável e não deve ser presumida quando houver contrato específico.

### 8.5 Eficiência

Inclui, quando válidos:

- CPM;
- CPP;
- CPC;
- CPA;
- custo por alcance;
- custo por alcance incremental;
- eficiência marginal.

### 8.6 Performance e retorno

Inclui:

- impressões;
- cliques;
- CTR;
- conversões;
- taxa de conversão;
- receita;
- CPA;
- ROAS;
- contribuição atribuída.

A fórmula e a definição efetiva de cada indicador devem vir da Biblioteca 17 e do contrato do projeto.

### 8.7 Temporalidade e flight

Inclui:

- distribuição por dia, semana, mês, fase ou faixa;
- continuidade;
- concentração;
- ondas;
- pulsação;
- intervalos;
- pressão acumulada;
- presença em datas críticas.

### 8.8 Overlap e deduplicação

O motor deve distinguir:

```text
sobreposicao informada
sobreposicao estimada
sobreposicao modelada
sobreposicao observada
sobreposicao indisponivel
```

Sem base válida, o motor poderá apresentar cenários brutos ou intervalos, mas não um alcance líquido certificado.

### 8.9 Saturação e rendimento marginal

A saturação deve consumir, quando possível, a distribuição temporal e a curva de frequência, não apenas uma média agregada.

O motor deverá preservar:

- curva utilizada;
- limiar ou faixa;
- procedimento;
- valor marginal;
- confiança;
- restrições.

---

## 9. Métricas nativas e equivalentes

Cada meio mantém suas métricas nativas.

Equivalências serão produzidas apenas quando:

- houver objeto de conhecimento aplicável;
- as unidades forem compatíveis ou transformáveis;
- o universo estiver identificado;
- o estado de equivalência for declarado;
- a confiança for suficiente para o uso solicitado.

Toda saída equivalente deverá conservar simultaneamente:

```text
valor nativo
unidade nativa
valor equivalente
unidade equivalente
procedimento de conversao
versao
restricoes
confianca
```

O valor equivalente não apaga nem substitui o valor nativo.

---

## 10. Contrato mínimo de mensuração

Toda saída mensurável deverá declarar, conforme o documento 17F:

```text
unidade_de_observacao
universo_de_referencia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

Também deverá registrar, quando pertinente:

- período de referência;
- praça;
- público;
- fonte;
- metodologia;
- versão;
- precisão e arredondamento;
- tratamento de ausência.

Resultado sem contrato mínimo suficiente não poderá ser promovido a comparável, consolidado ou definitivo.

---

## 11. Validações locais

O motor deve validar, conforme o caso:

- identidade de universo;
- compatibilidade de unidades;
- validade temporal dos dados;
- validade de preço e disponibilidade;
- coerência entre quantidade e unidade comercial;
- lote mínimo e indivisibilidade;
- consistência de audiência e impactos;
- possibilidade de deduplicação;
- comparabilidade das métricas;
- definição de conversão e receita;
- integridade das fórmulas;
- limites orçamentários;
- coerência territorial e temporal;
- ausência, zero e valor não aplicável.

Uma falha de dado deve produzir alerta, ressalva, resultado parcial ou estado não executável, conforme o impacto real.

---

## 12. Níveis de execução

### 12.1 `PREVIA`

Usada para triagem e decisão rápida.

Pode incluir:

- custos básicos;
- volume comprado;
- impactos ou impressões diretas;
- métricas essenciais;
- estimativas simples;
- alertas de inviabilidade.

Não deve executar automaticamente análises caras de deduplicação, sensibilidade ou distribuição detalhada.

### 12.2 `PADRAO`

Executa os procedimentos necessários para sustentar comparação e decisão na jornada principal.

### 12.3 `DETALHADA`

Pode incluir:

- distribuição de frequência;
- curvas de pressão e saturação;
- sensibilidade de taxas;
- múltiplas hipóteses de overlap;
- variantes metodológicas;
- decomposição temporal e territorial ampliada;
- memória técnica completa.

---

## 13. Estados específicos do resultado

Além dos estados comuns, cada valor poderá receber:

```text
INFORMADO
CALCULADO
ESTIMADO
INFERIDO
AJUSTADO
HERDADO
NAO_DISPONIVEL
NAO_APLICAVEL
INVALIDO
```

Para agregações e comparações, o estado do resultado deve acompanhar o valor.

---

## 14. Confiança

A confiança deve considerar:

- qualidade e atualidade da fonte;
- especificidade do dado;
- validade do universo;
- quantidade de inferências;
- presença de benchmarks;
- estado de deduplicação;
- estado de equivalência;
- sensibilidade às premissas;
- completude das entradas;
- cobertura dos procedimentos aplicados.

A confiança poderá ser registrada por resultado e de forma agregada, sem ocultar o componente mais frágil.

---

## 15. Explicabilidade e rastreabilidade

Cada cálculo deve permitir reconstruir:

```text
comando
→ objeto simulado
→ entradas utilizadas
→ valores substituidos ou herdados
→ problema tecnico
→ conhecimento e procedimento
→ formula ou regra versionada
→ resultados intermediarios
→ resultado final
→ validacoes e alertas
→ confianca
```

A interface deverá mostrar inicialmente a consequência prática. Fórmulas e memória técnica permanecem disponíveis em camadas de aprofundamento.

---

## 16. Reexecução incremental

O motor deverá declarar dependências entre entradas e resultados.

Exemplos:

| Alteração | Reexecução mínima |
|---|---|
| preço ou desconto | custos e indicadores econômicos dependentes |
| quantidade | entregas, custos e indicadores derivados |
| audiência | impactos, alcance, frequência, GRP/TRP e derivados |
| universo | percentuais e métricas normalizadas dependentes |
| overlap | alcance combinado, frequência e indicadores dependentes |
| saturação | rendimento marginal e resultados afetados |
| flight | distribuição temporal, pressão, frequência e custos temporais |
| definição de conversão | CPA, conversões, receita e ROAS dependentes |
| texto ou justificativa | nenhum cálculo |

Mudança localizada não deve invalidar todo o cenário sem necessidade.

---

## 17. Cache e reutilização

Podem ser reutilizados quando as dependências e versões permanecerem válidas:

- cálculos por componente;
- tabelas de audiência;
- preços e condições comerciais versionados;
- conversões de unidade;
- curvas de frequência;
- agregações territoriais;
- resultados intermediários;
- simulações anteriores.

A chave de reutilização deve incluir, conforme o caso:

```text
objeto
versao
procedimento
entradas relevantes
parametros locais
nivel de execucao
```

---

## 18. Controles contra peso excessivo

1. Executar somente indicadores solicitados ou necessários às dependências.
2. Não carregar procedimentos de meios ausentes no cenário.
3. Resolver primeiro custos e validade, evitando cálculos caros de cenários inviáveis.
4. Usar execução prévia antes da detalhada.
5. Reutilizar resultados por componente.
6. Interromper procedimentos que não possam produzir valor válido.
7. Não calcular equivalências sem uso decisório declarado.
8. Limitar análises de sensibilidade, hipóteses de overlap e variantes.
9. Decompor internamente por procedimentos pequenos, sem criar motores por KPI ou meio.
10. Retornar resultados parciais úteis quando o cálculo completo não for possível.

---

## 19. Intervenção humana

O usuário autorizado poderá:

- ajustar parâmetros permitidos;
- substituir fonte ou valor;
- escolher hipótese metodológica disponível;
- solicitar cálculo alternativo;
- aceitar ou rejeitar sugestão técnica;
- comparar valor original e ajustado;
- solicitar maior detalhamento.

Toda intervenção deve preservar o valor anterior, autor, justificativa, escopo e impacto na reexecução.

---

## 20. Estrutura interna recomendada

Sem antecipar classes definitivas, o motor poderá ser composto por:

```text
resolvedor de contexto tecnico
identificador de problemas
seletor de procedimentos
validador de unidades e bases
grafo de dependencias
executor de calculos
agregador de resultados
avaliador de confianca
compositor de explicacao
registrador de rastreabilidade
```

Esses componentes são procedimentos ou serviços internos, não novos motores especialistas.

---

## 21. Casos mínimos de teste

### Caso 1 — Cálculo isolado de CPM

Deve calcular apenas o indicador, registrar investimento, impressões, unidade, fórmula e versão.

### Caso 2 — Cenário apenas digital

Não deve carregar GRP televisivo ou procedimentos incompatíveis.

### Caso 3 — Cenário de TV com audiência válida

Deve produzir impactos, GRP/TRP e demais indicadores aplicáveis, preservando público e universo.

### Caso 4 — Alcance combinado sem deduplicação

Deve evitar alcance líquido certificado e devolver resultado bruto, intervalo ou ressalva.

### Caso 5 — Alteração de preço

Deve recalcular custos e indicadores econômicos, preservando entregas não afetadas.

### Caso 6 — Unidade comercial indivisível

Deve aplicar lote mínimo e arredondamento versionados, sem comprar frações impossíveis.

### Caso 7 — Comissão diferente do padrão

Deve aplicar a configuração específica e preservar a regra substituída.

### Caso 8 — Briefing sem receita

Pode calcular entrega e custos, mas não ROAS; ausência não se transforma em zero.

### Caso 9 — Flight alterado

Deve recalcular distribuição temporal, pressão, frequência e saturação dependentes.

### Caso 10 — Cenário multimídia incomparável

Deve preservar métricas nativas e impedir agregação artificial quando a equivalência não for válida.

### Caso 11 — Resultado parcial

Deve devolver cálculos válidos disponíveis e indicar precisamente quais análises não foram executadas.

### Caso 12 — Validação de cálculo manual

Deve reproduzir entradas, fórmula, arredondamento, resultado e divergência encontrada.

---

## 22. Critérios de aceite

O Motor de Simulação Técnica e Econômica estará apto à implementação quando:

1. seus modos possuírem entradas e saídas inequívocas;
2. os cálculos forem selecionados por problema e dependência;
3. fórmulas e regras permanecerem versionadas na Biblioteca 17;
4. problemas permanecerem na Biblioteca 18;
5. toda saída mensurável cumprir o contrato 17F;
6. ausência, zero e não aplicável forem distinguidos;
7. métricas nativas forem preservadas;
8. equivalências inválidas não forem fabricadas;
9. alterações locais gerarem reexecução seletiva;
10. confiança e rastreabilidade forem reproduzíveis;
11. cálculos por meio ou KPI não exigirem motores próprios;
12. o motor puder produzir resultados prévios, padrão e detalhados sem carregar todos os procedimentos.

---

## 23. Relação final entre os três motores

```text
Motor de Tradução Estratégica
→ define o que deve ser priorizado

Motor de Decisão de Arquitetura e Cenários
→ define quais configurações devem ser consideradas, comparadas ou ajustadas

Motor de Simulação Técnica e Econômica
→ calcula o que cada configuração entrega, custa e exige
```

O Motor de Decisão pode solicitar várias simulações, mas a camada de aplicação controla o ciclo, os limites e a persistência.

---

## 24. Princípio consolidado

> O Motor de Simulação Técnica e Econômica é um executor especialista de consequências mensuráveis, não um planejador autônomo. Ele reúne cálculos de audiência, alcance, frequência, pressão, custos, temporalidade, performance, overlap e saturação sob uma única fronteira técnica, mas carrega apenas os procedimentos necessários a cada caso. A economia de motores é preservada sem criar um componente monolítico, porque fórmulas, problemas, dados e procedimentos permanecem modularizados, versionados e acionados sob demanda.