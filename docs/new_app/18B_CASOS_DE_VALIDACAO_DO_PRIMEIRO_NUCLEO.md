# Casos de Validação do Primeiro Núcleo de Problemas Técnicos

**Documento relacionado:** `18A_PRIMEIRO_NUCLEO_DE_PROBLEMAS_TECNICOS.md`  
**Status:** Em validação  
**Última revisão:** 29/07/2026

## 1. Finalidade

Testar os problemas do primeiro núcleo contra situações representativas de televisão, rádio, digital, OOH/DOOH, impresso, cinema e combinações multimídia.

Os valores são didáticos. O objetivo é validar regras, estados e limites de interpretação.

## 2. Casos canônicos

### TV-01 — Audiência percentual

```text
universo: 1.000.000 pessoas
audiencia absoluta: 120.000 pessoas
resultado: 12%
estado: CONCLUIDO
```

Valida `CALCULAR_AUDIENCIA_PERCENTUAL`. O resultado não representa participação, alcance acumulado nem impactos.

### TV-02 — Participação de audiência

```text
universo total: 1.000.000 pessoas
universo ligado: 600.000 pessoas
audiencia: 120.000 pessoas
audiencia percentual: 12%
participacao: 20%
estado: CONCLUIDO
```

Valida que audiência percentual e participação possuem denominadores diferentes.

### TV-03 — Impactos com audiência constante

```text
audiencia por insercao: 120.000 pessoas
insercoes: 5
impactos: 600.000 exposicoes
estado: CONCLUIDO
```

Impactos admitem repetição e não equivalem a pessoas únicas.

### TV-04 — Impactos com audiências variáveis

```text
audiencias por ocorrencia: 120.000, 100.000, 130.000, 90.000
impactos: 440.000 exposicoes
procedimento: SOMA_ITEM_A_ITEM
estado: CONCLUIDO
```

A multiplicação simplificada não deve ser usada quando há granularidade por ocorrência.

### TV-05 — Domicílios versus pessoas

```text
alternativa A: audiencia domiciliar
alternativa B: audiencia individual
conversao reconhecida: ausente
estado de identidade: INCOMPATIVEL
estado: BLOQUEADO_INCOMPATIBILIDADE
```

### Rádio-01 — Coincidência entre impactos e universo

```text
universo: 200.000 ouvintes
audiencia por insercao: 20.000 ouvintes
insercoes: 10
impactos: 200.000 exposicoes
estado: CONCLUIDO
```

A coincidência numérica não implica alcance de 100%.

### Digital-01 — Impressões e alcance deduplicado

```text
impressoes validas: 1.000.000
alcance deduplicado: 250.000 pessoas
frequencia media: 4
estado de deduplicacao: DEDUPLICADO_NA_FONTE
estado: CONCLUIDO
```

O alcance deve declarar se representa pessoa, usuário, conta, cookie ou dispositivo.

### Digital-02 — Dispositivos tratados como pessoas

```text
alcance informado: dispositivos unicos
interpretacao solicitada: pessoas unicas
modelo de conversao: ausente
estado: BLOQUEADO_INCOMPATIBILIDADE
```

### Digital-03 — Zero válido

```text
impressoes validas: 0
metadados completos: sim
resultado: 0
estado: CONCLUIDO
```

Zero observado deve ser distinguido de dado ausente.

### Digital-04 — Dado ausente

```text
impressoes validas: ausente
estado: NAO_CALCULADO_DADO_AUSENTE
```

### Digital-05 — Impressões servidas e visíveis

```text
alternativa A: impressoes servidas
alternativa B: impressoes visiveis
estado de equivalencia: EQUIVALENCIA_CONDICIONADA
estado: CONCLUIDO_COM_RESSALVA
```

A comparação é possível, mas a soma como unidades idênticas deve ser bloqueada.

### OOH-01 — Fluxo

```text
fluxo: 500.000 passagens
fator de visibilidade: ausente
modelo de contato: ausente
camada valida: METRICA_NATIVA
estado: CONCLUIDO_COM_RESSALVA
```

Fluxo não equivale automaticamente a OTS, contato ajustado, impacto validado ou pessoas únicas.

### OOH-02 — Conversão em oportunidade de exposição

```text
fluxo: 500.000 passagens
fator de oportunidade: 0,60
oportunidades de exposicao: 300.000
estado de equivalencia: EQUIVALENCIA_APOS_CONVERSAO
estado: CONCLUIDO_COM_RESSALVA
```

### DOOH-01 — Impressões estimadas

```text
impressoes estimadas: 900.000
metodologia do operador: declarada
pessoas unicas: ausente
estado: CONCLUIDO_COM_RESSALVA
```

O valor não permite inferir alcance líquido.

### Impresso-01 — Circulação e leitores por exemplar

```text
circulacao: 20.000 exemplares
leitores por exemplar: 2,5
edicoes: 4
leitores estimados por edicao: 50.000
impactos estimados: 200.000
estado: CONCLUIDO_COM_RESSALVA
```

Circulação não é audiência, e a repetição entre edições não está deduplicada.

### Impresso-02 — Tiragem usada como circulação

```text
tiragem: 25.000
circulacao: ausente
estado: NAO_CALCULADO_DADO_AUSENTE
```

### Cinema-01 — Público por sessão

```text
publicos por sessao: 100, 120, 80, 110
impactos: 410 exposicoes
procedimento: SOMA_ITEM_A_ITEM
estado: CONCLUIDO
```

### Cinema-02 — Capacidade usada como público real

```text
capacidade da sala: 200 lugares
sessoes: 10
capacidade maxima: 2.000 oportunidades teoricas
impactos reais: NAO_CALCULADO
estado: CONCLUIDO_COM_RESSALVA
```

### Multimídia-01 — Soma bruta compatível

```text
TV: 600.000 exposicoes de pessoas
radio: 200.000 exposicoes de pessoas
mesmo target, praca e periodo: sim
pressao bruta agregada: 800.000 exposicoes
estado: CONCLUIDO_COM_RESSALVA
```

A soma não produz alcance multimídia deduplicado.

### Multimídia-02 — Pessoas e dispositivos

```text
TV: impactos em pessoas
digital: impressoes em dispositivos
conversao reconhecida: ausente
estado de equivalencia: NAO_EQUIVALENTE
estado: BLOQUEADO_INCOMPATIBILIDADE
```

### Multimídia-03 — GRP e pontos normalizados

```text
TV: 180 GRP certificado
OOH: 75 pontos de pressao normalizados
estado de equivalencia: EQUIVALENCIA_CONDICIONADA
estado: CONCLUIDO_COM_RESSALVA
```

Pontos normalizados não devem ser rotulados como GRP certificado.

### Multimídia-04 — Alcance sem overlap

```text
alcance TV: 400.000 pessoas
alcance radio: 150.000 pessoas
overlap: ausente
alcance multimidia: NAO_CALCULADO
estado: NAO_CALCULADO_DADO_AUSENTE
intervalo logico: 400.000 a 550.000
```

O intervalo é limite teórico, não estimativa deduplicada.

## 3. Casos de erro

```text
denominador zero → NAO_CALCULADO_DADO_INVALIDO
audiencia negativa → NAO_CALCULADO_DADO_INVALIDO
audiencia superior ao universo sem justificativa → NAO_CALCULADO_DADO_INVALIDO
valor de universo sem unidade, territorio e periodo → INDETERMINADO
```

## 4. Harmonização exigida

Os Núcleos 17C, 17D, 17E e o documento 18A devem usar os mesmos campos canônicos:

```text
unidade_de_observacao
universo_de_referencia
publico_ou_target
territorio
periodo_de_referencia
fonte
metodologia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

### Natureza do valor

```text
OBSERVADO
ESTIMADO
PROJETADO
CONTRATADO
ENTREGUE
POTENCIAL
DERIVADO
NORMALIZADO
```

### Estado de deduplicação

```text
NAO_APLICAVEL
NAO_DEDUPLICADO
DEDUPLICADO_NA_FONTE
DEDUPLICADO_POR_MODELO
PARCIALMENTE_DEDUPLICADO
DEDUPLICACAO_INDETERMINADA
```

### Estado de equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

## 5. Distinções obrigatórias

```text
audiencia percentual ≠ participacao de audiencia
impactos ≠ alcance liquido
impressoes ≠ pessoas
fluxo ≠ OTS
OTS ≠ contato ajustado
circulacao ≠ leitores
capacidade ≠ publico presente
GRP certificado ≠ pontos de pressao normalizados
soma de impactos ≠ alcance deduplicado
zero valido ≠ dado ausente
```

## 6. Critérios para formalização

O primeiro núcleo poderá migrar para `FORMALIZADO` quando:

1. os nomes de campos forem harmonizados entre 17C, 17D, 17E e 18A;
2. os estados de deduplicação e equivalência forem idênticos;
3. cada caso possuir resposta determinística ou regra explícita de indeterminação;
4. zero, ausência, invalidade e incompatibilidade tiverem tratamentos distintos;
5. os problemas forem vinculados aos indicadores da Biblioteca 15;
6. uma representação estruturada em YAML, JSON ou banco for validada sem perda semântica.

> A possibilidade algébrica de somar, dividir ou converter números não constitui, por si só, autorização metodológica.