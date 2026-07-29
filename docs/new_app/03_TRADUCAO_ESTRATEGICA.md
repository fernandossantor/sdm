# Tradução Estratégica

**Documento:** `03_TRADUCAO_ESTRATEGICA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado progressivamente  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Tradução Estratégica recebe o **Objeto Contextual Estruturado** produzido pelo Briefing e o converte em um **Perfil Estratégico de Mídia** estruturado, mensurável, explicável, editável e versionado.

Ela não produz apenas uma narrativa. Seu resultado operacional é um conjunto de objetos, relações, pontuações, intensidades, pesos, prioridades, restrições, tensões e graus de confiança aptos a alimentar os motores posteriores.

```text
Campanha
    ↓
Briefing
    ↓
Objeto Contextual Estruturado
    ↓
Tradução Estratégica
    ↓
Perfil Estratégico de Mídia
    ↓
Arquitetura de Mídia
    ↓
Simulações
    ↓
Plano Consolidado
```

---

## 2. Artefato de saída

O Perfil Estratégico de Mídia deve conter:

- objetivos de Marketing operacionalizados;
- objetivos de Comunicação operacionalizados;
- objetivos de Mídia derivados;
- relações entre objetivos;
- resultados pretendidos;
- indicadores e KPIs propostos;
- intensidades requeridas;
- prioridades;
- pesos estratégicos;
- ordens de adequação;
- condições de atendimento;
- dimensões técnicas;
- vínculos contextuais;
- compatibilidades;
- tensões;
- restrições;
- graus de confiança;
- valores calculados, ajustados e efetivos;
- rastreabilidade;
- histórico de alterações.

---

## 3. Limites

A Tradução Estratégica deve:

- interpretar tecnicamente o Briefing;
- validar a operacionalização dos objetivos declarados;
- correlacionar objetivos de Marketing e Comunicação;
- derivar objetivos de Mídia;
- pontuar e ordenar relações;
- transformar declarações em intensidades, prioridades e pesos;
- identificar compatibilidades, insuficiências, contradições e tensões;
- produzir parâmetros reutilizáveis;
- preservar a origem de cada derivação;
- permitir revisão pelo planejador.

Não deve:

- escolher inventários finais;
- distribuir definitivamente a verba;
- definir quantidades finais de inserções ou impressões;
- calcular resultados finais do plano;
- consolidar a grade de veiculação;
- acompanhar campanha em execução;
- armazenar resultados realizados.

---

## 4. Fontes de entrada

A Tradução Estratégica consome informações estruturadas do Briefing, especialmente:

- situação do anunciante, marca, produto ou serviço;
- situação do mercado, categoria e concorrência;
- objetivos de Marketing declarados;
- objetivos de Comunicação declarados;
- indicadores, linhas de base e metas disponíveis;
- praça;
- universo;
- segmentos e públicos;
- jornada;
- período;
- verba;
- prioridades;
- restrições;
- pretensões declaradas.

Nenhuma derivação pode existir sem rastreabilidade até uma entrada válida ou uma regra metodológica versionada.

---

## 5. Processo canônico

```text
Briefing estruturado
        ↓
Validação de suficiência e mensurabilidade
        ↓
Classificação dos objetivos declarados
        ↓
Operacionalização dos objetivos
        ↓
Matriz Marketing–Comunicação
        ↓
Pontuação e ordenação das relações
        ↓
Derivação dos objetivos de Mídia
        ↓
Matriz Comunicação–Mídia
        ↓
Pontuação e ordenação das relações
        ↓
Resultados pretendidos e indicadores
        ↓
Dimensões técnicas
        ↓
Intensidades e pesos
        ↓
Tensões, restrições e confiança
        ↓
Perfil Estratégico de Mídia
```

---

## 6. Validação de mensurabilidade

Antes de participar de qualquer cálculo, cada objetivo deve ser avaliado quanto a:

- objeto da mudança;
- público;
- praça;
- direção;
- indicador;
- unidade ou escala;
- linha de base, quando disponível;
- meta ou intensidade pretendida;
- horizonte temporal;
- fonte;
- confiança.

Estados canônicos:

- OPERACIONALIZADO;
- OPERACIONALIZAVEL_COM_DADOS_PENDENTES;
- OPERACIONALIZAVEL_POR_PROXY;
- QUALITATIVO_ESTRUTURADO;
- NAO_OPERACIONALIZADO.

Objetivos `NAO_OPERACIONALIZADO` podem permanecer como alerta ou pendência, mas não alimentam pontuações.

Objetivos qualitativos só podem ser processados quando convertidos em escala ordinal estruturada, índice composto, proxy declarado ou condição verificável.

---

## 7. Correlação entre objetivos

### 7.1 Relações admitidas

```text
Marketing N:N Comunicação
Comunicação N:N Mídia
```

Relações diretas Marketing–Mídia são derivadas ou excepcionais e não devem eliminar a mediação comunicacional.

### 7.2 Tipos de relação

- CONTRIBUI_PARA;
- SUSTENTA;
- POTENCIALIZA;
- HABILITA;
- COMPLEMENTA;
- ANTECEDE;
- DEPENDE_DE;
- COMPENSA;
- DISPUTA_RECURSO_COM;
- PODE_CONFLITAR_COM;
- INCOMPATIVEL_NO_CONTEXTO.

### 7.3 Direção

- POSITIVA;
- NEGATIVA;
- NEUTRA;
- CONDICIONAL.

### 7.4 Força

Escala comum:

```text
0 a 100
```

| Faixa | Classificação |
|---:|---|
| 0–19 | Muito fraca |
| 20–39 | Fraca |
| 40–59 | Moderada |
| 60–79 | Forte |
| 80–100 | Muito forte |

A força relacional padrão vem da Biblioteca 15. A Tradução Estratégica calcula a força contextual.

### 7.5 Ordem

Para cada objetivo de origem, as alternativas de destino devem ser ordenadas por adequação contextual:

```text
ordem 1 = mais adequada
ordem 2 = segunda mais adequada
ordem 3 = terceira mais adequada
```

A ordem é derivada da pontuação efetiva e pode admitir empate dentro da tolerância metodológica.

### 7.6 Condição

- ESSENCIAL;
- PRIORITARIA;
- COMPLEMENTAR;
- OPCIONAL;
- COMPENSAVEL;
- CONFLITANTE;
- EXCLUDENTE.

Condições excludentes atuam como filtros, não como simples pesos negativos.

---

## 8. Matriz Marketing–Comunicação

A matriz avalia quais objetivos de Comunicação são mais ou menos adequados para contribuir com cada objetivo de Marketing no contexto da campanha.

Entradas mínimas:

- objetivo de Marketing;
- prioridade declarada;
- objetivo de Comunicação candidato;
- força padrão da relação;
- situação mercadológica;
- situação competitiva;
- público;
- praça;
- jornada;
- período;
- verba;
- restrições;
- confiança.

Saídas:

- força contextual;
- ordem de adequação;
- condição;
- justificativa estruturada;
- confiança contextual;
- alertas de insuficiência ou conflito.

Exemplo:

```text
Objetivo de Marketing: aumentar vendas.

Situação A: baixa notoriedade.
Ordem de Comunicação:
1. conhecimento;
2. consideração;
3. intenção;
4. ação.

Situação B: alta notoriedade e baixa conversão.
Ordem de Comunicação:
1. intenção;
2. redução de incerteza;
3. ação;
4. consideração.
```

O sistema não presume que “aumentar vendas” implique automaticamente “ação”. A ordem depende do diagnóstico contextual.

---

## 9. Derivação dos objetivos de Mídia

Objetivos de Mídia são produzidos pela Tradução Estratégica e não declarados como solução no Briefing.

A derivação deve considerar:

- objetivos de Comunicação priorizados;
- resultados pretendidos;
- indicadores requeridos;
- públicos;
- praças;
- jornadas e etapas;
- período;
- verba;
- pressão competitiva;
- restrições;
- tensões.

Exemplo:

```text
Objetivo de Comunicação: ampliar notoriedade.
        ↓
Objetivos de Mídia candidatos:
- construir alcance;
- ampliar cobertura;
- acelerar construção de alcance;
- produzir impacto;
- gerar frequência mínima.
```

Cada candidato recebe pontuação e ordem próprias.

---

## 10. Matriz Comunicação–Mídia

A matriz avalia quais objetivos de Mídia melhor favorecem os objetivos de Comunicação priorizados.

Saídas mínimas:

- objetivo de Mídia derivado;
- pontuação contextual;
- ordem;
- intensidade requerida;
- prioridade;
- peso;
- condição;
- indicadores relacionados;
- rastreabilidade;
- confiança.

Exemplo:

```text
Objetivo de Comunicação: lembrança.

Objetivos de Mídia ordenados:
1. gerar frequência;
2. sustentar continuidade;
3. manter presença;
4. ampliar alcance incremental.
```

A ordem pode mudar conforme ciclo de compra, prazo, verba, notoriedade prévia e pressão competitiva.

---

## 11. Pontuação contextual

A relação não é binária. Sua adequação deve ser calculada.

Estrutura conceitual:

```text
Força padrão
    ×
Prioridade da origem
    ×
Compatibilidade com público
    ×
Compatibilidade territorial
    ×
Compatibilidade com jornada e etapa
    ×
Compatibilidade temporal
    ×
Viabilidade orçamentária
    ×
Confiança
    ±
Tensões e restrições
    =
Pontuação contextual
```

A fórmula matemática definitiva, os coeficientes e a normalização pertencem à Biblioteca 17.

A Tradução Estratégica deve, contudo, preservar todos os componentes usados no cálculo.

---

## 12. Propagação de prioridades

```text
Peso do objetivo de Marketing
        ↓
força Marketing–Comunicação
        ↓
prioridade derivada de Comunicação
        ↓
força Comunicação–Mídia
        ↓
prioridade derivada de Mídia
```

Quando vários caminhos levarem ao mesmo objetivo, o motor deve compor as contribuições sem contar repetidamente a mesma origem.

Quando objetivos de origem concorrerem por recursos, a matriz deve registrar tensão e permitir normalização dentro da família decisória.

---

## 13. Dimensões técnicas

A Tradução Estratégica também opera sobre dimensões técnicas utilizadas pelos motores posteriores.

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
- diferenciação;
- sustentação.

Objetivos de Mídia e dimensões técnicas não são sinônimos. O objetivo indica a condição pretendida; a dimensão representa o eixo técnico utilizado para avaliar alternativas.

---

## 14. Matriz de influências

Cada elemento do Briefing pode:

- aumentar uma dimensão;
- reduzir uma dimensão;
- não afetar uma dimensão;
- afetar apenas em combinação com outro elemento.

```text
Elemento do Briefing
        ↓
Regra de influência
        ↓
Objetivo, relação ou dimensão
        ↓
Contribuição positiva, negativa, neutra ou condicional
```

Exemplos já consolidados:

- penetração tende a elevar alcance e cobertura;
- notoriedade tende a elevar alcance, impacto e velocidade;
- fidelização tende a elevar frequência, continuidade e afinidade;
- público amplo tende a elevar alcance e dispersão;
- público restrito tende a elevar seletividade e afinidade;
- período curto tende a elevar concentração e velocidade;
- verba limitada tende a elevar eficiência;
- forte pressão competitiva pode elevar frequência, continuidade, impacto ou diferenciação.

Esses enunciados devem ser convertidos em relações parametrizadas, versionadas e testáveis.

---

## 15. Intensidade requerida

Escala canônica:

```text
0 a 100
```

| Faixa | Classificação |
|---:|---|
| 0–19 | Muito baixa |
| 20–39 | Baixa |
| 40–59 | Média |
| 60–79 | Alta |
| 80–100 | Muito alta |

A classificação ordinal é apenas representação do valor numérico.

---

## 16. Peso estratégico

O peso representa quanto um objetivo, relação ou dimensão deve influenciar a avaliação posterior.

```text
0,00 a 1,00
```

Dentro de uma família normalizada, a soma dos pesos efetivos deve ser 1,00.

Intensidade e peso não são sinônimos:

```text
Intensidade = quanto é requerido.
Peso = quanto influencia a decisão.
```

---

## 17. Prioridade e condição

Prioridade:

- Muito baixa;
- Baixa;
- Média;
- Alta;
- Muito alta.

Condição:

- Obrigatória;
- Desejável;
- Compensável;
- Diagnóstica.

As condições aplicadas às relações seguem também a classificação definida na Biblioteca 15.

---

## 18. Tensões

A Tradução Estratégica deve identificar tensões como objetos estruturados.

Exemplos:

```text
Alcance muito alto × frequência muito alta × verba limitada
```

```text
Conversão imediata × baixa notoriedade
```

```text
Múltiplos objetivos prioritários × orçamento restrito
```

```text
Ampliação territorial × período curto
```

Cada tensão deve registrar:

- elementos envolvidos;
- origem;
- gravidade;
- direção;
- possibilidade de compensação;
- condição de exclusão, quando houver;
- etapas afetadas;
- decisão requerida.

---

## 19. Grau de confiança

Escala:

```text
0 a 100
```

A confiança deve considerar:

- completude do Briefing;
- presença de dados quantitativos;
- qualidade e atualidade das fontes;
- operacionalização dos objetivos;
- coerência entre declarações;
- quantidade de inferências;
- conflitos;
- estabilidade das regras.

A confiança não altera silenciosamente o peso. Ela informa a robustez da derivação e pode exigir validação humana.

---

## 20. Rastreabilidade

Toda derivação deve mostrar:

- objetivo de origem;
- objetivo de destino;
- relação aplicada;
- força padrão;
- fatores contextuais;
- força calculada;
- ordem;
- prioridade;
- peso;
- confiança;
- regras;
- versão;
- ajustes humanos.

Exemplo:

```text
Objetivo de Mídia: construir alcance.
Pontuação: 87.
Ordem: 1.

Origens:
- Marketing: penetração;
- Comunicação: notoriedade;
- público: amplo;
- praça: expansão territorial;
- concorrência: presença superior;
- relação M–C: força 82;
- relação C–M: força 91.
```

---

## 21. Valores calculados e ajustados

Todo objeto pontuado deve preservar:

```text
valor_padrao
valor_calculado
valor_ajustado
valor_efetivo
origem_do_ajuste
justificativa
responsavel
alterado_em
```

O ajuste não apaga o cálculo original.

---

## 22. Vínculos contextuais

Objetivos, relações, dimensões e pesos podem existir nos níveis:

- geral da Campanha;
- praça;
- universo;
- segmento;
- público;
- jornada;
- etapa;
- combinação dos anteriores.

Um valor geral não deve apagar diferenças relevantes entre contextos.

---

## 23. Contrato de saída

O Perfil Estratégico de Mídia deve entregar à Arquitetura:

- objetivos de Marketing operacionalizados;
- objetivos de Comunicação priorizados;
- objetivos de Mídia derivados e ordenados;
- relações efetivas entre objetivos;
- resultados pretendidos;
- indicadores prioritários;
- intensidades;
- pesos;
- condições;
- dimensões técnicas;
- tensões;
- restrições;
- confiança;
- rastreabilidade;
- registro de ajustes.

A saída não pode depender da leitura manual de texto narrativo.

---

## 24. Reprocessamento e versionamento

Alterações no Briefing devem provocar recálculo seletivo.

Cada execução deve estar vinculada a:

- Campanha;
- versão do Briefing;
- versão da Biblioteca 15;
- versão das regras;
- versão dos parâmetros e fórmulas;
- versão do Perfil Estratégico de Mídia.

O sistema deve preservar valores anteriores e sinalizar ajustes humanos potencialmente incompatíveis com novas entradas.

---

## 25. Critérios de conclusão

A Tradução Estratégica está concluída quando:

- os objetivos ativos foram operacionalizados;
- objetivos não mensuráveis foram bloqueados ou tratados como pendência;
- as relações Marketing–Comunicação foram pontuadas e ordenadas;
- os objetivos de Mídia foram derivados;
- as relações Comunicação–Mídia foram pontuadas e ordenadas;
- resultados e indicadores foram vinculados;
- intensidades e pesos foram calculados;
- tensões e restrições foram registradas;
- graus de confiança foram atribuídos;
- toda derivação possui origem rastreável;
- a saída está apta a alimentar a Arquitetura.

---

## 26. Decisões consolidadas

1. O artefato principal é paramétrico, não narrativo.
2. Objetivos devem ser operacionalizáveis e mensuráveis.
3. Marketing, Comunicação e Mídia são níveis distintos.
4. As relações são N:N, direcionais, pontuadas e ordenáveis.
5. A existência de uma relação não basta; sua adequação é contextual.
6. O Briefing declara objetivos de Marketing e Comunicação.
7. A Tradução Estratégica deriva objetivos de Mídia.
8. Intensidade, prioridade, peso, ordem e confiança são conceitos distintos.
9. Relações excludentes atuam como restrições.
10. Todo cálculo deve ser explicável e reproduzível.
11. O planejador pode ajustar valores, sem apagar o cálculo.
12. A Biblioteca 17 definirá fórmulas, coeficientes e normalizações.

---

## 27. Pontos ainda dependentes da Biblioteca 17

- fórmula final de pontuação contextual;
- coeficientes dos fatores;
- composição de múltiplos caminhos;
- tratamento de dependência entre objetivos;
- tolerância para empates;
- normalização dos pesos;
- penalização de conflitos;
- tratamento matemático da confiança;
- limiares de exclusão;
- testes de sensibilidade.