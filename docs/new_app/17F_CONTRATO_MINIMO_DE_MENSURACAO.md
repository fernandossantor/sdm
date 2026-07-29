# Contrato Mínimo de Mensuração

**Documento:** `17F_CONTRATO_MINIMO_DE_MENSURACAO.md`  
**Biblioteca:** 17 — Conhecimento Técnico  
**Integração:** Núcleos 17C, 17D, 17E e problemas 18A  
**Status:** Consolidado para uso arquitetural  
**Natureza:** Camada transversal de metadados, não nova biblioteca

---

## 1. Finalidade

Este documento harmoniza os metadados mínimos usados pelos conhecimentos técnicos de universo, audiência, impactos, alcance, frequência, GRP e equivalências multimídia.

Ele não cria novas telas, novos cadastros independentes nem novos objetos de negócio. Seu objetivo é evitar que cada cálculo ou problema repita estruturas semelhantes com nomes diferentes.

O contrato deve funcionar como uma camada interna comum:

```text
valor ou métrica
+ contexto mínimo de mensuração
+ estado de validade
+ explicação
```

---

## 2. Princípio de usabilidade

A precisão metodológica deve permanecer no modelo, sem transferir complexidade desnecessária ao usuário.

Portanto:

- os campos devem ser preenchidos automaticamente sempre que puderem ser herdados do projeto, público, inventário, fonte ou período;
- campos técnicos avançados devem aparecer apenas quando o contexto exigir confirmação;
- estados de deduplicação, equivalência e confiança devem ser calculados ou sugeridos pelo sistema sempre que possível;
- a interface deve agrupar informações em blocos compreensíveis, e não expor cada metadado como cadastro autônomo;
- valores padrão não podem ocultar incerteza metodológica;
- a ausência de informação crítica deve gerar solicitação objetiva, não formulários extensos.

```text
complexidade interna alta
não implica
complexidade de uso alta
```

---

## 3. Estrutura mínima comum

Todo valor técnico que participe de cálculo, comparação ou interpretação deve poder ser descrito pelos seguintes grupos.

### 3.1 Identidade da medida

```text
metrica
valor
unidade_de_mensuracao
natureza_do_valor
```

`natureza_do_valor` utiliza, conforme aplicável:

```text
OBSERVADO
ESTIMADO
PROJETADO
CONTRATADO
ENTREGUE
CALCULADO
NORMALIZADO
```

Esses estados são qualificadores de um valor, não novos objetos.

### 3.2 Base de referência

```text
unidade_de_observacao
universo_de_referencia
publico_ou_target
territorio
periodo_de_referencia
```

A base deve distinguir, quando aplicável:

- pessoas;
- domicílios;
- dispositivos;
- contas ou usuários;
- exemplares;
- sessões;
- fluxos;
- oportunidades de exposição.

A lista deve ser controlada, porém extensível. Não deve gerar uma tela específica para cada modalidade.

### 3.3 Origem e método

```text
fonte
metodologia
versao_da_fonte_ou_metodo
```

A versão é obrigatória apenas quando mudanças metodológicas puderem alterar comparabilidade ou interpretação.

### 3.4 Qualificadores analíticos

```text
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
restricoes
```

Esses qualificadores são condicionais. Não devem ser exigidos em todos os formulários.

---

## 4. Estados canônicos

### 4.1 Deduplicação

```text
NAO_APLICAVEL
NAO_DEDUPLICADO
DEDUPLICADO_NO_INVENTARIO
DEDUPLICADO_NO_MEIO
DEDUPLICADO_MULTIMIDIA
ESTIMADO_COM_MODELO
DESCONHECIDO
```

A granularidade deve permanecer nesse nível. Métodos específicos de deduplicação pertencem à metodologia ou ao motor, não ao cadastro principal.

### 4.2 Equivalência

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

A equivalência qualifica uma comparação. Não transforma métricas nativas diferentes em uma única métrica universal.

### 4.3 Confiança

```text
ALTA
MEDIA
BAIXA
INDETERMINADA
```

O nível de confiança deve resultar de regras transparentes associadas à fonte, completude dos dados, método e compatibilidade.

---

## 5. Regras de herança

Para reduzir digitação e inconsistência, os metadados devem seguir esta ordem preferencial de herança:

```text
projeto
→ cenário
→ público ou target
→ praça e período
→ inventário ou veículo
→ ocorrência ou valor técnico
```

O nível mais específico pode substituir o nível anterior quando houver justificativa.

Exemplos:

- o território pode ser herdado do projeto;
- o target pode ser herdado do objetivo de mídia;
- a unidade de observação pode ser herdada da fonte de audiência;
- o período pode ser herdado da linha de programação;
- a metodologia pode ser herdada do fornecedor do dado;
- o estado de deduplicação pode ser produzido pelo motor.

---

## 6. Aplicação aos núcleos

### 6.1 Núcleo 17C — Universo e Audiência

Deve usar prioritariamente:

```text
unidade_de_observacao
universo_de_referencia
publico_ou_target
territorio
periodo_de_referencia
fonte
metodologia
natureza_do_valor
```

`tipo_de_unidade`, `unidade_populacional` e expressões equivalentes devem convergir para `unidade_de_observacao`, preservando descrições específicas apenas quando forem semanticamente necessárias.

### 6.2 Núcleo 17D — Alcance e Frequência

Além da base comum, deve utilizar:

```text
estado_de_deduplicacao
```

A distribuição de frequência, frequência eficiente, overlap e saturação permanecem propriedades, parâmetros ou resultados relacionados. Não se tornam cadastros independentes apenas por exigirem tratamento técnico.

### 6.3 Núcleo 17E — GRP e Equivalências Multimídia

Além da base comum, deve utilizar:

```text
estado_de_equivalencia
natureza_do_valor
nivel_de_confianca
```

GRP, TRP, impactos, impressões, OTS e pontos de pressão preservam identidades próprias. O contrato apenas padroniza o contexto no qual são comparados.

### 6.4 Biblioteca 18 — Problemas Técnicos

Os problemas devem receber o contrato de mensuração como um conjunto, e não repetir todos os campos em cada definição.

Cada problema declara somente:

- quais partes do contrato são obrigatórias;
- quais podem ser herdadas;
- quais são produzidas como saída;
- quais ausências bloqueiam o procedimento.

---

## 7. Política de interface

O app deve apresentar os metadados em no máximo quatro blocos conceituais:

```text
1. O que está sendo medido
2. Para quem, onde e quando
3. De onde veio o dado
4. Qual a validade da comparação
```

A interface padrão não deve exibir códigos técnicos. Códigos, versões, estados completos e memória de cálculo pertencem às áreas de detalhes, auditoria e explicação.

Campos avançados devem usar divulgação progressiva:

```text
visão simples
→ detalhes da medida
→ validação metodológica
→ memória técnica
```

---

## 8. Critério para não criar novos objetos

Um novo objeto somente deve ser criado quando possuir ao menos uma destas características:

- ciclo de vida próprio;
- versionamento independente;
- reutilização por diferentes domínios;
- regras próprias de autorização ou validade;
- necessidade de relacionamento N:N;
- execução independente por motor;
- histórico que precise ser preservado separadamente.

Caso contrário, deve permanecer como:

- campo;
- qualificador;
- estado;
- variante;
- parâmetro;
- mensagem explicativa.

---

## 9. Decisão arquitetural

Os seis elementos abaixo são suficientes como eixo transversal inicial:

```text
unidade_de_observacao
universo_de_referencia
natureza_do_valor
estado_de_deduplicacao
estado_de_equivalencia
nivel_de_confianca
```

Eles não constituem seis novos módulos nem seis novas etapas obrigatórias para o usuário. São metadados internos reutilizados apenas quando aplicáveis.

---

## 10. Princípio consolidado

> O MediAd Planner deve preservar a precisão necessária para não combinar medidas incompatíveis, mas deve fazer isso por herança, automação, agrupamento e explicação progressiva. A arquitetura técnica pode ser rigorosa sem transformar o planejamento de mídia em preenchimento burocrático.
