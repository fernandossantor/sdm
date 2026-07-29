# Inventário Preliminar de Conhecimentos Técnicos

**Documento:** `17A_INVENTARIO_PRELIMINAR_DE_CONHECIMENTOS_TECNICOS.md`  
**Documento relacionado:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em construção progressiva  
**Natureza:** Inventário metodológico e documental

---

## 1. Finalidade

Este documento registra os objetos de conhecimento técnico identificados nas aulas, manuais e documentos de mercado utilizados como fontes do MediAd Planner.

O inventário antecede a formalização definitiva de cada objeto. Seu papel é:

- identificar conhecimentos existentes nas fontes;
- separar conceitos, fórmulas, regras, técnicas e restrições;
- registrar variantes terminológicas ou matemáticas;
- evitar duplicidade entre objetos;
- sinalizar divergências entre fontes;
- preparar a posterior modelagem executável pela Biblioteca 17.

O inventário não transforma automaticamente todo termo encontrado em objeto definitivo.

---

## 2. Estados do inventário

Cada objeto deverá possuir um dos seguintes estados:

- `IDENTIFICADO`;
- `EM_REVISAO`;
- `DUPLICIDADE_POSSIVEL`;
- `VARIANTE_IDENTIFICADA`;
- `DIVERGENCIA_DE_FONTE`;
- `PRONTO_PARA_FORMALIZACAO`;
- `FORMALIZADO`;
- `DESCARTADO`.

---

## 3. Tipos preliminares

Os objetos identificados podem assumir um ou mais tipos:

- `CONCEITO`;
- `DEFINICAO_OPERACIONAL`;
- `FORMULA_DIRETA`;
- `FORMULA_INVERSA`;
- `FORMULA_DERIVADA`;
- `EQUIVALENCIA`;
- `CONVERSAO`;
- `REGRA_DE_VALIDACAO`;
- `REGRA_DE_COMPARABILIDADE`;
- `REGRA_DE_INTERPRETACAO`;
- `REGRA_DECISORIA`;
- `TECNICA_DE_PLANEJAMENTO`;
- `TECNICA_DE_SIMULACAO`;
- `RESTRICAO_METODOLOGICA`;
- `PROCESSO_OPERACIONAL`;
- `INFRAESTRUTURA_TECNOLOGICA`.

---

## 4. Núcleo de audiência e universo

### 4.1 Universo

**Código provisório:** `KT_UNIVERSO`  
**Estado:** `IDENTIFICADO`

Conhecimento necessário para definir a população, conjunto de pessoas, domicílios ou unidades sobre o qual um percentual, índice ou projeção é calculado.

Subobjetos ou relações:

- universo de pessoas;
- universo de domicílios;
- universo com televisão;
- universo da audiência ligada;
- universo do público-alvo;
- universo territorial;
- universo amostral;
- compatibilidade entre universos.

### 4.2 Audiência percentual

**Código provisório:** `KT_AUDIENCIA_PERCENTUAL`  
**Tipos:** `CONCEITO`, `FORMULA_DIRETA`

Forma preliminar:

```text
Audiência percentual =
quantidade de pessoas ou domicílios sintonizados
÷ universo correspondente
× 100
```

Validações necessárias:

- distinguir pessoa de domicílio;
- identificar o universo correto;
- preservar período, praça, programa e fonte;
- não misturar audiência domiciliar e individual.

### 4.3 Participação de audiência

**Código provisório:** `KT_SHARE_AUDIENCIA`  
**Tipos:** `CONCEITO`, `FORMULA_DIRETA`, `REGRA_DE_VALIDACAO`

Forma preliminar:

```text
Participação de audiência =
pessoas ou domicílios sintonizados no programa
÷ pessoas ou domicílios ligados no período
× 100
```

A participação de audiência usa como denominador o universo efetivamente ligado, não o universo total potencial.

### 4.4 Audiência acumulada

**Código provisório:** `KT_AUDIENCIA_ACUMULADA`  
**Estado:** `EM_REVISAO`

A expressão aparece associada à soma de pessoas, domicílios ou percentuais atingidos por uma programação. Deve ser distinguida de:

- soma bruta de audiências;
- alcance líquido;
- alcance acumulado;
- GRP;
- impactos.

A definição definitiva depende de revisão cruzada das fontes.

### 4.5 Impactos

**Código provisório:** `KT_IMPACTOS`  
**Tipos:** `CONCEITO`, `FORMULA_DERIVADA`, `CONVERSAO`

Representa o total bruto de exposições, admitindo repetição da mesma pessoa.

Relações preliminares:

```text
Impactos = audiência absoluta × número de inserções
```

ou, quando o universo e o GRP são compatíveis:

```text
Impactos = universo × GRP ÷ 100
```

As duas formas exigem validação de unidade e período.

---

## 5. Penetração, perfil e afinidade

### 5.1 Penetração do meio

**Código provisório:** `KT_PENETRACAO_MEIO`

```text
Penetração do meio =
pessoas que consomem o meio
÷ universo correspondente
× 100
```

Regra de interpretação: penetração representa hábito ou consumo declarado/estimado e não deve ser confundida automaticamente com audiência aferida.

### 5.2 Penetração do veículo

**Código provisório:** `KT_PENETRACAO_VEICULO`

Deve declarar explicitamente se o denominador é:

- o universo geral;
- o universo de consumidores do meio;
- outro universo definido pela pesquisa.

### 5.3 Perfil ou qualificação

**Código provisório:** `KT_PERFIL_QUALIFICACAO`

Conhecimento destinado a representar a composição interna da audiência ou do consumo de um meio ou veículo por segmentos.

Forma preliminar:

```text
Perfil do segmento =
pessoas do segmento no meio ou veículo
÷ total de pessoas do meio ou veículo
× 100
```

Deverá ser distinguido do alcance horizontal.

### 5.4 Índice de afinidade

**Código provisório:** `KT_INDICE_AFINIDADE`

```text
Índice de afinidade =
percentual do segmento no meio ou veículo
÷ percentual do mesmo segmento na população
× 100
```

Interpretação preliminar:

- acima de 100: concentração superior à média populacional;
- igual a 100: concentração equivalente à média;
- abaixo de 100: concentração inferior à média.

O índice não informa sozinho o tamanho absoluto da audiência.

### 5.5 Afastamento da audiência

**Código provisório:** `KT_AFASTAMENTO_AUDIENCIA`  
**Estado:** `DUPLICIDADE_POSSIVEL`

Deve ser verificado se constitui:

- um objeto autônomo;
- uma interpretação inversa da afinidade;
- uma classificação derivada do índice de afinidade.

---

## 6. Alcance, frequência e distribuição

### 6.1 Alcance

**Código provisório:** `KT_ALCANCE`

```text
Alcance percentual =
pessoas distintas atingidas pelo menos uma vez
÷ universo possível
× 100
```

Subobjetos:

- alcance absoluto;
- alcance percentual;
- alcance líquido;
- alcance projetado;
- alcance realizado;
- alcance por público;
- alcance por praça.

### 6.2 Alcance acumulado

**Código provisório:** `KT_ALCANCE_ACUMULADO`  
**Estado:** `EM_REVISAO`

Deve ser formalizado com cuidado para não confundir:

- soma progressiva de alcances líquidos;
- soma bruta de percentuais;
- curva de alcance;
- audiência acumulada;
- GRP.

### 6.3 Frequência média

**Código provisório:** `KT_FREQUENCIA_MEDIA`

```text
Frequência média =
soma das exposições individuais
÷ quantidade de pessoas distintas atingidas
```

Forma derivada:

```text
Frequência média = GRP ÷ alcance percentual
```

A fórmula derivada exige GRP e alcance calculados sobre o mesmo universo, público, praça e período.

### 6.4 Distribuição de frequências

**Código provisório:** `KT_DISTRIBUICAO_FREQUENCIAS`

Representa a distribuição do alcance conforme a quantidade de exposições recebidas.

Faixas possíveis:

- uma exposição;
- duas exposições;
- três exposições;
- quatro ou mais;
- outras faixas parametrizadas.

### 6.5 Frequência eficiente

**Código provisório:** `KT_FREQUENCIA_EFICIENTE`  
**Estado:** `EM_REVISAO`

Deve distinguir:

- frequência média;
- frequência mínima eficaz;
- intervalo eficiente;
- frequência excessiva;
- saturação.

Não deve ser registrada como valor universal independente de mensagem, objetivo, categoria, ciclo de compra, período e contexto.

### 6.6 OTS

**Código provisório:** `KT_OTS`

Objeto relacionado à oportunidade potencial de exposição.

Deve distinguir:

- oportunidade de ver;
- exposição efetivamente aferida;
- número de inserções;
- frequência média;
- frequência desejada.

---

## 7. GRP, TRP e relações derivadas

### 7.1 GRP

**Código provisório:** `KT_GRP`

Definição preliminar: soma dos pontos percentuais brutos de audiência de uma programação, admitindo duplicação de pessoas.

Forma por programa:

```text
GRP do programa = audiência percentual × número de inserções
```

Forma da programação:

```text
GRP total = soma dos GRPs dos programas
```

Forma derivada:

```text
GRP = alcance percentual × frequência média
```

### 7.2 TRP ou TARP

**Código provisório:** `KT_TRP`

Variação do raciocínio de rating points aplicada especificamente ao público-alvo.

Deve preservar:

- definição do target;
- universo do target;
- audiência individual ou domiciliar aplicável;
- relação com alcance e frequência do público-alvo.

### 7.3 Conversão de GRP em impactos

**Código provisório:** `KT_GRP_PARA_IMPACTOS`

```text
Impactos = GRP × universo ÷ 100
```

Pré-condições:

- universo correspondente ao rating utilizado;
- mesma praça e período;
- unidade absoluta válida;
- ausência de mistura entre domicílios e pessoas.

### 7.4 Comparabilidade multimídia de GRP

**Código provisório:** `KT_COMPARABILIDADE_GRP_MULTIMIDIA`

**Tipo:** `REGRA_DE_COMPARABILIDADE`

O raciocínio de GRP pode ser estendido a outros meios somente quando os dados forem convertidos para bases e universos comparáveis.

Conversões identificadas nas fontes:

- TV e rádio: audiência percentual relativa ao universo;
- OOH: relação entre oportunidades de exposição e fluxo/universo;
- digital: alcance ou visualizações relacionadas ao público-alvo;
- mídia impressa: circulação, leitores ou impressões, conforme a fonte.

As conversões precisam ser formalizadas separadamente e podem produzir comparabilidade com ressalvas.

---

## 8. Custos e eficiência

### 8.1 Custo bruto

**Código provisório:** `KT_CUSTO_BRUTO`

Valor de tabela ou valor anterior aos descontos, negociações e demais ajustes aplicáveis.

### 8.2 Custo líquido

**Código provisório:** `KT_CUSTO_LIQUIDO`

Deve ser definido conforme a arquitetura financeira do sistema e distinguido de:

- líquido do veículo;
- custo líquido para o anunciante;
- investimento após desconto;
- custo com ou sem comissão.

### 8.3 CPP ou custo por ponto

**Código provisório:** `KT_CPP`

```text
CPP = custo da inserção ÷ audiência percentual
```

ou, em programação:

```text
CPP = investimento total ÷ GRP total
```

As variantes devem ser registradas como formas relacionadas, e não confundidas.

Regra preliminar de comparação: menor CPP indica maior eficiência relativa apenas entre alternativas metodologicamente comparáveis.

### 8.4 CPM tradicional

**Código provisório:** `KT_CPM_TRADICIONAL`

```text
CPM = custo da inserção × 1.000
÷ audiência absoluta
```

Deve ser distinguido do CPM digital baseado em impressões servidas, visíveis ou compradas.

### 8.5 Desconto

**Código provisório:** `KT_DESCONTO`

Objetos derivados possíveis:

```text
valor do desconto = custo bruto × percentual de desconto
```

```text
custo após desconto = custo bruto − valor do desconto
```

### 8.6 Comissão de agência

**Código provisório:** `KT_COMISSAO_AGENCIA`

Deve respeitar a modelagem financeira consolidada do MediAd Planner e registrar explicitamente base de cálculo, percentual e partes envolvidas.

---

## 9. Pressão, continuidade e programação

### 9.1 Pressão de mídia

**Código provisório:** `KT_PRESSAO_MIDIA`

Conceito composto relacionado à intensidade do esforço publicitário em determinado público e período.

Possíveis componentes:

- GRP ou TRP;
- alcance;
- frequência;
- impressões;
- número de inserções;
- continuidade;
- concentração temporal.

Não deve ser reduzido automaticamente a um único indicador sem declaração do modelo adotado.

### 9.2 Flight

**Código provisório:** `KT_FLIGHT`

Família de técnicas de distribuição temporal.

Subobjetos previstos:

- continuidade linear;
- ondas;
- pulsação;
- concentração;
- hiato;
- reforço sazonal.

### 9.3 Mapa de programação

**Código provisório:** `KT_MAPA_PROGRAMACAO`

**Tipo:** `PROCESSO_OPERACIONAL`

Deve estruturar, conforme o meio:

- veículo;
- programa ou inventário;
- formato;
- datas;
- inserções;
- custo unitário;
- custo total;
- audiência ou entrega;
- GRP/pressão, quando aplicável;
- descontos;
- verba total.

---

## 10. Participação e desenvolvimento de mercado

### 10.1 Share of Market

**Código provisório:** `KT_SHARE_OF_MARKET`

```text
SOM = desempenho da marca
÷ desempenho total da categoria
× 100
```

A variável de desempenho precisa ser explicitada, por exemplo:

- unidades;
- receita;
- volume;
- clientes.

### 10.2 Share of Voice

**Código provisório:** `KT_SHARE_OF_VOICE`

```text
SOV = presença da marca
÷ presença total da categoria
× 100
```

A presença deve declarar a unidade observada:

- inserções;
- impressões;
- impactos;
- menções;
- tempo;
- espaço;
- índice composto.

### 10.3 Share of Spend

**Código provisório:** `KT_SHARE_OF_SPEND`

```text
Share of Spend = investimento da marca
÷ investimento total da categoria
× 100
```

Deve ser distinguido de Share of Voice.

### 10.4 BDI

**Código provisório:** `KT_BDI`  
**Estado:** `IDENTIFICADO`

Índice destinado a comparar o desenvolvimento da marca entre mercados ou praças.

A fórmula definitiva será extraída e validada em fontes específicas.

### 10.5 CDI

**Código provisório:** `KT_CDI`  
**Estado:** `IDENTIFICADO`

Índice destinado a comparar o desenvolvimento da categoria entre mercados ou praças.

A fórmula definitiva será extraída e validada em fontes específicas.

---

## 11. Mídia digital e programática

### 11.1 CPM digital

**Código provisório:** `KT_CPM_DIGITAL`

Deve declarar qual denominador é utilizado:

- impressões contratadas;
- impressões servidas;
- impressões válidas;
- impressões visíveis.

### 11.2 Viewability

**Código provisório:** `KT_VIEWABILITY`

Família de conhecimentos sobre elegibilidade e visibilidade da impressão.

Precisa registrar:

- critério técnico;
- padrão utilizado;
- duração mínima;
- percentual da peça visível;
- formato;
- fornecedor de medição.

### 11.3 Tráfego inválido

**Código provisório:** `KT_TRAFEGO_INVALIDO`

**Tipos:** `CONCEITO`, `REGRA_DE_VALIDACAO`, `RESTRICAO_METODOLOGICA`

Deve afetar a validade da entrega e a confiança dos cálculos derivados.

### 11.4 Brand safety e suitability

**Código provisório:** `KT_BRAND_SAFETY_SUITABILITY`

Família de regras para adequação contextual e exclusão de ambientes incompatíveis.

Não constitui fórmula de eficiência, mas pode operar como:

- filtro;
- condição obrigatória;
- penalização;
- restrição de inventário.

### 11.5 RTB

**Código provisório:** `KT_RTB`

**Tipo:** `PROCESSO_OPERACIONAL`

Conhecimento sobre leilão em tempo real e interação entre os participantes da cadeia programática.

### 11.6 DSP, SSP, DMP, CDP e DCR

**Códigos provisórios:**

- `KT_DSP`;
- `KT_SSP`;
- `KT_DMP`;
- `KT_CDP`;
- `KT_DCR`.

São objetos de infraestrutura tecnológica e fluxo de dados. Não devem ser tratados como indicadores ou fórmulas.

### 11.7 DCO

**Código provisório:** `KT_DCO`

Técnica de otimização e personalização dinâmica de criativos a partir de dados, regras e contexto.

---

## 12. Sobreposição, deduplicação e saturação

### 12.1 Sobreposição de audiência

**Código provisório:** `KT_SOBREPOSICAO_AUDIENCIA`

Conhecimento necessário para distinguir alcance bruto, alcance líquido e frequência resultante da combinação de meios, canais ou inventários.

### 12.2 Deduplicação

**Código provisório:** `KT_DEDUPLICACAO`

Processo destinado a identificar pessoas, domicílios, dispositivos ou identificadores repetidos entre fontes e pontos de contato.

### 12.3 Alcance combinado

**Código provisório:** `KT_ALCANCE_COMBINADO`

Depende da identificação ou estimativa da sobreposição.

Forma conceitual para dois conjuntos:

```text
Alcance combinado =
alcance A + alcance B − sobreposição A∩B
```

A fórmula só pode ser aplicada quando todos os termos usam a mesma unidade e universo.

### 12.4 Saturação

**Código provisório:** `KT_SATURACAO`

Família de conhecimentos sobre perda de rendimento marginal diante de repetição excessiva, concentração ou exposição acumulada.

Subobjetos previstos:

- limiar de saturação;
- frequência máxima útil;
- curva de resposta;
- rendimento marginal;
- penalização por excesso;
- desgaste criativo.

---

## 13. Regras transversais identificadas

### 13.1 Regra de identidade de universo

Dois valores percentuais só podem ser combinados diretamente quando utilizam universos compatíveis.

### 13.2 Regra de identidade de unidade

Pessoas, domicílios, dispositivos, impressões e oportunidades de ver não são unidades intercambiáveis sem conversão explícita.

### 13.3 Regra de identidade temporal

Indicadores, cálculos e comparações devem usar períodos equivalentes ou declarar a transformação realizada.

### 13.4 Regra de identidade territorial

Valores de praças distintas não devem ser somados como se representassem o mesmo universo, salvo quando a agregação territorial for metodologicamente válida.

### 13.5 Regra de distinção entre bruto e líquido

Somas brutas admitem duplicação. Alcance líquido e pessoas distintas exigem deduplicação observada ou estimada.

### 13.6 Regra de rastreabilidade

Todo cálculo deverá preservar:

- objeto aplicado;
- fórmula ou regra;
- versão;
- variáveis;
- unidades;
- universos;
- fontes;
- resultado bruto;
- arredondamento;
- alertas;
- confiança.

---

## 14. Objetos que exigem revisão prioritária

Os seguintes conhecimentos foram identificados, mas precisam de revisão documental antes da formalização:

- audiência acumulada;
- alcance acumulado;
- frequência eficiente;
- BDI;
- CDI;
- superposição multimídia;
- deduplicação cross-media;
- saturação;
- ROI, ROAS e ROMI;
- Share of Search;
- uplift de buscas;
- regras de atribuição;
- CPM otimizado;
- preço de reserva;
- bid;
- win rate;
- métricas de qualidade de inventário.

---

## 15. Próximas rodadas de extração

A continuidade do inventário deverá ocorrer por blocos:

1. manuais e livros de mídia tradicional;
2. materiais de alcance, frequência, GRP e rentabilidade;
3. mídia impressa, rádio, TV, cinema e OOH;
4. mídia digital e performance;
5. programática e ad tech;
6. compra, negociação, descontos e comissão;
7. cross-media, sobreposição e deduplicação;
8. saturação, otimização e simulação;
9. regras de interpretação e decisão.

---

## 16. Princípio de governança

> Um termo encontrado em uma fonte não se torna automaticamente um objeto definitivo. O inventário identifica o conhecimento; a revisão elimina duplicidades e separa variantes; a Biblioteca 17 formaliza o objeto; e somente depois os motores podem executá-lo.
