# Comparação de Cenários

**Documento:** `06_COMPARACAO_DE_CENARIOS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Comparação de Cenários é a função do Ambiente de Elaboração que transforma resultados simulados em uma avaliação estratégica explicável.

Ela não responde apenas qual cenário apresenta os maiores números. Responde:

```text
Qual cenário atende melhor ao Perfil Estratégico,
respeitando restrições, incertezas, custos,
papéis dos meios e compensações entre resultados?
```

Fluxo canônico:

```text
Arquiteturas Candidatas
        ↓
Cenários Simulados
        ↓
Comparação de Cenários
        ↓
Diagnósticos e trade-offs
        ↓
Otimização ou seleção
```

A Comparação pode resultar em:

- seleção de um cenário;
- encaminhamento para otimização;
- combinação de elementos de cenários;
- nova simulação;
- revisão da arquitetura;
- rejeição de alternativas.

Comparar não significa escolher imediatamente.

---

## 2. Artefato principal

O artefato desta função denomina-se:

```text
Análise Comparativa de Cenários
```

Ele deve preservar:

- cenários comparados e respectivas versões;
- Perfil Estratégico de referência;
- critérios;
- pesos;
- restrições;
- métodos de normalização;
- métricas nativas;
- métricas equivalentes;
- confiança;
- diferenças;
- compensações;
- diagnósticos;
- recomendações;
- decisão do planejador;
- histórico de versões.

Estrutura conceitual:

```text
Análise Comparativa
├── Conjunto de cenários
├── Base estratégica
├── Critérios
├── Restrições
├── Indicadores comparáveis
├── Indicadores contextuais
├── Normalizações
├── Pesos
├── Confiança
├── Resultados por critério
├── Trade-offs
├── Dominâncias
├── Fronteira de Pareto
├── Sensibilidade
├── Robustez
├── Diagnósticos
├── Recomendações
├── Decisão
└── Versionamento
```

---

## 3. Objetos comparáveis

A Comparação deve admitir:

### 3.1 Cenários da mesma arquitetura

Permite avaliar o efeito de diferenças em:

- verba;
- inventários;
- flight;
- audiência;
- overlap;
- saturação;
- taxas de performance;
- modelos de atribuição.

### 3.2 Cenários de arquiteturas diferentes

Permite comparar diferenças estruturais entre:

- meios;
- canais;
- papéis;
- relações entre mídias;
- pontos de contato;
- inventários;
- distribuição temporal e territorial.

### 3.3 Versões do mesmo cenário

Permite identificar o efeito de cada alteração registrada.

### 3.4 Cenários contra referências

Podem ser utilizados como referência:

- cenário-base;
- campanha anterior;
- benchmark;
- plano vigente;
- cenário mínimo;
- cenário ideal;
- cenário sem determinado meio.

---

## 4. Condições de comparabilidade

Dois cenários não devem ser comparados automaticamente apenas porque possuem resultados calculados.

A Comparação deve verificar:

- compatibilidade de universo;
- compatibilidade territorial;
- compatibilidade temporal;
- compatibilidade de públicos;
- mesma definição de conversão;
- mesma fórmula de ROAS;
- mesma base financeira;
- mesma moeda;
- mesma versão do motor de equivalências;
- mesma unidade de referência;
- modelos de atribuição compatíveis;
- níveis aceitáveis de confiança.

Quando essas condições não forem atendidas, o sistema deve:

```text
normalizar
ou
segmentar a comparação
ou
sinalizar incomparabilidade
```

Não deve produzir classificação artificial.

---

## 5. Camadas da comparação

A Comparação opera em três camadas.

### 5.1 Validade

Responde:

```text
O cenário pode ser considerado?
```

Verifica:

- restrições obrigatórias;
- orçamento;
- disponibilidade;
- cobertura mínima;
- públicos obrigatórios;
- praças obrigatórias;
- dados mínimos;
- consistência dos cálculos;
- alertas críticos.

Estados possíveis:

```text
Cenário válido
Cenário válido com ressalvas
Cenário inválido
```

Um cenário inválido pode permanecer visível para diagnóstico, mas não deve ser recomendado como solução final.

### 5.2 Desempenho

Responde:

```text
O que o cenário entrega?
```

Avalia resultados de:

- alcance;
- frequência;
- pressão;
- cobertura;
- GRP;
- TRP;
- CPM;
- CPP;
- CTR;
- CPC;
- CPA;
- conversões;
- receita;
- ROAS;
- alcance incremental;
- saturação;
- distribuição.

### 5.3 Aderência estratégica

Responde:

```text
O cenário entrega aquilo que é mais importante
para esta campanha?
```

Utiliza:

- pesos do Perfil Estratégico;
- prioridades;
- condições;
- papéis dos meios;
- jornada;
- pontos de contato;
- públicos;
- praças;
- objetivos;
- restrições;
- confiança.

Um cenário pode apresentar bom desempenho bruto e baixa aderência estratégica.

---

## 6. Restrições antes da pontuação

As restrições obrigatórias devem ser verificadas antes de qualquer índice geral.

Exemplos:

- orçamento máximo;
- presença obrigatória em determinada praça;
- alcance mínimo;
- frequência mínima ou máxima;
- canal obrigatório;
- canal proibido;
- período obrigatório;
- inventário indisponível;
- público prioritário sem atendimento;
- limite de saturação;
- condição legal ou institucional.

Nenhuma pontuação elevada pode compensar automaticamente o descumprimento de uma restrição obrigatória.

---

## 7. Famílias de critérios

Os critérios devem ser organizados em famílias.

### 7.1 Aderência estratégica

- alcance requerido;
- frequência requerida;
- cobertura geográfica;
- afinidade;
- seletividade;
- continuidade;
- impacto;
- velocidade de construção de alcance;
- mensurabilidade;
- capacidade de resposta;
- capacidade de conversão;
- adequação à jornada;
- flexibilidade;
- diferenciação;
- sustentação.

### 7.2 Entrega de mídia

- alcance líquido;
- alcance incremental;
- cobertura;
- frequência;
- impactos;
- GRP;
- TRP;
- pressão;
- continuidade;
- distribuição temporal;
- distribuição territorial.

### 7.3 Eficiência

- CPM;
- CPP;
- CPC;
- CPA;
- custo por alcance;
- custo por alcance incremental;
- custo por impacto equivalente;
- custo por conversão;
- eficiência marginal.

### 7.4 Performance

- CTR;
- cliques;
- taxa de conversão;
- conversões;
- receita;
- ROAS;
- contribuição atribuída.

### 7.5 Qualidade arquitetônica

- presença de meio principal coerente;
- complementaridade;
- equilíbrio entre papéis;
- cobertura da jornada;
- cobertura dos pontos de contato;
- dependência de um único canal;
- redundância;
- diversidade funcional;
- mensurabilidade;
- flexibilidade de ajuste.

### 7.6 Risco e confiança

- qualidade das fontes;
- confiança das equivalências;
- volatilidade dos preços;
- incerteza da audiência;
- dependência de benchmarks;
- sensibilidade a premissas;
- risco de saturação;
- risco de indisponibilidade;
- risco operacional.

---

## 8. Direção desejada dos indicadores

Cada critério deve declarar sua função de preferência.

### 8.1 Quanto maior, melhor

Exemplos:

- alcance;
- cobertura;
- conversões;
- receita;
- ROAS;
- afinidade;
- mensurabilidade;
- aderência estratégica.

### 8.2 Quanto menor, melhor

Exemplos:

- CPM;
- CPP;
- CPC;
- CPA;
- excesso de verba;
- redundância indesejada;
- risco;
- saturação;
- dependência.

### 8.3 Faixa ideal

Exemplos:

- frequência;
- pressão;
- concentração;
- participação do meio principal;
- diversidade de canais.

Nesses casos, valores muito baixos e muito altos podem ser inadequados.

A avaliação deve considerar a distância da faixa ideal, e não premiar automaticamente o maior valor.

---

## 9. Métricas nativas e equivalentes

A Comparação deve preservar simultaneamente:

```text
métrica nativa
métrica equivalente
```

A métrica nativa serve para:

- interpretação própria do meio;
- auditoria;
- negociação;
- avaliação operacional.

A métrica equivalente serve para:

- alcance combinado;
- frequência equivalente;
- overlap;
- saturação;
- eficiência transversal;
- atribuição;
- comparação entre meios.

A interface deve indicar claramente qual camada está sendo utilizada.

---

## 10. Normalização

Indicadores com unidades e escalas diferentes não podem ser somados diretamente.

A normalização deve convertê-los para uma escala comum, preferencialmente:

```text
0 a 100
```

O resultado normalizado não substitui o valor original.

Cada registro deve preservar:

```text
valor original
unidade
valor normalizado
método de normalização
referência
direção desejada
```

### 10.1 Métodos admitidos

- relativo ao conjunto comparado;
- relativo a meta;
- relativo a faixa ideal;
- relativo a benchmark;
- função personalizada.

O método deve ser escolhido conforme a natureza do critério e permanecer explícito e versionado.

---

## 11. Pesos estratégicos

Os pesos devem vir prioritariamente do Perfil Estratégico.

```text
Peso estratégico efetivo
×
resultado normalizado
=
contribuição ponderada
```

O sistema não deve criar pesos arbitrários durante a comparação.

Ajustes devem ser:

- explícitos;
- justificados;
- versionados;
- diferenciados do valor original.

Estrutura canônica:

```text
peso calculado
peso ajustado
peso efetivo
```

---

## 12. Pontuação por critério

Forma conceitual:

```text
Pontuação do critério =
desempenho normalizado
× peso estratégico
× fator de confiança
```

A interface deve mostrar separadamente:

- desempenho;
- peso;
- confiança;
- contribuição final.

O fator de confiança não deve ocultar a incerteza nem substituir sua apresentação explícita.

---

## 13. Índices compostos

A Comparação pode gerar índices por família:

```text
Índice de Aderência Estratégica
Índice de Entrega
Índice de Eficiência
Índice de Performance
Índice de Qualidade Arquitetônica
Índice de Confiança
Índice de Risco
Índice de Robustez
```

Somente depois poderá existir um:

```text
Índice Global do Cenário
```

Forma conceitual:

```text
Índice Global =
Σ índices de família × pesos das famílias
```

O índice global não deve apagar os índices parciais nem substituir a análise explicativa.

---

## 14. Compensações e trade-offs

A Comparação deve explicitar o que se ganha e o que se perde em cada alternativa.

Cada trade-off deve registrar:

```text
critério favorecido
critério prejudicado
magnitude
peso estratégico
relevância
aceitabilidade
```

A condição definida no Perfil Estratégico orienta a compensabilidade:

### Obrigatória

Não pode ser compensada.

### Desejável

Pode sofrer pequena perda, mas deve influenciar a recomendação.

### Compensável

Pode ser reduzida quando outro ganho estratégico justificar.

### Diagnóstica

Serve à compreensão sem determinar diretamente a escolha.

---

## 15. Dominância

Um cenário domina outro quando:

- é igual ou superior nos critérios relevantes;
- não viola mais restrições;
- possui confiança igual ou maior;
- não exige custo superior sem ganho correspondente.

Classificações possíveis:

```text
Cenário dominante
Cenário parcialmente dominante
Cenário dominado
```

Cenários dominados podem ser mantidos para auditoria, mas não devem ocupar a mesma prioridade das alternativas eficientes.

---

## 16. Fronteira de Pareto

Quando nenhum cenário for superior em todos os critérios, a Comparação deve identificar a fronteira de Pareto.

Um cenário pertence à fronteira quando:

```text
não é possível melhorar um critério
sem piorar outro
```

Os cenários de Pareto devem ser apresentados como alternativas legítimas antes da aplicação da decisão humana final.

---

## 17. Comparação marginal

A Comparação deve medir os efeitos incrementais entre cenários.

Indicadores possíveis:

- custo marginal por ponto de alcance;
- custo marginal por mil impactos;
- custo marginal por conversão;
- ganho marginal de frequência;
- ganho marginal de receita;
- ROAS marginal;
- redução marginal de risco.

A comparação marginal é um insumo essencial para a Otimização.

---

## 18. Comparação dos papéis dos meios

A Comparação deve observar:

- coerência entre papel arquitetônico e papel sugerido pela Simulação;
- papel efetivo adotado;
- centralidade real do meio;
- participação na entrega;
- participação no investimento;
- contribuição para objetivos;
- dependência da arquitetura;
- capacidade de substituição;
- complementaridade.

Pode diagnosticar:

- meio principal incoerente;
- ausência de liderança funcional;
- concentração excessiva em um único canal;
- meio de apoio exercendo função estrutural;
- meio complementar com contribuição principal.

A Comparação não altera os papéis silenciosamente. Ela registra discrepâncias e recomendações.

---

## 19. Comparação temporal

A análise temporal deve considerar:

- frequência por período;
- pressão por fase;
- continuidade;
- períodos de ausência;
- concentração;
- picos;
- intervalos;
- saturação;
- eficiência temporal.

Dois cenários com o mesmo volume agregado podem apresentar curvas de pressão e frequência muito diferentes.

A adequação deve ser julgada em relação à estratégia temporal e às fases da campanha.

---

## 20. Comparação territorial

Deve ser possível avaliar:

- cobertura por praça;
- alcance por praça;
- frequência por praça;
- investimento por praça;
- custo por praça;
- pressão territorial;
- públicos subatendidos;
- redundância;
- desigualdade de distribuição.

Resultados gerais não devem apagar falhas em praças prioritárias.

---

## 21. Comparação por público e jornada

Os resultados devem ser avaliados por:

- segmento;
- público;
- target;
- etapa da jornada;
- ponto de contato;
- função de mídia.

Um cenário com menor resultado total pode ser mais aderente se atender melhor o público prioritário ou uma etapa crítica da jornada.

---

## 22. Comparação de custos

A base financeira deve ser consistente entre os cenários.

Devem ser separados:

- investimento bruto de mídia;
- investimento líquido de mídia;
- comissão;
- taxas de plataforma;
- operação de mídia;
- custos não midiáticos;
- custo total da campanha.

Cada indicador deve declarar qual base utiliza.

Exemplo:

```text
CPM de mídia:
considera apenas o investimento de mídia definido pela regra

ROAS global:
considera o custo elegível segundo a fórmula e a política vigentes
```

---

## 23. Confiança e incerteza

Cada indicador deve preservar:

```text
valor central
faixa provável
confiança
sensibilidade
```

Quando as faixas prováveis se sobrepõem, o sistema não deve afirmar superioridade absoluta.

Classificações possíveis:

- diferença conclusiva;
- diferença provável;
- diferença incerta;
- diferença irrelevante;
- empate técnico.

---

## 24. Sensibilidade

A análise de sensibilidade verifica como a classificação muda quando as premissas variam dentro de intervalos plausíveis.

Exemplos:

- audiência;
- CTR;
- CPC;
- overlap;
- taxa de conversão;
- verba;
- preços;
- confiança;
- pesos estratégicos;
- parâmetros de equivalência.

Pergunta central:

```text
O cenário continua recomendado
quando as premissas mudam dentro de limites plausíveis?
```

---

## 25. Robustez

Um cenário é robusto quando:

- permanece competitivo sob diferentes premissas;
- não depende de um único dado incerto;
- mantém aderência com pequenas alterações;
- tolera variações de preço;
- não viola restrições com facilidade;
- não muda drasticamente diante de ajustes mínimos.

Confiança e robustez não são sinônimos:

```text
Confiança = qualidade dos dados e estimativas
Robustez = estabilidade da solução
```

---

## 26. Diagnósticos comparativos

A Comparação deve produzir diagnósticos explicativos.

Cada diagnóstico deve conter:

```text
origem
indicadores envolvidos
cenários afetados
magnitude
peso estratégico
confiança
ação sugerida
```

Exemplos:

- maior alcance, mas baixa afinidade;
- menor custo, porém frequência insuficiente;
- boa performance, mas dependência excessiva de um canal;
- alta pressão inicial e risco de saturação;
- superioridade dependente de premissas frágeis;
- meio principal incoerente;
- cobertura territorial desigual;
- cenário robusto sob redução de audiência.

---

## 27. Tipos de recomendação

A Comparação pode recomendar:

### Seleção

```text
Cenário recomendado para o Plano Consolidado
```

### Otimização

```text
Cenário promissor, mas exige ajustes
```

### Combinação

```text
Elementos de cenários diferentes podem formar
uma alternativa superior
```

### Nova simulação

```text
Resultados inconclusivos ou premissas insuficientes
```

### Revisão da arquitetura

```text
O problema é estrutural e não apenas paramétrico
```

### Rejeição

```text
Cenário dominado, inválido ou incompatível
```

---

## 28. Recomendação e decisão

O sistema deve separar:

```text
cenário tecnicamente recomendado
cenário selecionado pelo planejador
```

O planejador pode selecionar outra alternativa, desde que registre:

- justificativa;
- riscos aceitos;
- compensações;
- restrições flexibilizadas;
- diferenças em relação à recomendação.

A autonomia humana deve ser preservada com auditabilidade.

---

## 29. Matriz comparativa

A interface deve permitir comparar cenários por:

- valor nativo;
- valor equivalente;
- valor normalizado;
- contribuição ponderada;
- confiança;
- diferença absoluta;
- diferença relativa;
- resultado marginal.

Estrutura mínima:

| Critério | Peso | Cenário A | Cenário B | Cenário C |
|---|---:|---:|---:|---:|
| Alcance | 0,25 | — | — | — |
| Frequência | 0,20 | — | — | — |
| Afinidade | 0,15 | — | — | — |
| Eficiência | 0,15 | — | — | — |
| Performance | 0,15 | — | — | — |
| Confiança | 0,10 | — | — | — |

---

## 30. Visualizações

A Comparação pode apresentar:

- tabela comparativa;
- gráfico de perfis;
- curvas temporais;
- distribuição territorial;
- fronteira de Pareto;
- mapa de trade-offs;
- decomposição da pontuação;
- análise de sensibilidade;
- diferenças marginais;
- matriz de riscos.

Nenhuma visualização deve ocultar os dados, fórmulas, premissas ou versões que a originaram.

---

## 31. Estados da análise comparativa

Estados possíveis:

```text
rascunho
configurada
calculada
com inconsistências
apta para decisão
em revisão
selecionada
enviada para otimização
arquivada
```

A análise deve registrar:

- cenários e versões;
- data;
- responsável;
- Perfil Estratégico utilizado;
- pesos;
- normalizações;
- restrições;
- resultados;
- recomendação;
- decisão.

---

## 32. Recálculo e desatualização

A análise deve ser invalidada ou marcada como desatualizada quando houver alteração em:

- cenário;
- arquitetura;
- Perfil Estratégico;
- peso;
- restrição;
- fórmula;
- motor de equivalências;
- fonte de audiência;
- confiança;
- modelo de atribuição;
- base de custos.

O recálculo deve preservar a versão anterior.

---

## 33. Contrato com a Otimização

A Comparação deve entregar à Otimização:

```text
cenários válidos
cenários dominados
fronteira de Pareto
critérios
pesos
restrições
metas
faixas ideais
resultados normalizados
resultados marginais
trade-offs
sensibilidade
riscos
confiança
diagnósticos
```

A Otimização poderá procurar alterações capazes de:

- elevar aderência;
- reduzir custo;
- aumentar alcance;
- corrigir frequência;
- reduzir saturação;
- melhorar robustez;
- redistribuir verba;
- substituir inventários;
- corrigir papéis;
- melhorar cobertura territorial;
- melhorar cobertura da jornada.

---

## 34. Limites da Comparação

A Comparação deve:

- validar cenários;
- normalizar resultados;
- aplicar pesos;
- identificar trade-offs;
- detectar dominância;
- identificar a fronteira de Pareto;
- analisar confiança;
- medir robustez;
- produzir diagnósticos;
- gerar recomendações.

A Comparação não deve:

- alterar cenários silenciosamente;
- escolher com base apenas no maior resultado;
- compensar restrições obrigatórias;
- ocultar métricas nativas;
- tratar estimativas frágeis como certezas;
- impor automaticamente uma decisão;
- executar a otimização dentro da própria comparação.

---

## 35. Formulação canônica

A **Comparação de Cenários** é o processo estruturado que avalia cenários simulados segundo sua validade, desempenho, aderência estratégica, eficiência, confiança, risco e robustez, tornando explícitas as diferenças, compensações e consequências de cada alternativa.

Seu resultado não é apenas um ranking. É uma **Análise Comparativa de Cenários** capaz de indicar:

```text
qual alternativa é mais aderente;
por que ela é mais aderente;
o que se ganha;
o que se perde;
quais incertezas permanecem;
e quais ajustes devem ser encaminhados à Otimização.
```
