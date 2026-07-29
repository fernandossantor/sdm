# Finalização das Bibliotecas 17 e 18 — Versão 1.0

**Documento:** `17G_18C_FINALIZACAO_DAS_BIBLIOTECAS_17_E_18.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo de encerramento de escopo

---

## 1. Finalidade

Este documento encerra a formalização conceitual das Bibliotecas 17 — Conhecimento Técnico — e 18 — Problemas Técnicos de Planejamento de Mídia — para a versão 1.0 do MediAd Planner.

O encerramento não significa que todos os conhecimentos possíveis do mercado foram catalogados. Significa que:

- a estrutura das bibliotecas está definida;
- os primeiros núcleos necessários aos motores estão formalizados;
- os estados, relações e contratos mínimos foram harmonizados;
- os conteúdos antes previstos para as Bibliotecas 19, 20 e 21 foram absorvidos pela arquitetura existente;
- novas inclusões passam a ocorrer apenas quando exigidas por um motor, problema ou caso de uso real.

---

## 2. Escopo consolidado da Biblioteca 17

A Biblioteca 17 permanece responsável por formalizar conhecimentos reutilizáveis necessários para:

```text
calcular
transformar
validar
comparar
interpretar
explicar
```

Sua unidade básica continua sendo o `objeto_de_conhecimento_tecnico`.

A versão 1.0 considera formalizados os seguintes núcleos:

1. Universo e Audiência;
2. Alcance e Frequência;
3. GRP e Equivalências Multimídia;
4. Contrato Mínimo de Mensuração.

Também fazem parte do escopo, sem exigir novos núcleos autônomos:

- fórmulas econômicas e indicadores de eficiência;
- regras de comparabilidade;
- regras de validade metodológica;
- tratamento de zero, ausência e inconsistência;
- confiança metodológica e confiança do cálculo;
- regras de deduplicação, overlap e saturação;
- referências, versões e proveniência;
- restrições técnicas e comerciais utilizadas nos cálculos.

Esses conteúdos devem ser incorporados como objetos, atributos, variantes ou relações apenas quando houver aplicação demonstrada.

---

## 3. Contrato mínimo da Biblioteca 17

Todo conhecimento executável deve poder declarar, quando aplicável:

```text
codigo
nome
definicao
finalidade
entradas
saida
unidades
condicoes_de_validade
restricoes
tratamento_de_zero_e_ausencia
interpretacao
fontes
versao
confianca_metodologica
```

Os metadados transversais são:

```text
unidade_de_observacao
universo_de_referencia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

Eles devem ser herdados, inferidos ou calculados sempre que possível, sem se converterem em etapas obrigatórias da interface.

---

## 4. Critério de granularidade da Biblioteca 17

Um novo objeto técnico somente deve ser criado quando houver diferença material de:

- significado;
- fórmula;
- universo;
- unidade;
- condição de validade;
- interpretação;
- metodologia;
- versionamento;
- execução independente.

Não justificam novo objeto:

- sinônimos;
- exemplos;
- mensagens ao usuário;
- faixas de apresentação;
- pequenas variações de arredondamento;
- exceções tratáveis por parâmetro;
- classificações editoriais;
- diferenças de interface.

---

## 5. Escopo consolidado da Biblioteca 18

A Biblioteca 18 permanece responsável por organizar perguntas técnicas orientadas à decisão.

A versão 1.0 adota oito famílias estáveis de problemas:

```text
ESTRATEGIA
DIMENSIONAMENTO_E_PROJECAO
COMPARACAO
SELECAO_E_COMPOSICAO
ECONOMIA_E_ORCAMENTO
TEMPO_E_OPERACAO
VALIDACAO
EXPLICACAO_E_DIAGNOSTICO
```

Os problemas iniciais já formalizados cobrem a cadeia mínima:

```text
validar base e dados
→ calcular ou recuperar audiência
→ calcular impactos
→ estimar alcance e frequência
→ calcular pressão
→ validar comparabilidade
→ interpretar e explicar
```

A Biblioteca 18 não deve reproduzir todas as fórmulas da Biblioteca 17. Ela apenas referencia os conhecimentos e procedimentos necessários para cada decisão.

---

## 6. Catálogo funcional mínimo de problemas

Para evitar excesso de granularidade, a versão 1.0 considera suficientes os seguintes problemas canônicos, expansíveis apenas por necessidade comprovada:

### Estratégia

```text
VALIDAR_OBJETIVOS
DERIVAR_OBJETIVOS_DE_MIDIA
PRIORIZAR_RESULTADOS
SELECIONAR_JORNADA_E_FUNCOES
```

### Dimensionamento e projeção

```text
VALIDAR_BASE_POPULACIONAL
CALCULAR_AUDIENCIA_PERCENTUAL
CALCULAR_PARTICIPACAO_AUDIENCIA
CALCULAR_IMPACTOS
ESTIMAR_ALCANCE_E_FREQUENCIA
CALCULAR_PRESSAO_DE_MIDIA
ESTIMAR_OVERLAP_E_ALCANCE_INCREMENTAL
AVALIAR_SATURACAO
```

### Comparação

```text
VALIDAR_COMPARABILIDADE
COMPARAR_ALTERNATIVAS_DE_MIDIA
COMPARAR_CENARIOS
AVALIAR_AFINIDADE
AVALIAR_EFICIENCIA_RELATIVA
```

### Seleção e composição

```text
SELECIONAR_PONTOS_DE_CONTATO
SELECIONAR_INVENTARIOS
DEFINIR_PAPEL_ESTRATEGICO_DOS_CANAIS
COMPOR_ARQUITETURA_DE_MIDIA
```

### Economia e orçamento

```text
VALIDAR_VIABILIDADE_ORCAMENTARIA
CALCULAR_INVESTIMENTOS_E_COMISSAO
DISTRIBUIR_ORCAMENTO
AVALIAR_EFICIENCIA_DE_CUSTO
```

### Tempo e operação

```text
DEFINIR_FLIGHT
DISTRIBUIR_INSERCOES_NO_TEMPO
CONTROLAR_FREQUENCIA_E_SATURACAO
VERIFICAR_DISPONIBILIDADE_E_PRAZOS
```

### Validação

```text
VALIDAR_DADOS_DE_ENTRADA
VALIDAR_IDENTIDADES_DE_BASE
VALIDAR_ELEGIBILIDADE
DETECTAR_INCONSISTENCIAS_E_AUSENCIAS
```

### Explicação e diagnóstico

```text
EXPLICAR_RECOMENDACAO
JUSTIFICAR_SELECAO
DIAGNOSTICAR_LIMITACAO_OU_INVIABILIDADE
EXPRESSAR_NIVEL_DE_CONFIANCA
```

Problemas próximos devem ser tratados como variantes, subproblemas ou procedimentos internos antes de se criar novo código canônico.

---

## 7. Estrutura mínima do problema técnico

Todo problema deve declarar:

```text
codigo
nome
pergunta_orientadora
objetivo_decisorio
categoria
gatilhos
entradas
saidas
pre_condicoes
restricoes
conhecimentos_aplicaveis
procedimentos_possiveis
criterios_de_conclusao
estado_de_resultado
nivel_de_confianca
versao
```

Campos adicionais somente devem ser implementados quando forem usados por um motor ou necessários para rastreabilidade.

---

## 8. Estados harmonizados

### Validação

```text
VALIDO
VALIDO_COM_ALERTA
INVALIDO
INDETERMINADO
```

### Comparabilidade

```text
COMPARAVEL_DIRETAMENTE
COMPARAVEL_APOS_CONVERSAO
COMPARAVEL_COM_RESSALVA
NAO_COMPARAVEL
DADOS_INSUFICIENTES
```

### Resultado de problema

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

### Deduplicação

```text
DEDUPLICADO
PARCIALMENTE_DEDUPLICADO
NAO_DEDUPLICADO
NAO_APLICAVEL
INDETERMINADO
```

### Equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

Esses estados devem ser reutilizados. Não devem ser criados novos estados apenas para adaptar textos de interface.

---

## 9. Relações mínimas para os motores

A implementação deve preservar três relações principais:

```text
indicador_da_biblioteca_15
↔ objeto_de_conhecimento_da_biblioteca_17
```

```text
problema_da_biblioteca_18
↔ objeto_de_conhecimento_da_biblioteca_17
```

```text
problema_da_biblioteca_18
↔ procedimento_de_resolucao
```

Os vínculos podem registrar:

```text
papel
obrigatoriedade
prioridade
condicao_de_uso
ordem_logica
nivel_de_confianca
versao
```

Não é necessário criar uma entidade adicional para cada combinação.

---

## 10. Conteúdos incorporados das antigas Bibliotecas 19, 20 e 21

### Custos e condições comerciais

- os dados cadastrais acompanham produtos e ofertas da Biblioteca 13;
- as fórmulas e interpretações econômicas permanecem na Biblioteca 17;
- os problemas de orçamento e eficiência permanecem na Biblioteca 18.

### Regras e restrições

- regras específicas permanecem junto ao conhecimento, inventário ou problema que condicionam;
- regras transversais podem ser relações compartilhadas, sem biblioteca autônoma;
- referências permanecem como metadados versionados.

### Modelos reutilizáveis

- arquiteturas de referência, flights, cenários, pesos e templates são configurações dos módulos existentes;
- podem ser salvos e reutilizados;
- não constituem uma biblioteca obrigatória nem criam decisões automáticas.

---

## 11. Critério de encerramento

As Bibliotecas 17 e 18 são consideradas formalizadas para a versão 1.0 porque:

1. possuem finalidade, fronteira e unidade básica definidas;
2. possuem contratos mínimos e estados harmonizados;
3. cobrem os conhecimentos e problemas necessários aos primeiros motores;
4. foram testadas em casos de televisão, rádio, digital, OOH/DOOH, impresso, cinema e multimídia;
5. distinguem cálculo, validação, comparabilidade, confiança e interpretação;
6. absorvem custos, regras e modelos sem novas bibliotecas;
7. possuem limites explícitos contra granularidade excessiva;
8. admitem expansão incremental sem alteração da arquitetura.

---

## 12. Política posterior à finalização

A partir deste documento:

- novos conhecimentos somente serão adicionados por demanda comprovada de motor, indicador ou caso de uso;
- novos problemas somente serão criados quando não puderem ser representados por problema existente, variante ou subproblema;
- a interface não reproduzirá a complexidade interna das bibliotecas;
- detalhes técnicos permanecerão em memória de cálculo, explicação e auditoria;
- a próxima etapa estrutural é a especificação dos motores especialistas.

---

## 13. Princípio consolidado

> A Biblioteca 17 deve conter somente o conhecimento necessário para calcular, validar, comparar e interpretar; a Biblioteca 18 deve conter somente os problemas necessários para decidir. Tudo o que puder permanecer como atributo, estado, relação, variante, parâmetro ou procedimento não deve se transformar em novo objeto, nova tela ou nova biblioteca.
