# Biblioteca de Conhecimento Técnico do MediAd Planner

**Documento:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Subtítulo:** Lógicas, cálculos, fórmulas, regras e técnicas de planejamento de mídia  
**Plano Mestre:** MediAd Planner  
**Status:** Em consolidação progressiva  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Conhecimento Técnico organiza, versiona e torna computáveis as lógicas, os cálculos, as fórmulas, as equivalências, as conversões, as regras de utilização, as condições de validade, as técnicas e as restrições metodológicas empregadas no planejamento, na compra, na comparação, na simulação e na avaliação de mídia.

Ela constitui a base de conhecimento técnico-operacional utilizada pelos motores do MediAd Planner.

```text
Conhecimento técnico do mercado
        ↓
Objeto de conhecimento estruturado
        ↓
Conceitos, modelos matemáticos e regras
        ↓
Validação das condições de aplicação
        ↓
Execução pelos motores
        ↓
Resultado calculado, interpretável e rastreável
```

A Biblioteca não deve ser reduzida a um catálogo de fórmulas. Uma expressão matemática somente é utilizável pelo sistema quando acompanhada de definição, variáveis, unidades, contexto, pré-condições, limitações, regras de comparabilidade e interpretação.

---

## 2. Fronteira com a Biblioteca 15

A Biblioteca 15 define objetivos, resultados pretendidos, indicadores e KPIs possíveis.

A Biblioteca 17 define como o conhecimento técnico necessário para calcular, transformar, validar, comparar e interpretar esses indicadores é formalizado.

```text
Biblioteca 15
Indicadores e KPIs
        ↓
define o que deve ser observado
```

```text
Biblioteca 17
Conhecimento Técnico
        ↓
define como calcular, validar, comparar e interpretar
```

Exemplo:

```text
Biblioteca 15
Indicador: frequência média
Família: planejamento e pressão de mídia
Pode receber meta: sim
Pode ser projetado: sim
```

```text
Biblioteca 17
Objeto de conhecimento: frequência média
Lógica: exposições totais divididas pelo alcance líquido
Entradas: impactos ou impressões; alcance único
Condições: mesmo universo, período e base de deduplicação
Restrições: não somar frequências de veículos sem deduplicação válida
```

Indicadores não devem ser recadastrados como objetos independentes nesta Biblioteca. A relação será N:N:

```text
Indicador da Biblioteca 15
        ↕
Objetos de conhecimento da Biblioteca 17
```

---

## 3. Natureza da Biblioteca

A Biblioteca 17 funciona como uma base de conhecimento de sistema especialista.

Ela deve permitir que os motores formulem perguntas como:

```text
Qual lógica é aplicável nesta situação?
Quais dados são necessários?
Os universos são comparáveis?
Qual fórmula pode ser executada?
Há variantes possíveis?
Quais limitações precisam ser informadas?
Como interpretar o resultado?
```

Os motores não devem depender de fórmulas codificadas diretamente em seus fluxos decisórios. Eles devem consultar objetos de conhecimento versionados.

```text
Motor
    ↓
Solicita uma operação técnica
    ↓
Biblioteca identifica objetos aplicáveis
    ↓
Valida contexto e pré-condições
    ↓
Seleciona lógica, fórmula ou regra
    ↓
Executa ou encaminha para função correspondente
    ↓
Retorna valor, interpretação, confiança e rastreabilidade
```

---

## 4. Unidade básica: Objeto de Conhecimento Técnico

A unidade básica da Biblioteca será denominada:

```text
objeto_de_conhecimento_tecnico
```

Um objeto pode representar:

- conceito técnico;
- definição operacional;
- fórmula direta;
- fórmula inversa;
- fórmula derivada;
- equivalência;
- conversão;
- regra condicional;
- regra de validação;
- regra de comparabilidade;
- regra de interpretação;
- técnica de planejamento;
- técnica de simulação;
- restrição metodológica;
- procedimento de cálculo;
- procedimento de decisão.

O objeto não precisa possuir fórmula matemática. Regras de comparabilidade, deduplicação, saturação, brand safety e qualidade de entrega são conhecimentos computáveis mesmo quando não assumem uma única expressão algébrica.

---

## 5. Três camadas do conhecimento

Cada domínio técnico poderá possuir três camadas complementares.

### 5.1 Camada conceitual

Define:

- significado;
- finalidade;
- objeto observado;
- domínio de aplicação;
- relação com outros conceitos;
- interpretação geral;
- limitações conceituais.

### 5.2 Camada matemática

Define, quando aplicável:

- variáveis;
- unidades;
- fórmula principal;
- fórmulas derivadas;
- equivalências;
- transformações;
- conversões;
- precisão;
- arredondamento.

### 5.3 Camada operacional

Define:

- quando utilizar;
- quando não utilizar;
- pré-condições;
- dados mínimos;
- comparabilidade;
- tratamento de ausência e zero;
- restrições;
- alertas;
- regras de decisão;
- interpretação contextual.

```text
Conceito
    ↓
Modelo matemático
    ↓
Regras operacionais
    ↓
Aplicação pelos motores
```

---

## 6. Tipos canônicos de objeto

Tipos iniciais:

```text
CONCEITO_TECNICO
DEFINICAO_OPERACIONAL
FORMULA_DIRETA
FORMULA_INVERSA
FORMULA_DERIVADA
EQUIVALENCIA
CONVERSAO
REGRA_CONDICIONAL
REGRA_DE_VALIDACAO
REGRA_DE_COMPARABILIDADE
REGRA_DE_INTERPRETACAO
TECNICA_DE_PLANEJAMENTO
TECNICA_DE_SIMULACAO
PROCEDIMENTO_DE_CALCULO
PROCEDIMENTO_DE_DECISAO
RESTRICAO_METODOLOGICA
```

Um mesmo domínio, como GRP, poderá ser composto por vários objetos relacionados.

```text
GRP
 ├── conceito
 ├── cálculo por inserções e audiência
 ├── relação com alcance e frequência
 ├── conversão para impactos
 ├── comparação por CPP
 ├── restrição de comparabilidade
 └── interpretação da pressão de mídia
```

---

## 7. Estrutura canônica do objeto

Cada objeto deverá conter, conforme aplicável:

```text
id
codigo
nome
tipo
status
dominio_tecnico
familia_tecnica
definicao
finalidade
logica_operacional
expressao_matematica
variaveis_de_entrada
variavel_de_saida
unidades_de_entrada
unidade_de_saida
pre_condicoes
condicoes_de_validade
regras_de_comparabilidade
restricoes
excecoes
tratamento_de_zero
tratamento_de_ausencia
precisao
arredondamento
interpretacao
alertas
objetos_relacionados
indicadores_relacionados
tipologias_de_midia_aplicaveis
exemplo_resolvido
fonte
pagina_ou_secao
validade
confianca_metodologica
versao
criado_em
atualizado_em
```

Campos não aplicáveis devem ser nulos, e não preenchidos artificialmente.

---

## 8. Fontes e método de incorporação

A Biblioteca será construída progressivamente a partir de:

- aulas e materiais didáticos do projeto;
- manuais de veículos;
- glossários técnicos;
- documentos do IAB e outras entidades do setor;
- bibliografia de planejamento e pesquisa de mídia;
- documentação de plataformas;
- normas e padrões de mensuração;
- decisões metodológicas consolidadas no MediAd Planner.

Cada conhecimento incorporado deve preservar:

- fonte;
- edição ou versão;
- página ou seção, quando disponível;
- data de consulta ou incorporação;
- interpretação adotada;
- divergências entre fontes;
- grau de confiança.

A Biblioteca não deve converter automaticamente uma definição encontrada em fonte externa em regra universal. Divergências terminológicas e metodológicas devem permanecer registradas.

---

## 9. Famílias técnicas iniciais

### 9.1 Audiência, universo e impactos

Inclui conhecimentos sobre:

- universo;
- audiência absoluta;
- audiência percentual;
- audiência domiciliar;
- audiência individual;
- audiência do público-alvo;
- impactos;
- conversões entre valores absolutos e percentuais;
- bases e períodos de referência.

### 9.2 Perfil, qualificação e afinidade

Inclui:

- perfil vertical;
- composição da audiência;
- qualificação do meio;
- qualificação do veículo;
- índice de afinidade;
- comparação com a população de referência;
- condições de interpretação de valores acima, iguais ou abaixo de 100.

### 9.3 Alcance, frequência e pressão

Inclui:

- alcance absoluto;
- alcance percentual;
- alcance líquido;
- alcance acumulado;
- alcance incremental;
- frequência média;
- distribuição de frequência;
- frequência eficiente;
- OTS;
- pressão de mídia;
- repetição;
- saturação.

### 9.4 GRP, TRP e relações derivadas

Inclui:

- soma dos pontos de audiência;
- cálculo por programa e inserções;
- GRP da programação;
- TRP ou TARP;
- relação GRP–alcance–frequência;
- conversão em impactos;
- intensidade de comunicação;
- condições para análise multimídia;
- limitações de interpretação isolada.

### 9.5 Custos, negociação e eficiência

Inclui:

- custo bruto;
- custo líquido;
- desconto;
- comissão;
- custo unitário;
- investimento total;
- CPP;
- CPM;
- CPC;
- CPA;
- CPL;
- CPV;
- custo por alcance;
- custo por impacto;
- comparação de rentabilidade;
- diferenças de denominador entre mídias.

### 9.6 Participação e competitividade

Inclui:

- Share of Market;
- Share of Voice;
- Share of Spend;
- Share of Search;
- BDI;
- CDI;
- presença relativa;
- investimento relativo;
- desempenho territorial;
- relações entre marca, categoria, praça e concorrência.

### 9.7 Digital, programática e performance

Inclui:

- impressões servidas;
- impressões visíveis;
- viewability;
- cliques;
- CTR;
- conversões;
- taxas de conversão;
- frequência digital;
- alcance único;
- deduplicação;
- atribuição;
- uplift;
- bid;
- win rate;
- preço de reserva;
- qualidade de entrega;
- tráfego inválido;
- GIVT e SIVT;
- brand safety;
- listas de inclusão e exclusão;
- RTB;
- relações entre DSP, SSP, ad exchange e inventário.

### 9.8 Distribuição temporal e programação

Inclui:

- inserções;
- exibições;
- faces;
- ocupação;
- continuidade;
- concentração;
- dispersão;
- flight contínuo;
- ondas;
- pulsação;
- distribuição temporal;
- distribuição geográfica;
- flow-chart.

### 9.9 Sobreposição, deduplicação e alcance combinado

Inclui:

- superposição de audiência;
- duplicação;
- alcance líquido combinado;
- alcance incremental;
- frequência incremental;
- sobreposição entre meios;
- sobreposição entre veículos;
- mesma praça;
- praças distintas;
- deduplicação cross-media;
- limitações de soma direta.

### 9.10 Saturação e rendimento marginal

Inclui:

- frequência ótima;
- frequência máxima útil;
- ponto de saturação;
- rendimento marginal decrescente;
- curva de saturação;
- penalização por excesso;
- limites configuráveis;
- diferenças por público, objetivo, meio e formato.

### 9.11 Regras de comparação e decisão

Inclui:

- menor CPP;
- menor CPM;
- maior afinidade;
- maior alcance incremental;
- eficiência relativa;
- comparação dentro do mesmo universo;
- comparação após conversão de base;
- dominância;
- ordenação;
- empate técnico;
- alternativas incomparáveis;
- filtros obrigatórios e excludentes.

---

## 10. Relação entre conhecimento e indicador

Um indicador poderá depender de vários objetos.

Exemplo:

```text
Indicador: GRP
        ↕
CONCEITO_DE_GRP
CALCULO_DE_GRP_POR_PROGRAMACAO
RELACAO_GRP_ALCANCE_FREQUENCIA
CONVERSAO_DE_GRP_EM_IMPACTOS
VALIDACAO_DE_COMPARABILIDADE
INTERPRETACAO_DA_PRESSAO_DE_MIDIA
```

Um objeto também poderá servir a vários indicadores.

Exemplo:

```text
REGRA_DE_DEDUPLICACAO_CROSS_MEDIA
        ↕
alcance líquido
frequência média
alcance incremental
impactos únicos
```

---

## 11. Fórmulas e variantes

Uma fórmula não deve ser tratada como universal quando o mercado utiliza variantes.

Cada fórmula deverá declarar:

- domínio;
- variante;
- convenção;
- unidade;
- denominador;
- numerador;
- base populacional;
- período;
- condição de uso;
- fonte.

Exemplo conceitual:

```text
CPM tradicional
custo da inserção ou programação
÷ audiência absoluta ou impactos
× 1.000
```

```text
CPM digital
investimento
÷ impressões servidas ou válidas
× 1.000
```

As duas variantes possuem forma algébrica semelhante, mas não podem ser equiparadas sem verificar o significado do denominador.

---

## 12. Fórmulas diretas, inversas e derivadas

A Biblioteca deverá registrar relações matemáticas navegáveis.

Exemplo:

```text
frequencia_media = impactos ÷ alcance_absoluto
```

```text
impactos = alcance_absoluto × frequencia_media
```

```text
GRP = alcance_percentual × frequencia_media
```

```text
frequencia_media = GRP ÷ alcance_percentual
```

Cada transformação deve possuir objeto próprio ou vínculo formal com a fórmula de origem, para que as dependências e condições de validade permaneçam explícitas.

---

## 13. Regras de comparabilidade

A comparação somente é válida quando as bases forem compatíveis ou tiverem sido convertidas por procedimento reconhecido.

Os motores devem verificar, conforme o caso:

- universo;
- público;
- praça;
- período;
- unidade;
- metodologia;
- fonte;
- nível de deduplicação;
- definição de exposição;
- validade da entrega;
- qualidade dos dados.

Estados canônicos:

```text
COMPARAVEL_DIRETAMENTE
COMPARAVEL_APOS_CONVERSAO
COMPARAVEL_COM_RESSALVA
NAO_COMPARAVEL
DADOS_INSUFICIENTES
```

Uma operação classificada como `NAO_COMPARAVEL` não deve participar de ordenação numérica como se fosse equivalente às demais.

---

## 14. Regras de validação

Antes de executar uma fórmula, o sistema deverá validar:

- presença das variáveis obrigatórias;
- unidade correta;
- valores não negativos, quando aplicável;
- denominador diferente de zero;
- intervalo admissível;
- compatibilidade do universo;
- compatibilidade temporal;
- aplicabilidade à tipologia de mídia;
- versão metodológica.

Resultado da validação:

```text
VALIDO
VALIDO_COM_ALERTA
INVALIDO
INDETERMINADO
```

---

## 15. Tratamento de zero, ausência e inconsistência

O sistema deve distinguir:

```text
ZERO_OBSERVADO
ZERO_CALCULADO
NAO_APLICAVEL
NAO_INFORMADO
DADO_INDISPONIVEL
DADO_INVALIDO
DIVISAO_POR_ZERO
```

Ausência de dado não pode ser convertida automaticamente em zero.

Uma fórmula não executada por ausência de entrada deve produzir estado próprio, e não resultado numérico artificial.

---

## 16. Interpretação

Todo cálculo deve poder retornar, além do valor:

- significado técnico;
- unidade;
- contexto;
- faixa interpretativa, quando houver;
- comparação permitida;
- limitações;
- alertas;
- confiança;
- objetos utilizados.

Exemplo:

```text
Resultado: 210 GRP
Interpretação: soma bruta de 210 pontos de audiência na programação
Alerta: o valor não informa isoladamente alcance líquido
Dependência: distribuição de frequência não disponível
```

---

## 17. Confiança metodológica e confiança do cálculo

Devem ser separadas:

```text
confianca_metodologica
```

Robustez do objeto de conhecimento e das fontes que o sustentam.

```text
confianca_do_calculo
```

Robustez da aplicação concreta, considerando qualidade das entradas, completude, comparabilidade e número de inferências.

Uma fórmula metodologicamente consolidada pode gerar um cálculo de baixa confiança quando aplicada a dados frágeis.

---

## 18. Relação com a Tradução Estratégica

A Tradução Estratégica utiliza esta Biblioteca para:

- converter escalas;
- compor pontuações;
- normalizar pesos;
- aplicar penalizações;
- verificar mínimos obrigatórios;
- ordenar relações;
- calcular confiança;
- registrar explicações.

As fórmulas de propagação e composição estratégica também são objetos de conhecimento técnico, mas devem permanecer separadas das fórmulas de mercado de mídia por família e domínio.

---

## 19. Relação com a Biblioteca de Inventários

A Biblioteca de Inventários declara propriedades, disponibilidades, unidades comerciais, capacidades analíticas e dados existentes.

A Biblioteca de Conhecimento Técnico declara como esses dados podem ser utilizados.

```text
Inventário fornece entradas e capacidades
        ↓
Conhecimento Técnico valida e calcula
        ↓
Motor compara e simula
```

Um inventário não deve conter fórmulas próprias duplicadas. Ele deve referenciar os objetos técnicos aplicáveis.

---

## 20. Relação com os motores

Cada execução deverá registrar:

```text
motor
operacao_solicitada
objeto_de_conhecimento
versao_do_objeto
entradas
fontes_das_entradas
validacoes
formula_ou_regra_aplicada
resultado_bruto
resultado_arredondado
unidade
interpretacao
alertas
confianca
executado_em
```

O resultado deve ser reproduzível para o mesmo conjunto de entradas, regras e versões.

---

## 21. Ajustes e decisões humanas

O planejador poderá:

- selecionar variante metodológica permitida;
- ajustar parâmetro configurável;
- rejeitar aplicação sugerida;
- escolher entre objetos equivalentes;
- informar dado externo;
- registrar exceção.

O ajuste não pode apagar:

- valor padrão;
- regra selecionada pelo sistema;
- resultado calculado original;
- alerta emitido;
- versão utilizada.

Toda intervenção relevante exige justificativa e rastreabilidade.

---

## 22. Versionamento

Objetos de conhecimento são versionados independentemente.

Mudanças que exigem nova versão incluem:

- alteração da fórmula;
- alteração do significado das variáveis;
- mudança de unidade;
- mudança de condição de validade;
- inclusão ou remoção de restrição;
- nova fonte normativa;
- mudança de interpretação;
- alteração relevante de arredondamento.

Planos existentes devem preservar snapshot ou referência imutável à versão utilizada.

---

## 23. Modelo lógico mínimo

```text
objetos_conhecimento_tecnico
tipos_objeto_conhecimento
dominios_tecnicos
familias_tecnicas
objetos_variaveis
variaveis_tecnicas
unidades
objetos_formulas
formulas_variantes
objetos_regras
objetos_pre_condicoes
objetos_restricoes
objetos_interpretacoes
objetos_fontes
objetos_relacoes
objetos_indicadores
objetos_tipologias
execucoes_tecnicas
execucoes_entradas
execucoes_validacoes
execucoes_resultados
```

Não será criada uma tabela única genérica para todos os componentes internos. Fórmulas, variáveis, regras, fontes e execuções devem possuir estruturas próprias quando seus atributos forem distintos.

---

## 24. Inventário inicial de conhecimentos a extrair

A primeira rodada de incorporação deve contemplar, no mínimo:

- audiência absoluta e percentual;
- impactos;
- perfil e afinidade;
- alcance absoluto, percentual e acumulado;
- frequência média e eficiente;
- GRP e TRP;
- relação GRP–alcance–frequência;
- CPP e CPM;
- pressão de mídia e OTS;
- SOV e Share of Spend;
- BDI e CDI;
- superposição e alcance combinado;
- saturação;
- flight e distribuição temporal;
- CTR e taxa de conversão;
- CPC, CPA, CPL e CPV;
- viewability;
- tráfego inválido;
- brand safety;
- regras de deduplicação cross-media;
- comparabilidade multimídia;
- regras de precisão e arredondamento.

Esse inventário inicial não encerra a Biblioteca. Novos objetos serão incorporados conforme as fontes forem examinadas e os motores forem especificados.

---

## 25. Decisões consolidadas

1. O nome canônico é Biblioteca de Conhecimento Técnico.
2. O subtítulo explicita lógicas, cálculos, fórmulas, regras e técnicas de planejamento de mídia.
3. A Biblioteca 17 não recadastra indicadores e KPIs.
4. A unidade básica é o Objeto de Conhecimento Técnico.
5. Cada domínio pode possuir camadas conceitual, matemática e operacional.
6. Nem todo objeto possui fórmula.
7. Fórmulas sem contexto, validade e interpretação não são executáveis.
8. Os motores consultam objetos versionados, e não expressões fixas embutidas no fluxo.
9. Variantes metodológicas devem permanecer distintas.
10. Comparabilidade deve ser validada antes de qualquer ordenação.
11. Ausência de dado não equivale a zero.
12. Confiança metodológica e confiança do cálculo são diferentes.
13. Todo cálculo deve ser reproduzível e rastreável.
14. Ajustes humanos não apagam os resultados originais.
15. O inventário de conhecimentos será construído progressivamente a partir das fontes didáticas e profissionais.

---

## 26. Princípio consolidado

> A Biblioteca 15 define o que o planejamento pretende observar. A Biblioteca 17 formaliza o conhecimento técnico necessário para calcular, transformar, validar, comparar e interpretar. Seu conteúdo não é um espelho de indicadores, mas uma base estruturada de conceitos, modelos matemáticos, regras operacionais, técnicas e restrições que permite aos motores raciocinar sobre mídia de forma explicável, reproduzível e versionada.
