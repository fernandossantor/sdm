# Primeiro Núcleo de Problemas Técnicos

**Documento:** `18A_PRIMEIRO_NUCLEO_DE_PROBLEMAS_TECNICOS.md`  
**Documento principal:** `18_BIBLIOTECA_DE_PROBLEMAS_TECNICOS_DE_PLANEJAMENTO_DE_MIDIA.md`  
**Biblioteca relacionada:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Status:** Em validação  
**Última revisão:** 29/07/2026  
**Natureza:** Formalização inicial de Objetos de Problema Técnico

---

## 1. Finalidade

Este documento formaliza o primeiro núcleo executável da Biblioteca 18, limitado aos problemas necessários para mobilizar os conhecimentos dos Núcleos 1, 2 e 3 da Biblioteca 17.

O núcleo cobre a sequência:

```text
validar a base
→ calcular ou recuperar audiência
→ calcular impactos
→ estimar alcance e frequência
→ calcular pressão em GRP ou equivalente
→ validar comparabilidade
→ interpretar o resultado
```

Não cria novos indicadores nem novas fórmulas. Organiza problemas decisórios que consultam objetos já formalizados na Biblioteca 17 e indicadores da Biblioteca 15.

---

## 2. Estados canônicos de resultado

Todos os problemas deste núcleo devem utilizar, conforme aplicável, os seguintes estados:

```text
CONCLUIDO
CONCLUIDO_COM_RESSALVA
PARCIAL
NAO_APLICAVEL
NAO_CALCULADO_DADO_AUSENTE
NAO_CALCULADO_DADO_INVALIDO
BLOQUEADO_INCOMPATIBILIDADE
INDETERMINADO
```

### 2.1 Significado

- `CONCLUIDO`: entradas válidas e resposta produzida sem ressalva material.
- `CONCLUIDO_COM_RESSALVA`: resposta tecnicamente utilizável, acompanhada de limitação explícita.
- `PARCIAL`: apenas parte do escopo foi resolvida.
- `NAO_APLICAVEL`: o problema não se aplica ao contexto informado.
- `NAO_CALCULADO_DADO_AUSENTE`: falta ao menos uma entrada obrigatória.
- `NAO_CALCULADO_DADO_INVALIDO`: existe entrada, mas ela viola condição de validade.
- `BLOQUEADO_INCOMPATIBILIDADE`: os dados ou universos não podem ser combinados.
- `INDETERMINADO`: os metadados disponíveis não permitem classificar a situação.

Zero válido nunca deve ser tratado como ausência.

---

# 3. PT_VALIDAR_BASE_POPULACIONAL

```text
codigo: VALIDAR_BASE_POPULACIONAL
nome: Validar base populacional
categoria: VALIDACAO
momento_do_planejamento: PRE_CALCULO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

A base populacional está suficientemente definida e é compatível com o cálculo ou comparação pretendidos?

## Objetivo decisório

Autorizar, condicionar ou bloquear cálculos dependentes de universo.

## Gatilhos

- existência de percentual de audiência, alcance, GRP ou TRP;
- conversão entre percentual e valor absoluto;
- comparação entre veículos, praças, períodos ou públicos;
- agregação de resultados.

## Entradas obrigatórias

```text
tipo_de_unidade
criterios_de_inclusao
territorio
periodo_de_referencia
fonte_ou_metodologia
```

Entradas condicionais:

```text
publico_ou_target
criterios_de_exclusao
valor_populacional
universo_de_comparacao
```

## Conhecimentos aplicáveis

```text
KT_CONCEITO_UNIVERSO: DEFINE, OBRIGATORIO
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO: VALIDA, OBRIGATORIO_QUANDO_HOUVER_COMPARACAO
```

## Procedimento

1. verificar presença dos metadados mínimos;
2. distinguir unidade populacional, território, período e target;
3. quando houver mais de um universo, executar validação de identidade;
4. classificar a compatibilidade;
5. emitir justificativa e restrições.

## Saídas

```text
estado_de_resultado
estado_de_identidade_do_universo
universo_validado
restricoes
mensagem_explicativa
nivel_de_confianca
```

## Critérios de conclusão

- universo definido para uso isolado; ou
- identidade classificada como `IDENTICO`, `COMPATIVEL_APOS_CONVERSAO`, `COMPATIVEL_COM_RESSALVA`, `INCOMPATIVEL` ou `INDETERMINADO`.

---

# 4. PT_CALCULAR_AUDIENCIA_PERCENTUAL

```text
codigo: CALCULAR_AUDIENCIA_PERCENTUAL
nome: Calcular audiência percentual
categoria: DIMENSIONAMENTO
momento_do_planejamento: DIAGNOSTICO_OU_PROJECAO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

Qual proporção do universo correspondente constitui a audiência observada ou estimada?

## Objetivo decisório

Produzir audiência percentual válida para avaliação, comparação e cálculos posteriores.

## Entradas obrigatórias

```text
audiencia_absoluta
universo_correspondente
```

Metadados obrigatórios:

```text
unidade_populacional
territorio
periodo
fonte
metodologia
```

## Conhecimentos aplicáveis

```text
KT_CONCEITO_UNIVERSO: FUNDAMENTA, OBRIGATORIO
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO: VALIDA, OBRIGATORIO
KT_CONCEITO_AUDIENCIA_PERCENTUAL: DEFINE, OBRIGATORIO
KT_CALCULO_AUDIENCIA_PERCENTUAL: CALCULA, OBRIGATORIO
```

## Procedimento

1. executar `VALIDAR_BASE_POPULACIONAL`;
2. confirmar denominador maior que zero;
3. confirmar audiência não negativa e contida no universo;
4. calcular audiência percentual;
5. preservar valor bruto e registrar arredondamento de apresentação.

## Saídas

```text
audiencia_percentual
estado_de_resultado
memoria_de_calculo
alertas
nivel_de_confianca
```

## Bloqueios

- unidade incompatível;
- universo ausente ou igual a zero;
- audiência negativa;
- audiência superior ao universo sem justificativa metodológica.

---

# 5. PT_CALCULAR_PARTICIPACAO_AUDIENCIA

```text
codigo: CALCULAR_PARTICIPACAO_AUDIENCIA
nome: Calcular participação de audiência
categoria: DIMENSIONAMENTO
momento_do_planejamento: DIAGNOSTICO_OU_PROJECAO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

Qual é a participação da audiência observada no universo efetivamente ligado, ativo ou exposto à escolha entre alternativas?

## Objetivo decisório

Distinguir participação de audiência de audiência percentual sobre a população ou universo total.

## Entradas obrigatórias

```text
audiencia_absoluta
universo_ligado_ou_ativo
```

## Conhecimentos aplicáveis

```text
KT_CONCEITO_UNIVERSO: FUNDAMENTA, OBRIGATORIO
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO: VALIDA, OBRIGATORIO
KT_CONCEITO_PARTICIPACAO_AUDIENCIA: DEFINE, OBRIGATORIO
KT_CALCULO_PARTICIPACAO_AUDIENCIA: CALCULA, OBRIGATORIO
```

## Restrições

O denominador deve representar o universo efetivamente ligado ou ativo. Não pode ser substituído pelo universo populacional geral apenas porque os valores estão disponíveis.

## Saídas

```text
participacao_de_audiencia
estado_de_resultado
identidade_do_denominador
memoria_de_calculo
alertas
```

---

# 6. PT_CALCULAR_IMPACTOS

```text
codigo: CALCULAR_IMPACTOS
nome: Calcular impactos brutos
categoria: DIMENSIONAMENTO
momento_do_planejamento: PROJECAO_OU_POS_COMPRA
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

Quantas exposições brutas são produzidas pela programação considerada?

## Objetivo decisório

Quantificar pressão bruta de exposição sem confundi-la com pessoas distintas ou alcance líquido.

## Entradas

Variante A:

```text
audiencia_absoluta_por_insercao
numero_de_insercoes
```

Variante B:

```text
lista_de_audiencias_absolutas_por_ocorrencia
```

## Conhecimentos aplicáveis

```text
KT_CONCEITO_IMPACTOS: DEFINE, OBRIGATORIO
KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES: CALCULA, OBRIGATORIO
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO: VALIDA, OBRIGATORIO
```

## Critério de escolha do procedimento

- usar multiplicação somente quando a audiência for aplicável de forma equivalente a todas as inserções;
- usar soma item a item quando programas, horários, inventários ou audiências variarem.

## Saídas

```text
impactos_brutos
unidade_dos_impactos
variante_utilizada
estado_de_resultado
memoria_de_calculo
alertas
```

## Alertas obrigatórios

```text
Impactos admitem repetição.
Impactos não equivalem a pessoas únicas.
Impactos não equivalem a alcance líquido.
```

---

# 7. PT_ESTIMAR_ALCANCE_E_FREQUENCIA

```text
codigo: ESTIMAR_ALCANCE_E_FREQUENCIA
nome: Estimar alcance e frequência
categoria: DIMENSIONAMENTO
momento_do_planejamento: PROJECAO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

Quantas unidades distintas poderão ser atingidas e quantas exposições médias serão distribuídas entre elas no período?

## Objetivo decisório

Avaliar o equilíbrio entre expansão de cobertura de audiência e repetição da mensagem.

## Entradas condicionais

```text
universo_do_target
impactos_ou_pontos_de_pressao
alcance_absoluto_ou_percentual
frequencia_media
periodo_de_referencia
estado_de_deduplicacao
overlap, quando aplicável
```

## Conhecimentos aplicáveis

```text
KT_CONCEITO_ALCANCE: DEFINE, OBRIGATORIO
KT_CONCEITO_FREQUENCIA_MEDIA: DEFINE, OBRIGATORIO
KT_CALCULO_ALCANCE_PERCENTUAL: CALCULA, CONDICIONAL
KT_CALCULO_FREQUENCIA_MEDIA: CALCULA, CONDICIONAL
KT_VALIDACAO_DEDUPLICACAO: VALIDA, OBRIGATORIO
KT_REGRA_RELACAO_ALCANCE_FREQUENCIA: FUNDAMENTA, OBRIGATORIO
```

## Procedimento

1. validar universo, target e período;
2. classificar o estado de deduplicação;
3. usar cálculo direto quando alcance absoluto e impactos forem válidos;
4. usar relação com pontos de pressão apenas quando a equivalência estiver autorizada;
5. tratar overlap e saturação como condicionantes, não como simples somas;
6. emitir alcance, frequência e limites de interpretação.

## Saídas

```text
alcance_absoluto
alcance_percentual
frequencia_media
estado_de_deduplicacao
estado_de_resultado
restricoes
nivel_de_confianca
```

## Restrições

- frequência média não revela distribuição de frequência;
- alcance de canais diferentes não pode ser somado sem deduplicação;
- inserções, impressões, impactos e frequência não são unidades intercambiáveis;
- o período de referência é obrigatório.

---

# 8. PT_CALCULAR_PRESSAO_DE_MIDIA

```text
codigo: CALCULAR_PRESSAO_DE_MIDIA
nome: Calcular pressão de mídia
categoria: DIMENSIONAMENTO
momento_do_planejamento: PROJECAO_OU_AVALIACAO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

Qual é o volume de pressão publicitária produzido pela programação dentro de uma base comparável?

## Objetivo decisório

Mensurar intensidade de veiculação e apoiar comparação de alternativas sem declarar equivalências não demonstradas.

## Entradas possíveis

```text
audiencias_percentuais_e_insercoes
alcance_percentual_e_frequencia_media
universo_e_impactos
metricas_nativas_de_outros_meios
```

## Conhecimentos aplicáveis

```text
KT_CONCEITO_GRP: DEFINE, CONDICIONAL
KT_CALCULO_GRP_POR_SOMA_DE_AUDIENCIAS: CALCULA, CONDICIONAL
KT_CALCULO_GRP_POR_ALCANCE_E_FREQUENCIA: CALCULA, CONDICIONAL
KT_CONVERSAO_GRP_EM_IMPACTOS: CONVERTE, CONDICIONAL
KT_MODELO_EQUIVALENCIA_MULTIMIDIA: COMPARA, CONDICIONAL
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO: VALIDA, OBRIGATORIO
```

## Saídas

```text
valor_de_pressao
unidade_de_pressao
metodo_utilizado
estado_de_equivalencia
estado_de_resultado
restricoes
memoria_de_calculo
```

## Estados de equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

## Regra central

Pontos de pressão multimídia constituem índice analítico normalizado. Não devem ser apresentados automaticamente como GRP certificado, alcance deduplicado, pessoas únicas, atenção ou efeito.

---

# 9. PT_VALIDAR_COMPARABILIDADE_DE_AUDIENCIA_E_PRESSAO

```text
codigo: VALIDAR_COMPARABILIDADE_DE_AUDIENCIA_E_PRESSAO
nome: Validar comparabilidade de audiência e pressão
categoria: VALIDACAO
momento_do_planejamento: PRE_COMPARACAO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

Os resultados podem ser comparados diretamente, após conversão, com ressalvas ou não podem ser comparados?

## Objetivo decisório

Autorizar ou bloquear comparações entre resultados provenientes de meios, métricas, universos e metodologias diferentes.

## Entradas

Para cada resultado:

```text
metrica_nativa
unidade
universo
publico_ou_target
territorio
periodo
metodologia
estado_de_deduplicacao
natureza_do_valor
fonte
```

## Conhecimentos aplicáveis

```text
KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO: VALIDA, OBRIGATORIO
KT_VALIDACAO_IDENTIDADE_TEMPORAL: VALIDA, OBRIGATORIO
KT_VALIDACAO_IDENTIDADE_TERRITORIAL: VALIDA, OBRIGATORIO
KT_MODELO_EQUIVALENCIA_MULTIMIDIA: COMPARA, OBRIGATORIO_QUANDO_MULTIMIDIA
```

## Procedimento

1. preservar a métrica nativa;
2. validar identidade de universo, território, período e target;
3. identificar a camada comparável:

```text
metrica nativa
→ oportunidade de exposição
→ contato qualificado
→ efeito ou resultado
```

4. classificar a equivalência;
5. impedir soma quando a equivalência não estiver demonstrada;
6. produzir explicação rastreável.

## Saídas

```text
estado_de_comparabilidade
camada_comparavel
conversao_autorizada
restricoes
estado_de_resultado
nivel_de_confianca
```

---

# 10. PT_INTERPRETAR_RESULTADOS_DE_AUDIENCIA_E_PRESSAO

```text
codigo: INTERPRETAR_RESULTADOS_DE_AUDIENCIA_E_PRESSAO
nome: Interpretar resultados de audiência e pressão
categoria: EXPLICACAO_E_DIAGNOSTICO
momento_do_planejamento: POS_CALCULO
status_editorial: EM_VALIDACAO
versao: 1.0.0
```

## Pergunta orientadora

O que o resultado permite afirmar e quais conclusões permanecem proibidas ou indeterminadas?

## Objetivo decisório

Transformar cálculo em resposta técnica explicável, preservando limites metodológicos.

## Entradas

```text
resultado_calculado
unidade
universo
metodologia
estado_de_deduplicacao
estado_de_equivalencia
estado_de_resultado
alertas_do_calculo
```

## Conhecimentos aplicáveis

Todos os objetos efetivamente mobilizados pelo cálculo, acrescidos das regras de interpretação e restrição correspondentes.

## Saídas

```text
afirmacoes_autorizadas
afirmacoes_proibidas
hipoteses
limitacoes
nivel_de_confianca
rastreabilidade
mensagem_para_usuario
```

## Critério de conclusão

A interpretação somente é concluída quando declara:

- o que foi medido ou estimado;
- a unidade e o universo;
- o período;
- a natureza bruta, líquida, deduplicada, estimada ou observada;
- as principais limitações;
- o nível de confiança.

---

## 11. Matriz inicial de encadeamento

| Ordem | Problema | Depende de | Alimenta |
|---|---|---|---|
| 1 | `VALIDAR_BASE_POPULACIONAL` | metadados de universo | todos os cálculos populacionais |
| 2 | `CALCULAR_AUDIENCIA_PERCENTUAL` | base validada | impactos, GRP, comparação |
| 3 | `CALCULAR_PARTICIPACAO_AUDIENCIA` | universo ligado validado | diagnóstico de audiência |
| 4 | `CALCULAR_IMPACTOS` | audiência absoluta e inserções | frequência, pressão, custo |
| 5 | `ESTIMAR_ALCANCE_E_FREQUENCIA` | universo, impactos ou pressão | saturação, mix e avaliação |
| 6 | `CALCULAR_PRESSAO_DE_MIDIA` | audiência, alcance e frequência ou conversão | comparação e programação |
| 7 | `VALIDAR_COMPARABILIDADE_DE_AUDIENCIA_E_PRESSAO` | metadados e resultados | comparação multimídia |
| 8 | `INTERPRETAR_RESULTADOS_DE_AUDIENCIA_E_PRESSAO` | qualquer resultado anterior | explicação e decisão |

---

## 12. Casos mínimos de validação

A próxima revisão deverá testar, para cada problema:

1. caso válido direto;
2. caso válido após conversão;
3. caso válido com ressalva;
4. caso bloqueado por incompatibilidade;
5. caso não calculado por dado ausente;
6. caso com zero válido;
7. caso indeterminado por metadados insuficientes.

Os testes devem abranger, no mínimo:

```text
televisao
radio
digital
OOH e DOOH
impresso
cinema
```

---

## 13. Decisões consolidadas

```text
problema decisorio
≠ formula
≠ indicador
≠ tela
≠ motor
```

```text
comparar pressao
≠ somar alcance
≠ deduplicar pessoas
```

```text
impactos
≠ pessoas unicas
≠ alcance liquido
```

```text
zero valido
≠ dado ausente
```

Este núcleo é suficiente para iniciar a ligação operacional entre as Bibliotecas 15, 17 e 18 sem antecipar a modelagem definitiva do banco ou dos motores especialistas.