# Núcleo 2 — Alcance e Frequência

**Documento:** `17D_NUCLEO_2_ALCANCE_E_FREQUENCIA.md`  
**Documento principal:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Protocolo:** `17B_PROTOCOLO_DE_FORMALIZACAO_DOS_OBJETOS_DE_CONHECIMENTO_TECNICO.md`  
**Núcleo anterior:** `17C_NUCLEO_1_UNIVERSO_E_AUDIENCIA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em validação  
**Última revisão:** 29/07/2026  
**Natureza:** Conjunto de Objetos de Conhecimento Técnico

---

## 1. Finalidade

Este documento formaliza o núcleo técnico de alcance e frequência sem criar micro-objetos para cada variação terminológica, regra auxiliar ou interpretação.

O núcleo utiliza quatro objetos principais:

```text
KT_CONCEITO_ALCANCE
KT_CALCULO_ALCANCE_PERCENTUAL
KT_CONCEITO_FREQUENCIA_MEDIA
KT_CALCULO_FREQUENCIA_MEDIA
```

Validações de universo, tratamento de zero, interpretação e alertas permanecem como componentes internos desses objetos ou reutilizam `KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO`, formalizado no Núcleo 1.

A ordem metodológica é:

```text
Definir o universo
    ↓
Identificar pessoas ou unidades distintas atingidas
    ↓
Calcular alcance absoluto ou percentual
    ↓
Relacionar exposições totais ao alcance líquido
    ↓
Calcular e interpretar a frequência média
```

---

# 2. KT_CONCEITO_ALCANCE

## 2.1 Identificação

```text
codigo: KT_CONCEITO_ALCANCE
nome: Conceito técnico de alcance
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: ALCANCE_E_FREQUENCIA
familia_tecnica: COBERTURA_DE_PUBLICO
status: EM_VALIDACAO
versao: 1.0.0
```

## 2.2 Definição

Alcance é a quantidade ou proporção de unidades distintas de um universo que tiveram pelo menos uma oportunidade de exposição ou contato, conforme a metodologia declarada, em determinado território e período.

A unidade normalmente é pessoa, domicílio, usuário, dispositivo ou outra unidade deduplicada explicitamente definida.

## 2.3 Finalidade

Representar a extensão líquida da cobertura de uma ação, programação, veículo, meio ou combinação de alternativas.

## 2.4 Formas de representação

```text
alcance_absoluto
alcance_percentual
```

As expressões abaixo permanecem como qualificadores do mesmo domínio, e não como objetos autônomos nesta etapa:

```text
alcance_liquido
alcance_acumulado
alcance_incremental
alcance_projetado
alcance_realizado
```

Elas somente serão separadas futuramente se exigirem método de cálculo, validade ou execução realmente independentes.

## 2.5 Entradas conceituais

```text
unidades_distintas_atingidas
universo_correspondente
criterio_de_exposicao
regra_de_deduplicacao
territorio
periodo
publico_ou_target
fonte
metodologia
```

## 2.6 Saída

Quantidade absoluta ou percentual de unidades distintas atingidas pelo menos uma vez.

## 2.7 Condições de validade

- O universo deve estar definido.
- A unidade populacional deve ser conhecida.
- A regra de deduplicação deve ser declarada.
- O critério mínimo de exposição ou contato deve estar definido.
- Território, período, público e metodologia devem estar identificados.
- Em combinações de veículos ou meios, deve existir procedimento de deduplicação reconhecido.

## 2.8 Restrições

- Alcance não é soma de audiências ou impressões.
- Alcance não é impactos.
- Alcance não informa quantas vezes cada unidade foi exposta.
- A soma de alcances de alternativas distintas geralmente superestima o alcance combinado.
- Alcances obtidos por metodologias incompatíveis não devem ser combinados diretamente.
- Dispositivos únicos não equivalem necessariamente a pessoas únicas.

## 2.9 Interpretação

Alcance responde prioritariamente à pergunta:

> Quantas unidades distintas do universo foram atingidas pelo menos uma vez?

Um alcance de 60% significa que seis em cada dez unidades do universo declarado foram atingidas ao menos uma vez segundo a metodologia utilizada. Não informa a distribuição das exposições entre essas unidades.

## 2.10 Relações

```text
DEPENDE_DE → KT_CONCEITO_UNIVERSO
VALIDADO_POR → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
CALCULADO_POR → KT_CALCULO_ALCANCE_PERCENTUAL
COMPLEMENTA → KT_CONCEITO_FREQUENCIA_MEDIA
DIFERENTE_DE → KT_CONCEITO_IMPACTOS
```

## 2.11 Fontes e confiança

```text
fonte: inventário preliminar e decisões metodológicas do MediAd Planner
confianca_metodologica: ALTA
```

---

# 3. KT_CALCULO_ALCANCE_PERCENTUAL

## 3.1 Identificação

```text
codigo: KT_CALCULO_ALCANCE_PERCENTUAL
nome: Cálculo do alcance percentual
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA]
dominio_tecnico: ALCANCE_E_FREQUENCIA
familia_tecnica: COBERTURA_DE_PUBLICO
status: EM_VALIDACAO
versao: 1.0.0
```

## 3.2 Finalidade

Converter alcance absoluto deduplicado em percentual do universo correspondente.

## 3.3 Fórmula

```text
alcance_percentual = alcance_absoluto / universo_correspondente × 100
```

## 3.4 Variáveis

```text
alcance_absoluto: quantidade de unidades distintas atingidas
universo_correspondente: total de unidades elegíveis da mesma base
alcance_percentual: proporção percentual atingida
```

## 3.5 Unidades

```text
alcance_absoluto: pessoas, domicílios, usuários ou unidade definida
universo_correspondente: mesma unidade do alcance absoluto
alcance_percentual: percentual
```

## 3.6 Condições de validade

- `universo_correspondente > 0`.
- `alcance_absoluto >= 0`.
- `alcance_absoluto <= universo_correspondente`, salvo metodologia explicitamente justificada.
- Alcance e universo devem possuir a mesma unidade, público, território, período e metodologia.
- O alcance absoluto deve ser deduplicado.

## 3.7 Tratamento de zero e ausência

```text
universo_correspondente = 0 → DIVISAO_POR_ZERO / cálculo bloqueado
alcance_absoluto = 0 → alcance_percentual = 0
alcance_absoluto ausente → NAO_INFORMADO / cálculo não executado
universo ausente → DADO_INDISPONIVEL / cálculo não executado
```

Ausência não deve ser convertida em zero.

## 3.8 Precisão e arredondamento

O cálculo deve preservar precisão interna superior à apresentada. O arredondamento é uma propriedade de exibição e deve ser configurável, com padrão inicial de duas casas decimais.

## 3.9 Alertas

- `O alcance informado não possui regra de deduplicação identificada.`
- `O alcance absoluto excede o universo declarado.`
- `Alcance e universo utilizam unidades incompatíveis.`
- `O percentual calculado não pode ser combinado diretamente com outro alcance sem validação metodológica.`

## 3.10 Exemplo

```text
alcance_absoluto = 30.000 pessoas
universo_correspondente = 50.000 pessoas

alcance_percentual = 30.000 / 50.000 × 100
alcance_percentual = 60%
```

## 3.11 Relações

```text
CALCULA → KT_CONCEITO_ALCANCE
DEPENDE_DE → KT_CONCEITO_UNIVERSO
VALIDADO_POR → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
FORNECE_ENTRADA_PARA → KT_CALCULO_FREQUENCIA_MEDIA
```

## 3.12 Fontes e confiança

```text
fonte: inventário preliminar de conhecimentos técnicos
confianca_metodologica: ALTA
```

---

# 4. KT_CONCEITO_FREQUENCIA_MEDIA

## 4.1 Identificação

```text
codigo: KT_CONCEITO_FREQUENCIA_MEDIA
nome: Conceito técnico de frequência média
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: ALCANCE_E_FREQUENCIA
familia_tecnica: REPETICAO_DE_EXPOSICAO
status: EM_VALIDACAO
versao: 1.0.0
```

## 4.2 Definição

Frequência média é a média de exposições ou oportunidades de contato recebidas pelas unidades distintas que compõem o alcance líquido, em determinado período, território, público e metodologia.

## 4.3 Finalidade

Representar a intensidade média de repetição entre as unidades efetivamente atingidas.

## 4.4 Entradas conceituais

```text
impactos_ou_exposicoes_totais
alcance_absoluto_deduplicado
periodo
territorio
publico_ou_target
criterio_de_exposicao
fonte
metodologia
```

## 4.5 Saída

Número médio de exposições por unidade distinta atingida.

## 4.6 Condições de validade

- Impactos e alcance devem referir-se ao mesmo público, universo, território, período e critério de exposição.
- O alcance deve ser líquido e maior que zero.
- As unidades devem ser compatíveis.
- Em combinações multimídia, impactos e alcance devem utilizar deduplicação coerente.

## 4.7 Restrições

- Frequência média não representa a frequência recebida por cada indivíduo.
- Não informa a distribuição de frequência.
- Não comprova frequência eficiente.
- Não identifica isoladamente saturação.
- Não deve ser somada entre veículos ou meios.
- Não equivale ao número de inserções.

## 4.8 Interpretação

Uma frequência média de 3 indica que o total de exposições equivale, em média, a três exposições para cada unidade distinta alcançada. Algumas unidades podem ter recebido uma exposição e outras, muitas mais.

As seguintes noções permanecem relacionadas, mas não são objetos autônomos neste núcleo:

```text
distribuicao_de_frequencia
frequencia_eficiente
frequencia_minima
frequencia_excessiva
saturacao
```

Elas serão formalizadas somente quando os problemas técnicos e os motores exigirem métodos próprios.

## 4.9 Relações

```text
DEPENDE_DE → KT_CONCEITO_IMPACTOS
DEPENDE_DE → KT_CONCEITO_ALCANCE
CALCULADO_POR → KT_CALCULO_FREQUENCIA_MEDIA
COMPLEMENTA → KT_CONCEITO_ALCANCE
```

## 4.10 Fontes e confiança

```text
fonte: inventário preliminar e decisões metodológicas do MediAd Planner
confianca_metodologica: ALTA
```

---

# 5. KT_CALCULO_FREQUENCIA_MEDIA

## 5.1 Identificação

```text
codigo: KT_CALCULO_FREQUENCIA_MEDIA
nome: Cálculo da frequência média
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA, FORMULA_DERIVADA]
dominio_tecnico: ALCANCE_E_FREQUENCIA
familia_tecnica: REPETICAO_DE_EXPOSICAO
status: EM_VALIDACAO
versao: 1.0.0
```

## 5.2 Finalidade

Calcular a quantidade média de exposições por unidade distinta alcançada.

## 5.3 Fórmula principal

```text
frequencia_media = impactos_ou_exposicoes_totais / alcance_absoluto
```

A relação derivada abaixo pertence ao mesmo objeto enquanto utilizar as mesmas condições metodológicas:

```text
frequencia_media = GRP / alcance_percentual
```

Não será criado objeto separado apenas para essa transformação, salvo se a implementação futura exigir versionamento ou validações independentes.

## 5.4 Variáveis

```text
impactos_ou_exposicoes_totais: total bruto de exposições, admitindo repetição
alcance_absoluto: quantidade de unidades distintas atingidas
GRP: soma bruta de pontos percentuais de audiência
alcance_percentual: proporção percentual do universo atingida
frequencia_media: número médio de exposições por unidade alcançada
```

## 5.5 Unidades

```text
impactos / alcance absoluto → exposições por unidade atingida
GRP / alcance percentual → frequência média adimensional
```

## 5.6 Condições de validade

### Forma por impactos e alcance absoluto

- `alcance_absoluto > 0`.
- Impactos e alcance devem usar a mesma unidade populacional.
- Devem corresponder ao mesmo público, território, período e critério de exposição.
- O alcance deve ser deduplicado.

### Forma por GRP e alcance percentual

- `alcance_percentual > 0`.
- GRP e alcance devem usar o mesmo universo, target, território, período e metodologia.
- Ambos devem estar expressos em pontos percentuais compatíveis.

## 5.7 Tratamento de zero e ausência

```text
alcance = 0 e impactos = 0 → NAO_APLICAVEL ou frequência zero, conforme o contexto declarado
alcance = 0 e impactos > 0 → INCONSISTENCIA_METODOLOGICA
alcance ausente → cálculo não executado
impactos ou GRP ausente → cálculo não executado
```

O sistema não deve produzir infinito, zero artificial ou valor padrão quando o denominador for zero ou estiver ausente.

## 5.8 Precisão e arredondamento

A frequência deve manter precisão interna suficiente para cálculos posteriores. A exibição pode adotar duas casas decimais, sem alterar o valor bruto armazenado.

## 5.9 Interpretação e alertas

O resultado deve ser acompanhado da mensagem:

```text
A frequência média não descreve a distribuição individual das exposições.
```

Alertas adicionais:

- `Impactos e alcance não utilizam a mesma base populacional.`
- `O alcance não está identificado como líquido ou deduplicado.`
- `GRP e alcance percentual pertencem a períodos ou targets diferentes.`
- `A frequência média não deve ser interpretada automaticamente como frequência eficiente.`

## 5.10 Exemplos

### Por impactos e alcance

```text
impactos = 120.000
alcance_absoluto = 40.000 pessoas

frequencia_media = 120.000 / 40.000
frequencia_media = 3
```

### Por GRP e alcance percentual

```text
GRP = 180
alcance_percentual = 60

frequencia_media = 180 / 60
frequencia_media = 3
```

## 5.11 Relações

```text
CALCULA → KT_CONCEITO_FREQUENCIA_MEDIA
DEPENDE_DE → KT_CONCEITO_IMPACTOS
DEPENDE_DE → KT_CONCEITO_ALCANCE
VALIDADO_POR → KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO
RELACIONA_SE_A → núcleo de GRP
```

## 5.12 Fontes e confiança

```text
fonte: inventário preliminar de conhecimentos técnicos
confianca_metodologica: ALTA
```

---

## 6. Validações integradas do núcleo

As validações abaixo não constituem objetos adicionais neste estágio. São regras internas reutilizáveis pelos quatro objetos principais.

### 6.1 Identidade metodológica

```text
SE público, universo, unidade, território, período ou metodologia forem incompatíveis
ENTAO bloquear cálculo ou combinação
```

### 6.2 Alcance deduplicado

```text
SE o alcance não for líquido ou sua deduplicação for desconhecida
ENTAO permitir apenas uso com alerta ou bloquear, conforme o cálculo
```

### 6.3 Coerência entre impactos e alcance

```text
SE impactos > 0 E alcance = 0
ENTAO classificar como INCONSISTENCIA_METODOLOGICA
```

### 6.4 Limites do alcance percentual

```text
SE alcance_percentual < 0 OU alcance_percentual > 100
ENTAO bloquear, salvo metodologia explicitamente documentada
```

---

## 7. Casos de teste mínimos

### 7.1 Válidos

- alcance absoluto e universo de pessoas, mesma praça e período;
- impactos e alcance líquido do mesmo target;
- GRP e alcance percentual calculados sobre o mesmo universo;
- alcance igual a zero em universo válido;
- frequência média superior a um.

### 7.2 Inválidos

- alcance em pessoas dividido por universo de domicílios;
- soma direta de alcances de dois veículos sem deduplicação;
- frequência calculada com impactos mensais e alcance semanal;
- frequência calculada com alcance zero e impactos positivos;
- GRP do público geral dividido pelo alcance percentual de um target específico;
- alcance percentual superior a 100 sem justificativa metodológica.

---

## 8. Relação com indicadores e problemas

### Indicadores da Biblioteca 15

```text
alcance_absoluto
alcance_percentual
frequencia_media
```

### Problemas da Biblioteca 18

```text
ESTIMAR_ALCANCE
VALIDAR_ALCANCE
ESTIMAR_FREQUENCIA_MEDIA
VALIDAR_FREQUENCIA_MEDIA
COMPARAR_PRESSAO_E_COBERTURA
```

Os nomes dos problemas permanecem provisórios até a revisão sistemática da Biblioteca 18.

---

## 9. Decisões consolidadas

1. Alcance absoluto e percentual pertencem ao mesmo domínio, mas o cálculo percentual permanece formalizado separadamente por possuir execução matemática própria.
2. Alcance líquido, acumulado, incremental, projetado e realizado permanecem como qualificadores, não como novos objetos neste estágio.
3. Frequência média possui um único conceito e um único objeto de cálculo com duas formas matemáticas relacionadas.
4. A fórmula por GRP e alcance não gera novo objeto enquanto não houver necessidade de versionamento independente.
5. Validações e interpretações permanecem integradas aos objetos principais.
6. Distribuição de frequência, frequência eficiente e saturação serão formalizadas apenas diante de necessidade concreta dos motores.
7. O núcleo prioriza sustentabilidade operacional sobre decomposição máxima.

---

## 10. Princípio consolidado

> Alcance descreve quantas unidades distintas foram atingidas; frequência média descreve quantas exposições, em média, corresponderam a cada unidade atingida. Os dois conceitos devem ser interpretados conjuntamente, mas não confundidos. Sua formalização deve preservar universo, deduplicação, período e metodologia sem transformar cada variação em um objeto autônomo.