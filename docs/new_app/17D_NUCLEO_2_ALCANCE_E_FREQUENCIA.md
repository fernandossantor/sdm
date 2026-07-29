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

Este núcleo formaliza alcance e frequência sem criar objetos autônomos para cada variação terminológica ou interpretação auxiliar.

Objetos principais:

```text
KT_CONCEITO_ALCANCE
KT_CALCULO_ALCANCE_PERCENTUAL
KT_CONCEITO_FREQUENCIA_MEDIA
KT_CALCULO_FREQUENCIA_MEDIA
```

Ordem metodológica:

```text
Definir universo e unidade
    ↓
Definir critério mínimo de exposição
    ↓
Identificar unidades distintas atingidas
    ↓
Declarar método de deduplicação
    ↓
Calcular alcance
    ↓
Relacionar exposições totais ao alcance
    ↓
Calcular e interpretar frequência média
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
versao: 1.1.0
```

## 2.2 Definição

Alcance é a quantidade ou proporção de unidades distintas de um universo que tiveram pelo menos uma exposição ou oportunidade de contato válida segundo critério e metodologia declarados, em determinado território e período.

A unidade pode ser pessoa, domicílio, usuário, conta, dispositivo ou outra unidade explicitamente definida e deduplicada.

## 2.3 Formas de representação

```text
alcance_absoluto
alcance_percentual
```

Qualificadores do mesmo domínio:

```text
alcance_liquido
alcance_acumulado
alcance_incremental
alcance_projetado
alcance_realizado
alcance_por_meio
alcance_multimidia
```

Esses qualificadores não se tornam objetos independentes enquanto não exigirem fórmula ou validade própria.

## 2.4 Entradas conceituais

```text
unidades_distintas_atingidas
universo_correspondente
unidade_de_identidade
criterio_de_exposicao
regra_de_deduplicacao
estado_de_deduplicacao
territorio
periodo
janela_de_acumulacao
publico_ou_target
fonte
metodologia
```

## 2.5 Estados de deduplicação

```text
DEDUPLICADO_POR_IDENTIDADE
DEDUPLICADO_POR_PAINEL
DEDUPLICADO_POR_MODELO
ESTIMADO_POR_PROXY
NAO_DEDUPLICADO
INDETERMINADO
```

Somente os três primeiros estados podem sustentar alcance combinado sem ressalva estrutural. `ESTIMADO_POR_PROXY` exige confiança e limitações explícitas. `NAO_DEDUPLICADO` não pode ser apresentado como alcance líquido combinado.

## 2.6 Condições de validade

- universo e unidade identificados;
- critério mínimo de exposição definido;
- período, praça e target declarados;
- regra e estado de deduplicação registrados;
- fonte e metodologia identificadas;
- em combinações, procedimento reconhecido para tratar sobreposição.

## 2.7 Restrições

- alcance não é soma de audiências, impressões ou alcances isolados;
- alcance não é impactos;
- dispositivo único não equivale automaticamente a pessoa única;
- cobertura territorial não é alcance de audiência;
- disponibilidade de rede não é alcance de campanha;
- alcance institucional de veículo não é garantia de entrega;
- alcance sem janela temporal não é interpretável;
- alcances de metodologias incompatíveis não devem ser combinados diretamente.

## 2.8 Coberturas que não são alcance

Devem permanecer distintas:

```text
cobertura_territorial_do_inventario
abrangencia_da_programacao
alcance_de_audiencia
```

O termo `cobertura` deve sempre receber qualificador.

## 2.9 Interpretação

Alcance responde:

> Quantas unidades distintas do universo foram atingidas ao menos uma vez segundo a metodologia declarada?

Um alcance de 60% significa que seis em cada dez unidades do universo declarado foram atingidas ao menos uma vez. Não informa a distribuição das exposições.

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
versao: 1.1.0
```

## 3.2 Fórmula

```text
alcance_percentual = alcance_absoluto / universo_correspondente × 100
```

## 3.3 Validações

```text
universo_correspondente > 0
alcance_absoluto >= 0
alcance_absoluto <= universo_correspondente
unidade_alcance = unidade_universo
```

Também devem ser equivalentes público, território, período, janela e metodologia.

## 3.4 Tratamento de ausência

```text
universo = 0 → DIVISAO_POR_ZERO
alcance = 0 observado → 0%
alcance ausente → NAO_INFORMADO
universo ausente → DADO_INDISPONIVEL
regra de deduplicação ausente → CALCULO_BLOQUEADO_POR_METADADOS
```

Ausência não deve ser convertida em zero.

## 3.5 Alertas

- alcance sem deduplicação identificada;
- alcance superior ao universo;
- unidades incompatíveis;
- janela temporal ausente;
- alcance institucional usado como entrega de campanha;
- soma de alcances isolados apresentada como alcance combinado.

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
versao: 1.1.0
```

## 4.2 Definição

Frequência média é a média de exposições ou oportunidades de contato recebidas pelas unidades distintas que compõem o alcance líquido, em determinado período, território, público, critério de exposição e metodologia.

## 4.3 Entradas conceituais

```text
exposicoes_totais_qualificadas
alcance_absoluto_deduplicado
periodo
territorio
publico_ou_target
criterio_de_exposicao
qualificador_da_exposicao
fonte
metodologia
```

## 4.4 Condições de validade

- exposições e alcance devem utilizar mesma unidade, público, território e período;
- o alcance deve ser líquido e maior que zero;
- a definição de exposição deve ser a mesma no numerador e no alcance;
- em multimídia, deduplicação e combinação devem ser metodologicamente coerentes.

## 4.5 Restrições

- frequência média não é frequência individual;
- não informa distribuição de frequência;
- não comprova frequência eficiente;
- não identifica isoladamente saturação;
- não deve ser somada entre veículos;
- não equivale ao número de inserções;
- não deve combinar impressões servidas com alcance baseado em contato visível sem conversão validada.

## 4.6 Limitação interpretativa obrigatória

Duas campanhas podem ter a mesma frequência média e distribuições muito diferentes.

```text
Campanha A:
maior parte das pessoas entre 3 e 5 exposições

Campanha B:
muitas pessoas com 1 exposição
e poucas pessoas com 15 exposições
```

Portanto, a frequência média é uma medida sintética de intensidade, não uma descrição da distribuição.

As noções abaixo permanecem relacionadas, mas não se tornam objetos autônomos nesta etapa:

```text
distribuicao_de_frequencia
frequencia_eficiente
frequencia_minima
frequencia_excessiva
saturacao
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
versao: 1.1.0
```

## 5.2 Fórmula por valores absolutos

```text
frequencia_media = exposicoes_totais / alcance_absoluto
```

## 5.3 Fórmula derivada por GRP

```text
frequencia_media = grp / alcance_percentual
```

A fórmula derivada somente é válida quando GRP e alcance usam o mesmo universo, target, período, território e definição de exposição.

## 5.4 Tratamento de zero e ausência

```text
alcance = 0 e exposicoes = 0 → NAO_APLICAVEL
alcance = 0 e exposicoes > 0 → INCONSISTENCIA
alcance ausente → CALCULO_NAO_EXECUTADO
exposicoes ausentes → CALCULO_NAO_EXECUTADO
```

## 5.5 Saída mínima

```text
frequencia_media
forma_de_calculo
qualificador_da_exposicao
estado_de_deduplicacao
periodo
territorio
publico
fonte
metodologia
confianca
alertas
```

---

## 6. Relação com overlap e saturação

Overlap é dado ou hipótese sobre sobreposição de pessoas entre alternativas. Saturação é avaliação sobre repetição excessiva e retorno marginal.

```text
overlap → influencia alcance combinado
alcance combinado + exposições → influencia frequência
frequência e distribuição → subsidiam saturação
```

Overlap não é frequência, e frequência média não é saturação.

---

## 7. Princípio consolidado

> Alcance mede extensão líquida; frequência média mede intensidade média entre as unidades alcançadas. Ambos dependem de universo, período, critério de exposição e deduplicação coerentes. Cobertura territorial, audiência institucional, impressões e número de inserções não os substituem.