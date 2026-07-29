# Protocolo de Formalização dos Objetos de Conhecimento Técnico

**Documento:** `17B_PROTOCOLO_DE_FORMALIZACAO_DOS_OBJETOS_DE_CONHECIMENTO_TECNICO.md`  
**Documento principal:** `17_BIBLIOTECA_DE_CONHECIMENTO_TECNICO.md`  
**Inventário de origem:** `17A_INVENTARIO_PRELIMINAR_DE_CONHECIMENTOS_TECNICOS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Provisório normativo  
**Última revisão:** 29/07/2026  
**Natureza:** Protocolo metodológico

---

## 1. Finalidade

Este protocolo define como um item identificado no inventário preliminar deve ser transformado em um ou mais Objetos de Conhecimento Técnico formalizados, versionados, relacionáveis e utilizáveis pelos motores especialistas.

O protocolo evita quatro problemas:

- objetos excessivamente amplos;
- duplicação de indicadores da Biblioteca 15;
- incorporação de problemas decisórios da Biblioteca 18;
- mistura entre conhecimento técnico, valores comerciais e regras externas.

---

## 2. Unidade de formalização

Um item do inventário não corresponde necessariamente a um único objeto definitivo.

Um domínio como `GRP` deve ser decomposto em objetos atômicos e relacionáveis, por exemplo:

```text
CONCEITO_GRP
CALCULO_GRP_POR_INSERCOES
CALCULO_GRP_POR_ALCANCE_E_FREQUENCIA
CONVERSAO_GRP_EM_IMPACTOS
VALIDACAO_UNIVERSO_GRP
INTERPRETACAO_PRESSAO_GRP
RESTRICAO_COMPARABILIDADE_GRP_MULTIMIDIA
```

A atomicidade não significa fragmentação artificial. Um objeto deve representar uma unidade técnica que possa ser:

- definida sem ambiguidade;
- versionada de modo independente;
- ativada ou substituída sem alterar todo o domínio;
- relacionada a problemas, indicadores e tipologias;
- utilizada em uma execução rastreável.

---

## 3. Teste de pertencimento

Antes da formalização, cada item deve responder às perguntas abaixo.

### 3.1 Pertence à Biblioteca 15?

Pertence à Biblioteca 15 quando define **o que será observado, priorizado ou tratado como KPI**.

Exemplos:

- indicador alcance;
- indicador frequência média;
- indicador CPM;
- possibilidade de meta;
- prioridade decisória do KPI.

A Biblioteca 17 apenas referencia esses indicadores e formaliza o conhecimento necessário para calculá-los, validá-los e interpretá-los.

### 3.2 Pertence à Biblioteca 17?

Pertence à Biblioteca 17 quando representa:

- conceito técnico;
- definição operacional;
- modelo matemático;
- fórmula ou transformação;
- equivalência ou conversão;
- regra técnica de validação;
- regra técnica de comparabilidade;
- interpretação metodológica;
- técnica de planejamento ou simulação;
- restrição técnica de aplicação.

### 3.3 Pertence à Biblioteca 18?

Pertence à Biblioteca 18 quando a unidade principal é um **problema a resolver**.

Exemplos:

- estimar alcance;
- comparar veículos;
- distribuir orçamento;
- validar comparabilidade;
- controlar saturação;
- montar flight.

Um problema usa objetos da Biblioteca 17, mas não deve ser cadastrado como conhecimento técnico.

### 3.4 Pertence à Biblioteca 19?

Pertence à Biblioteca 19 quando registra valores, tabelas, condições, descontos, comissões, preços, vigências, moedas ou regras comerciais aplicadas a uma oferta concreta.

A fórmula de cálculo do desconto pertence à Biblioteca 17. O desconto de 15% negociado com determinado veículo pertence à Biblioteca 19 ou à instância do projeto.

### 3.5 Pertence à Biblioteca 20?

Pertence à Biblioteca 20 quando a regra tem origem externa, institucional, legal, contratual, ética, normativa ou de governança.

Exemplos:

- proibição legal de segmentação;
- restrição contratual de uso;
- padrão obrigatório de brand safety;
- regra institucional de aprovação;
- referência metodológica normativa.

A Biblioteca 17 pode referenciar a regra, mas não deve duplicá-la.

---

## 4. Critérios de decomposição

Um item deve ser dividido em mais de um objeto quando houver diferença relevante de:

- finalidade;
- fórmula;
- direção do cálculo;
- unidade;
- universo;
- denominador;
- tipologia de mídia;
- condição de validade;
- fonte metodológica;
- interpretação;
- versão;
- nível de confiança.

Exemplo:

```text
CPM_TRADICIONAL
CPM_DIGITAL_IMPRESSOES_SERVIDAS
CPM_DIGITAL_IMPRESSOES_VALIDAS
CPM_DIGITAL_IMPRESSOES_VISIVEIS
```

Esses objetos podem compartilhar uma família algébrica, mas não possuem o mesmo significado operacional.

---

## 5. Critérios para manter um objeto único

Variações não exigem objetos separados quando forem apenas:

- sinônimos controlados;
- diferenças de notação sem mudança semântica;
- exemplos de aplicação;
- unidades convertíveis por regra explícita;
- traduções terminológicas;
- arredondamentos configuráveis sem alteração metodológica.

Nesses casos, as variações devem ser registradas como aliases, representações ou parâmetros do mesmo objeto.

---

## 6. Estrutura mínima obrigatória

Nenhum item deve receber o estado `FORMALIZADO` sem possuir:

```text
codigo
nome
classe_do_objeto
dominio_tecnico
familia_tecnica
definicao
finalidade
entradas
saida
condicoes_de_validade
restricoes
interpretacao
fonte
confianca_metodologica
versao
```

Quando houver expressão matemática, também são obrigatórios:

```text
formula
significado_das_variaveis
unidades
tratamento_de_zero
tratamento_de_ausencia
precisao
arredondamento
```

Quando houver regra, também são obrigatórios:

```text
condicao
resultado_da_regra
severidade
mensagem_explicativa
```

---

## 7. Classes canônicas revisadas

Para evitar confusão entre forma e finalidade, cada objeto deve possuir uma classe principal:

```text
CONCEITO_TECNICO
DEFINICAO_OPERACIONAL
MODELO_MATEMATICO
TRANSFORMACAO
REGRA_TECNICA
TECNICA_DE_PLANEJAMENTO
RESTRICAO_METODOLOGICA
INTERPRETACAO_TECNICA
```

Subtipos podem detalhar a classe:

```text
FORMULA_DIRETA
FORMULA_INVERSA
FORMULA_DERIVADA
EQUIVALENCIA
CONVERSAO
VALIDACAO
COMPARABILIDADE
CLASSIFICACAO
DECISAO_TECNICA
SIMULACAO
```

A classe principal deve ser única. Os subtipos podem ser múltiplos quando necessário.

---

## 8. Relações entre objetos

Relações canônicas iniciais:

```text
DEFINE
CALCULA
DERIVA_DE
INVERTE
CONVERTE_PARA
VALIDA
RESTRINGE
INTERPRETA
COMPLEMENTA
SUBSTITUI
EQUIVALE_COM_RESSALVA
DEPENDE_DE
INCOMPATIVEL_COM
APLICAVEL_A
```

Toda relação deve poder registrar:

- condição;
- direção;
- fonte;
- versão;
- validade;
- confiança;
- observação metodológica.

---

## 9. Relação com os problemas técnicos

A Biblioteca 18 deve relacionar problemas a objetos da Biblioteca 17 por uma estrutura N:N.

```text
problema_tecnico
        ↕
problema_objeto_conhecimento
        ↕
objeto_conhecimento_tecnico
```

O vínculo deve registrar o papel do objeto no problema:

```text
DEFINICAO
ENTRADA
VALIDACAO
CALCULO
CONVERSAO
RESTRICAO
INTERPRETACAO
CRITERIO_DE_ESCOLHA
```

Exemplo:

```text
Problema: ESTIMAR_FREQUENCIA_MEDIA

Objetos utilizados:
- CONCEITO_FREQUENCIA_MEDIA
- CALCULO_FREQUENCIA_POR_IMPACTOS_E_ALCANCE
- CALCULO_FREQUENCIA_POR_GRP_E_ALCANCE
- VALIDACAO_COMPATIBILIDADE_DE_UNIVERSO
- TRATAMENTO_ALCANCE_ZERO
- INTERPRETACAO_FREQUENCIA_MEDIA
```

---

## 10. Fluxo editorial

```text
IDENTIFICADO
    ↓
TRIADO
    ↓
DECOMPOSTO
    ↓
EM_FORMALIZACAO
    ↓
EM_VALIDACAO
    ↓
PRONTO_PARA_PUBLICACAO
    ↓
FORMALIZADO
```

Estados excepcionais:

```text
DUPLICIDADE_POSSIVEL
VARIANTE_IDENTIFICADA
DIVERGENCIA_DE_FONTE
BLOQUEADO_POR_FONTE
DESCARTADO
SUBSTITUIDO
```

O estado `FORMALIZADO` significa que o objeto possui estrutura suficiente para ser referenciado pelos problemas técnicos. Não significa necessariamente que sua execução em código já tenha sido implementada.

---

## 11. Validação antes da publicação

Cada objeto deve passar por cinco validações:

### 11.1 Validação ontológica

Confirma que o objeto pertence à Biblioteca 17 e não duplica entidades das demais bibliotecas.

### 11.2 Validação semântica

Confirma que nome, definição, entradas, saída e interpretação são coerentes.

### 11.3 Validação matemática

Confirma fórmula, unidades, domínio, intervalos, transformações e casos-limite.

### 11.4 Validação metodológica

Confirma fonte, variante, aplicabilidade, comparabilidade e limitações.

### 11.5 Validação computacional

Confirma que o objeto pode ser convertido em regra ou função executável sem perda das condições metodológicas.

---

## 12. Primeiro lote de formalização

O primeiro lote deve ser pequeno e estruturalmente representativo.

### Núcleo 1 — Universo e audiência

- `KT_CONCEITO_UNIVERSO`;
- `KT_VALIDACAO_IDENTIDADE_DE_UNIVERSO`;
- `KT_CONCEITO_AUDIENCIA_PERCENTUAL`;
- `KT_CALCULO_AUDIENCIA_PERCENTUAL`;
- `KT_CONCEITO_PARTICIPACAO_AUDIENCIA`;
- `KT_CALCULO_PARTICIPACAO_AUDIENCIA`;
- `KT_CONCEITO_IMPACTOS`;
- `KT_CALCULO_IMPACTOS_POR_AUDIENCIA_E_INSERCOES`.

### Núcleo 2 — Alcance e frequência

- `KT_CONCEITO_ALCANCE`;
- `KT_CALCULO_ALCANCE_PERCENTUAL`;
- `KT_CONCEITO_FREQUENCIA_MEDIA`;
- `KT_CALCULO_FREQUENCIA_POR_IMPACTOS_E_ALCANCE`;
- `KT_VALIDACAO_FREQUENCIA_MESMO_UNIVERSO`;
- `KT_INTERPRETACAO_FREQUENCIA_MEDIA`.

### Núcleo 3 — GRP

- `KT_CONCEITO_GRP`;
- `KT_CALCULO_GRP_POR_INSERCOES`;
- `KT_CALCULO_GRP_POR_ALCANCE_E_FREQUENCIA`;
- `KT_CONVERSAO_GRP_EM_IMPACTOS`;
- `KT_RESTRICAO_COMPARABILIDADE_GRP_MULTIMIDIA`;
- `KT_INTERPRETACAO_GRP`.

Esse lote foi escolhido porque permite testar:

- conceitos;
- fórmulas diretas e derivadas;
- conversões;
- validações;
- restrições;
- interpretações;
- relações com indicadores;
- relações com problemas técnicos.

---

## 13. Entregáveis do primeiro lote

Para cada objeto serão produzidos:

1. ficha normativa em Markdown;
2. representação estruturada em YAML ou JSON;
3. conjunto de casos válidos;
4. conjunto de casos inválidos;
5. mensagens de validação e explicação;
6. relações com indicadores da Biblioteca 15;
7. relações com problemas da Biblioteca 18;
8. referências e versão.

A escolha definitiva entre YAML e JSON será feita na fase de modelagem técnica. Durante a formalização documental, Markdown permanece como fonte legível e auditável.

---

## 14. Decisões consolidadas

1. Um domínio técnico não equivale necessariamente a um objeto.
2. Objetos devem ser suficientemente atômicos para permitir versionamento independente.
3. Indicadores permanecem exclusivamente na Biblioteca 15.
4. Problemas decisórios permanecem exclusivamente na Biblioteca 18.
5. Valores e condições comerciais pertencem à Biblioteca 19.
6. Regras externas e institucionais pertencem à Biblioteca 20.
7. A Biblioteca 17 preserva o conhecimento técnico que permite calcular, validar, transformar, comparar e interpretar.
8. Fórmulas semelhantes com denominadores semanticamente diferentes devem ser formalizadas separadamente.
9. O estado `FORMALIZADO` não implica implementação em código.
10. A relação entre problemas e conhecimentos é N:N e registra o papel de cada objeto na resolução.

---

## 15. Princípio consolidado

> Um Objeto de Conhecimento Técnico não é apenas um termo, uma fórmula ou uma recomendação. É uma unidade técnica delimitada, versionável e rastreável, acompanhada das condições necessárias para que um sistema especialista possa utilizá-la sem apagar sua validade metodológica.