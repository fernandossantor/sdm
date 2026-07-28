# Tradução Estratégica

**Documento:** `03_TRADUCAO_ESTRATEGICA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Em consolidação progressiva  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Tradução Estratégica recebe o **Objeto Contextual Estruturado** produzido pelo Briefing e o converte em parâmetros técnicos de mídia que orientarão a Arquitetura de Mídia, as Simulações, a Comparação, a Otimização e o Plano Consolidado.

A etapa não tem como artefato principal um texto estratégico. Seu resultado operacional é um conjunto estruturado, explicável, editável e versionado de indicadores técnicos.

Fluxo canônico:

```text
Campanha
    ↓
Briefing
Objeto Contextual Estruturado
    ↓
Tradução Estratégica
Perfil Estratégico de Mídia
    ↓
Arquitetura de Mídia
    ↓
Simulações
    ↓
Plano Consolidado
```

A explicação textual pode existir como camada secundária de auditoria e compreensão humana, mas não substitui os parâmetros técnicos persistidos pelo sistema.

---

## 2. Natureza do artefato de saída

O artefato final da Tradução Estratégica será denominado:

```text
Perfil Estratégico de Mídia
```

O Perfil Estratégico de Mídia deverá conter, progressivamente:

- dimensões técnicas;
- intensidades requeridas;
- prioridades;
- pesos estratégicos;
- condições de atendimento;
- vínculos contextuais;
- compatibilidades;
- tensões;
- restrições classificadas;
- graus de confiança;
- rastreabilidade;
- valores calculados;
- valores ajustados;
- valores efetivos;
- histórico de alterações.

A primeira composição consolidada desse perfil é a **Leitura Estratégica do Contexto**.

---

## 3. Limites da etapa

A Tradução Estratégica deve:

- interpretar tecnicamente o contexto do Briefing;
- identificar quais dimensões de mídia são mais ou menos relevantes;
- transformar informações declaradas em intensidades, prioridades e pesos;
- registrar compatibilidades e tensões;
- produzir parâmetros reutilizáveis pelas etapas posteriores;
- preservar a origem de cada parâmetro;
- permitir revisão e alteração pelo planejador.

A Tradução Estratégica não deve:

- escolher meios;
- escolher canais;
- escolher veículos;
- escolher formatos;
- selecionar inventários;
- distribuir verba entre meios ou canais;
- calcular resultados finais de alcance ou frequência;
- construir o flight;
- definir quantidades de inserções;
- consolidar um plano de mídia.

---

## 4. Leitura Estratégica do Contexto

### 4.1 Finalidade

A Leitura Estratégica do Contexto responde à seguinte questão:

```text
Dadas as condições registradas no Briefing,
quais dimensões técnicas de mídia devem exercer maior ou menor influência
nas decisões posteriores?
```

Ela transforma o Briefing em uma configuração técnica inicial.

Exemplo:

```text
Briefing indica:
- necessidade de ampla presença;
- público numeroso;
- expansão territorial;
- forte pressão competitiva;
- necessidade de repetição.

Leitura Estratégica produz:
- alcance: intensidade alta, peso elevado;
- cobertura geográfica: intensidade alta, peso elevado;
- frequência: intensidade alta, peso elevado;
- eficiência: intensidade média ou alta, conforme verba;
- afinidade: peso definido conforme públicos e segmentos.
```

A etapa não determina antecipadamente o plano. Ela configura o sistema de avaliação que será mobilizado pelas etapas seguintes.

---

## 5. Fontes de entrada

A Leitura Estratégica deve consumir apenas informações estruturadas e válidas do Briefing, especialmente:

- situação da marca, produto ou serviço;
- situação do mercado e da categoria;
- situação competitiva;
- objetivos de Marketing;
- objetivos de Comunicação;
- praça;
- universo;
- segmentação;
- segmentos;
- públicos;
- jornada;
- período de veiculação pretendido;
- verba disponível;
- prioridades declaradas;
- restrições declaradas;
- pretensões.

Nenhum parâmetro técnico pode ser gerado sem rastreabilidade até uma ou mais dessas fontes ou até regras metodológicas explícitas do sistema.

---

## 6. Dimensões técnicas iniciais

A Leitura Estratégica deve operar sobre uma biblioteca canônica de dimensões técnicas.

Conjunto inicial:

- alcance;
- frequência;
- cobertura geográfica;
- continuidade;
- velocidade de construção de alcance;
- impacto;
- afinidade;
- seletividade;
- presença territorial;
- concentração;
- dispersão;
- eficiência;
- mensurabilidade;
- capacidade de resposta;
- capacidade de conversão;
- adequação à jornada;
- flexibilidade operacional;
- pressão competitiva;
- necessidade de diferenciação;
- necessidade de sustentação.

Essa lista é controlada pelo sistema.

Novas dimensões não devem ser criadas livremente durante o preenchimento de uma Campanha. Inclusões exigem revisão metodológica e registro formal de decisão.

---

## 7. Intensidade requerida

A intensidade requerida representa quanto determinada dimensão parece necessária diante do Briefing.

Escala canônica de armazenamento:

```text
0 a 100
```

Representação ordinal correspondente:

| Faixa | Classificação |
|---:|---|
| 0–19 | Muito baixa |
| 20–39 | Baixa |
| 40–59 | Média |
| 60–79 | Alta |
| 80–100 | Muito alta |

A classificação ordinal é uma visualização do valor numérico e não um dado independente.

Exemplo:

```text
Alcance requerido: 88 — Muito alto
Frequência requerida: 81 — Muito alta
Afinidade requerida: 56 — Média
Mensurabilidade requerida: 35 — Baixa
```

---

## 8. Peso estratégico

O peso estratégico representa quanto uma dimensão deve influenciar a avaliação das alternativas nas etapas posteriores.

A intensidade requerida e o peso estratégico não são sinônimos.

```text
Intensidade requerida = quanto a dimensão é necessária.
Peso estratégico = quanto a dimensão influencia os cálculos e avaliações.
```

Os pesos devem ser normalizados dentro da família de decisão em que serão utilizados.

Forma canônica:

```text
0,00 a 1,00
```

Quando exibidos como percentual:

```text
0% a 100%
```

Em uma mesma família normalizada, a soma dos pesos efetivos deve totalizar:

```text
1,00
```

Os pesos não devem ser universais nem fixos. Devem resultar da combinação entre o Briefing e as regras metodológicas vigentes.

---

## 9. Prioridade e condição

Além da intensidade e do peso, cada dimensão poderá receber prioridade e condição.

### 9.1 Prioridade

Valores canônicos:

- Muito baixa;
- Baixa;
- Média;
- Alta;
- Muito alta.

### 9.2 Condição

Valores canônicos:

- Obrigatória;
- Desejável;
- Compensável;
- Diagnóstica.

A condição não substitui o peso.

Uma dimensão pode possuir peso elevado e ser compensável. Uma restrição rígida pode operar como condição de exclusão e não integrar uma soma de pesos.

---

## 10. Matriz de influências

Cada elemento do Briefing pode:

- aumentar uma dimensão;
- reduzir uma dimensão;
- não afetar uma dimensão;
- afetar uma dimensão apenas em combinação com outro elemento.

A relação deve ser registrada em uma Matriz de Influências parametrizada.

Estrutura conceitual:

```text
Elemento do Briefing
        ↓
Regra de influência
        ↓
Dimensão técnica
        ↓
Contribuição positiva, negativa, neutra ou condicional
```

Exemplos metodológicos:

- penetração tende a elevar alcance e cobertura;
- notoriedade tende a elevar alcance, impacto e velocidade de construção de alcance;
- fidelização tende a elevar frequência, continuidade e afinidade;
- público amplo tende a elevar alcance e dispersão;
- público restrito tende a elevar seletividade e afinidade;
- período curto pode elevar concentração e velocidade;
- verba limitada tende a elevar o peso da eficiência;
- forte pressão competitiva pode elevar frequência, continuidade, impacto ou necessidade de diferenciação.

Os coeficientes numéricos dessas relações serão definidos e validados em especificação própria. Este documento consolida a lógica, não fixa valores arbitrários.

---

## 11. Processo de parametrização

Processo canônico:

```text
Briefing estruturado
        ↓
Seleção das regras aplicáveis
        ↓
Matriz de influências
        ↓
Pontuação bruta por dimensão
        ↓
Aplicação de prioridades, restrições e contexto
        ↓
Normalização
        ↓
Intensidade requerida
        ↓
Peso estratégico calculado
        ↓
Revisão ou ajuste do planejador
        ↓
Peso estratégico efetivo
```

O processo deve ser determinístico para o mesmo conjunto de entradas, regras e versões de parâmetros.

---

## 12. Vínculos contextuais

Os parâmetros podem existir em diferentes níveis.

### 12.1 Nível geral da Campanha

Exemplo:

```text
Alcance geral: peso 0,22
Frequência geral: peso 0,18
```

### 12.2 Nível de praça

Exemplo:

```text
Cobertura na praça principal: peso elevado
Cobertura na praça secundária: peso médio
```

### 12.3 Nível de público ou segmento

Exemplo:

```text
Afinidade para o Público A: muito alta
Afinidade para o Público B: média
```

### 12.4 Nível de jornada

Exemplo:

```text
Adequação à etapa de descoberta: alta
Adequação à etapa de decisão: muito alta
```

### 12.5 Nível combinado

O sistema deve admitir parâmetros vinculados simultaneamente a:

- praça;
- universo;
- segmento;
- público;
- etapa da jornada.

Um parâmetro geral não deve apagar diferenças relevantes entre territórios, públicos ou jornadas.

---

## 13. Tensões

A Leitura Estratégica deve identificar combinações de exigências que disputem recursos ou produzam incompatibilidades.

Exemplos:

```text
Alcance muito alto × Frequência muito alta × Verba limitada
```

```text
Cobertura de muitas praças × Período curto
```

```text
Múltiplos públicos prioritários × Orçamento restrito
```

```text
Conversão imediata × Baixa notoriedade
```

Cada tensão deve registrar:

- identificador;
- tipo;
- dimensões envolvidas;
- elementos do Briefing que a originaram;
- gravidade;
- possibilidade de compensação;
- necessidade de decisão posterior;
- etapas afetadas.

A Leitura Estratégica identifica a tensão, mas não precisa resolvê-la definitivamente.

---

## 14. Grau de confiança

Todo parâmetro calculado deve possuir um grau de confiança.

A confiança deve considerar:

- completude do Briefing;
- presença de dados quantitativos;
- qualidade e atualidade das fontes;
- coerência entre declarações;
- quantidade de inferências necessárias;
- existência de conflito entre entradas;
- estabilidade das regras aplicadas.

Escala canônica de armazenamento:

```text
0 a 100
```

Representação ordinal:

- Muito baixa;
- Baixa;
- Média;
- Alta;
- Muito alta.

O grau de confiança não altera automaticamente o peso. Ele informa a robustez da derivação e pode gerar alerta, solicitação de revisão ou necessidade de validação humana.

---

## 15. Rastreabilidade

Todo parâmetro deve preservar sua origem.

Exemplo:

```text
Dimensão: Alcance
Intensidade calculada: 90
Peso calculado: 0,23

Origens:
- objetivo de Marketing: penetração;
- objetivo de Comunicação: notoriedade;
- público: amplo;
- praça: expansão territorial;
- situação competitiva: presença inferior à concorrência;
- pretensão: alcançar novos públicos.
```

A rastreabilidade deve permitir:

- explicar o resultado;
- revisar o raciocínio;
- recalcular apenas dimensões afetadas;
- identificar a regra aplicada;
- distinguir cálculo do sistema e ajuste humano;
- reproduzir versões anteriores.

---

## 16. Alterações do planejador

Todos os parâmetros derivados devem ser revisáveis pelo planejador autorizado.

A alteração não pode apagar o valor calculado pelo sistema.

Campos mínimos:

```text
valor_calculado
valor_ajustado
valor_efetivo
origem_do_ajuste
justificativa
responsavel
alterado_em
```

Regra canônica:

```text
Se não houver ajuste:
valor_efetivo = valor_calculado

Se houver ajuste válido:
valor_efetivo = valor_ajustado
```

A justificativa é obrigatória quando o valor ajustado ultrapassar a tolerância definida pelo sistema ou alterar prioridade, condição ou peso de forma metodologicamente relevante.

---

## 17. Explicação textual

O sistema pode produzir explicações como:

> Alcance recebeu peso elevado em razão da combinação entre penetração, notoriedade, público amplo e expansão territorial.

Essa explicação é uma representação humana de uma estrutura paramétrica.

A persistência principal deve ocorrer em dados estruturados, como:

```text
dimensao = alcance
intensidade = 90
peso_calculado = 0.23
peso_efetivo = 0.23
confianca = 86
origens = [penetracao, notoriedade, publico_amplo, expansao_territorial]
```

O texto não pode ser a única forma de registrar a decisão.

---

## 18. Estrutura mínima do parâmetro técnico

Cada parâmetro técnico deve conter, no mínimo:

- ID técnico;
- Campanha;
- versão do Briefing de origem;
- versão da Tradução Estratégica;
- dimensão técnica;
- escopo do parâmetro;
- intensidade calculada;
- intensidade ajustada, quando houver;
- intensidade efetiva;
- prioridade calculada;
- prioridade ajustada, quando houver;
- prioridade efetiva;
- peso calculado;
- peso ajustado, quando houver;
- peso efetivo;
- condição;
- grau de confiança;
- origens;
- regras aplicadas;
- vínculos com praças;
- vínculos com universos;
- vínculos com segmentos;
- vínculos com públicos;
- vínculos com etapas da jornada;
- compatibilidades;
- tensões relacionadas;
- justificativa estruturada;
- explicação textual gerada, quando houver;
- responsável pelo ajuste;
- data e hora da criação;
- data e hora da atualização.

---

## 19. Contrato de entrada

### 19.1 Pré-condições

- Campanha existente;
- Briefing existente;
- Briefing em versão válida para processamento;
- bibliotecas metodológicas disponíveis;
- regras de influência versionadas;
- usuário autorizado.

### 19.2 Entradas obrigatórias

- snapshot do Briefing;
- versão das regras metodológicas;
- versão das bibliotecas de dimensões;
- prioridades e restrições declaradas;
- metadados de processamento.

---

## 20. Contrato de saída

A Leitura Estratégica do Contexto produz, no mínimo:

- conjunto versionado de parâmetros técnicos;
- intensidades requeridas;
- prioridades;
- pesos calculados;
- pesos efetivos;
- condições;
- vínculos contextuais;
- tensões;
- graus de confiança;
- rastreabilidade;
- registro de ajustes;
- alertas de insuficiência ou conflito.

A saída deve estar apta a alimentar a Arquitetura de Mídia sem depender de interpretação manual de um texto narrativo.

---

## 21. Reprocessamento

Alterações no Briefing devem provocar reprocessamento apenas dos parâmetros afetados.

O sistema deve:

- identificar dependências;
- preservar parâmetros não afetados;
- recalcular parâmetros dependentes;
- manter o histórico da versão anterior;
- sinalizar ajustes humanos potencialmente incompatíveis com a nova entrada;
- solicitar confirmação antes de descartar ajustes válidos.

---

## 22. Versionamento

Cada execução da Tradução Estratégica deve estar vinculada a:

- uma Campanha;
- uma versão do Briefing;
- uma versão das regras metodológicas;
- uma versão das bibliotecas de parâmetros.

O Perfil Estratégico de Mídia deve possuir versão própria.

Exemplo:

```text
Briefing v2
Regras metodológicas v1.3
Perfil Estratégico de Mídia v3
```

A alteração do Perfil Estratégico não modifica o Código da Campanha.

---

## 23. Critérios de conclusão da Leitura Estratégica

A Leitura Estratégica pode ser considerada concluída quando:

- todas as dimensões aplicáveis foram avaliadas;
- intensidades e pesos foram calculados;
- vínculos contextuais foram preservados;
- tensões relevantes foram identificadas;
- graus de confiança foram atribuídos;
- ajustes humanos foram justificados;
- não existem parâmetros sem origem rastreável;
- o conjunto está apto a alimentar a Arquitetura de Mídia.

---

## 24. Decisões consolidadas

1. O artefato principal da Tradução Estratégica é paramétrico, não narrativo.
2. A explicação textual é secundária e auditável.
3. O Briefing não determina diretamente meios, canais ou resultados.
4. A Leitura Estratégica converte o contexto em dimensões, intensidades, prioridades e pesos.
5. Intensidade requerida e peso estratégico são conceitos distintos.
6. Os pesos devem variar conforme a combinação das entradas.
7. Os parâmetros podem existir em níveis geral, territorial, populacional e de jornada.
8. Toda derivação deve ser rastreável.
9. Todo parâmetro derivado pode ser ajustado por usuário autorizado.
10. O valor calculado nunca é apagado por um ajuste.
11. Tensões devem ser registradas como objetos estruturados.
12. A confiança deve acompanhar todo parâmetro calculado.
13. Alterações no Briefing devem provocar recálculo seletivo.
14. A saída deve alimentar diretamente a Arquitetura, as Simulações e o Plano.
15. Os coeficientes numéricos da Matriz de Influências serão definidos em especificação metodológica própria.

---

## 25. Pontos ainda não consolidados neste documento

Permanecem para detalhamento posterior:

- taxonomia final das dimensões técnicas;
- coeficientes da Matriz de Influências;
- funções de normalização;
- regras de composição entre influências simultâneas;
- tolerâncias para ajustes manuais;
- tratamento matemático da confiança;
- resolução ou compensação de tensões;
- derivação formal dos objetivos de mídia;
- classificação técnica das restrições;
- contrato completo do Perfil Estratégico de Mídia;
- passagem dos parâmetros para a Arquitetura de Mídia.
