# Motor de Tradução Estratégica

**Documento:** `26_MOTOR_DE_TRADUCAO_ESTRATEGICA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Especificação consolidada para a versão 1.0  
**Natureza:** Contrato funcional e decisório do primeiro motor especialista  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

O Motor de Tradução Estratégica transforma o contexto estruturado da campanha em um contrato estratégico utilizável pelos demais motores.

Sua pergunta central é:

> O que o planejamento de mídia deve priorizar, preservar, limitar e mensurar neste contexto?

O motor não escolhe meios, veículos, inventários ou ofertas comerciais. Também não calcula a entrega final do plano. Sua responsabilidade é converter objetivos, públicos, jornadas, restrições, prioridades e condições do briefing em uma estrutura estratégica explícita, ponderada, revisável e rastreável.

```text
Objeto Contextual Estruturado
        ↓
Motor de Tradução Estratégica
        ↓
Contrato Estratégico do Planejamento
        ↓
Motor de Decisão de Arquitetura e Cenários
```

---

## 2. Posição arquitetural

O Motor de Tradução Estratégica é o primeiro dos três motores especialistas da versão 1.0:

1. Motor de Tradução Estratégica;
2. Motor de Decisão de Arquitetura e Cenários;
3. Motor de Simulação Técnica e Econômica.

Ele implementa o contrato comum definido no documento 25 e utiliza seletivamente os campos e objetos dos documentos 01 a 18B.

O motor é autônomo porque:

- possui decisão própria;
- recebe entradas próprias;
- produz saída reutilizável;
- pode ser reexecutado sem obrigar a simulação completa;
- possui validações e estados próprios;
- altera a orientação dos motores posteriores.

---

## 3. Responsabilidade exclusiva

Compete ao motor:

- avaliar a suficiência estratégica do briefing;
- classificar objetivos declarados;
- operacionalizar objetivos de Marketing e Comunicação;
- estabelecer relações Marketing–Comunicação;
- derivar objetivos de Mídia;
- estabelecer relações Comunicação–Mídia;
- associar resultados pretendidos e KPIs;
- priorizar públicos, segmentos, praças, jornadas e etapas;
- converter prioridades em intensidades, pesos, mínimos e restrições;
- identificar compatibilidades, tensões, conflitos e lacunas;
- produzir condições estratégicas para a arquitetura de mídia;
- registrar confiança e rastreabilidade de cada derivação;
- permitir ajustes humanos autorizados sem apagar a origem automática.

Não compete ao motor:

- selecionar inventários finais;
- escolher veículos ou plataformas específicos;
- determinar preços ou condições comerciais;
- distribuir definitivamente a verba;
- definir inserções, impressões, faces ou ocorrências finais;
- calcular alcance, frequência, GRP, CPM, CPA, ROAS ou investimento final;
- comparar cenários simulados;
- otimizar configurações de mídia;
- aprovar o plano;
- gerar o mapa de veiculação ou o documento final.

---

## 4. Resultado principal

O resultado principal do motor será:

```text
contrato_estrategico_do_planejamento
```

O contrato estratégico corresponde operacionalmente ao Perfil Estratégico de Mídia definido no documento 03, apresentado em formato consumível pelos motores posteriores.

Ele deverá conter, no mínimo:

```text
contrato_estrategico_do_planejamento
├── identidade_e_versao
├── estado_estrategico
├── objetivos_de_marketing
├── objetivos_de_comunicacao
├── objetivos_de_midia_derivados
├── relacoes_marketing_comunicacao
├── relacoes_comunicacao_midia
├── resultados_pretendidos
├── kpis_priorizados
├── publicos_e_segmentos_priorizados
├── pracas_e_universos_priorizados
├── jornadas_etapas_necessidades_e_funcoes
├── intensidades
├── pesos
├── minimos_obrigatorios
├── restricoes
├── tensoes_e_compensacoes
├── criterios_para_arquitetura
├── lacunas_e_perguntas_priorizadas
├── confianca
├── intervencoes_humanas
├── rastreabilidade
└── politica_de_reexecucao
```

---

## 5. Modos de execução

A versão 1.0 terá poucos modos, todos relacionados à mesma responsabilidade decisória.

### 5.1 `TRADUZIR_BRIEFING`

Executa a tradução completa do contexto disponível e produz uma nova versão do contrato estratégico.

Uso principal:

- primeira tradução de uma campanha;
- reconstrução após alteração relevante de objetivo, público, praça ou restrição;
- geração do contrato inicial para o Motor de Decisão.

### 5.2 `REVISAR_TRADUCAO`

Reavalia uma tradução existente após intervenção humana, complementação de dados ou alteração localizada.

Deve preservar:

- versão anterior;
- valores automáticos originais;
- ajustes humanos;
- justificativas;
- diferenças entre versões.

### 5.3 `VALIDAR_SUFICIENCIA_ESTRATEGICA`

Verifica se o contexto disponível é suficiente para produzir contrato definitivo, provisório, parcial ou insuficiente.

Esse modo não constitui Motor de Validação separado. É uma operação do próprio motor sobre suas entradas.

### 5.4 `RECALCULAR_DEPENDENCIAS_ESTRATEGICAS`

Recalcula apenas relações, pesos, prioridades e objetos afetados por uma alteração identificada.

Exemplos:

```text
mudou um KPI secundário
→ recalcular vínculos e pesos dependentes
→ preservar públicos e objetivos não afetados

mudou o público prioritário
→ recalcular compatibilidades, relações e prioridades dependentes

mudou apenas uma observação textual
→ não recalcular o contrato
```

Não serão criados modos separados para cada matriz, objetivo ou tipo de público. Essas operações permanecem procedimentos internos.

---

## 6. Envelope de comando

O motor recebe o envelope comum do documento 25, com:

```text
id_comando
motor_destino = TRADUCAO_ESTRATEGICA
modo_execucao
nivel_execucao
id_campanha
id_snapshot_campanha
id_usuario
perfil_de_acesso
origem_do_comando
objetivo_da_execucao
referencias_de_entrada
parametros_locais
limites_de_execucao
```

Referências de entrada possíveis:

- snapshot da campanha;
- Objeto Contextual Estruturado do Briefing;
- versão anterior do contrato estratégico;
- ajustes humanos autorizados;
- objetos selecionados das Bibliotecas 14, 15 e 16;
- conhecimentos versionados da Biblioteca 17;
- problemas aplicáveis da Biblioteca 18.

O comando não deve transportar indiscriminadamente todos os cadastros e bibliotecas.

---

## 7. Consumo dos documentos 01 a 11

| Documento | Consumo | Uso pelo motor |
|---|---|---|
| 01 — Campanha | condicionado | identidade, anunciante, marca, produto, vigência e contexto geral |
| 02 — Briefing | principal | objetivos, situação, públicos, praça, período, verba, restrições, concorrência e prioridades |
| 03 — Tradução Estratégica | principal | campos, relações, estados, escalas, matrizes e estrutura do resultado |
| 04 — Arquitetura de Mídia | condicionado | somente requisitos que precisam ser preparados para o motor posterior; não seleciona arquitetura |
| 05 — Simulações | não pertinente na primeira tradução | resultados anteriores podem ser referência em revisão, sem redefinir a estratégia automaticamente |
| 06 — Comparação | condicionado | critérios estratégicos que deverão orientar comparação posterior |
| 07 — Otimização | condicionado | prioridades preserváveis, mínimos e restrições que limitarão ajustes futuros |
| 08 — Plano Consolidado | herdado em revisão | decisões aprovadas anteriores podem ser preservadas ou marcadas para reavaliação |
| 09 — Validação e aprovação | condicionado | estados de aprovação, bloqueios e ressalvas; não produz aprovação |
| 10 — Mapa de Veiculação | não pertinente | não é entrada da tradução inicial |
| 11 — Perfis e permissões | condicionado | autoriza execução, revisão e alteração manual de parâmetros |

---

## 8. Consumo das Bibliotecas 12 a 18B

| Biblioteca | Consumo | Uso pelo motor |
|---|---|---|
| 12 — Sistema de Bibliotecas | principal | contratos de acesso, versões, snapshots, relações e proveniência |
| 12A — Consolidação Operacional | condicionado | localização correta de regras e objetos, sem bibliotecas paralelas |
| 13 — Inventários | geralmente não pertinente | apenas categorias abstratas ou restrições declaradas; não consulta ofertas para traduzir objetivos |
| 14 — Públicos e Segmentos | principal | universos, segmentos, públicos, territórios, comportamentos e prioridades |
| 15 — Objetivos, Resultados e KPIs | principal | taxonomias, relações padrão, indicadores, compatibilidades e metas |
| 16 — Jornadas, Necessidades, Funções e Pontos de Contato | principal | etapas, necessidades, funções e relações estratégicas |
| 17 — Conhecimento Técnico | principal e seletivo | regras de operacionalização, pontuação, normalização, composição e interpretação |
| 17A — Inventário Preliminar | condicionado | verifica disponibilidade e lacunas do conhecimento |
| 17B — Protocolo de Formalização | principal | valida a estrutura e a versão dos conhecimentos consultados |
| 17C–17E | condicionado | conceitos de mensuração necessários para formular objetivos e KPIs, sem executar a simulação final |
| 17F — Contrato Mínimo de Mensuração | principal | qualifica todos os valores e metas mensuráveis do contrato |
| 18 — Problemas Técnicos | principal | identifica problemas estratégicos e de operacionalização aplicáveis |
| 18A–18B | condicionado | utiliza casos de validação pertinentes; problemas estritamente de cálculo permanecem para a simulação |

---

## 9. Entradas por grupo

### 9.1 Obrigatórias para `TRADUZIR_BRIEFING`

O conjunto mínimo dependerá do objetivo da execução, mas deverá incluir:

- identidade da campanha e snapshot;
- ao menos um objetivo declarado ou problema estratégico explícito;
- objeto, marca, produto ou serviço a que a campanha se refere;
- público ou universo mínimo de referência;
- praça ou escopo territorial;
- período ou horizonte temporal;
- restrições declaradas relevantes;
- origem e versão das informações.

A verba pode ser:

- obrigatória quando a viabilidade orçamentária altera a priorização;
- condicional em tradução preliminar;
- ausente com ressalva quando ainda não houver definição.

### 9.2 Condicionais

- linha de base;
- metas numéricas;
- concorrência;
- pressão competitiva;
- estágio do produto ou marca;
- maturidade do mercado;
- ciclo de compra;
- jornada;
- restrições legais ou institucionais;
- metas por público ou praça;
- KPI já solicitado pelo usuário;
- pretensões de meio declaradas no briefing.

Pretensões de meio não serão tratadas automaticamente como solução. Serão registradas como preferência, restrição, hipótese ou imposição conforme a justificativa.

### 9.3 Opcionais

- pesquisas anteriores;
- benchmarks;
- dados históricos;
- aprendizados de campanhas anteriores;
- notas qualitativas estruturadas;
- preferências não vinculantes;
- proxies sugeridos.

### 9.4 Herdadas

- objetos mestres selecionados e seus snapshots;
- taxonomias das Bibliotecas 14 a 16;
- parâmetros institucionais;
- versão anterior do contrato;
- relações padrão;
- metadados de mensuração.

### 9.5 Não pertinentes

Na tradução inicial, não devem ser carregados:

- listas completas de ofertas comerciais;
- preços detalhados de inventários;
- grades de programação;
- quantidades finais de inserções;
- resultados de alcance e frequência ainda inexistentes;
- relatórios documentais finais.

---

## 10. Problemas acionáveis

O motor identifica apenas problemas de sua responsabilidade, vinculados à Biblioteca 18.

Famílias iniciais:

### 10.1 Objetivo não operacionalizado

Gatilhos possíveis:

- objetivo genérico;
- ausência de objeto da mudança;
- ausência de público, direção ou horizonte;
- falta de indicador ou condição verificável;
- mistura entre objetivo e solução de mídia.

### 10.2 Objetivos conflitantes ou concorrentes

Gatilhos possíveis:

- prioridades incompatíveis;
- metas disputando a mesma verba;
- exigências simultâneas de alcance amplo e alta frequência com recursos insuficientes;
- públicos ou praças em competição sem regra de prioridade.

### 10.3 Relação estratégica indeterminada

Gatilhos possíveis:

- objetivo de Marketing sem objetivo de Comunicação compatível;
- objetivo de Comunicação sem objetivo de Mídia derivável;
- força contextual insuficiente;
- ausência de conhecimento formalizado para o caso.

### 10.4 Público, praça ou jornada insuficientemente definidos

Gatilhos possíveis:

- público excessivamente amplo;
- segmentos sobrepostos sem prioridade;
- praça incompatível com universo informado;
- etapa da jornada inexistente ou contraditória.

### 10.5 KPI inadequado ou incomparável

Gatilhos possíveis:

- KPI sem vínculo com o objetivo;
- unidade incompatível;
- mistura de resultado de mídia com resultado de negócio sem mediação;
- ausência de linha de base quando necessária;
- meta sem universo de referência.

### 10.6 Restrições impeditivas ou subespecificadas

Gatilhos possíveis:

- prazo incompatível com o resultado pretendido;
- verba sem ordem de grandeza suficiente para o escopo declarado;
- restrição que elimina todas as alternativas;
- pretensão de meio tratada como obrigação sem justificativa.

O motor não cria novos códigos de problema em sua implementação. Ele referencia os códigos versionados da Biblioteca 18.

---

## 11. Processo interno canônico

```text
1. resolver contexto
2. validar suficiência mínima
3. identificar problemas estratégicos
4. classificar objetivos declarados
5. operacionalizar objetivos válidos
6. construir relações Marketing–Comunicação
7. pontuar e ordenar relações
8. derivar objetivos de Mídia
9. construir relações Comunicação–Mídia
10. associar resultados e KPIs
11. priorizar públicos, praças, jornadas e funções
12. calcular intensidades, pesos e mínimos
13. identificar tensões, restrições e compensações
14. compor critérios para arquitetura
15. calcular confiança
16. registrar perguntas e lacunas
17. compor contrato estratégico
18. declarar dependências e política de reexecução
```

As etapas internas poderão ser executadas por procedimentos pequenos e substituíveis. Não devem ser implementadas como um único bloco rígido.

---

## 12. Classificação e operacionalização dos objetivos

Cada objetivo declarado deverá registrar:

```text
id_objetivo
categoria
origem
texto_original
objeto_da_mudanca
publico
praca
direcao
indicador
unidade_ou_escala
linha_de_base
meta_ou_intensidade
horizonte_temporal
fonte
estado_de_operacionalizacao
confianca
```

Estados:

```text
OPERACIONALIZADO
OPERACIONALIZAVEL_COM_DADOS_PENDENTES
OPERACIONALIZAVEL_POR_PROXY
QUALITATIVO_ESTRUTURADO
NAO_OPERACIONALIZADO
```

Regras:

- objetivos não operacionalizados permanecem como alerta ou pendência;
- não entram em pontuações como se fossem válidos;
- objetivos qualitativos exigem escala, proxy, índice ou condição verificável;
- a solução de mídia não deve substituir a formulação do objetivo;
- objetivos informados pelo usuário não são apagados quando o sistema propõe reformulação.

---

## 13. Relações Marketing–Comunicação

As relações são N:N e deverão admitir os tipos definidos no documento 03:

```text
CONTRIBUI_PARA
SUSTENTA
POTENCIALIZA
HABILITA
COMPLEMENTA
ANTECEDE
DEPENDE_DE
COMPENSA
DISPUTA_RECURSO_COM
PODE_CONFLITAR_COM
INCOMPATIVEL_NO_CONTEXTO
```

Cada relação registra:

```text
objetivo_origem
objetivo_destino
tipo_de_relacao
direcao
forca_padrao
forca_contextual
pontuacao_efetiva
ordem
condicao
confianca
justificativa
restricoes
```

Direções:

```text
POSITIVA
NEGATIVA
NEUTRA
CONDICIONAL
```

Condições:

```text
ESSENCIAL
PRIORITARIA
COMPLEMENTAR
OPCIONAL
COMPENSAVEL
CONFLITANTE
EXCLUDENTE
```

Relações excludentes funcionam como filtro, não como simples peso negativo.

---

## 14. Derivação dos objetivos de Mídia

Objetivos de Mídia serão derivados, não aceitos automaticamente como solução declarada no briefing.

A derivação considerará:

- objetivos de Comunicação priorizados;
- resultados pretendidos;
- públicos e praças;
- jornada e etapa;
- horizonte temporal;
- verba e restrições;
- pressão competitiva;
- indicadores requeridos;
- tensões entre objetivos;
- confiança das entradas.

Cada objetivo derivado deverá conter:

```text
id_objetivo_midia
origens_de_comunicacao
resultado_pretendido
pontuacao_contextual
ordem
intensidade_requerida
prioridade
peso
condicao
indicadores_relacionados
restricoes
confianca
rastreabilidade
```

O motor poderá derivar objetivos como:

- construir alcance;
- ampliar cobertura;
- acelerar construção de alcance;
- gerar frequência;
- sustentar continuidade;
- concentrar pressão;
- ampliar presença territorial;
- produzir impacto;
- gerar tráfego ou resposta;
- apoiar conversão mensurável.

A lista oficial e suas relações pertencem à Biblioteca 15.

---

## 15. Pontuação contextual

A pontuação contextual coordena conhecimentos versionados da Biblioteca 17.

Estrutura conceitual:

```text
forca_padrao
× prioridade_da_origem
× compatibilidade_com_publico
× compatibilidade_territorial
× compatibilidade_com_jornada
× compatibilidade_temporal
× viabilidade_orcamentaria
× confianca
± tensoes_e_restricoes
= pontuacao_contextual
```

A fórmula definitiva, normalização, coeficientes e tolerâncias não ficam codificados no motor. O motor deve:

- selecionar o objeto de conhecimento aplicável;
- fornecer as entradas;
- executar o procedimento;
- preservar os componentes utilizados;
- registrar a versão;
- rejeitar métodos incompatíveis;
- explicar o resultado.

A escala de força relacional será de 0 a 100, conforme o documento 03, mas a interpretação do valor deve preservar a faixa e a confiança.

---

## 16. Propagação e normalização das prioridades

Fluxo básico:

```text
peso do objetivo de Marketing
→ força Marketing–Comunicação
→ prioridade derivada de Comunicação
→ força Comunicação–Mídia
→ prioridade derivada de Mídia
```

Regras:

1. múltiplos caminhos até o mesmo objetivo não podem duplicar a mesma contribuição;
2. relações negativas ou condicionais devem permanecer explícitas;
3. objetivos concorrentes devem ser normalizados dentro da família decisória adequada;
4. mínimos obrigatórios não podem desaparecer por normalização;
5. restrições excludentes não participam como peso compensável;
6. ajustes humanos devem manter o valor calculado original;
7. empates dentro da tolerância não devem gerar falsa precisão ordinal.

---

## 17. Públicos, praças, jornadas e funções

O motor deverá produzir prioridades contextuais para:

- universos;
- públicos;
- segmentos;
- praças;
- etapas da jornada;
- necessidades;
- funções comunicacionais;
- pontos de contato em nível categorial.

Ele não escolhe inventários específicos. Sua saída deve orientar o Motor de Decisão com relações como:

```text
publico prioritario
+ etapa da jornada
+ necessidade
+ funcao comunicacional
+ contexto territorial e temporal
→ criterio de elegibilidade para pontos de contato e categorias de mídia
```

O papel estratégico principal, complementar ou de apoio será atribuído pelo Motor de Decisão, não por este motor.

---

## 18. Intensidades, pesos, mínimos e restrições

### 18.1 Intensidade

Expressa quanto determinado resultado ou objetivo é requerido no contexto.

Pode ser:

- baixa;
- moderada;
- alta;
- crítica;
- escala contínua versionada.

### 18.2 Peso

Expressa a importância relativa dentro de uma família decisória comparável.

O peso não substitui:

- mínimo obrigatório;
- restrição excludente;
- condição essencial;
- sequência temporal necessária.

### 18.3 Mínimos obrigatórios

Devem ser declarados separadamente dos pesos.

Exemplos:

- público que não pode ser excluído;
- praça de presença obrigatória;
- etapa da jornada que precisa ser atendida;
- resultado mínimo exigido;
- KPI cuja mensuração é condição do plano.

### 18.4 Restrições

Classificação mínima:

```text
INFORMATIVA
PREFERENCIAL
CONDICIONAL
RESTRITIVA
EXCLUDENTE
```

O motor registra a restrição estratégica. A verificação operacional final pertence aos motores posteriores conforme o objeto afetado.

---

## 19. Verba no Motor de Tradução

A verba participa apenas como condição estratégica e de viabilidade geral.

O motor pode:

- identificar incompatibilidade entre escopo e ordem de grandeza da verba;
- reduzir confiança de objetivos excessivamente amplos;
- priorizar objetivos, públicos ou praças;
- registrar necessidade de escolha ou faseamento;
- produzir limites estratégicos para o Motor de Decisão.

O motor não pode:

- distribuir valores definitivos entre meios;
- calcular custo de inventário;
- substituir preço ausente por estimativa não declarada;
- otimizar verba;
- produzir investimento final.

---

## 20. Estados do contrato estratégico

Além dos estados comuns da execução, o resultado principal terá:

```text
DEFINITIVO
PROVISORIO
PARCIAL
INSUFICIENTE
SUPERADO
```

### `DEFINITIVO`

Entradas suficientes e relações válidas para orientar a arquitetura no nível solicitado.

### `PROVISORIO`

Há lacunas, mas o contrato pode orientar uma primeira arquitetura com ressalvas.

### `PARCIAL`

Somente parte dos objetivos, públicos ou relações pôde ser traduzida.

### `INSUFICIENTE`

Não há base mínima para produzir orientação estratégica sem fabricar informação.

### `SUPERADO`

Versão anterior preservada apenas para histórico após substituição por nova tradução.

---

## 21. Perguntas priorizadas e ausência de dados

O motor não deve exigir a conclusão integral do briefing antes de produzir qualquer auxílio.

Perguntas serão priorizadas por impacto decisório:

```text
BLOQUEANTE
muda a possibilidade de produzir o contrato

ALTO_IMPACTO
pode alterar objetivos, públicos ou prioridades principais

MEDIO_IMPACTO
altera pesos, ordens ou confiança

BAIXO_IMPACTO
melhora explicação ou precisão sem mudar a decisão central
```

Cada pergunta deverá registrar:

```text
campo_ou_objeto
motivo
impacto
objetos_dependentes
resposta_esperada
alternativa_provisoria
```

Ausência nunca será convertida em zero.

---

## 22. Intervenção humana

O planejador poderá:

- aceitar uma derivação;
- rejeitar uma derivação;
- alterar peso autorizado;
- fixar mínimo;
- incluir restrição;
- escolher entre relações empatadas;
- substituir proxy;
- justificar exceção;
- solicitar nova execução.

Cada intervenção deve registrar:

```text
valor_calculado
valor_ajustado
valor_efetivo
autor
momento
justificativa
escopo
objetos_dependentes
```

O motor nunca deve apagar o valor calculado original nem apresentar ajuste humano como inferência automática.

---

## 23. Confiança

A confiança será composta conforme conhecimentos da Biblioteca 17, considerando:

- completude das entradas;
- qualidade das fontes;
- validade dos objetos relacionados;
- presença de linha de base e meta;
- uso de proxy;
- consistência entre objetivos;
- adequação do conhecimento ao contexto;
- número e severidade das ressalvas;
- intervenção humana não justificada;
- atualidade das versões.

A saída deverá declarar:

```text
nivel_de_confianca
fatores_positivos
fatores_redutores
lacunas
condicoes_para_melhoria
```

O motor não deve produzir precisão numérica aparente quando a base for predominantemente qualitativa.

---

## 24. Explicabilidade

A explicação seguirá camadas.

### Camada 1 — resultado prático

- prioridades principais;
- objetivos de Mídia derivados;
- públicos e praças prioritárias;
- principais restrições;
- confiança geral.

### Camada 2 — justificativa resumida

- por que cada prioridade foi estabelecida;
- principais relações entre objetivos;
- tensões e compensações;
- dados ausentes relevantes.

### Camada 3 — memória técnica

- entradas consumidas;
- problemas identificados;
- conhecimentos e versões;
- procedimentos selecionados;
- componentes da pontuação;
- alternativas rejeitadas;
- intervenções humanas;
- dependências.

Não haverá Motor de Explicação separado.

---

## 25. Envelope de saída especializado

O envelope comum do documento 25 será preenchido com:

```text
motor = TRADUCAO_ESTRATEGICA
modo_execucao
nivel_execucao
estado_execucao
resultado_principal = contrato_estrategico_do_planejamento
resultados_secundarios
validacoes
alertas
restricoes
confianca
explicacao
rastreabilidade
dependencias
reexecucao
```

Resultados secundários possíveis:

- diagnóstico de suficiência;
- objetivos não operacionalizados;
- perguntas priorizadas;
- matriz resumida Marketing–Comunicação;
- matriz resumida Comunicação–Mídia;
- conflitos e tensões;
- diferenças em relação à versão anterior.

---

## 26. Níveis de execução

### 26.1 `PREVIA`

Produz:

- diagnóstico de suficiência;
- classificação inicial dos objetivos;
- prioridades preliminares;
- principais lacunas;
- contrato provisório quando possível.

Não executa todas as relações secundárias ou análises de sensibilidade.

### 26.2 `PADRAO`

Produz o contrato necessário para orientar a arquitetura de mídia, incluindo:

- objetivos operacionalizados;
- matrizes principais;
- objetivos de Mídia derivados;
- pesos, mínimos e restrições;
- confiança e rastreabilidade.

### 26.3 `DETALHADA`

Pode incluir:

- variantes metodológicas;
- análise de sensibilidade dos pesos;
- caminhos alternativos de derivação;
- decomposição ampliada por público, praça ou etapa;
- comparação com versão anterior;
- memória técnica completa.

O nível detalhado não será padrão da interface.

---

## 27. Limites de processamento e usabilidade

Para impedir que o motor se torne pesado:

- consultar apenas relações candidatas pertinentes;
- filtrar taxonomias pelo contexto antes da pontuação;
- limitar alternativas secundárias apresentadas;
- não recalcular relações não afetadas;
- reutilizar relações padrão e snapshots válidos;
- interromper derivações sem suporte metodológico;
- executar análises avançadas somente sob solicitação;
- apresentar poucas prioridades principais;
- manter detalhes técnicos em camada expandida.

Limites configuráveis podem incluir:

```text
maximo_de_objetivos_candidatos_por_origem
maximo_de_relacoes_secundarias
maximo_de_proxies_por_objetivo
maximo_de_variantes_metodologicas
tolerancia_de_empate
tempo_maximo_de_execucao
```

Esses limites não alteram silenciosamente a lógica estratégica; devem ser registrados na execução.

---

## 28. Dependências e reexecução

| Alteração | Ação no motor |
|---|---|
| objetivo de Marketing ou Comunicação | recalcular objetivo, relações e dependentes |
| público ou segmento prioritário | recalcular compatibilidades e prioridades dependentes |
| praça ou universo | recalcular relações territoriais e mensuração associada |
| jornada, etapa ou necessidade | recalcular relações e objetivos de Mídia dependentes |
| período | recalcular compatibilidade temporal e intensidades afetadas |
| verba ou restrição | reavaliar viabilidade e prioridades afetadas |
| KPI, linha de base ou meta | recalcular operacionalização e vínculos dependentes |
| ajuste humano de peso | preservar cálculo original e recalcular normalizações dependentes |
| preço ou disponibilidade de inventário | normalmente preservar tradução; reavaliar apenas se mudar restrição estratégica |
| quantidade ou programação de cenário | preservar tradução |
| texto ou formatação do plano | preservar tradução |

O motor deverá devolver a lista de objetos posteriores a invalidar:

- arquiteturas dependentes;
- avaliações de cenário;
- simulações cuja configuração deixou de atender ao contrato;
- artefatos consolidados afetados.

A invalidação é executada pela camada de aplicação.

---

## 29. Cache e versionamento

Uma execução poderá ser reutilizada quando permanecerem iguais:

- snapshot relevante;
- modo e nível;
- versões das Bibliotecas 14 a 18;
- parâmetros locais;
- limites que alterem a saída;
- intervenções humanas efetivas.

Chave conceitual:

```text
hash(
  contexto_estrategico_relevante
  + modo
  + nivel
  + versoes_de_conhecimento
  + parametros_locais
  + intervencoes_humanas
)
```

Qualquer reutilização deve registrar a execução original.

---

## 30. Critérios de aceite

O motor estará funcionalmente aceitável quando:

1. produzir contrato estratégico sem selecionar inventário final;
2. distinguir objetivos válidos, provisórios, qualitativos e não operacionalizados;
3. derivar objetivos de Mídia com rastreabilidade;
4. consumir Bibliotecas 14, 15, 16, 17 e 18 seletivamente;
5. preservar pesos, mínimos, restrições e intervenções humanas;
6. não transformar ausência em zero;
7. produzir resultado provisório quando metodologicamente possível;
8. bloquear somente quando faltar dado essencial;
9. explicar relações e prioridades;
10. declarar dependências e reexecução;
11. evitar consulta a ofertas e preços sem pertinência;
12. permitir revisão localizada sem reconstrução integral;
13. produzir saída compatível com o Motor de Decisão;
14. respeitar o contrato comum do documento 25.

---

## 31. Casos mínimos de teste

### Caso A — objetivo genérico

Entrada:

```text
Aumentar vendas.
```

Esperado:

- não assumir automaticamente objetivo de ação;
- identificar contexto, público, prazo e diagnóstico necessários;
- produzir tradução provisória ou pergunta priorizada;
- preservar o texto original.

### Caso B — alta notoriedade e baixa conversão

Esperado:

- priorizar objetivos de Comunicação relacionados a intenção, redução de incerteza ou ação conforme o contexto;
- justificar por que notoriedade adicional pode não ser prioridade principal.

### Caso C — baixa notoriedade

Esperado:

- priorizar conhecimento, alcance, cobertura ou impacto conforme o contexto;
- não impor meio específico.

### Caso D — objetivos conflitantes e verba limitada

Esperado:

- identificar disputa de recursos;
- produzir pesos, mínimos e tensões;
- não distribuir a verba entre meios.

### Caso E — público ausente

Esperado:

- indicar impacto da ausência;
- produzir contrato parcial somente quando possível;
- não usar público genérico artificial.

### Caso F — pretensão declarada de televisão

Esperado:

- registrar como preferência, restrição ou imposição conforme justificativa;
- não converter automaticamente em recomendação estratégica.

### Caso G — ajuste humano de prioridade

Esperado:

- preservar valor calculado;
- registrar valor ajustado e justificativa;
- recalcular apenas dependências afetadas.

### Caso H — alteração posterior de preço

Esperado:

- preservar contrato estratégico;
- não reexecutar o motor, salvo quando o preço alterar uma restrição estratégica de viabilidade.

---

## 32. Estrutura interna recomendada

A especificação não obriga classes definitivas, mas recomenda separar responsabilidades internas:

```text
MotorDeTraducaoEstrategica
├── resolvedor_de_contexto
├── validador_de_suficiencia
├── identificador_de_problemas
├── operacionalizador_de_objetivos
├── relacionador_marketing_comunicacao
├── derivador_de_objetivos_de_midia
├── relacionador_comunicacao_midia
├── priorizador_contextual
├── normalizador_de_pesos
├── analisador_de_tensoes
├── compositor_de_contrato
└── registrador_de_rastreabilidade
```

Esses componentes são procedimentos ou serviços internos, não novos motores.

---

## 33. Decisão consolidada

A versão 1.0 terá um único Motor de Tradução Estratégica, com quatro modos de execução:

```text
TRADUZIR_BRIEFING
REVISAR_TRADUCAO
VALIDAR_SUFICIENCIA_ESTRATEGICA
RECALCULAR_DEPENDENCIAS_ESTRATEGICAS
```

Ele será responsável pela passagem entre contexto e decisão de mídia, produzindo um contrato estratégico explícito e versionado.

Não serão criados motores autônomos para:

- classificação de objetivos;
- recomendação de KPIs;
- análise de públicos;
- jornada;
- pontuação;
- pesos;
- validação estratégica;
- explicação.

Essas funções permanecem procedimentos internos da mesma responsabilidade.

---

## 34. Próxima etapa

Validar esta especificação contra os campos efetivamente definidos nos documentos 02, 03, 14, 15, 16, 17 e 18 e, em seguida, especificar o Motor de Decisão de Arquitetura e Cenários.

Nenhuma implementação definitiva de banco, interface ou classes deve anteceder essa validação de aderência.

---

## 35. Princípio consolidado

> O Motor de Tradução Estratégica não escolhe a mídia e não calcula o plano. Ele transforma o contexto em critérios de decisão. Sua qualidade depende menos de produzir muitas recomendações e mais de tornar explícito o que deve ser priorizado, por quê, com que intensidade, sob quais restrições e com qual confiança.