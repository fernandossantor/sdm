# Decisões metodológicas dos engines

Última revisão: 26 de julho de 2026 (UTC).

## Finalidade

Este documento fixa as decisões metodológicas que orientarão os cálculos, os
dados e as explicações produzidas pelo PlanOS. Ele é normativo para novas
implementações e substitui decisões implícitas, valores silenciosos e
interpretações divergentes entre interface, serviços e engines.

As decisões foram consolidadas a partir do código atual, da documentação do
projeto e dos materiais acadêmicos e mercadológicos armazenados em
`docs/pdfs/`. Os materiais dão fundamento conceitual; as regras abaixo definem
como o PlanOS aplicará esse fundamento.

## Princípios obrigatórios

1. O PlanOS propõe e calcula, mas não inventa fatos.
2. Todo resultado deve ser reproduzível a partir de entradas versionadas.
3. Fato, premissa, decisão e resultado são categorias distintas.
4. Métricas de naturezas ou universos incompatíveis não são agregadas.
5. Estimativa não é apresentada como medição.
6. Atribuição não é apresentada como causalidade.
7. Ausência de dado não será convertida silenciosamente em zero ou em média.
8. Restrições duras não serão substituídas por penalizações de score.
9. A interface nunca conterá uma fórmula diferente da usada pelo engine.
10. Toda aproximação deve informar método, confiança e limitações.

## Vocabulário canônico

### Fato

Dado observado ou contratado, acompanhado de fonte, período e unidade. Exemplos:
preço, audiência medida, impressões entregues, inserções, fluxo, conversões e
receita observada.

### Premissa

Valor necessário ao cálculo, mas não observado como fato daquele plano.
Exemplos: CTR projetado, taxa de conversão, alcance incremental, curva de
resposta e valor de conversão.

### Decisão

Escolha do planejador ou regra aprovada. Exemplos: orçamento, pesos, pisos,
tetos, inventários obrigatórios, função objetivo e reserva para testes.

### Resultado

Valor derivado por fórmula ou algoritmo. Todo resultado deve apontar as entradas
e a versão do método que o produziram.

### Contato estimado

Unidade abstrata usada apenas para compatibilização matemática. Não substitui
a métrica nativa. O resultado deve preservar se a origem foi impressão,
impacto, audiência, OTS, circulação, fluxo, reprodução ou outra unidade.

## DM-001 — Proveniência e confiança

Todo valor usado pelos engines terá, quando aplicável:

- valor e unidade;
- natureza: `FATO`, `PREMISSA`, `DECISAO` ou `RESULTADO`;
- origem: `MEDIDO`, `CONTRATADO`, `INFORMADO`, `CALCULADO` ou `ESTIMADO`;
- fonte e metodologia;
- início e fim de referência;
- universo, público e praça;
- nível de confiança: `ALTA`, `MEDIA`, `BAIXA` ou `NAO_AVALIADA`;
- versão do método de cálculo.

Valores sem fonte podem ser usados como premissa manual, nunca como medição.
Os engines não usarão defaults numéricos silenciosos para completar CPM, CTR,
conversão, frequência, alcance ou retorno.

## DM-002 — Universo e comparabilidade

Uma métrica de audiência ou entrega somente poderá participar de agregação se
seu denominador estiver identificado.

São dimensões mínimas de compatibilidade:

- universo;
- público-alvo;
- praça;
- período;
- métrica nativa;
- metodologia de medição;
- granularidade.

O sistema classificará conjuntos como:

- `COMPARAVEL`: agregação direta autorizada;
- `CONVERTIVEL`: agregação autorizada após conversão explícita;
- `NAO_COMPARAVEL`: exibição lado a lado, sem total agregado;
- `INDETERMINADO`: cálculo bloqueado por falta de metadados.

## DM-003 — Audiência, penetração, perfil, alcance e afinidade

Esses conceitos permanecerão distintos:

- audiência: parcela aferida de um universo exposta a um veículo ou conteúdo;
- penetração: hábito ou consumo declarado de um meio ou veículo;
- perfil: composição do público de um meio;
- alcance: pessoas distintas atingidas ao menos uma vez;
- afinidade: relação entre a presença do target no meio e sua presença na
  população.

Quando calculável:

`indice_afinidade = perfil_target_no_meio / perfil_target_na_populacao * 100`

Scores informados por especialistas continuarão permitidos, mas serão
identificados como julgamento e não como índice de afinidade medido.

## DM-004 — GRP, TRP e impactos

As identidades adotadas são:

- `GRP = soma(audiencia_percentual * insercoes)`;
- `GRP = alcance_percentual * frequencia_media`;
- `TRP` usa o mesmo raciocínio aplicado ao público-alvo;
- `impactos = soma das exposicoes em numeros absolutos`.

GRP pode ultrapassar 100. Alcance não pode ultrapassar 100% do universo.

O PlanOS não somará GRPs de universos incompatíveis. Um total cross-media só
será denominado `GRP agregado` quando os componentes forem comparáveis ou
convertidos para o mesmo universo e target. Caso contrário, serão exibidos
GRPs por meio e contatos estimados, sem total enganoso.

## DM-005 — Alcance líquido e superposição

O alcance líquido será calculado pela melhor evidência disponível, nesta ordem:

1. alcance deduplicado medido;
2. alcance incremental medido por meio;
3. matriz de duplicação ou superposição;
4. modelo calibrado e versionado;
5. hipótese de independência probabilística;
6. indisponível.

A independência probabilística será fallback de baixa confiança e nunca o
método padrão invisível.

O alcance incremental:

- não poderá ser negativo;
- não poderá exceder a parcela ainda não alcançada;
- deverá estar associado à ordem ou ao conjunto de meios que o originou;
- não será tratado como alcance próprio do inventário.

Quando o método for sequencial, a ordem fará parte das premissas auditadas. Um
modelo independente da ordem será preferido quando houver dados suficientes.

## DM-006 — Frequência e saturação

Frequência média não será suficiente para caracterizar a distribuição.
O modelo deverá admitir:

- alcance `1+`, `2+`, `3+` e demais faixas disponíveis;
- frequência mínima ou efetiva;
- faixa eficiente;
- parcela subexposta;
- parcela na faixa;
- parcela sobre-exposta.

Até haver distribuição ou curva calibrada, o PlanOS poderá sinalizar excesso
de frequência, mas não afirmará calcular saturação econômica ou resposta
decrescente.

Curvas de saturação futuras deverão ser específicas por objetivo, meio, formato,
público e período. Uma curva genérica só poderá ser usada como cenário de baixa
confiança explicitamente selecionado.

## DM-007 — Unidades de compra e entrega

Cada unidade de compra terá uma estratégia de cálculo própria, com:

- métrica nativa de entrega;
- conversão para contatos, quando defensável;
- aceitação ou não de quantidade fracionária;
- regra de arredondamento;
- mínimo comercial;
- preço e modelo de cobrança;
- capacidade e disponibilidade;
- fórmula de investimento.

Não será permitido tratar automaticamente toda unidade que não seja impressão
como inserção.

O modelo inicial deverá distinguir pelo menos:

- inserção ou spot;
- impressão;
- mil impressões;
- diária;
- período;
- pacote;
- patrocínio ou cota;
- GRP/TRP contratado;
- clique, lead, aquisição, visualização e visita, quando forem modelos de compra.

## DM-008 — Custos e rentabilidade

Serão mantidos separados:

- preço de tabela;
- desconto;
- mídia líquida;
- fee de tecnologia;
- fee de dados;
- fee de verificação;
- fee operacional;
- criação ou produção;
- impostos e outros custos;
- custo total do anunciante.

As fórmulas mínimas são:

- `CPP = custo / pontos_de_audiencia`;
- `CPM = custo * 1000 / base_absoluta`;
- `CPC = custo / cliques`;
- `CPL = custo / leads`;
- `CPA = custo / aquisicoes`;
- `ROAS = receita_atribuida / investimento_publicitario`;
- `ROI = (retorno - custo_total) / custo_total`.

Cada indicador mostrará qual custo e qual denominador foram usados. CPM de
impressões servidas, visíveis e impactos estimados são indicadores diferentes.

## DM-009 — Objetivos, métricas e KPIs

O encadeamento obrigatório será:

`objetivo de negocio -> objetivo de comunicacao -> objetivo de midia -> KPI -> metrica`

O PlanOS terá famílias de objetivo:

- conhecimento e alcance;
- consideração;
- tráfego e engajamento;
- lead;
- conversão e venda;
- visita;
- retenção e fidelização.

Cada KPI conterá fórmula, direção desejada, meta, período, fonte e objetivos
compatíveis. Métricas diagnósticas não serão promovidas automaticamente a KPI.

O plano poderá ter vários KPIs, mas deverá identificar um objetivo primário ou
uma função multiobjetivo com pesos explícitos.

## DM-010 — Elegibilidade, qualidade, aderência e confiança

O ranking será decomposto em dimensões independentes:

1. elegibilidade;
2. qualidade;
3. aderência estratégica;
4. eficiência econômica;
5. capacidade de entrega;
6. confiança dos dados.

Elegibilidade é binária e aplicada antes do score. Inclui proibições, ausência
de disponibilidade, incompatibilidade legal, brand safety obrigatório e
incapacidade técnica.

Qualidade pode considerar viewability, tráfego inválido, fraude, brand safety,
suitability e transparência. Dado ausente não será interpretado como qualidade
zero; será falta de evidência e reduzirá a confiança conforme regra explícita.

## DM-011 — Restrições

As restrições serão classificadas como:

- `DURA`: deve ser satisfeita; caso contrário, não há solução;
- `FLEXIVEL`: preferência com peso ou penalidade;
- `OPERACIONAL`: quantidade, verba, período, capacidade ou disponibilidade;
- `ESTRATEGICA`: diversidade, papel, jornada ou participação mínima;
- `REGULATORIA`: condição que não pode ser relaxada.

Inventário proibido é excluído. Inventário obrigatório precisa estar presente
ou a geração falha com diagnóstico. Piso e teto permanecem válidos após toda
normalização e arredondamento.

## DM-012 — Score e explicabilidade

O score será versionado e composto por contribuições visíveis. Cada item deverá
informar:

- componentes brutos;
- normalização;
- peso;
- contribuição;
- bônus ou penalidade;
- dado ausente;
- confiança;
- score final.

Não haverá renormalização silenciosa de pesos. Alterações manuais serão
registradas como decisão do planejador. Um mesmo conjunto de entradas e versão
de método deverá produzir o mesmo ranking.

## DM-013 — Alocação e otimização

Distribuição proporcional por score será chamada de `ALOCACAO_HEURISTICA`, não
de otimização.

O otimizador resolverá uma função objetivo declarada, simples ou multiobjetivo,
sujeita às restrições. Funções iniciais:

- maximizar alcance líquido;
- atingir faixa eficiente de frequência;
- minimizar custo para uma meta;
- maximizar resultado projetado;
- maximizar cobertura da jornada;
- maximizar aderência com orçamento limitado.

O resultado deverá informar:

- condição de viabilidade;
- função e pesos;
- restrições ativas;
- restrições relaxadas, se autorizadas;
- sobra ou déficit;
- método e qualidade da solução.

Se não houver solução, o sistema não fabricará uma. Apresentará as causas e
simulações de relaxamento, que exigirão aprovação do usuário.

## DM-014 — Planejamento, forecast e realizado

São estados diferentes:

- planejamento: decisão antes da veiculação;
- forecast: projeção condicionada a premissas;
- realizado: entrega observada;
- diagnóstico: comparação entre planejado, projetado e realizado.

O `ForecastEngine` não recalculará silenciosamente a mesma entrega com defaults
diferentes do plano. Ele reutilizará fatos do plano e acrescentará cenários.

Toda projeção materialmente incerta terá, quando possível:

- cenário conservador;
- cenário base;
- cenário otimista;
- variáveis sensíveis;
- faixa, em vez de falsa precisão.

Meios não clicáveis não gerarão cliques por fórmula genérica. Resultados de
negócio só serão projetados quando houver uma cadeia de premissas compatível.

## DM-015 — Atribuição e incrementalidade

O PlanOS admitirá modelos configuráveis:

- primeira interação;
- última interação;
- último clique elegível;
- linear;
- decaimento temporal;
- posição;
- algorítmico, quando houver dados.

Cada execução registrará janela, eventos, canais observáveis, identidade,
limitações e crédito fracionado.

Atribuição será identificada como análise descritiva. Incrementalidade exigirá
experimento, grupo de controle ou modelo causal apropriado. Receita atribuída
e receita incremental nunca serão sinônimos.

## DM-016 — Localização

Dados de localização exigirão:

- fonte do sinal;
- precisão e raio;
- período;
- finalidade;
- base de consentimento ou autorização aplicável;
- método de associação;
- confiança.

Visita observada e visita inferida serão métricas distintas. Localização será
contexto de segmentação e medição, não definição suficiente de público.

## DM-017 — Flight e cronograma

O flight será uma decisão estratégica, não apenas distribuição visual:

- `LINEAR`: pressão relativamente homogênea;
- `ONDAS`: períodos ativos e pausas regulares;
- `CONCENTRADO`: pressão em período curto;
- `PERSONALIZADO`: distribuição informada pelo planejador.

O cronograma respeitará disponibilidade, unidade de compra, sazonalidade,
quantidade e orçamento por período. Totais semanais e mensais deverão reconciliar
com o plano.

## DM-018 — Estrutura mínima do plano

Um plano completo terá:

1. contexto de mercado e concorrência;
2. produto, marca, praça, público, período e verba;
3. objetivos de negócio, comunicação e mídia;
4. estratégia e papéis dos meios;
5. premissas e qualidade das fontes;
6. táticas, compras, custos e entrega;
7. alcance, frequência e continuidade;
8. KPIs e resultados-chave;
9. cronograma e resumo de verba;
10. riscos, limitações e alternativas;
11. versão, autor, aprovações e trilha de alterações.

## DM-019 — Versionamento e auditoria

Planos persistirão:

- versão dos engines;
- versão das fórmulas;
- snapshot das entradas;
- decisões e alterações manuais;
- avisos e limitações;
- data, autor e espaço de trabalho;
- hash ou identificador reproduzível da execução.

Planos antigos serão restauráveis com sua metodologia original. Recalcular um
plano antigo com método novo criará nova versão, sem reescrever o histórico.

## DM-020 — Critérios de aceitação metodológica

Uma evolução de engine só poderá ser publicada quando:

- possuir especificação da fórmula ou algoritmo;
- declarar domínio de validade;
- ter casos determinísticos;
- testar limites e inviabilidade;
- testar dados ausentes e incompatíveis;
- produzir explicação auditável;
- manter reconciliação financeira e de entrega;
- passar por revisão metodológica;
- não alterar silenciosamente planos históricos.

## Fontes do acervo

As principais bases utilizadas foram:

- `Aula 03.pdf`: objetivos, público, alcance, frequência e critérios criativos;
- `Aula 04.pdf`: audiência, penetração, perfil, afinidade, alcance, frequência,
  CPP e CPM;
- `Aula 05.pdf`: GRP, TRP, impactos, alcance, frequência, agregação multimídia
  e flight;
- `Aula 06.pdf`: pressão, OTS, competitividade, estrutura e mapa do plano;
- `4_Mídia Programática e Mídia de Performance.pdf`: OKRs, KPIs e métricas;
- `E-BOOK-IAB-BRASIL-MÍDIA-PROGRAMÁTICA.pdf`: compra, dados, transparência,
  qualidade e otimização;
- `Ebook-IAB-Modelos-de-Atribuição-link-adjust.pdf`: modelos e limitações de
  atribuição;
- `Ebook-IAB-Location-Based-Marketing.pdf`: localização, qualidade, contexto,
  mensuração e privacidade.

Os materiais comerciais são referências operacionais complementares, não
autoridade exclusiva para decisões metodológicas.
