# Plano Mestre do MediAd Planner

**Versão:** 1.0  
**Status:** Consolidado  
**Branch de referência:** `main`  
**Finalidade:** fixar a filosofia, o fluxo geral, as etapas, os contratos e as decisões estruturais do MediAd Planner antes da implementação ou revisão de módulos específicos.

---

## 1. Filosofia do sistema

O MediAd Planner é um sistema orientado de planejamento de mídia que converte uma composição de intenções, contextos, públicos, restrições e metas em alternativas de plano calculadas, justificadas, comparáveis e revisáveis.

O sistema não deve funcionar como um conjunto de cadastros, formulários isolados ou motores independentes. Seu núcleo é a transformação de escolhas do briefing em consequências mensuráveis no planejamento.

Princípios obrigatórios:

1. Toda escolha relevante deve produzir efeito no plano.
2. Os efeitos devem variar conforme a combinação das escolhas.
3. Pesos, compatibilidades, restrições e compensações devem ser explícitos.
4. O sistema deve explicar recomendações, penalidades e conflitos.
5. O usuário deve poder avançar e regressar sem reconstruir todo o trabalho.
6. Uma alteração anterior deve recalcular apenas o que foi afetado, preservando decisões válidas.
7. Cenários, comparação, otimização e insights integram o núcleo do simulador.
8. O plano de mídia é a consolidação de uma simulação escolhida, não o ponto de partida dos cálculos.

---

## 2. Governança das decisões

Nenhuma proposta nova altera automaticamente este plano.

Cada definição deve receber um estado:

| Estado | Significado |
|---|---|
| Em discussão | Ainda pode ser alterada livremente |
| Proposta | Formulação candidata à aprovação |
| Consolidada | Integra o Plano Mestre vigente |
| Substituída | Permanece no histórico, mas não está vigente |
| Adiada | Considerada válida, porém fora do escopo atual |

Uma decisão consolidada somente poderá ser modificada por revisão explícita, contendo:

- decisão vigente;
- problema identificado;
- alteração proposta;
- etapas afetadas;
- motores afetados;
- consequências para banco, interface e cálculos;
- aprovação da nova versão.

Além deste documento, o projeto deverá manter:

- **Registro de Decisões**: decisões consolidadas e suas versões;
- **Backlog de Hipóteses**: ideias ainda não aprovadas;
- **Dicionário do Domínio**: termos, definições, relações e fontes metodológicas.

---

## 3. Unidade de trabalho

O título visível da unidade de trabalho será formado por:

> **Nome da campanha — Cliente ou Marca**

O antigo “nome de projeto” pode permanecer apenas como identificador técnico interno, sem exigir um título adicional do usuário.

Estrutura conceitual:

```text
Cliente / Anunciante
        ↓
Marca ou Produto
        ↓
Campanha
        ↓
Briefing de mídia
        ↓
Simulações
        ↓
Plano de mídia consolidado
```

O cadastro do anunciante deve ser reutilizável em múltiplas campanhas e briefings.

---

## 4. Camada permanente: bibliotecas e parâmetros

Esta camada não é uma etapa da campanha. É a base reutilizável do sistema.

Deve conter, no mínimo:

- anunciantes;
- marcas;
- produtos;
- contatos;
- planners;
- concorrentes;
- praças;
- universos;
- segmentos;
- públicos;
- jornadas e pontos de contato;
- objetivos;
- KPIs;
- inventários;
- unidades de compra;
- custos;
- parâmetros dos motores.

As bibliotecas não podem ser apenas cadastrais. Sempre que uma entidade interferir no planejamento, ela deve alimentar diretamente os motores de decisão.

### 4.1 Snapshot de campanha

Ao selecionar um item reutilizável, o briefing deve guardar uma fotografia versionada das informações utilizadas.

Fluxo:

```text
Cadastro mestre
      ↓
Seleção no briefing
      ↓
Snapshot da campanha
      ↓
Ajustes locais
      ↓
Uso nos motores
```

Alterações futuras no cadastro mestre não devem modificar retroativamente campanhas anteriores.

---

## 5. Fluxo mestre consolidado

```text
Bibliotecas e parâmetros
          ↓
1. Abertura da campanha
          ↓
2. Briefing de mídia
          ↓
3. Tradução estratégica
          ↓
4. Arquitetura de mídia
          ↓
5. Ambiente de simulação
   ├── Construção de cenários
   ├── Comparação de planos
   ├── Otimização da verba
   └── Insights
          ↓
6. Consolidação do plano de mídia
          ↓
7. Validação e aprovação
          ↓
8. Acompanhamento e resultados
```

O fluxo é progressivo, mas também admite regressão controlada.

---

## 6. Etapa 1 — Abertura da campanha

### Finalidade

Criar a unidade de trabalho.

### Entradas

- anunciante;
- marca;
- produto ou serviço;
- nome da campanha;
- contato solicitante;
- e-mail;
- planner responsável, vinculado ao login.

### Saída

Campanha criada e identificada, ainda sem planejamento.

---

## 7. Etapa 2 — Briefing de mídia

### Finalidade

Registrar o que o anunciante demanda: pretensões, prioridades, metas, restrições e condições que tenham impacto em decisões de mídia.

O briefing não confirma a viabilidade das metas e não define o plano final.

### Conteúdo consolidado

- identificação da campanha;
- situação da marca e do mercado;
- concorrentes e indicadores competitivos disponíveis;
- objetivo de marketing;
- objetivo de comunicação;
- objetivo de mídia;
- praça;
- universo;
- público;
- segmentos;
- jornada e pontos de contato;
- KPIs;
- alcance pretendido;
- frequência média pretendida;
- período de veiculação;
- flight pretendido;
- verba de mídia;
- prioridades;
- restrições de mídia.

### Regras

1. Campos cadastrais podem usar texto livre.
2. Campos decisórios devem ser preferencialmente parametrizados.
3. Toda lista deve permitir a criação controlada de nova opção.
4. Objetivos de marketing, comunicação e mídia não podem ser escolhas independentes e fortuitas.
5. As relações entre objetivos devem gerar pesos e compatibilidades.
6. KPIs devem conter meta, mínimo aceitável, prioridade e flexibilidade.
7. Alcance e frequência registrados no briefing são pretensões, não resultados calculados.

### Interface

O briefing não deve ser exibido em uma única tela extensa. Deve ser organizado em subetapas progressivas, com resumo permanente e possibilidade de retorno.

---

## 8. Etapa 3 — Tradução estratégica

### Finalidade

Transformar o briefing em um perfil estratégico comum a todos os motores.

### Funções

- definir dimensões prioritárias;
- definir pesos variáveis;
- classificar KPIs em principais, secundários e diagnósticos;
- verificar compatibilidades;
- identificar tensões;
- classificar restrições como rígidas ou flexíveis;
- definir possíveis compensações.

### Exemplo

Uma campanha de awareness tende a elevar o peso de:

- alcance;
- cobertura;
- impacto;
- continuidade;
- Share of Voice;
- velocidade de construção de alcance.

Se conversão for escolhida como objetivo ou KPI principal, o sistema deve indicar a tensão metodológica, reduzir a eficácia esperada da composição ou sugerir uma estratégia de funil combinado.

### Regra estrutural

O briefing configura o sistema de avaliação. Ele não escolhe antecipadamente o resultado.

---

## 9. Etapa 4 — Arquitetura de mídia

### Finalidade

Avaliar a adequação de meios, canais e inventários à campanha.

### Dimensões mínimas

- adequação ao objetivo;
- adequação ao público;
- adequação à jornada;
- adequação geográfica;
- afinidade;
- capacidade de alcance;
- capacidade de frequência;
- impacto;
- mensurabilidade;
- eficiência;
- disponibilidade;
- restrições;
- papéis estratégicos.

### Papéis estratégicos

- principal;
- complementar;
- apoio.

Os pesos dos papéis estratégicos devem variar conforme o briefing, o perfil do público e as demais escolhas da campanha.

### Saída

Arquitetura recomendada de meios, canais, inventários e papéis, ainda não consolidada como plano final.

---

## 10. Etapa 5 — Ambiente de simulação

Esta é a etapa central do MediAd Planner.

Comparação de planos, otimização da verba e insights não são opções avançadas nem etapas posteriores ao plano. Elas integram o mesmo ambiente de simulação que antecede a consolidação.

### Regra central

Todas as funções devem consumir os resultados de um único motor comum de cálculo.

```text
Configuração da simulação
          ↓
Motor comum de cálculo
          ↓
Resultado da simulação
          ├── Cenários
          ├── Comparação
          ├── Otimização
          ├── Insights
          └── Consolidação
```

Não pode existir um cálculo de alcance no cenário, outro na comparação, outro na otimização e outro no plano final.

### 10.1 Construção de cenários

Um cenário é uma composição possível de plano.

Exemplos:

- orientado a alcance;
- orientado a frequência;
- orientado a afinidade;
- orientado a conversão;
- equilibrado;
- verba mínima;
- cobertura geográfica máxima;
- personalizado.

Cada cenário deve guardar:

- briefing de origem;
- perfil estratégico;
- parâmetros;
- composição de mídia;
- inventários;
- unidades;
- quantidades;
- custos;
- distribuição geográfica;
- distribuição temporal;
- resultados calculados;
- conflitos;
- alertas;
- alterações manuais;
- versão;
- origem da simulação.

### 10.2 Comparação de planos

A função compara simulações candidatas a plano.

A comparação deve contemplar, no mínimo:

- investimento;
- alcance;
- frequência;
- impactos;
- cobertura;
- sobreposição;
- saturação;
- GRP/TRP;
- afinidade;
- eficiência de custo;
- distribuição por meio;
- distribuição por praça;
- distribuição temporal;
- atendimento aos objetivos;
- atendimento aos KPIs;
- riscos;
- compensações.

O sistema deve explicar as diferenças, não apenas exibir números.

### 10.3 Otimização da verba

A otimização deve respeitar o perfil estratégico da campanha.

O motor precisa considerar:

- prioridades;
- metas;
- restrições rígidas;
- variáveis flexíveis;
- papéis estratégicos;
- limites dos inventários;
- saturação;
- alcance incremental;
- sobreposição;
- cobertura geográfica;
- eficiência marginal;
- distribuição temporal;
- verba disponível.

Uma otimização nunca deve substituir automaticamente o cenário original. Deve criar uma nova versão comparável.

### 10.4 Insights

Insights devem ser produzidos durante toda a simulação.

Tipos mínimos:

- explicativo;
- alerta;
- oportunidade;
- comparativo.

Todo insight deve indicar:

- dado ou regra que o originou;
- variável afetada;
- consequência;
- ação possível;
- natureza da conclusão: metodológica, matemática ou indicativa.

### Ciclo iterativo

```text
Construir cenário
      ↓
Calcular
      ↓
Comparar
      ↓
Receber insights
      ↓
Otimizar
      ↓
Criar nova versão
      ↓
Comparar novamente
      ↺
```

---

## 11. Praça, universo, alcance e sobreposição

A praça não é apenas um campo descritivo. É uma sinalização geográfica operacional.

Ela deve influenciar:

- universo de referência;
- cobertura;
- alcance potencial;
- disponibilidade de inventários;
- custos;
- distribuição da verba;
- overlap;
- alcance incremental;
- comparação entre cenários.

### Regras

1. Combinar mídias pode aumentar o alcance, mas as audiências não podem ser simplesmente somadas.
2. Meios na mesma praça e com públicos semelhantes tendem a produzir maior sobreposição.
3. Meios em praças distintas tendem a ampliar cobertura geográfica.
4. Coberturas parcialmente coincidentes devem gerar sobreposição geográfica parcial.
5. O universo deve estar associado à praça, à fonte, ao período e à unidade.
6. Alcance, cobertura e frequência devem usar a mesma base populacional em cada cálculo.

---

## 12. Inventários, unidades, frequência e flight

Inventários devem funcionar como dicionário aplicável e objeto operacional.

Cada inventário deve possuir, conforme sua natureza:

- meio;
- canal;
- veículo ou plataforma;
- formato;
- unidade de compra;
- valor unitário;
- quantidade;
- audiência, impressões ou capacidade estimada;
- cobertura geográfica;
- disponibilidade temporal;
- modalidade de compra;
- métricas aplicáveis;
- limites de frequência;
- limites de saturação;
- restrições.

As unidades adquiridas devem ser distribuídas no tempo e no flight.

Exemplos:

- TV: inserções por dia, programa, faixa e período;
- rádio: inserções por faixa e praça;
- OOH: faces, circuitos ou períodos;
- digital: impressões, cliques, visualizações, períodos ou pacotes;
- cinema: inserções, sessões ou semanas;
- jornal e revista: espaços, formatos e edições.

O flight não pode ser apenas uma classificação visual. Deve orientar a distribuição de unidades e a construção da frequência ao longo do período.

---

## 13. Etapa 6 — Consolidação do plano de mídia

### Finalidade

Transformar uma simulação escolhida em plano oficial.

O plano de mídia é uma fotografia da simulação selecionada.

### Deve registrar

- cenário de origem;
- versão;
- briefing de origem;
- perfil estratégico;
- parâmetros;
- resultados estimados;
- otimizações aplicadas;
- insights considerados;
- diferenças em relação ao briefing;
- decisões manuais;
- responsável pela consolidação.

### Conteúdo operacional

- meios;
- canais;
- veículos ou plataformas;
- inventários;
- formatos;
- unidades de compra;
- quantidades;
- valores unitários;
- investimento;
- praça;
- público;
- período;
- flight;
- calendário;
- alcance estimado;
- frequência estimada;
- impactos;
- KPIs esperados;
- papéis estratégicos.

O plano consolidado deve ser imutável. Alterações posteriores exigem nova versão.

---

## 14. Etapa 7 — Validação e aprovação

### Finalidade

Verificar a conformidade do plano com:

- objetivos;
- prioridades;
- metas;
- restrições;
- orçamento;
- praça;
- público;
- período;
- regras metodológicas.

### Saída

- aprovado;
- rejeitado;
- devolvido para revisão.

O sistema deve apresentar:

- metas atendidas;
- metas parcialmente atendidas;
- incompatibilidades;
- compensações;
- diferenças em relação ao briefing;
- justificativas.

---

## 15. Etapa 8 — Acompanhamento e resultados

### Finalidade

Comparar o planejado com o realizado.

### Conteúdo

- contratação;
- execução;
- entrega;
- investimento realizado;
- KPIs observados;
- desvios;
- resultados;
- avaliação do plano.

Os resultados não devem modificar retroativamente o briefing ou o plano aprovado.

---

## 16. Modelo comum de decisão

Cada simulação deve ser avaliada por operações distintas, porém integradas.

### 16.1 Compatibilidade

Verifica se as escolhas combinam conceitualmente.

### 16.2 Prioridade

Define a importância relativa de cada dimensão na campanha.

### 16.3 Desempenho estimado

Calcula quanto a simulação entrega em cada variável.

### 16.4 Compensação

Verifica se uma deficiência pode ser justificada ou compensada por outra característica.

Exemplos:

- menor alcance com maior afinidade;
- menor frequência com formato de maior impacto;
- maior CPM com público mais qualificado;
- campanha curta com maior pressão;
- verba limitada com priorização geográfica ou temporal.

O sistema não deve ser apenas um mecanismo de penalidades.

---

## 17. Interface progressiva e regressiva

A interface deve ser progressiva, objetiva e contextual.

### Três níveis simultâneos

1. **Etapa atual**: mostra apenas a decisão em curso.
2. **Contexto permanente**: resumo compacto do briefing e das escolhas principais.
3. **Consequências**: efeitos imediatos, alertas e recomendações.

### Regressão controlada

Ao alterar uma escolha anterior, os elementos posteriores devem ser classificados como:

- válido;
- requer recálculo;
- requer revisão;
- incompatível;
- preservado manualmente;
- substituído.

O sistema não deve apagar automaticamente o trabalho posterior.

### Dicas e orientações

Devem aparecer em camadas:

- definição curta junto ao campo;
- ajuda aprofundada sob demanda;
- aviso de incompatibilidade;
- recomendação contextual;
- justificativa no resultado.

---

## 18. Contratos entre etapas

| Etapa | Recebe | Produz |
|---|---|---|
| Abertura | cadastros reutilizáveis | campanha |
| Briefing | campanha e bibliotecas | demandas estruturadas |
| Tradução estratégica | briefing | pesos, prioridades e regras |
| Arquitetura de mídia | perfil estratégico e inventários | adequação e papéis |
| Simulação | arquitetura, custos e restrições | cenários calculados |
| Comparação | cenários | diferenças e trade-offs |
| Otimização | cenário e perfil estratégico | nova versão otimizada |
| Insights | resultados das simulações | explicações, alertas e oportunidades |
| Consolidação | cenário escolhido | plano de mídia oficial |
| Validação | plano e briefing | conformidade e justificativa |
| Resultados | plano aprovado e execução | desempenho observado |

Um campo ou cálculo só poderá ser criado se houver resposta para:

1. em qual etapa nasce;
2. qual etapa o modifica;
3. qual motor o utiliza;
4. qual saída ele afeta;
5. como aparece na interface.

---

## 19. Objeto Simulação

Estrutura conceitual mínima:

```text
Simulação
├── campanha
├── briefing de origem
├── perfil estratégico
├── arquitetura de mídia
├── versão
├── cenário
├── composição de mídia
├── distribuição de verba
├── distribuição geográfica
├── distribuição temporal
├── unidades de inventário
├── resultados calculados
├── atendimento às metas
├── conflitos
├── insights
├── origem
│   ├── manual
│   ├── duplicada
│   └── otimizada
└── status
    ├── rascunho
    ├── calculada
    ├── comparada
    ├── candidata
    ├── consolidada
    └── descartada
```

---

## 20. Decisões consolidadas v1.0

### DEC-001 — Identificação da unidade de trabalho

O título visível será “Nome da campanha — Cliente ou Marca”. O nome de projeto poderá permanecer apenas como identificador técnico.

### DEC-002 — Reutilização do anunciante

O anunciante será uma entidade reutilizável em múltiplos briefings e campanhas.

### DEC-003 — Bibliotecas aplicáveis

Universos, segmentos, públicos e inventários devem deixar de ser apenas cadastros e passar a alimentar os motores de decisão.

### DEC-004 — Relações ponderadas

Toda escolha decisória deve produzir pesos, compatibilidades, restrições ou compensações mensuráveis.

### DEC-005 — Praça operacional

A praça será uma entidade geográfica utilizada em universo, cobertura, alcance, disponibilidade, custo e sobreposição.

### DEC-006 — Inventário operacional

Inventários terão unidades, valores, capacidades e distribuição temporal associadas à frequência e ao flight.

### DEC-007 — Motor comum

Cenários, comparação, otimização, insights e plano consolidado utilizarão a mesma base de cálculo.

### DEC-008 — Núcleo de simulação

Construção de cenários, comparação de planos, otimização da verba e insights integram o Ambiente de Simulação e antecedem o plano de mídia.

### DEC-009 — Plano como consolidação

O plano de mídia será a consolidação de uma simulação escolhida, após comparação, otimização e análise de insights.

### DEC-010 — Interface progressiva e regressiva

A interface deve permitir avanço, retorno, recálculo seletivo, preservação de decisões válidas e explicação contextual.

---

## 21. Critério para novas propostas

Nenhuma nova biblioteca, etapa, motor, campo ou parâmetro deverá ser acrescentado sem responder:

- o conceito já existe com outro nome?
- pertence a qual etapa?
- altera qual decisão?
- produz qual cálculo?
- substitui algo ou duplica?
- exige alteração do Plano Mestre?
- é essencial agora ou pertence ao backlog?

---

## 22. Próxima etapa autorizada

Com este Plano Mestre consolidado, a próxima etapa de especificação é o **Briefing de mídia**, respeitando integralmente:

- os limites deste fluxo;
- os contratos entre etapas;
- a necessidade de efeitos calculáveis;
- a interface progressiva e regressiva;
- a reutilização de bibliotecas;
- a preservação das decisões já consolidadas.

Nenhuma nova etapa deverá ser criada durante a especificação do briefing sem revisão formal deste documento.
