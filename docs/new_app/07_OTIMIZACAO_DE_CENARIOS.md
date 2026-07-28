# Otimização de Cenários

A **Otimização de Cenários** é a função do Ambiente de Elaboração responsável por propor alterações em variáveis controláveis de um cenário já simulado e comparado, buscando melhorar sua aderência estratégica, eficiência, entrega, performance, robustez ou viabilidade, sem violar restrições e sem ocultar os trade-offs produzidos.

A pergunta orientadora é:

> Que alterações podem tornar o cenário mais aderente, eficiente, robusto e operacionalmente viável, sem violar as restrições da campanha?

A Otimização não encerra o processo. Ela produz um **Cenário Otimizado Candidato**, que deve retornar à Simulação e à Comparação.

```text
Arquitetura
    ↓
Simulação
    ↓
Comparação
    ↓
Otimização
    ↓
Nova Simulação
    ↓
Nova Comparação
    ↓
Seleção ou nova iteração
```

## 1. Artefato principal

O artefato desta função é a:

```text
Proposta de Otimização de Cenário
```

Ela deve conter:

- cenário de origem;
- Perfil Estratégico;
- diagnóstico que motivou a otimização;
- objetivos;
- restrições;
- variáveis de decisão;
- variáveis protegidas;
- método utilizado;
- alterações propostas;
- impacto esperado;
- cenário otimizado candidato;
- comparação incremental;
- ganhos e perdas;
- trade-offs;
- confiança;
- robustez;
- riscos;
- recomendação;
- decisão do planejador;
- versionamento.

Estrutura conceitual:

```text
Proposta de Otimização
├── Cenário de origem
├── Perfil Estratégico
├── Diagnóstico
├── Objetivos
├── Restrições
├── Variáveis de decisão
├── Variáveis protegidas
├── Métodos
├── Alterações sugeridas
├── Resultados estimados
├── Cenário otimizado candidato
├── Comparação incremental
├── Trade-offs
├── Confiança
├── Robustez
├── Recomendação
├── Decisão
└── Versionamento
```

## 2. O que pode ser otimizado

A Otimização deve operar apenas sobre elementos legitimamente modificáveis.

### 2.1 Distribuição de verba

Pode redistribuir investimento entre:

- meios;
- canais;
- veículos;
- inventários;
- praças;
- públicos;
- fases;
- períodos;
- funções de mídia;
- papéis estratégicos.

Toda redistribuição deve considerar quantidade mínima, lote comercial, disponibilidade, perda de desconto, variação de preço, pressão mínima, papel do meio e impacto arquitetônico.

### 2.2 Seleção de inventários

Pode:

- substituir inventários;
- retirar inventários dominados;
- incluir inventários elegíveis;
- trocar faixas, formatos e veículos;
- reorganizar pacotes;
- ajustar quantidades.

### 2.3 Distribuição temporal

Pode modificar:

- início e fim;
- duração;
- distribuição por fase;
- continuidade;
- concentração;
- intervalos;
- pulsação;
- ondas;
- curvas crescentes ou decrescentes;
- presença em datas críticas.

### 2.4 Distribuição territorial

Pode alterar:

- verba por praça;
- pressão por praça;
- canais por praça;
- inventários locais;
- prioridade territorial;
- cobertura mínima;
- equilíbrio entre territórios.

### 2.5 Distribuição por público

Pode ajustar:

- investimento por target;
- intensidade por segmento;
- meios por público;
- frequência;
- pontos de contato;
- etapas da jornada.

### 2.6 Papéis dos meios

Pode propor reclassificações entre:

- Principal;
- Complementar;
- Apoio.

Também pode propor papéis múltiplos e contextuais:

```text
papel_geral
papel_por_objetivo
papel_por_publico
papel_por_praca
papel_por_fase
papel_por_jornada
```

A reclassificação deve ser fundamentada por resultados simulados e comparativos.

### 2.7 Overlap

Pode alterar a composição do cenário para produzir um overlap mais favorável, ajustando combinações de canais, redundância, concentração e expansão de alcance.

Não deve alterar arbitrariamente coeficientes técnicos de overlap apenas para melhorar resultados.

### 2.8 Saturação

Pode reduzir saturação por:

- redistribuição temporal;
- redução de frequência;
- substituição de inventário;
- expansão territorial;
- ampliação de público;
- diversificação de canais;
- mudança de flight;
- deslocamento de verba.

### 2.9 Custos e condições comerciais

Pode procurar:

- inventários de menor custo;
- pacotes mais eficientes;
- descontos existentes;
- bonificações existentes;
- redução de taxas;
- melhor relação entre preço e entrega;
- substituição de inventários com baixa eficiência marginal.

O motor não deve inventar preços, descontos, bonificações ou condições comerciais inexistentes.

## 3. Elementos protegidos

Alguns elementos não devem ser alterados livremente:

- objetivo estratégico;
- público obrigatório;
- praça obrigatória;
- orçamento máximo;
- período institucional;
- canal contratualmente obrigatório;
- inventário já comprado;
- frequência mínima;
- restrição legal;
- meio proibido;
- identidade territorial;
- data de lançamento;
- regra de comissão;
- fórmula de ROAS;
- definição de conversão.

Cada parâmetro deve possuir um estado:

```text
livre
ajustável
condicionado
protegido
obrigatório
```

## 4. Objetivos da Otimização

### 4.1 Maximização

Exemplos:

- maximizar alcance;
- maximizar alcance incremental;
- maximizar cobertura;
- maximizar conversões;
- maximizar receita;
- maximizar ROAS;
- maximizar aderência estratégica;
- maximizar robustez;
- maximizar confiança média;
- maximizar cobertura da jornada.

### 4.2 Minimização

Exemplos:

- minimizar custo;
- minimizar CPM;
- minimizar CPA;
- minimizar redundância;
- minimizar saturação;
- minimizar risco;
- minimizar dependência de canal;
- minimizar concentração territorial;
- minimizar verba não alocada.

### 4.3 Aproximação de meta

Exemplos:

- frequência entre 4 e 7;
- alcance mínimo de 70%;
- pressão semanal dentro de uma faixa;
- participação do meio principal entre 35% e 55%;
- investimento por praça proporcional à prioridade;
- CPA abaixo de um teto.

### 4.4 Equilíbrio

Exemplos:

- equilibrar alcance e frequência;
- equilibrar performance e construção de marca;
- equilibrar custo e confiança;
- equilibrar cobertura territorial;
- equilibrar papéis dos meios;
- equilibrar pressão entre fases.

## 5. Otimização mono-objetivo e multiobjetivo

### 5.1 Mono-objetivo

Busca melhorar uma única variável principal, como minimizar CPA ou maximizar alcance.

É adequada quando a prioridade é inequívoca, mas pode gerar distorções, como concentração excessiva, queda de cobertura, aumento de risco ou descaracterização arquitetônica.

### 5.2 Multiobjetivo

Busca equilibrar várias dimensões simultaneamente.

Exemplo:

```text
Maximizar:
- alcance;
- aderência estratégica;
- robustez.

Minimizar:
- custo;
- saturação;
- risco.
```

Essa abordagem é mais coerente com o planejamento de mídia e pode resultar em um conjunto de soluções eficientes, não em uma única solução.

## 6. Função-objetivo

Forma conceitual:

```text
Função-objetivo =
benefícios ponderados
− custos ponderados
− penalizações
```

Exemplo:

```text
Resultado da otimização =
aderência estratégica
+ alcance incremental
+ robustez
− custo
− saturação
− risco
```

Os pesos devem vir do Perfil Estratégico ou ser configurados explicitamente. O motor não deve criar prioridades ocultas.

## 7. Restrições

### 7.1 Financeiras

- orçamento máximo e mínimo;
- limite por meio;
- limite por praça;
- limite por período;
- saldo máximo permitido;
- comissão;
- custos obrigatórios.

### 7.2 Comerciais

- pacote mínimo;
- quantidade mínima;
- preço válido;
- inventário indisponível;
- compra indivisível;
- contrato firmado;
- bonificação condicionada.

### 7.3 Estratégicas

- meio obrigatório;
- função obrigatória;
- presença em etapa da jornada;
- cobertura mínima;
- público prioritário;
- praça prioritária;
- papel mínimo ou máximo.

### 7.4 Técnicas

- frequência mínima e máxima;
- alcance mínimo;
- saturação máxima;
- overlap aceitável;
- pressão por período;
- quantidade máxima de inserções.

### 7.5 Temporais

- duração;
- datas fixas;
- fase obrigatória;
- janela de veiculação;
- presença mínima;
- intervalo máximo sem mídia.

### 7.6 Operacionais

- capacidade de produção;
- limite de peças;
- disponibilidade de formatos;
- capacidade de monitoramento;
- número máximo de plataformas;
- prazo de implementação.

## 8. Restrições rígidas e flexíveis

### Rígidas

Não podem ser violadas.

Exemplos:

- orçamento máximo;
- praça obrigatória;
- inventário indisponível;
- restrição legal;
- data de lançamento.

### Flexíveis

Podem ser violadas dentro de tolerância, mediante penalização.

Exemplos:

- frequência desejada;
- participação ideal de um meio;
- distribuição territorial recomendada;
- diversidade de canais;
- CPM de referência.

Estrutura:

```text
restrição
tipo
limite
tolerância
penalização
prioridade
```

## 9. Variáveis de decisão

Exemplos:

```text
verba por meio
verba por canal
quantidade de inventário
praça
período
fase
flight
frequência
papel do meio
combinação de canais
seleção de inventários
```

Cada variável deve registrar:

- valor atual;
- mínimo;
- máximo;
- passo de alteração;
- unidade;
- estado;
- dependências;
- custo de mudança.

## 10. Dependências entre variáveis

As variáveis não são independentes.

```text
Aumentar verba em TV
    ↓
aumenta inserções
    ↓
altera GRP
    ↓
altera frequência
    ↓
altera pressão
    ↓
pode aumentar saturação
```

```text
Retirar um inventário
    ↓
pode perder desconto do pacote
    ↓
aumentar preço unitário
    ↓
reduzir eficiência total
```

Toda alteração deve provocar recálculo de suas consequências.

## 11. Métricas nativas e equivalentes

A otimização transversal deve operar principalmente sobre métricas equivalentes, como:

- impactos equivalentes;
- alcance equivalente;
- frequência equivalente;
- custo por impacto equivalente;
- alcance incremental equivalente;
- pressão equivalente;
- contribuição equivalente.

As métricas nativas permanecem preservadas para interpretação, negociação, controle e auditoria.

## 12. Alcance, frequência, pressão e flight

A Otimização deve tratar alcance e frequência de forma articulada.

Mais frequência não significa necessariamente mais alcance. Após determinado ponto:

- a frequência cresce;
- o alcance cresce pouco;
- a saturação aumenta;
- o custo marginal piora.

O motor deve identificar:

```text
ponto de eficiência
ponto de retorno decrescente
ponto de saturação
```

A pressão deve ser otimizada como curva temporal, considerando:

- frequência por período;
- concentração;
- continuidade;
- picos;
- intervalos;
- simultaneidade;
- sobreposição entre canais;
- pressão acumulada.

## 13. Otimização da saturação

A saturação pode ser reduzida sem necessariamente diminuir o investimento total.

Possíveis ações:

- expandir alcance;
- variar inventários;
- mudar praça;
- mudar público;
- redistribuir no tempo;
- reduzir repetição;
- combinar meios;
- ampliar cobertura da jornada;
- deslocar verba para canais de menor saturação marginal.

A proposta deve mostrar:

```text
saturação antes
saturação depois
ganho esperado
efeitos colaterais
```

## 14. Otimização do overlap

O overlap pode ser desejável quando aumenta frequência, reforço, lembrança, continuidade, sequenciamento ou retargeting.

Pode ser indesejável quando produz redundância, desperdício, concentração, saturação ou baixa expansão de alcance.

A Otimização deve considerar o papel estratégico do overlap e não assumir que menor overlap é sempre melhor.

## 15. Otimização por função de mídia

A Otimização não deve se limitar aos meios. Deve verificar se as funções necessárias estão suficientemente atendidas.

Exemplos:

- gerar alcance;
- reforçar frequência;
- sustentar presença;
- ativar conversão;
- produzir dados;
- cobrir território;
- apoiar decisão;
- ampliar afinidade.

Um meio pode ser substituído por outro desde que a função seja preservada ou melhorada.

## 16. Otimização territorial, por público e por jornada

### Territorial

Pode considerar prioridade, população, potencial, custo, cobertura, presença competitiva, capacidade de conversão e disponibilidade de inventário.

A média geral não deve esconder praças subatendidas.

### Por público

Pode buscar maior cobertura do público prioritário, menor exposição fora do target, melhor afinidade, frequência adequada e menor custo por target.

A melhoria do total geral não deve ocorrer à custa do público prioritário.

### Pela jornada

Pode identificar lacunas como excesso de presença em conhecimento, pouca presença em consideração ou ausência em conversão.

Pode então incluir canais, mudar formatos, redistribuir verba, alterar papéis, criar sequenciamento ou reforçar pontos de contato.

## 17. Otimização de custos

O motor deve distinguir:

- redução absoluta de custo;
- aumento de eficiência;
- redução de custo marginal;
- redução de desperdício;
- melhor distribuição do orçamento.

Economizar não é necessariamente melhorar se a perda estratégica for desproporcional.

A proposta deve apresentar:

```text
economia
perda de entrega
perda de aderência
variação de risco
efeito marginal
```

## 18. Eficiência marginal

A Otimização deve considerar quanto cada unidade adicional de investimento produz.

Indicadores possíveis:

- custo marginal por ponto de alcance;
- custo marginal por conversão;
- receita marginal;
- ROAS marginal;
- frequência marginal;
- impacto equivalente marginal.

O motor deve identificar inventários com retorno marginal alto, retorno decrescente, verba realocável e pontos em que o investimento adicional deixa de ser eficiente.

## 19. Otimização do ROAS

O ROAS não deve ser otimizado isoladamente.

Um cenário pode aumentar o ROAS reduzindo drasticamente alcance, escala, cobertura, construção de marca ou presença territorial.

A Otimização deve considerar simultaneamente:

- ROAS;
- receita;
- escala;
- conversões;
- aderência;
- risco;
- confiança;
- objetivos não financeiros.

A saída deve declarar:

```text
ROAS antes
ROAS depois
receita antes
receita depois
investimento antes
investimento depois
escala perdida ou adquirida
```

## 20. Métodos de otimização

O sistema pode admitir diferentes métodos.

### 20.1 Regras heurísticas

Úteis para recomendações explicáveis, como:

- reduzir verba em inventários saturados;
- aumentar investimento em praças subatendidas;
- substituir inventários dominados;
- redistribuir frequência excessiva;
- priorizar maior eficiência marginal.

### 20.2 Busca por cenários

Gera múltiplas combinações e as envia para Simulação e Comparação.

### 20.3 Programação linear

Adequada quando relações e restrições são lineares.

### 20.4 Programação inteira

Adequada quando compras são indivisíveis, como inserções, pacotes, faces, diárias e patrocínios.

### 20.5 Otimização não linear

Adequada para saturação, curvas de alcance, frequência, resposta, conversão e retornos decrescentes.

### 20.6 Métodos multiobjetivo

Adequados para construir uma fronteira de soluções eficientes.

### 20.7 Simulação estocástica

Adequada quando há incertezas relevantes em audiência, preços, CTR, conversão, overlap, receita ou disponibilidade.

## 21. Explicabilidade

Independentemente do método, o sistema deve explicar:

- o que foi alterado;
- por que foi alterado;
- qual restrição foi considerada;
- qual objetivo foi favorecido;
- qual perda foi aceita;
- qual resultado era esperado;
- qual confiança existe.

A saída não deve se limitar a informar que uma solução ótima foi encontrada.

## 22. Ótimo matemático e solução estratégica satisfatória

### Ótimo matemático

É o melhor resultado segundo a função definida.

### Solução estratégica satisfatória

É a alternativa que:

- atende às restrições;
- alcança metas;
- possui risco aceitável;
- é operacionalmente simples;
- mantém coerência arquitetônica;
- é explicável;
- preserva flexibilidade.

Uma solução matematicamente ótima pode ser inadequada se depender de premissas frágeis, concentrar risco, exigir execução inviável ou perder coerência estratégica.

## 23. Robustez e incerteza

Toda solução otimizada deve ser submetida a variações plausíveis, como:

- audiência −10%;
- preço +10%;
- CTR −15%;
- conversão −20%;
- overlap maior;
- inventário indisponível;
- redução de orçamento;
- atraso de fase.

O sistema deve verificar:

```text
A solução permanece válida?
A recomendação permanece superior?
As restrições continuam atendidas?
```

Pode ser preferível uma solução ligeiramente inferior no valor central, mas mais estável em cenários adversos.

Quando os parâmetros possuem intervalos, a Otimização deve trabalhar com:

- valor esperado;
- cenário conservador;
- cenário provável;
- cenário favorável;
- pior caso;
- melhor caso.

Posturas possíveis:

```text
conservadora
equilibrada
agressiva
```

## 24. Penalizações

A função de otimização pode penalizar:

- violação de meta;
- saturação;
- concentração;
- baixa confiança;
- excesso de complexidade;
- dependência de canal;
- ausência de cobertura;
- desvio de papel;
- verba ociosa;
- risco operacional.

Cada penalização deve registrar regra, intensidade, origem, justificativa e versão.

## 25. Complexidade operacional

Mais canais e inventários não significam automaticamente uma solução melhor.

Pode existir custo de complexidade relacionado a:

- número de plataformas;
- quantidade de peças;
- fornecedores;
- formatos;
- praças;
- adaptações;
- monitoramento;
- equipes;
- contratos.

A proposta deve poder medir:

```text
complexidade atual
complexidade proposta
ganho estratégico
custo operacional adicional
```

## 26. Flexibilidade e reversibilidade

A Otimização pode considerar:

- facilidade de redistribuição;
- possibilidade de cancelamento;
- velocidade de ativação;
- possibilidade de pausa;
- granularidade da compra;
- disponibilidade de dados;
- capacidade de reotimização.

A flexibilidade pode ser tratada como critério estratégico.

## 27. Tipos de proposta

A Otimização pode gerar:

- redistribuição;
- substituição;
- reconfiguração temporal;
- reconfiguração territorial;
- reconfiguração de públicos;
- reclassificação de papéis;
- simplificação;
- expansão;
- combinação de cenários;
- revisão estrutural da Arquitetura.

A combinação de cenários gera um novo cenário. Não é uma média simples entre alternativas.

## 28. Cenário Otimizado Candidato

A saída operacional da Otimização é o:

```text
Cenário Otimizado Candidato
```

Ele deve preservar:

- cenário de origem;
- alterações;
- justificativas;
- parâmetros novos;
- parâmetros mantidos;
- resultados recalculados;
- comparação incremental;
- confiança;
- alertas;
- riscos.

## 29. Comparação antes e depois

Toda proposta deve apresentar:

```text
Antes
Depois
Diferença absoluta
Diferença percentual
Diferença normalizada
Efeito estratégico
Confiança
```

Exemplo:

```text
Alcance:
62% → 68%

Frequência:
8,4 → 6,7

Investimento:
R$ 100.000 → R$ 100.000

Saturação:
Alta → Média
```

## 30. Ganhos e perdas

A proposta deve declarar explicitamente ganhos e perdas.

### Ganhos possíveis

- maior alcance;
- menor saturação;
- melhor cobertura territorial;
- menor custo;
- maior robustez;
- maior aderência.

### Perdas possíveis

- redução de frequência;
- menor presença em determinado canal;
- aumento de complexidade;
- menor flexibilidade;
- perda de desconto;
- aumento de risco em uma praça.

## 31. Critérios de aceitação

Uma proposta pode ser classificada como:

```text
recomendada
recomendada com ressalvas
alternativa
experimental
inviável
dominada
```

Para ser recomendada, deve:

- atender às restrições rígidas;
- melhorar ao menos um objetivo relevante;
- não produzir perdas desproporcionais;
- possuir confiança aceitável;
- ser operacionalmente viável;
- superar ou complementar o cenário de origem.

## 32. Decisão humana

O sistema deve separar:

```text
proposta gerada pelo sistema
proposta aceita pelo planejador
```

O planejador pode:

- aceitar integralmente;
- aceitar parcialmente;
- ajustar;
- rejeitar;
- solicitar nova otimização;
- bloquear uma variável;
- alterar prioridades.

A decisão deve registrar responsável, data, justificativa, riscos aceitos, mudanças manuais e nova versão.

## 33. Estados da otimização

```text
rascunho
configurada
em processamento
calculada
com inconsistências
apta para revisão
aceita
aceita parcialmente
rejeitada
convertida em cenário
enviada para nova comparação
arquivada
```

## 34. Versionamento e recálculo

Cada alteração deve gerar uma nova versão, preservando:

- método;
- parâmetros;
- pesos;
- restrições;
- cenário de origem;
- resultados;
- alterações manuais;
- decisão.

A proposta deve ser marcada como desatualizada quando houver alteração em:

- cenário de origem;
- Perfil Estratégico;
- pesos;
- restrições;
- preços;
- inventários;
- audiência;
- equivalências;
- overlap;
- saturação;
- fórmula;
- modelo de atribuição;
- confiança.

## 35. Alertas

O motor deve sinalizar:

- solução inviável;
- ausência de melhoria relevante;
- ganho baseado em premissa frágil;
- violação de restrição;
- aumento excessivo de complexidade;
- concentração de risco;
- perda de função estratégica;
- papel incoerente;
- dependência de inventário indisponível;
- melhoria apenas aparente;
- resultado muito sensível;
- solução dominada;
- pequena diferença em relação ao cenário atual.

## 36. Contrato de entrada

A Otimização deve receber:

```text
cenário de origem
arquitetura
Perfil Estratégico
comparação
diagnósticos
critérios
pesos
restrições
metas
faixas ideais
variáveis alteráveis
variáveis protegidas
inventários elegíveis
preços
disponibilidade
métricas nativas
métricas equivalentes
curvas de alcance
curvas de saturação
overlap
resultados marginais
confiança
riscos
```

## 37. Contrato de saída

A Otimização deve entregar:

```text
proposta identificada e versionada
cenário de origem
objetivo
método
restrições
variáveis alteradas
alterações propostas
cenário otimizado candidato
resultados recalculados
comparação antes e depois
ganhos
perdas
trade-offs
confiança
robustez
riscos
alertas
recomendação
decisão
```

## 38. Relação com Simulação, Comparação e Arquitetura

A Otimização não deve calcular isoladamente os resultados finais.

```text
Otimização propõe
Simulação recalcula
Comparação avalia
```

A Comparação fornece diagnósticos, dominâncias, trade-offs, resultados marginais, sensibilidade, robustez e fronteira de Pareto.

Quando a melhoria exige mudança estrutural, a Otimização deve devolver o problema à Arquitetura.

Exemplos:

- ausência de função essencial;
- meio principal inadequado;
- jornada incompleta;
- inexistência de canal para praça prioritária;
- dependência estrutural excessiva;
- combinação de meios incapaz de atingir a meta.

## 39. Limites da Otimização

A Otimização deve:

- propor melhorias;
- respeitar restrições;
- operar sobre variáveis declaradas;
- explicitar ganhos e perdas;
- considerar risco e confiança;
- testar robustez;
- gerar cenários candidatos;
- permitir decisão humana.

Ela não deve:

- alterar objetivos silenciosamente;
- inventar preços ou inventários;
- modificar parâmetros técnicos para favorecer resultados;
- violar restrições obrigatórias;
- tratar solução matemática como decisão final;
- ocultar perdas;
- substituir o julgamento do planejador;
- consolidar automaticamente o plano.

## 40. Formulação canônica

A **Otimização de Cenários** é o processo estruturado que, a partir dos diagnósticos da Comparação, propõe alterações em variáveis controláveis de um cenário, buscando melhorar sua aderência estratégica, eficiência, entrega, performance, robustez ou viabilidade, sem violar restrições e sem ocultar os trade-offs produzidos.

Seu resultado não é um plano definitivo, mas uma sequência controlada:

```text
Proposta de Otimização
        ↓
Cenário Otimizado Candidato
        ↓
Nova Simulação
        ↓
Nova Comparação
```

O Ambiente de Elaboração passa, assim, a constituir um ciclo completo:

```text
Arquitetura
    ↓
Simulação
    ↓
Comparação
    ↓
Otimização
    ↺
```

A etapa seguinte é o **Plano Consolidado de Mídia**, responsável por transformar a alternativa selecionada em estrutura final de execução, documentação, acompanhamento e posterior avaliação.
