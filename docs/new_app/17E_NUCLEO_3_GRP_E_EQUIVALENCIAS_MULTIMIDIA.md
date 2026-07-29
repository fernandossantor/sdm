# Núcleo 3 — GRP e Equivalências Multimídia

**Documento:** `17E_NUCLEO_3_GRP_E_EQUIVALENCIAS_MULTIMIDIA.md`  
**Documento principal:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Protocolo:** `17B_PROTOCOLO_DE_FORMALIZACAO_DOS_OBJETOS_DE_CONHECIMENTO_TECNICO.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em validação  
**Última revisão:** 29/07/2026  
**Natureza:** Conjunto coeso de Objetos de Conhecimento Técnico

---

## 1. Finalidade

Este núcleo formaliza o GRP como medida de pressão bruta e estabelece equivalências condicionadas entre mídias.

O objetivo não é declarar identidade entre todas as exposições, mas permitir que o MediAd Planner:

- reconheça métricas diretamente expressas em pontos sobre um universo;
- converta exposições brutas em pontos percentuais quando houver base compatível;
- preserve a diferença entre impressão servida, oportunidade de contato, contato ajustado e exposição aferida;
- classifique comparabilidade, conversão e confiança;
- impeça que pontos de pressão sejam tratados como alcance deduplicado ou efeito publicitário.

Princípio central:

```text
mesma forma algébrica
não implica
mesmo significado de exposição
```

---

## 2. Objetos principais

```text
KT_CONCEITO_GRP
KT_CALCULO_GRP
KT_CONVERSAO_GRP_IMPACTOS
KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA
```

Variantes por meio permanecem como regras internas, não como novos objetos ou bibliotecas.

---

# 3. KT_CONCEITO_GRP

## 3.1 Identificação

```text
codigo: KT_CONCEITO_GRP
nome: Conceito técnico de GRP
classe_do_objeto: CONCEITO_TECNICO
subtipos: [DEFINICAO_OPERACIONAL]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: GRP_TRP
status: EM_VALIDACAO
versao: 1.1.0
```

## 3.2 Definição

GRP — Gross Rating Points — representa a soma bruta de pontos percentuais de audiência ou exposição de uma programação em relação a um universo declarado.

Admite repetição da mesma unidade ao longo das exposições e, por isso, não representa alcance líquido.

## 3.3 Unidade

```text
pontos percentuais brutos
```

Um ponto corresponde matematicamente a exposições brutas equivalentes a 1% do universo declarado.

## 3.4 Condições de validade

- universo, unidade, praça e período identificados;
- definição de audiência ou exposição conhecida;
- componentes calculados sobre base compatível;
- regra de contagem declarada;
- ausência de mistura direta entre pessoas, domicílios, contas, dispositivos, fluxos ou sessões.

## 3.5 Restrições

- GRP não informa alcance líquido;
- não informa distribuição de frequência;
- não comprova atenção, lembrança, resposta ou resultado;
- GRP domiciliar e individual não são idênticos;
- pontos construídos com exposições diferentes não são automaticamente equivalentes;
- conversão matemática não aumenta qualidade, auditabilidade ou representatividade da medição.

## 3.6 Interpretação

Um valor de 250 GRP significa que as exposições brutas equivalem a 250% do universo declarado. Diversas combinações de alcance e frequência podem produzir o mesmo total.

---

# 4. KT_CALCULO_GRP

## 4.1 Identificação

```text
codigo: KT_CALCULO_GRP
nome: Cálculo de GRP
classe_do_objeto: MODELO_MATEMATICO
subtipos: [FORMULA_DIRETA, FORMULA_DERIVADA]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: GRP_TRP
status: EM_VALIDACAO
versao: 1.1.0
```

## 4.2 Formas de cálculo

### Por audiência e inserções

```text
grp_programa = audiencia_percentual × numero_de_insercoes
```

### Pela soma da programação

```text
grp_total = soma(grp_de_cada_unidade)
```

### Por alcance e frequência

```text
grp = alcance_percentual × frequencia_media
```

### Por exposições brutas e universo

```text
grp = exposicoes_brutas / universo_correspondente × 100
```

## 4.3 Validações

- audiência e inserções devem se referir à mesma unidade de programação;
- componentes somados devem utilizar universo, target, praça, período e definição de exposição compatíveis;
- alcance e frequência devem derivar da mesma base deduplicada;
- exposições e universo devem possuir unidade compatível;
- valores ausentes não devem ser substituídos por zero.

## 4.4 Saída mínima

```text
grp
forma_de_calculo
universo
unidade_populacional
periodo
praca
definicao_de_exposicao
qualificador_da_exposicao
status_de_validacao
confianca
alertas
```

---

# 5. KT_CONVERSAO_GRP_IMPACTOS

## 5.1 Identificação

```text
codigo: KT_CONVERSAO_GRP_IMPACTOS
nome: Conversão entre GRP e impactos
classe_do_objeto: TRANSFORMACAO
subtipos: [CONVERSAO, FORMULA_INVERSA]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: GRP_TRP
status: EM_VALIDACAO
versao: 1.1.0
```

## 5.2 Fórmulas

```text
impactos = grp × universo / 100
```

```text
grp = impactos / universo × 100
```

## 5.3 Condições

- impactos significam exposições brutas compatíveis com o universo;
- universo e GRP devem usar a mesma unidade;
- praça, período e target devem coincidir;
- a definição de impacto deve permanecer registrada.

## 5.4 Qualificação obrigatória de impactos

```text
IMPACTO_CALCULADO_POR_AUDIENCIA
CONTATO_AJUSTADO
OPORTUNIDADE_DE_CONTATO
IMPACTO_DECLARADO_PELO_FORNECEDOR
IMPRESSAO_SERVIDA
IMPRESSAO_VALIDA
IMPRESSAO_VISIVEL
EXPOSICAO_ESTIMADA
```

O nome comercial `impactos` não basta para autorizar a conversão.

---

# 6. KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA

## 6.1 Identificação

```text
codigo: KT_EQUIVALENCIA_PRESSAO_MULTIMIDIA
nome: Equivalência condicionada de pressão entre mídias
classe_do_objeto: REGRA_TECNICA
subtipos: [COMPARABILIDADE, CONVERSAO, CLASSIFICACAO]
dominio_tecnico: PRESSAO_DE_MIDIA
familia_tecnica: COMPARABILIDADE_MULTIMIDIA
status: EM_VALIDACAO
versao: 1.1.0
```

## 6.2 Definição

Regra que verifica se uma métrica de determinada mídia pode ser expressa em pontos percentuais brutos sobre um universo comum e comparada a métricas de outras mídias.

A equivalência é de escala e pressão. Não implica identidade de qualidade de contato, duração, visibilidade, audibilidade, atenção, contexto, efeito ou resultado.

## 6.3 Camadas de comparação

```text
CAMADA_1_METRICA_NATIVA
CAMADA_2_OPORTUNIDADE_DE_EXPOSICAO
CAMADA_3_CONTATO_QUALIFICADO
CAMADA_4_EFEITO_OU_RESULTADO
```

### Camada 1 — métrica nativa

Preserva a medida original: rating, impressões, fluxo, OTS, downloads, audiência, leitores, sessões ou espectadores únicos.

### Camada 2 — oportunidade de exposição

Converte, quando possível, a métrica para oportunidades brutas sobre universo comum.

### Camada 3 — contato qualificado

Aplica apenas ajustes metodologicamente validados de visibilidade, audibilidade, duração, completude ou probabilidade de contato.

### Camada 4 — efeito ou resultado

Inclui lembrança, consideração, visita, clique, conversão, venda ou brand lift. Não deve ser convertida em GRP ou pontos de pressão sem modelo causal específico.

## 6.4 Estados de equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

### EQUIVALENCIA_DIRETA

A métrica já representa pontos percentuais brutos sobre universo, target, praça, período e exposição compatíveis.

### EQUIVALENCIA_APOS_CONVERSAO

Há exposições brutas e universo compatível:

```text
pontos_de_pressao = exposicoes_brutas / universo × 100
```

### EQUIVALENCIA_CONDICIONADA

A conversão é matematicamente possível, mas depende de hipótese relevante ou exposição de natureza diferente.

### NAO_EQUIVALENTE

Não existe unidade de exposição compatível, universo identificável ou procedimento defensável.

### DADOS_INSUFICIENTES

Faltam metadados para classificar.

## 6.5 Metadados obrigatórios

```text
metrica_original
valor_original
unidade_original
universo
unidade_de_identidade
territorio
periodo
janela_temporal
definicao_de_exposicao
qualificador_da_exposicao
metodo_de_conversao
estado_de_equivalencia
estado_de_deduplicacao
fonte
metodologia
auditabilidade
confianca
ressalvas
```

## 6.6 Estatuto dos pontos de pressão

`pontos_de_pressao` é um índice analítico normalizado para comparação de escala bruta.

Não deve ser apresentado como:

- GRP certificado, quando a métrica de origem não for rating compatível;
- alcance deduplicado;
- pessoas únicas;
- contato efetivamente visto ou ouvido;
- medida de atenção;
- resultado de comunicação ou negócio.

A interface deve mostrar o qualificador da exposição ao lado do valor.

---

## 7. Regras por família de mídia

### 7.1 Televisão linear e rádio aferido

Origem preferencial:

```text
rating percentual
impactos derivados de audiência
alcance e frequência compatíveis
```

Estado esperado:

```text
EQUIVALENCIA_DIRETA
ou
EQUIVALENCIA_APOS_CONVERSAO
```

Ressalvas: audiência individual versus domiciliar, praça, target, janela e transmissão efetiva.

### 7.2 Digital display, social e vídeo online

Origens possíveis:

```text
IMPRESSAO_SERVIDA
IMPRESSAO_VALIDA
IMPRESSAO_VISIVEL
ALCANCE_DE_CONTA
ALCANCE_DE_DISPOSITIVO
ALCANCE_MODELADO_DE_PESSOA
```

Estado esperado:

```text
EQUIVALENCIA_APOS_CONVERSAO
ou
EQUIVALENCIA_CONDICIONADA
```

Ressalvas: pessoa, conta, cookie e dispositivo não são idênticos; tráfego inválido; viewability; walled gardens; deduplicação entre plataformas.

### 7.3 OOH e DOOH

Cadeia necessária:

```text
FLUXO_BRUTO
→ OTS
→ PTS OU CONTATO_AJUSTADO
→ EXPOSICOES ESTIMADAS
```

Fluxo bruto isolado não deve gerar GRP comparável sem metodologia de oportunidade e visibilidade.

Estado esperado:

```text
EQUIVALENCIA_CONDICIONADA
```

Pode evoluir para conversão mais forte quando houver inventário auditado, modelo de audiência, universo, alcance e frequência documentados.

### 7.4 Jornal e revista

Circulação não equivale automaticamente a leitores ou exposições.

Possíveis bases:

```text
circulacao_auditada
leitores_por_exemplar
leitura_aferida
impactos_estimados
```

Estado esperado:

```text
EQUIVALENCIA_CONDICIONADA
ou
DADOS_INSUFICIENTES
```

### 7.5 Cinema

Sessões, capacidade e público histórico não equivalem à audiência da campanha.

Conversão exige público efetivo ou projeção documentada por sala, sessão, período e cobertura programada.

### 7.6 Áudio digital, podcast e streaming

Downloads, plays, streams iniciados, ouvintes únicos, retenção e completude são métricas diferentes.

A conversão deve preservar evento medido, janela e identidade.

### 7.7 CTV

CTV descreve ambiente/dispositivo, não uma única modalidade de compra ou métrica.

Devem ser preservados serviço, dispositivo, impressão, household, conta, pessoa modelada, viewability, completude e deduplicação com TV linear.

---

## 8. Deduplicação cross-media

Estados:

```text
DEDUPLICADO_POR_IDENTIDADE
DEDUPLICADO_POR_PAINEL
DEDUPLICADO_POR_MODELO
ESTIMADO_POR_PROXY
NAO_DEDUPLICADO
INDETERMINADO
```

Pressões brutas podem ser comparadas sem deduplicação quando a limitação estiver explícita. Alcance combinado e frequência de pessoa exigem deduplicação metodologicamente válida.

```text
comparabilidade de pressão ≠ deduplicação de pessoas
```

---

## 9. Qualidade, atenção e contexto

Dimensões de qualidade devem permanecer separadas:

```text
visibilidade
audibilidade
duracao
completude
contexto
atencao
interacao
```

Não deve existir fator universal que transforme automaticamente impressões em `impactos qualificados`. Qualquer ajuste exige metodologia, fonte, validade e confiança próprias.

---

## 10. Saída explicável

Toda execução deve informar:

```text
metrica_original
valor_original
conversao_realizada
formula
universo
qualificador_da_exposicao
estado_de_equivalencia
estado_de_deduplicacao
confianca
ressalvas
```

Mensagem mínima:

> O valor apresentado permite comparar pressão bruta na base declarada, mas não implica alcance deduplicado, qualidade equivalente de contato ou efeito equivalente entre meios.

---

## 11. Princípio consolidado

> O MediAd Planner pode normalizar escalas quando houver universo e exposição definidos, mas deve preservar a métrica nativa, a unidade de identidade, a metodologia e as limitações. Equivalência matemática é apenas uma das condições da comparabilidade; não é prova de equivalência metodológica, deduplicação ou efeito.