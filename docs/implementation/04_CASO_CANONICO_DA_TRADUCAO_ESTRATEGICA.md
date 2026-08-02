# Caso canônico da Tradução Estratégica

## Finalidade

Este caso fixa a referência comportamental da primeira fatia vertical. A fonte
executável das entradas é `tests/fixtures/campanha_canonica.py`. O caso não
escolhe meios, veículos ou inventários, não distribui verba e não define fórmula
de pontuação.

## 1. Entradas do caso

| Campo | Valor |
| --- | --- |
| Campanha | Lume Casa — Primavera 2026 (`campanha-canonica-lume-2026`) |
| Marca e oferta | Lume Casa; assinatura de energia solar residencial |
| Situação | Notoriedade auxiliada alta (78%), mas apenas 1,1% das visitas à página concluem o pedido de proposta; há ofertas semelhantes e receio sobre economia real e prazo de retorno. |
| Objetivos de Marketing | 1. aumento de vendas — prioridade muito alta; 2. crescimento — prioridade alta |
| Candidatos de Comunicação | intenção; redução de incerteza; notoriedade |
| Público prioritário | Responsáveis pela decisão de energia residencial, de 30 a 55 anos, que pesquisaram redução da conta; prioridade muito alta |
| Segmento secundário | Interessados em sustentabilidade sem pesquisa recente sobre redução da conta; prioridade média |
| Praça | Município de Campinas (SP) |
| Período | 1º de setembro a 31 de outubro de 2026 |
| Verba | BRL 300.000; limite rígido; flexibilidade não informada |
| Prioridade transversal | O público prioritário não pode perder precedência para o segmento secundário. |
| Restrição | A campanha não pode ultrapassar BRL 300.000. |
| Tensão | Aumento de vendas no curto período e crescimento disputam a mesma verba rígida. |
| Indicadores disponíveis | Notoriedade auxiliada: 78%; conclusão do pedido de proposta: 1,1%. Ambos são observados, referentes a junho de 2026 e têm confiança média. |

## 2. Saída esperada em linguagem de negócio

A tradução deve declarar que o principal problema não é ampliar conhecimento da
existência da marca. A prioridade é aproximar o público pesquisador da decisão,
reduzindo sua incerteza sobre economia e retorno e favorecendo uma resposta
mensurável. Notoriedade permanece como apoio, não como prioridade principal.

A saída deve ser provisória: faltam linha de base e meta de vendas, indicador de
intenção, dimensões populacionais e ciclo de compra. A saída não pode apresentar
essas ausências como valor zero nem prometer aumento de vendas como efeito causal
da mídia.

## 3. Objetivos de Comunicação esperados

| Ordem | Objetivo | Condição observável |
| ---: | --- | --- |
| 1 | intenção | Deve ser a primeira prioridade por relacionar o objetivo de aumento de vendas ao público já pesquisador e à baixa conclusão de proposta. |
| 2 | redução de incerteza | Deve anteceder notoriedade porque a barreira declarada é o receio sobre economia e prazo de retorno. |
| 3 | notoriedade | Deve permanecer candidata, mas não pode ocupar as ordens 1 ou 2 enquanto o indicador disponível permanecer em 78%. |

Os três candidatos informados devem permanecer rastreáveis; a tradução não pode
apagar o texto ou descartar silenciosamente o terceiro colocado.

## 4. Objetivos de Mídia esperados

| Ordem | Objetivo | Origem principal |
| ---: | --- | --- |
| 1 | favorecer resposta | intenção e baixa conclusão do pedido de proposta |
| 2 | gerar tráfego | intenção, com necessidade de conduzir o público a uma resposta mensurável |
| 3 | alcançar públicos prioritários | precedência declarada do público que já pesquisou redução da conta |
| 4 | construir alcance | notoriedade como objetivo complementar |

Nenhuma linha dessa ordem autoriza seleção de ponto de contato, meio, formato,
veículo, inventário ou divisão da verba.

## 5. Pesos e faixas esperadas

Não há coeficientes definitivos neste caso. Para comparação futura, a saída deve
obedecer simultaneamente às seguintes relações:

- `peso(intenção) > peso(redução de incerteza) > peso(notoriedade)`;
- `peso(favorecer resposta) > peso(gerar tráfego) > peso(alcançar públicos prioritários) > peso(construir alcance)`;
- intenção deve ter intensidade **muito alta**, faixa canônica de 80 a 100;
- redução de incerteza deve ter intensidade **alta**, faixa canônica de 60 a 79;
- notoriedade deve ter intensidade **baixa**, faixa canônica de 20 a 39;
- os pesos efetivos de cada família, quando futuramente calculados, devem estar
  entre 0,00 e 1,00 e somar 1,00 dentro da respectiva família normalizada.

Essas comparações e faixas são expectativas. Nenhum valor pontual ou fórmula de
normalização é definido aqui.

## 6. Restrições e tensões esperadas

- A restrição orçamentária deve ser classificada como `RESTRITIVA`, porque o teto
  é rígido, e preservada separadamente dos pesos.
- A saída deve registrar disputa de recursos entre aumento de vendas e
  crescimento.
- A tensão deve citar os quatro elementos observáveis: os dois objetivos de
  Marketing, o período de dois meses e a verba rígida.
- A tradução pode pedir priorização ou validação humana, mas não pode resolver a
  tensão distribuindo BRL 300.000 entre alternativas de mídia.

## 7. Indicadores sugeridos

| Objetivo | Indicador sugerido | Situação no caso |
| --- | --- | --- |
| intenção | intenção declarada de solicitar proposta | pendente; não substituir por zero |
| redução de incerteza | proporção que reconhece corretamente economia e prazo de retorno | pendente; requer definição de instrumento e fonte |
| favorecer resposta | taxa de conclusão do pedido de proposta | disponível como linha observada de 1,1% |
| gerar tráfego | visitas qualificadas à página de proposta | pendente; requer critério de qualificação |
| alcançar públicos prioritários | alcance no público prioritário | pendente; depende do tamanho mensurável do público |
| construir alcance | alcance da campanha na praça | pendente; depende do universo populacional da praça |

Notoriedade auxiliada de 78% deve ser preservada como indicador contextual, mas
não promovida a KPI principal deste caso.

## 8. Explicações esperadas

A saída futura deve conter, de forma comparável, estas afirmações:

1. intenção ficou em primeiro lugar porque aumento de vendas é a prioridade
   declarada, o público prioritário já pesquisa a categoria e a conclusão de
   proposta observada é baixa;
2. redução de incerteza ficou em segundo lugar porque receio sobre economia e
   prazo de retorno é uma barreira explícita;
3. notoriedade ficou em terceiro lugar porque a linha observada de 78% indica que
   conhecimento adicional não é a lacuna principal;
4. favorecer resposta e gerar tráfego foram derivados de intenção, sem equivaler
   resposta ou tráfego a venda;
5. a confiança é limitada pela ausência de metas, dimensões populacionais,
   indicador de intenção e ciclo de compra;
6. a verba foi usada somente para sinalizar viabilidade e disputa, nunca para
   produzir uma alocação.

## 9. Dados que devem permanecer pendentes

Os seguintes campos devem continuar com valor `None` até serem informados:

- meta de vendas;
- linha de base de vendas;
- indicador de intenção;
- tamanho do público prioritário;
- tamanho do segmento secundário;
- universo populacional da praça;
- ciclo de compra;
- margem de flexibilidade da verba.

Nenhum desses campos pode receber `0`, estimativa silenciosa ou público genérico
artificial.

## 10. Alterações de entrada que devem mudar a saída

| Alteração isolada | Mudança observável esperada |
| --- | --- |
| Notoriedade auxiliada cai de 78% para menos de 40%, mantendo as demais entradas | notoriedade passa à ordem 1 de Comunicação; construir alcance passa à ordem 1 de Mídia. |
| Taxa de conclusão do pedido sobe de 1,1% para pelo menos 10%, sem nova evidência de barreira | intenção deixa a ordem 1; a saída deve solicitar validação do problema antes de manter favorecer resposta como primeiro objetivo de Mídia. |
| Prioridade de crescimento muda de alta para muito baixa | a tensão por disputa entre os dois objetivos de Marketing perde gravidade e aumento de vendas permanece dominante. |
| Limite da verba muda de rígido para flexível | a restrição deixa de ser `RESTRITIVA` e precisa ser reclassificada; a tensão orçamentária perde gravidade. |
| Indicador de intenção é informado com fonte, período e confiança | a pendência correspondente desaparece e a explicação deve passar a citar o valor informado. |
| Público prioritário passa a ser o segmento sem pesquisa recente | a justificativa baseada em proximidade da decisão deixa de ser válida e as prioridades de Comunicação e Mídia devem ser recalculadas. |
| Período final muda de 31 de outubro para 15 de setembro de 2026 | a tensão temporal aumenta; a saída deve registrar maior pressão de concentração e menor confiança na viabilidade do escopo. |

As mudanças acima definem relações metamórficas para testes futuros: cada linha
altera uma entrada e determina qual parte ordenada ou explicativa da saída deve
mudar.
