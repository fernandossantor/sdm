# Núcleo 1 — Universo e Audiência

**Documento:** `17C_NUCLEO_1_UNIVERSO_E_AUDIENCIA.md`  
**Documento principal:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Protocolo:** `17B_PROTOCOLO_DE_FORMALIZACAO_DOS_OBJETOS_DE_CONHECIMENTO_TECNICO.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em validação  
**Última revisão:** 29/07/2026  
**Natureza:** Conjunto inicial de Objetos de Conhecimento Técnico

---

## 1. Finalidade

Este documento formaliza o primeiro núcleo de Objetos de Conhecimento Técnico da Biblioteca 17.

O núcleo estabelece a base populacional e matemática necessária para cálculos posteriores de audiência, impactos, alcance, frequência, GRP, TRP, afinidade e eficiência.

A ordem metodológica é:

```text
Definir o universo
    ↓
Validar a identidade do universo
    ↓
Definir o fenômeno observado
    ↓
Executar o cálculo aplicável
    ↓
Interpretar o resultado com unidade, contexto e limitações
```

Nenhum percentual de audiência, participação ou impacto deve ser calculado sem que a unidade populacional e o universo correspondente estejam identificados.

---

# 2. KT_CONCEITO_UNIVERSO

## 2.1 Identificação

```text
codigo: KT_CONCEITO_UNIVERSO
nome: Conceito técnico de universo
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: BASE_POPULACIONAL
status: EM_VALIDACAO
versao: 1.0.0
```

## 2.2 Definição

Universo é o conjunto total de unidades elegíveis que constitui a base de referência de uma mensuração, estimativa, proporção, índice ou projeção.

As unidades podem ser, entre outras:

- pessoas;
- domicílios;
- indivíduos de determinado público-alvo;
- usuários cadastrados;
- dispositivos, quando a metodologia assim o definir;
- estabelecimentos;
- veículos;
- fluxos ou oportunidades potenciais, desde que explicitamente definidos.

## 2.3 Finalidade

Fornecer o denominador conceitual e quantitativo que torna percentuais, índices e projeções interpretáveis.

## 2.4 Entradas

Não possui entradas matemáticas obrigatórias. Para uso operacional, requer metadados:

```text
tipo_de_unidade
criterios_de_inclusao
criterios_de_exclusao
territorio
periodo_de_referencia
fonte
metodologia
valor_populacional, quando disponível
```

## 2.5 Saída

Uma definição operacional de universo, com identidade própria e metadados suficientes para comparação.

## 2.6 Condições de validade

O universo somente é considerado definido quando forem conhecidos, no mínimo:

- tipo de unidade;
- critérios de inclusão;
- território;
- período de referência;
- fonte ou origem metodológica.

## 2.7 Restrições

- Um universo de pessoas não é equivalente a um universo de domicílios.
- Um universo total não é equivalente ao universo de aparelhos ligados.
- Um universo de população geral não é equivalente ao universo do público-alvo.
- Um universo estimado para um ano não deve ser tratado como idêntico a outro período sem justificativa.
- A simples igualdade numérica entre dois universos não comprova identidade metodológica.

## 2.8 Interpretação

O universo não representa audiência, alcance ou impactos. Ele representa a base potencial ou de referência sobre a qual essas medidas podem ser calculadas.

## 2.9 Relações

```text
DEFINE → base de audiência percentual
DEFINE → base de alcance percentual
DEFINE → base de GRP e TRP
DEFINE → base de afinidade
DEPENDE_DE → território
DEPENDE_DE → período
DEPENDE_DE → critérios populacionais
```

## 2.10 Fontes e confiança

```text
fonte: inventário preliminar e decisões metodológicas do MediAd Planner
confianca_metodologica: ALTA
```

---

# 3. KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO

## 3.1 Identificação

```text
codigo: KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
nome: Validação da identidade de universo
classe_do_objeto: REGRA_TECNICA
subtipos: [VALIDACAO, COMPARABILIDADE]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: BASE_POPULACIONAL
status: EM_VALIDACAO
versao: 1.0.0
```

## 3.2 Definição

Regra que verifica se dois ou mais valores, percentuais ou cálculos utilizam universos semanticamente e metodologicamente compatíveis.

## 3.3 Finalidade

Impedir cálculos, conversões, somas ou comparações inválidas causadas por diferenças de base populacional.

## 3.4 Entradas

Para cada universo comparado:

```text
tipo_de_unidade
criterios_de_inclusao
criterios_de_exclusao
publico_ou_target
territorio
periodo_de_referencia
fonte
metodologia
valor_populacional
```

## 3.5 Saída

```text
IDENTICO
COMPATIVEL_APOS_CONVERSAO
COMPATIVEL_COM_RESSALVA
INCOMPATIVEL
INDETERMINADO
```

## 3.6 Condição e resultado da regra

### Identidade direta

```text
SE tipo_de_unidade, critérios, público, território, período e metodologia forem equivalentes
ENTAO IDENTICO
```

### Compatibilidade após conversão

```text
SE houver diferença reconhecida e existir procedimento técnico validado de conversão
ENTAO COMPATIVEL_APOS_CONVERSAO
```

### Compatibilidade com ressalva

```text
SE houver pequenas diferenças temporais, territoriais ou metodológicas sem conversão plena
E a comparação permanecer tecnicamente informativa
ENTAO COMPATIVEL_COM_RESSALVA
```

### Incompatibilidade

```text
SE houver diferença de unidade, target, território, período ou metodologia que altere o significado do denominador
E não existir conversão reconhecida
ENTAO INCOMPATIVEL
```

### Indeterminação

```text
SE metadados obrigatórios estiverem ausentes
ENTAO INDETERMINADO
```

## 3.7 Severidade

```text
IDENTICO: INFO
COMPATIVEL_APOS_CONVERSAO: AVISO
COMPATIVEL_COM_RESSALVA: AVISO_RELEVANTE
INCOMPATIVEL: BLOQUEIO
INDETERMINADO: BLOQUEIO_POR_DADOS
```

## 3.8 Mensagens explicativas

Exemplos:

- `Os valores utilizam universos equivalentes.`
- `Os universos podem ser comparados após conversão reconhecida.`
- `A comparação é possível apenas com ressalva metodológica.`
- `Universo de domicílios não pode ser combinado diretamente com universo de pessoas.`
- `Não foi possível validar a identidade de universo por ausência de metadados.`

## 3.9 Restrições

A validação não deve usar apenas o valor numérico do universo. Deve comparar sua identidade semântica e metodológica.

## 3.10 Relações

```text
VALIDA → KT_CALCULO_AUDIENCIA_PERCENTUAL
VALIDA → KT_CALCULO_PARTICIPACAO_AUDIENCIA
VALIDA → KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES
VALIDA → cálculos de alcance, frequência, GRP e TRP
```

## 3.11 Fontes e confiança

```text
fonte: princípios de identidade de universo consolidados no MediAd Planner
confianca_metodologica: ALTA
```

---

# 4. KT_CONCEITO_AUDIENCIA_PERCENTUAL

## 4.1 Identificação

```text
codigo: KT_CONCEITO_AUDIENCIA_PERCENTUAL
nome: Conceito técnico de audiência percentual
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: AUDIENCIA
status: EM_VALIDACAO
versao: 1.0.0
```

## 4.2 Definição

Audiência percentual é a proporção do universo correspondente que foi observada ou estimada como audiência de um veículo, programa, conteúdo, ambiente ou inventário em determinado território e período.

## 4.3 Finalidade

Expressar audiência em uma escala proporcional comparável dentro de uma mesma base populacional.

## 4.4 Entradas conceituais

```text
audiencia_absoluta
universo_correspondente
unidade_populacional
territorio
periodo
fonte
metodologia
```

## 4.5 Saída

Percentual de audiência relativo ao universo declarado.

## 4.6 Condições de validade

- A audiência absoluta e o universo devem possuir a mesma unidade populacional.
- A audiência deve estar contida no universo.
- Território, período e metodologia devem estar declarados.
- O denominador deve ser maior que zero.

## 4.7 Restrições

- Audiência percentual de pessoas não deve ser confundida com audiência domiciliar.
- Não deve ser confundida com participação de audiência.
- Não representa alcance líquido acumulado.
- Não representa impactos.
- Não informa, isoladamente, composição de público ou afinidade.

## 4.8 Interpretação

Um resultado de 12% significa que a audiência observada ou estimada corresponde a 12% do universo declarado, não necessariamente a 12% de toda a população existente.

## 4.9 Relações

```text
DEFINE → indicador audiência percentual da Biblioteca 15
DEPENDE_DE → KT_CONCEITO_UNIVERSO
CALCULADO_POR → KT_CALCULO_AUDIENCIA_PERCENTUAL
DIFERENTE_DE → KT_CONCEITO_PARTICIPACAO_AUDIENCIA
```

## 4.10 Fontes e confiança

```text
fonte: inventário preliminar de conhecimentos técnicos
confianca_metodologica: ALTA
```

---

# 5. KT_CALCULO_AUDIENCIA_PERCENTUAL

## 5.1 Identificação

```text
codigo: KT_CALCULO_AUDIENCIA_PERCENTUAL
nome: Cálculo da audiência percentual
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: AUDIENCIA
status: EM_VALIDACAO
versao: 1.0.0
```

## 5.2 Finalidade

Converter audiência absoluta em percentual do universo correspondente.

## 5.3 Fórmula

```text
audiencia_percentual = audiencia_absoluta / universo_correspondente × 100
```

## 5.4 Variáveis

```text
audiencia_absoluta: quantidade de unidades observadas ou estimadas como audiência
universo_correspondente: total de unidades elegíveis da mesma base
audiencia_percentual: proporção percentual da audiência
```

## 5.5 Unidades

```text
entrada 1: pessoas, domicílios ou outra unidade explicitamente definida
entrada 2: mesma unidade da entrada 1
saida: percentual
```

## 5.6 Condições de validade

- `universo_correspondente > 0`;
- `audiencia_absoluta >= 0`;
- `audiencia_absoluta <= universo_correspondente`, salvo metodologia explicitamente distinta;
- identidade de unidade, território, período e base metodológica;
- validação por `KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO`.

## 5.7 Tratamento de zero

```text
universo = 0 → DIVISAO_POR_ZERO, cálculo bloqueado
audiencia = 0 e universo > 0 → resultado 0%
```

## 5.8 Tratamento de ausência

```text
audiencia ausente → NAO_CALCULADO_DADO_AUSENTE
universo ausente → NAO_CALCULADO_DADO_AUSENTE
metadados insuficientes → INDETERMINADO
```

## 5.9 Precisão e arredondamento

- preservar valor bruto com precisão suficiente para reprodução;
- apresentar por padrão duas casas decimais;
- permitir configuração de exibição sem alterar o valor bruto.

## 5.10 Interpretação

O resultado representa a proporção do universo declarado que integra a audiência no período observado.

## 5.11 Alertas

- `Percentual calculado sobre universo específico; não generalizar para outra população.`
- `Audiência percentual não equivale a participação de audiência.`

## 5.12 Relações

```text
CALCULA → KT_CONCEITO_AUDIENCIA_PERCENTUAL
DEPENDE_DE → KT_CONCEITO_UNIVERSO
DEPENDE_DE → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
```

## 5.13 Fontes e confiança

```text
fonte: formalização do inventário preliminar
confianca_metodologica: ALTA
```

---

# 6. KT_CONCEITO_PARTICIPACAO_AUDIENCIA

## 6.1 Identificação

```text
codigo: KT_CONCEITO_PARTICIPACAO_AUDIENCIA
nome: Conceito técnico de participação de audiência
aliases: [share de audiência, audience share]
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: AUDIENCIA
status: EM_VALIDACAO
versao: 1.0.0
```

## 6.2 Definição

Participação de audiência é a proporção da audiência de um veículo, programa ou conteúdo em relação ao total de unidades que estavam efetivamente consumindo o meio no mesmo período.

## 6.3 Finalidade

Expressar a parcela relativa obtida dentro do consumo efetivamente ativo do meio.

## 6.4 Entradas conceituais

```text
audiencia_absoluta_da_entidade
universo_ligado_ou_ativo
unidade_populacional
periodo
territorio
fonte
metodologia
```

## 6.5 Saída

Percentual de participação no universo ligado ou ativo.

## 6.6 Condições de validade

- numerador e denominador devem utilizar a mesma unidade;
- o denominador deve representar unidades efetivamente ligadas ou ativas;
- período, território e metodologia devem ser equivalentes;
- o universo ligado deve ser maior que zero.

## 6.7 Restrições

- Não utilizar o universo populacional total como denominador, salvo se a metodologia definir participação dessa forma e isso for explicitado.
- Não confundir participação de audiência com audiência percentual.
- Não confundir com Share of Voice, Share of Market ou Share of Spend.

## 6.8 Interpretação

Uma participação de 30% significa que, entre as unidades efetivamente ligadas ou ativas no período, 30% estavam na entidade observada.

## 6.9 Relações

```text
DEPENDE_DE → KT_CONCEITO_UNIVERSO
CALCULADO_POR → KT_CALCULO_PARTICIPACAO_AUDIENCIA
DIFERENTE_DE → KT_CONCEITO_AUDIENCIA_PERCENTUAL
```

## 6.10 Fontes e confiança

```text
fonte: inventário preliminar de conhecimentos técnicos
confianca_metodologica: ALTA
```

---

# 7. KT_CALCULO_PARTICIPACAO_AUDIENCIA

## 7.1 Identificação

```text
codigo: KT_CALCULO_PARTICIPACAO_AUDIENCIA
nome: Cálculo da participação de audiência
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: AUDIENCIA
status: EM_VALIDACAO
versao: 1.0.0
```

## 7.2 Fórmula

```text
participacao_audiencia = audiencia_absoluta_entidade / universo_ligado_ou_ativo × 100
```

## 7.3 Variáveis

```text
audiencia_absoluta_entidade: unidades observadas na entidade
universo_ligado_ou_ativo: total de unidades consumindo o meio no período
participacao_audiencia: percentual relativo ao universo ativo
```

## 7.4 Unidades

```text
entradas: mesma unidade populacional
saida: percentual
```

## 7.5 Condições de validade

- `universo_ligado_ou_ativo > 0`;
- `audiencia_absoluta_entidade >= 0`;
- `audiencia_absoluta_entidade <= universo_ligado_ou_ativo`;
- mesmo território, período, unidade e metodologia;
- validação da identidade de universo.

## 7.6 Tratamento de zero e ausência

```text
universo ativo = 0 → DIVISAO_POR_ZERO, cálculo bloqueado
audiencia da entidade = 0 → resultado 0%
dado ausente → NAO_CALCULADO_DADO_AUSENTE
```

## 7.7 Precisão e arredondamento

- valor bruto preservado;
- apresentação padrão com duas casas decimais.

## 7.8 Interpretação

O resultado informa a participação relativa da entidade entre os consumidores ativos do meio no período.

## 7.9 Alertas

- `O denominador é o universo ligado ou ativo, não a população total.`
- `Não comparar diretamente com audiência percentual sem converter ou contextualizar as bases.`

## 7.10 Relações

```text
CALCULA → KT_CONCEITO_PARTICIPACAO_AUDIENCIA
DEPENDE_DE → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
```

## 7.11 Fontes e confiança

```text
fonte: formalização do inventário preliminar
confianca_metodologica: ALTA
```

---

# 8. KT_CONCEITO_IMPACTOS

## 8.1 Identificação

```text
codigo: KT_CONCEITO_IMPACTOS
nome: Conceito técnico de impactos
aliases: [exposições brutas, contatos brutos]
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: IMPACTOS_E_PRESSAO
status: EM_VALIDACAO
versao: 1.0.0
```

## 8.2 Definição

Impactos representam o total bruto de exposições ou contatos produzidos por uma programação, admitindo repetição da mesma pessoa, domicílio ou unidade de audiência.

## 8.3 Finalidade

Quantificar o volume bruto de exposição gerado por inserções, exibições ou entregas.

## 8.4 Entradas conceituais

Conforme o método:

```text
audiencia_absoluta_por_insercao
numero_de_insercoes
```

ou outras entradas formalizadas em objetos específicos, como universo e GRP.

## 8.5 Saída

Quantidade absoluta de exposições brutas.

## 8.6 Condições de validade

- a unidade da audiência deve estar declarada;
- a programação e o período devem estar delimitados;
- o método deve admitir multiplicação ou soma das exposições;
- alterações de audiência entre inserções devem ser tratadas por cálculo item a item, e não por multiplicação simplificada.

## 8.7 Restrições

- Impactos não equivalem a pessoas distintas.
- Impactos não equivalem a alcance líquido.
- Impactos podem superar o universo devido à repetição.
- Impactos de unidades diferentes não devem ser somados diretamente.
- Impressões digitais podem constituir uma modalidade de impactos, mas exigem definição própria de validade, visibilidade e tráfego inválido.

## 8.8 Interpretação

Um total de 100.000 impactos pode representar 100.000 pessoas expostas uma vez, 10.000 pessoas expostas dez vezes ou qualquer outra distribuição compatível. Sem alcance e distribuição de frequência, não é possível identificar a duplicação.

## 8.9 Relações

```text
DEFINE → indicador impactos da Biblioteca 15
CALCULADO_POR → KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES
RELACIONA_SE_COM → alcance
RELACIONA_SE_COM → frequência
RELACIONA_SE_COM → GRP
DIFERENTE_DE → alcance líquido
```

## 8.10 Fontes e confiança

```text
fonte: inventário preliminar e decisões metodológicas do MediAd Planner
confianca_metodologica: ALTA
```

---

# 9. KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES

## 9.1 Identificação

```text
codigo: KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES
nome: Cálculo de impactos por audiência e inserções
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA]
dominio_tecnico: AUDIENCIA_E_UNIVERSO
familia_tecnica: IMPACTOS_E_PRESSAO
status: EM_VALIDACAO
versao: 1.0.0
```

## 9.2 Finalidade

Calcular exposições brutas quando uma audiência absoluta válida é associada a uma ou mais inserções.

## 9.3 Variante A — audiência constante

```text
impactos = audiencia_absoluta_por_insercao × numero_de_insercoes
```

Esta variante somente é válida quando a mesma audiência absoluta é aplicável a todas as inserções consideradas.

## 9.4 Variante B — audiências variáveis

```text
impactos_totais = soma(audiencia_absoluta_de_cada_insercao)
```

Esta variante deve ser preferida quando inserções, programas, horários ou audiências forem diferentes.

## 9.5 Variáveis

```text
audiencia_absoluta_por_insercao: exposição estimada ou observada por inserção
numero_de_insercoes: quantidade de inserções equivalentes
impactos_totais: soma bruta das exposições
```

## 9.6 Unidades

```text
audiencia: pessoas, domicílios ou outra unidade definida
numero_de_insercoes: contagem inteira não negativa
impactos: mesma unidade da audiência, interpretada como exposições brutas
```

## 9.7 Condições de validade

- audiência absoluta não negativa;
- número de inserções não negativo;
- identidade de unidade, praça, período e target;
- na variante A, equivalência da audiência entre inserções;
- na variante B, cada inserção deve possuir audiência e metadados próprios.

## 9.8 Tratamento de zero

```text
audiencia = 0 → impactos = 0
numero_de_insercoes = 0 → impactos = 0
```

Zero válido deve ser distinguido de dado ausente.

## 9.9 Tratamento de ausência

```text
audiencia ausente → NAO_CALCULADO_DADO_AUSENTE
numero de inserções ausente → NAO_CALCULADO_DADO_AUSENTE
algumas inserções sem audiência → PARCIAL ou cálculo bloqueado, conforme política do problema
```

## 9.10 Precisão e arredondamento

- preservar valor bruto;
- para unidades indivisíveis, apresentar número inteiro;
- quando a audiência for estimativa decimal, manter precisão metodológica e registrar arredondamento.

## 9.11 Interpretação

O resultado é uma soma bruta de exposições. Não representa indivíduos únicos e não revela a distribuição de frequência.

## 9.12 Alertas

- `Impactos admitem repetição da mesma unidade de audiência.`
- `Audiências diferentes entre inserções exigem soma item a item.`
- `Não converter impactos em alcance sem modelo de deduplicação.`

## 9.13 Relações

```text
CALCULA → KT_CONCEITO_IMPACTOS
DEPENDE_DE → audiência absoluta
DEPENDE_DE → inserções
DEPENDE_DE → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
COMPLEMENTA → futura conversão de GRP em impactos
```

## 9.14 Fontes e confiança

```text
fonte: formalização do inventário preliminar
confianca_metodologica: ALTA
```

---

## 10. Relações internas do núcleo

```text
KT_CONCEITO_UNIVERSO
    ↓ DEFINE BASE
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
    ↓ VALIDA
KT_CALCULO_AUDIENCIA_PERCENTUAL
KT_CALCULO_PARTICIPACAO_AUDIENCIA
KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES
```

```text
KT_CONCEITO_AUDIENCIA_PERCENTUAL
    ≠
KT_CONCEITO_PARTICIPACAO_AUDIENCIA
```

```text
KT_CONCEITO_IMPACTOS
    ≠ alcance líquido
    ≠ pessoas distintas
    ≠ frequência
```

---

## 11. Validações pendentes

Antes do estado `FORMALIZADO`, o núcleo deve passar por:

1. revisão terminológica cruzada com as fontes didáticas e profissionais;
2. confirmação das variantes de audiência domiciliar e individual;
3. definição de códigos canônicos para unidades populacionais;
4. modelagem do vínculo entre universo geral, universo do target e universo ligado;
5. validação computacional dos estados de erro e ausência;
6. vinculação aos indicadores correspondentes da Biblioteca 15;
7. vinculação aos primeiros problemas técnicos da Biblioteca 18.

---

## 12. Problemas técnicos candidatos

Os objetos deste núcleo poderão servir, entre outros, aos problemas:

```text
VALIDAR_BASE_POPULACIONAL
CALCULAR_AUDIENCIA_PERCENTUAL
CALCULAR_PARTICIPACAO_AUDIENCIA
CALCULAR_IMPACTOS
CONVERTER_PERCENTUAL_EM_VALOR_ABSOLUTO
VALIDAR_COMPARABILIDADE_DE_AUDIENCIA
INTERPRETAR_VOLUME_BRUTO_DE_EXPOSICAO
```

A formalização definitiva desses problemas pertence à Biblioteca 18.

---

## 13. Princípio consolidado

> Todo cálculo de audiência depende da identidade do universo. Audiência percentual utiliza o universo populacional correspondente; participação de audiência utiliza o universo efetivamente ligado ou ativo; impactos representam exposições brutas e admitem repetição. O MediAd Planner deve preservar essas diferenças antes de calcular, comparar ou interpretar qualquer resultado.