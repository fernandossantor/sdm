# Auditoria de aderência do planejador — 2 de agosto de 2026

## Objetivo

Esta auditoria confronta o prompt operacional, os documentos normativos, os
motores, as telas, as bibliotecas e o código efetivamente executado pelo novo
MediAd Planner. O critério central é verificar se o produto já opera como um
planejador interdependente ou apenas como uma sequência de cadastros.

## Parecer executivo

O prompt vigente e a arquitetura documental estão coerentes. A implementação,
porém, ainda não materializa a cadeia decisória descrita nos documentos 23–30.
Campanha e Briefing possuem domínio, persistência, estados e versionamento
reais. A Tradução Estratégica possui um primeiro contrato persistido, mas ainda
é uma derivação parcial e paralela à fachada comum dos motores.

O sistema atual deve ser classificado como **fundação transacional com primeira
derivação estratégica parcial**, e não como planejador de mídia funcional.

O principal desvio não é falta de telas. É falta de conexão executável entre:

```text
Briefing versionado
→ Bibliotecas 14–18 versionadas
→ problemas e procedimentos selecionados
→ Motor de Tradução Estratégica
→ contrato comum com dependências
→ Motor de Decisão
→ Motor de Simulação
→ retorno quantitativo ao Motor de Decisão
```

## 1. Prompt e precedência documental

### Situação

O prompt de retomada do documento 31 está correto ao exigir:

- uso exclusivo de `docs/new_app` como contrato funcional;
- precedência do documento 30;
- domínio independente de Streamlit e Supabase;
- incrementos verificáveis;
- proibição de inventar regras ausentes;
- criação e edição visíveis com rastreabilidade e versionamento.

### Desvio encontrado

A execução recente respeitou estados e persistência, mas não respeitou
integralmente a separação entre apresentação, motor e biblioteca. Indicadores e
tensões foram compostos na tela, e relações Comunicação–Mídia foram codificadas
como mapa estático no domínio. O problema está na aderência da implementação,
não na instrução do prompt.

### Decisão

O prompt não precisa ser reescrito. Os próximos incrementos devem adicionar um
gate explícito: nenhuma regra metodológica pode nascer em `presentation/`, em
casos de uso ou em mapas sem referência a objeto versionado das Bibliotecas
15, 17 ou 18.

## 2. Fluxo funcional e telas

| Etapa | Estado real | Aderência |
|---|---|---|
| Campanha | criação, correção, autoria, snapshot e persistência | adequada para o incremento |
| Briefing | conteúdo estruturado, edição, conclusão e versões | parcial; valida presença, ainda não mensurabilidade ou coerência profunda |
| Tradução Estratégica | contrato persistido e revisão versionada de objetivos | parcial; não executa o processo canônico completo |
| Arquitetura de Mídia | não existe no novo fluxo | não implementada |
| Simulações | não existem no novo fluxo | não implementadas |
| Comparação e otimização | não existem no novo fluxo | não implementadas |
| Plano consolidado e etapas posteriores | não existem no novo fluxo | não implementadas |

### Correções imediatas realizadas nesta auditoria

- período do Briefing alterado de texto livre para campos de data;
- domínio passou a rejeitar datas inválidas e período invertido;
- removido bloqueio circular do botão `Concluir briefing`: o reconhecimento de
  alertas agora pode ser enviado pelo formulário e continua validado pelo caso
  de uso.

### Problemas remanescentes nas telas

1. A tela de Tradução mistura apresentação com regras de indicador e tensão.
2. A maior parte do Perfil Estratégico exibido é leitura estruturada do
   Briefing, não resultado persistido do motor.
3. Não há visualização de relações Marketing–Comunicação com força, condição,
   confiança, peso ou origem versionada.
4. Não há perguntas priorizadas nem fluxo de complementação seletiva.
5. Não há navegação para Arquitetura porque o contrato estratégico ainda não é
   consumível pelo motor seguinte.

## 3. Motores especialistas

### Contrato comum

O pacote `domain/contracts` implementa envelopes, valores tipados, validações,
alertas, rastreabilidade, dependências e políticas de reexecução. É uma fundação
válida e alinhada ao documento 25.

### Motor de Tradução Estratégica

Existem hoje duas implementações desconectadas:

1. `engines/traducao_estrategica/facade.py`, declaradamente falsa, que usa o
   contrato comum e informa que não executa procedimentos;
2. `domain/traducao/models.py`, usado pelo fluxo real, que deriva alguns
   objetivos por mapa estático e não produz `SaidaMotor`.

Essa duplicidade é crítica. O fluxo funcional contorna justamente a arquitetura
criada para resolver contexto, selecionar problemas, consultar conhecimento,
explicar resultados e declarar dependências.

Faltam no motor ativo:

- resolução seletiva do contexto;
- identificação de problemas da Biblioteca 18;
- seleção de procedimentos da Biblioteca 17;
- operacionalização mensurável dos objetivos;
- matriz Marketing–Comunicação;
- pontuação contextual e ordenação fundamentada;
- resultados, KPIs, intensidades, pesos e mínimos;
- tensões como objetos estruturados;
- confiança numérica e explicável;
- perguntas priorizadas;
- dependências e política de reexecução;
- envelope especializado compatível com o Motor de Decisão.

### Motores de Decisão e Simulação

Não há implementação nova dos motores definidos nos documentos 27 e 28. Os
módulos em `engine/` e serviços associados pertencem ao legado arquivado. Eles
podem conter funções reaproveitáveis depois de revisão, mas não estão ligados ao
novo domínio e não podem ser tratados como os motores vigentes.

## 4. Bibliotecas 13–18

| Biblioteca | Evidência atual | Uso no novo fluxo |
|---|---|---|
| 13 — inventários e custos | tabelas e repositórios legados | nenhum |
| 14 — públicos e segmentos | tabelas legadas e campos do Briefing | não consultada como biblioteca versionada |
| 15 — objetivos, resultados e KPIs | catálogos legados de objetivos/KPIs | não consultada; listas e indicadores estão no código da tela |
| 16 — jornadas e funções | tabelas legadas e lista fixa na tela | não consultada pelo motor |
| 17 — conhecimento técnico | contrato documental e catálogo métrico legado parcial | nenhum objeto versionado consumido pela Tradução |
| 18 — problemas técnicos | especificação documental | nenhum catálogo ou identificador consumido |

### Conclusão sobre as bibliotecas

As bibliotecas existem majoritariamente como documentação ou estruturas do
legado. Não há provedores tipados para o novo aplicativo nem referências de
versão no contrato estratégico efetivamente usado. O mapa
`MAPA_COMUNICACAO_MIDIA` e o dicionário de indicadores na apresentação são
atalhos provisórios que devem ser substituídos por consultas versionadas.

## 5. Relações e interdependências

### O que já existe

- Campanha referencia Briefing;
- Tradução referencia Campanha, Briefing e versão do Briefing;
- revisão humana preserva a derivação anterior e cria nova versão;
- alterações são persistidas com autoria e instante.

### O que ainda não existe

- grafo de dependências por objetivo, público, praça, jornada, KPI e restrição;
- invalidação seletiva quando um fator muda;
- relações N:N Marketing–Comunicação e Comunicação–Mídia;
- vínculo de cada relação a regra, problema, procedimento e versão;
- propagação de prioridades, pesos, mínimos e restrições para Arquitetura;
- solicitação seletiva de cálculos ao Motor de Simulação;
- retorno de alcance, frequência, custo e confiança ao Motor de Decisão;
- explicação de trade-offs e decisão humana final.

Sem esses vínculos, a experiência continua próxima de formulários sequenciais,
mesmo quando a tela apresenta informações relacionadas.

## 6. Riscos técnicos prioritários

### P0 — bloqueiam a identidade do produto

1. Fluxo ativo contorna o contrato comum dos motores.
2. Regras metodológicas estão hardcoded fora das bibliotecas.
3. Perfil Estratégico exibido não corresponde integralmente ao artefato
   persistido.
4. Não há saída consumível pelo Motor de Decisão.

### P1 — comprometem explicabilidade e manutenção

1. Objetos do Briefing usam dicionários sem identidade e referência
   versionada às taxonomias.
2. Confiança é apenas ordinal e baseada quase exclusivamente na presença de
   fontes.
3. Completude do Briefing valida presença, não mensurabilidade e coerência.
4. Não existe grafo de dependências ou recálculo seletivo.
5. Código legado de motores permanece testado, mas não representa o novo fluxo.

### P2 — evolução funcional

1. Motor de Decisão ainda ausente.
2. Motor de Simulação ainda ausente.
3. Arquitetura, cenários, comparação, otimização e plano consolidado ausentes.

## 7. Sequência obrigatória de correção

### Incremento A — integrar Tradução ao contrato comum

1. substituir a fachada falsa por um motor real em modo
   `TRADUZIR_BRIEFING`;
2. fazer o caso de uso enviar `ComandoMotor` e persistir a `SaidaMotor`;
3. mover toda regra da apresentação para procedimentos do motor;
4. unificar os dois contratos e os dois enums estratégicos;
5. declarar dependências e política de reexecução.

### Incremento B — núcleo mínimo das Bibliotecas 15, 17 e 18

1. modelar objetivos, relações, resultados, KPIs, conhecimentos, problemas e
   procedimentos com código e versão;
2. criar portas de consulta independentes de Supabase;
3. semear somente as regras necessárias aos casos mínimos do documento 26;
4. substituir listas e mapas hardcoded por referências consultadas;
5. testar ausência, incompatibilidade e confiança.

### Incremento C — Perfil Estratégico realmente interdependente

1. operacionalizar objetivos;
2. produzir matrizes Marketing–Comunicação e Comunicação–Mídia;
3. gerar prioridades, intensidades, pesos, mínimos e restrições;
4. identificar tensões e perguntas priorizadas;
5. persistir valores calculados, ajustados e efetivos;
6. recalcular somente objetos dependentes após intervenção.

### Incremento D — cadeia decisória posterior

Somente após o contrato estratégico ser consumível:

1. implementar `GERAR_ARQUITETURAS` no Motor de Decisão;
2. consultar Bibliotecas 13, 14, 16, 17 e 18 seletivamente;
3. implementar o núcleo mínimo do Motor de Simulação;
4. fechar o ciclo Decisão → Simulação → Decisão;
5. liberar comparação e otimização como modos do Motor de Decisão.

## 8. Critério de aceite para chamar o produto de planejador

Um teste ponta a ponta deve demonstrar que a alteração de pelo menos um fator
do Briefing — objetivo, público, praça, jornada, período, verba ou restrição —:

1. invalida apenas dependências afetadas;
2. altera relações ou prioridades explicavelmente;
3. gera nova versão do Perfil Estratégico;
4. altera candidaturas ou critérios da Arquitetura;
5. solicita somente os cálculos técnicos pertinentes;
6. preserva valores anteriores e intervenção humana;
7. apresenta origem, regra, versão, confiança e trade-off ao planejador.

Até esse teste existir e passar, cada entrega deve declarar explicitamente seu
caráter parcial.

## 9. Próximo ponto de implementação

O próximo incremento não deve criar outra tela. Deve integrar o modo
`TRADUZIR_BRIEFING` ao contrato comum e introduzir o primeiro núcleo versionado
das Bibliotecas 15, 17 e 18, removendo regras estratégicas da apresentação.
