# Simulações de Mídia

**Documento:** `05_SIMULACOES.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado conceitualmente  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Simulação de Mídia transforma uma **Arquitetura Candidata de Mídia** em um cenário quantitativo, rastreável, editável, versionado e comparável.

A etapa aplica valores concretos de orçamento, preços, quantidades, inventários, audiência, tempo, públicos, praças, overlap, saturação, performance e atribuição às estruturas definidas na Arquitetura.

Fluxo canônico:

```text
Perfil Estratégico de Mídia
        ↓
Arquitetura Candidata de Mídia
        ↓
Configuração da Simulação
        ↓
Cenário Simulado de Mídia
        ↓
Comparação
        ↓
Otimização
```

A Simulação não substitui a Arquitetura. Ela testa quantitativamente suas hipóteses.

---

## 2. Artefato principal

O artefato da etapa será denominado:

```text
Cenário Simulado de Mídia
```

Cada cenário corresponde a uma combinação específica de:

- arquitetura de origem;
- inventários selecionados;
- distribuição orçamentária;
- preços e condições comerciais;
- volumes adquiridos;
- estratégia temporal;
- fases;
- flight operacional;
- públicos e praças;
- dados de audiência e entrega;
- parâmetros de equivalência;
- overlap;
- saturação;
- performance;
- atribuição;
- premissas e ajustes.

Uma mesma Arquitetura Candidata pode gerar vários cenários.

```text
Arquitetura A
├── Cenário A1 — maior alcance
├── Cenário A2 — maior frequência
├── Cenário A3 — verba reduzida
└── Cenário A4 — flight alternativo
```

---

## 3. Estrutura do Cenário Simulado

```text
Cenário Simulado
├── Identificação e versão
├── Arquitetura de origem
├── Papéis arquitetônicos
├── Papéis sugeridos pela simulação
├── Papéis efetivos
├── Inventários selecionados
├── Dados nativos dos inventários
├── Audiência dos inventários
├── Configuração orçamentária
├── Configuração comercial
├── Remuneração e intermediação
├── Custos não midiáticos associados
├── Estratégia temporal
├── Fases
├── Flight operacional
├── Curva de frequência
├── Curva de pressão
├── Modelo de equivalências
├── Métricas nativas
├── Métricas equivalentes
├── Overlap
├── Saturação
├── Performance
├── Atribuição
├── Resultados financeiros
├── Indicadores de confiança
├── Alertas
└── Histórico de alterações
```

---

## 4. Papéis dos meios durante a Simulação

A classificação entre **Principal, Complementar e Apoio** nasce na Arquitetura, mas deve ser reavaliada pela Simulação à luz das entregas efetivamente calculadas.

O sistema deve distinguir:

```text
papel arquitetônico sugerido
papel definido pelo planejador
papel sugerido pela simulação
papel efetivo adotado
```

A sugestão produzida pela Simulação poderá considerar:

- contribuição para os objetivos prioritários;
- participação no alcance;
- participação na frequência;
- contribuição para a pressão;
- cobertura de públicos e praças;
- contribuição para resultados;
- participação no investimento;
- centralidade na jornada;
- contribuição incremental;
- dependência da arquitetura em relação ao meio;
- capacidade de complementar outros meios.

Exemplo:

```text
Papel arquitetônico:
Canal A = Complementar

Resultado simulado:
- 42% do alcance incremental;
- 38% do investimento;
- maior contribuição para o público prioritário.

Sugestão da simulação:
Reclassificar como Principal.
```

A reclassificação nunca deve ocorrer automaticamente. O sistema deve apresentar:

```text
papel atual
papel sugerido
fundamentos
impactos estimados
aceitar
rejeitar
```

---

## 5. Configuração orçamentária

A configuração orçamentária trata dos limites e reservas de recursos.

Deve conter:

- orçamento total da campanha;
- orçamento disponível para mídia;
- orçamento reservado;
- limite por praça;
- limite por período;
- limite por meio ou canal;
- saldo disponível;
- tolerância de excedente;
- margem de contingência.

O Ambiente de Elaboração deve trabalhar prioritariamente com:

```text
orçamento disponível para mídia
```

O orçamento total da campanha pode incluir itens externos à compra de mídia, mas estes não devem ser confundidos com investimento de mídia.

---

## 6. Configuração comercial de mídia

A configuração comercial trata da compra dos inventários.

Deve conter:

- preço de tabela;
- preço negociado;
- desconto;
- bonificação;
- quantidade;
- unidade de compra;
- investimento bruto de mídia;
- investimento líquido de mídia;
- validade do preço;
- lote mínimo;
- disponibilidade;
- condições comerciais;
- fonte do preço;
- grau de confiança.

Modelos e unidades de compra podem incluir:

- inserção;
- segundo;
- página;
- coluna;
- face;
- diária;
- semana;
- período;
- pacote;
- patrocínio;
- impressão;
- mil impressões;
- clique;
- visualização;
- lead;
- conversão;
- audiência;
- ponto de audiência;
- disparo.

Quando a unidade for indivisível, o sistema deverá aplicar regras de arredondamento, lote mínimo, pacote obrigatório e limite de disponibilidade.

---

## 7. Remuneração e intermediação

A Simulação deve tratar separadamente valores incidentes sobre a compra de mídia:

- comissão da agência;
- fee;
- honorários;
- taxa de plataforma;
- taxa de operação;
- taxa tecnológica;
- outras remunerações aplicáveis.

A regra inicial já consolidada permanece disponível:

```text
Cliente paga: 100%
Veículo recebe: 80%
Agência recebe: 20%
```

Essa regra deve ser parametrizável quando houver outro acordo comercial.

---

## 8. Custos associados, mas não propriamente de mídia

Custos não midiáticos podem ser registrados para composição global, mas não devem ser confundidos com investimento de mídia.

Exemplos:

- produção;
- criação;
- pesquisa;
- monitoramento;
- tecnologia;
- deslocamento;
- instalação;
- impressão;
- materiais de PDV;
- serviços de terceiros.

O sistema deverá distinguir:

```text
investimento de mídia
custos de operação da mídia
custos não midiáticos
custo total da campanha
```

Por padrão, custos não midiáticos não devem integrar métricas como CPM, CPP, CPC ou CPA de mídia, salvo configuração explícita do indicador.

---

## 9. Estratégia temporal, fases e flight operacional

A modelagem temporal deve separar três níveis.

### 9.1 Estratégia temporal

Representa a finalidade estratégica da campanha no tempo.

Exemplos:

- lançamento;
- sustentação;
- manutenção;
- retomada;
- reposicionamento;
- sazonalidade;
- resposta a evento;
- defesa competitiva;
- campanha permanente.

Essas categorias não são tipos de flight.

### 9.2 Fases da campanha

As fases organizam momentos funcionais.

```text
Fase 1 — Lançamento
Fase 2 — Expansão
Fase 3 — Sustentação
Fase 4 — Reforço
```

Cada fase pode possuir:

- objetivo;
- público;
- praça;
- função de mídia;
- pressão pretendida;
- papel dos meios;
- verba;
- indicadores prioritários.

### 9.3 Flight operacional

O flight define a distribuição concreta dos inventários no tempo.

Modelos iniciais:

- contínuo;
- linear;
- concentrado;
- ondas;
- pulsação;
- intermitente;
- crescente;
- decrescente;
- personalizado.

O flight pode ser configurado por:

- dia;
- semana;
- mês;
- faixa horária;
- fase;
- praça;
- público;
- canal;
- inventário.

Relação canônica:

```text
Estratégia temporal
        ↓
Fases da campanha
        ↓
Flight operacional
        ↓
Distribuição efetiva do inventário
```

---

## 10. Frequência e pressão de mídia

A pressão de mídia não é sinônimo de frequência, embora derive dela em articulação com o flight.

Conceitualmente:

```text
Pressão de mídia =
frequência
× concentração temporal
× intensidade das exposições
× distribuição no flight
```

Uma mesma frequência média pode produzir pressões diferentes conforme sua distribuição temporal.

A pressão poderá considerar:

- frequência média;
- frequência por período;
- GRP ou TRP por período;
- quantidade de inserções;
- impressões por janela;
- concentração;
- continuidade;
- intervalo entre exposições;
- intensidade relativa ao público;
- Share of Voice;
- simultaneidade entre canais.

O sistema deve distinguir:

```text
pressão pretendida
pressão configurada
pressão simulada
pressão relativa
pressão acumulada
```

A Simulação deverá produzir uma curva de pressão no tempo. A saturação deverá consumir essa curva, e não apenas um valor agregado de frequência.

---

## 11. Inventários e audiência

Cada inventário pode conter dados próprios de audiência e entrega.

Atributos possíveis:

- audiência absoluta;
- audiência percentual;
- audiência no target;
- alcance estimado;
- cobertura;
- impressões;
- circulação;
- fluxo;
- visualizações;
- usuários únicos;
- afinidade;
- perfil de audiência;
- período de referência;
- metodologia;
- fonte;
- confiança;
- validade.

O sistema deve distinguir:

```text
audiência do veículo
audiência do programa ou faixa
audiência do formato
audiência do inventário
audiência estimada da compra
```

A Simulação deve priorizar o dado mais específico, válido e confiável.

---

## 12. Métricas nativas e modelo de equivalências

Mídias distintas produzem métricas nativas diferentes. A solução não deve tratar arbitrariamente circulação, impressão, impacto, fluxo, visualização ou sessão como unidades idênticas.

Ao mesmo tempo, o Ambiente de Elaboração precisa produzir equivalências capazes de alimentar os motores combinados de alcance, frequência, overlap, saturação, atribuição, custos e resultados.

O sistema deve preservar sempre dois níveis:

```text
métrica nativa
métrica equivalente
```

### 12.1 Unidade intermediária comum

A unidade intermediária inicial será conceitualmente denominada:

```text
Impacto Equivalente de Mídia
```

Cada unidade nativa será convertida mediante coeficientes explícitos.

```text
Unidade nativa
× fator de exposição
× fator de visibilidade
× fator de audiência
× fator de qualificação
× fator de confiança
=
Impacto equivalente
```

O nome definitivo da unidade poderá ser revisto em especificação metodológica própria.

### 12.2 Camadas de equivalência

#### Camada 1 — Unidade comercial nativa

Exemplos:

- inserções;
- exemplares;
- faces;
- impressões;
- visualizações;
- disparos;
- sessões;
- fluxos.

#### Camada 2 — Exposição potencial

Exemplos:

```text
inserção × audiência
impressões entregues
circulação × leitores por exemplar
fluxo × oportunidade de visualização
disparos × taxa de entrega
```

#### Camada 3 — Exposição qualificada

Considera:

- público-alvo;
- praça;
- contexto;
- visibilidade;
- viewability;
- tempo de exposição;
- afinidade;
- atenção estimada.

#### Camada 4 — Alcance e frequência equivalentes

Aplica:

- deduplicação;
- overlap;
- recorrência;
- pessoas únicas;
- universo;
- distribuição temporal.

#### Camada 5 — Resposta e resultado

Aplica:

- propensão à resposta;
- taxas de ação;
- conversão;
- atribuição;
- valor econômico.

Fluxo completo:

```text
Inventário
    ↓
Unidade nativa
    ↓
Exposição potencial
    ↓
Exposição qualificada
    ↓
Impacto equivalente
    ↓
Alcance e frequência
    ↓
Resposta
    ↓
Conversão
    ↓
Resultado econômico
```

### 12.3 Modelos iniciais por meio

#### Televisão e rádio

```text
inserções × audiência da faixa = impactos brutos
```

#### Digital

```text
impressões × viewability × qualificação do target = exposições qualificadas
```

#### Impresso

```text
circulação × leitores por exemplar × exposição provável × afinidade = exposições qualificadas
```

#### OOH

```text
fluxo × oportunidade de visualização × visibilidade × frequência de passagem = exposições qualificadas
```

#### E-mail

```text
disparos × taxa de entrega × taxa de abertura ou visualização = exposições qualificadas
```

#### Cinema

```text
sessões × ocupação × audiência do filme = impactos potenciais
```

Os coeficientes devem ser transparentes, editáveis, versionados, vinculados a fontes e acompanhados de confiança.

### 12.4 Equivalência não significa identidade

O sistema nunca deve apagar a métrica original.

Exemplo:

```text
OOH:
1.200.000 oportunidades de visualização

Equivalência:
620.000 exposições qualificadas estimadas
```

---

## 13. Alcance, frequência e impactos

Quando houver dados suficientes, a Simulação poderá calcular:

- impactos brutos;
- impactos equivalentes;
- alcance líquido;
- alcance equivalente;
- alcance incremental;
- frequência média;
- frequência equivalente;
- cobertura;
- duplicação;
- GRP;
- TRP.

Estruturas básicas:

```text
Impactos = audiência absoluta × número de inserções
```

```text
Frequência equivalente = impactos equivalentes ÷ alcance equivalente
```

Quando os dados forem incompletos, o sistema deverá informar que o resultado é estimado e registrar seu grau de confiança.

Quando os dados forem insuficientes, deverá retornar indicador indisponível, sem produzir falsa precisão.

---

## 14. GRP e TRP

### 14.1 GRP

```text
GRP = soma dos pontos de audiência das inserções
```

ou:

```text
GRP = alcance percentual × frequência média
```

### 14.2 TRP

```text
TRP = soma dos pontos de audiência no público-alvo
```

ou:

```text
TRP = alcance percentual no target × frequência média no target
```

O sistema deve registrar:

- universo de referência;
- praça;
- público;
- período;
- fonte da audiência;
- método de cálculo;
- grau de confiança.

---

## 15. Métricas de custo e eficiência

### 15.1 CPM

```text
CPM = investimento ÷ impressões × 1.000
```

Variantes possíveis:

- CPM bruto;
- CPM líquido;
- CPM total;
- CPM por público;
- CPM por praça;
- CPM incremental;
- CPM equivalente.

### 15.2 CPP

```text
CPP = investimento ÷ pontos de audiência
```

Variantes possíveis:

- CPP geral;
- CPP no público-alvo;
- CPP bruto;
- CPP líquido;
- CPP por praça;
- CPP por período.

### 15.3 CTR

```text
CTR = cliques ÷ impressões × 100
```

### 15.4 CPC

```text
CPC = investimento ÷ cliques
```

O catálogo deve distinguir:

```text
CPC como preço de compra
CPC como indicador calculado
```

### 15.5 CPA

```text
CPA = investimento ÷ conversões
```

Assim como o CPC, o CPA pode ser modelo comercial, parâmetro, KPI calculado ou resultado observado.

---

## 16. Performance

A Simulação poderá estimar a cadeia:

```text
Impressões
    ↓ CTR
Cliques
    ↓ taxa de conversão
Conversões
    ↓ valor médio
Receita estimada
    ↓
ROAS
```

Fórmulas iniciais:

```text
Cliques estimados = impressões × CTR
```

```text
Conversões estimadas = cliques × taxa de conversão
```

```text
Receita estimada = conversões × valor médio
```

Cada elo deverá registrar:

- valor de entrada;
- fórmula;
- benchmark;
- fonte;
- confiança;
- possibilidade de ajuste.

Uma conversão deve possuir definição operacional explícita, como compra, cadastro, lead, visita, instalação, agendamento, download ou outro evento validado.

---

## 17. ROAS

A fórmula canônica já definida no projeto permanece:

```text
ROAS = (Receita − Investimento) ÷ Investimento × 100
```

O MediAd Planner deverá:

- manter essa fórmula de forma explícita;
- indicar qual investimento está sendo considerado;
- evitar confusão com ROI ou ROMI;
- não misturar essa definição com a fórmula de receita bruta dividida pelo investimento.

---

## 18. Overlap

O overlap será aplicado quantitativamente na Simulação.

Para cada combinação, o sistema deverá admitir:

```text
Canal A
Canal B
Público
Praça
Período
Overlap calculado
Overlap ajustado
Overlap efetivo
Confiança
Fonte
```

O overlap poderá variar por público, praça, período, plataforma, nível de exposição e combinação de inventários.

O motor de equivalências deverá fornecer a base comum necessária para deduplicar públicos de meios originalmente medidos por unidades diferentes.

---

## 19. Saturação

A saturação representa retornos decrescentes conforme aumentam frequência e pressão.

```text
Mais investimento
        ↓
Mais exposições
        ↓
Maior frequência e pressão
        ↓
Ganho progressivamente menor
        ↓
Saturação
```

A função deve ser configurável por canal e poderá atuar sobre:

- alcance;
- frequência;
- cliques;
- conversões;
- impacto;
- resposta;
- eficiência.

Cada cenário deverá armazenar:

```text
modelo de saturação
coeficientes
limiar
penalização
origem
valor calculado
valor ajustado
valor efetivo
```

A saturação deverá considerar a curva temporal de pressão.

---

## 20. Modelos de atribuição

A Simulação deverá admitir, inicialmente:

- primeiro contato;
- último contato;
- linear;
- baseado em posição;
- decaimento temporal;
- assistido;
- personalizado;
- não aplicável.

A configuração deverá conter:

```text
modelo
janela de atribuição
eventos considerados
canais rastreáveis
canais não rastreáveis
premissas
limitações
```

O motor de equivalências deverá contribuir para a atribuição entre pontos de contato rastreáveis e não rastreáveis, sem apagar as diferenças metodológicas entre eles.

---

## 21. Resultados por nível

Os resultados devem poder ser calculados por:

- campanha;
- arquitetura;
- cenário;
- meio;
- canal;
- veículo;
- formato;
- inventário;
- praça;
- público;
- segmento;
- etapa da jornada;
- período;
- fase;
- papel estratégico.

---

## 22. Resultados gerais do cenário

### 22.1 Orçamentários e comerciais

- orçamento disponível para mídia;
- investimento bruto de mídia;
- investimento líquido de mídia;
- comissão;
- taxas de operação;
- saldo;
- excesso de orçamento;
- custos não midiáticos associados;
- custo total da campanha.

### 22.2 Audiência e exposição

- audiência;
- impactos brutos;
- impactos equivalentes;
- alcance;
- alcance equivalente;
- alcance incremental;
- cobertura;
- frequência;
- GRP;
- TRP;
- impressões.

### 22.3 Eficiência

- CPM;
- CPM equivalente;
- CPP;
- CPC;
- CPA;
- custo por alcance;
- custo por alcance incremental;
- custo por impacto equivalente.

### 22.4 Performance

- CTR;
- cliques;
- conversões;
- taxa de conversão;
- receita;
- ROAS.

### 22.5 Distribuição

- investimento por meio;
- investimento por praça;
- investimento por público;
- investimento por período;
- investimento por fase;
- participação por papel estratégico;
- curva de frequência;
- curva de pressão.

### 22.6 Qualidade

- aderência ao Perfil Estratégico;
- atendimento de restrições;
- risco de saturação;
- confiança;
- equilíbrio da arquitetura;
- contribuição incremental;
- pontos de tensão;
- coerência dos papéis.

---

## 23. Alertas

O motor deverá detectar, entre outras situações:

- orçamento excedido;
- saldo elevado não utilizado;
- inventário indisponível;
- volume inferior ao mínimo;
- frequência insuficiente;
- frequência excessiva;
- pressão desproporcional;
- saturação;
- praça sem cobertura;
- público prioritário subatendido;
- excesso de concentração;
- ausência de meio principal;
- incoerência entre papel e contribuição;
- dependência excessiva de um canal;
- KPI sem dados de entrada;
- fórmula inviável;
- baixa confiança;
- conflito entre metas.

Cada alerta deverá conter:

```text
tipo
gravidade
origem
dimensões afetadas
impacto
recomendação
```

O alerta não deverá alterar o cenário automaticamente.

---

## 24. Confiança e incerteza

Cada estimativa relevante deverá registrar:

```text
valor estimado
faixa provável
confiança
fonte
modelo
premissas
sensibilidade
```

Exemplo:

```text
Alcance equivalente estimado:
120.000 pessoas

Faixa provável:
100.000 a 145.000

Confiança:
Média
```

A confiança deverá considerar especialmente:

- qualidade dos dados de audiência;
- atualidade dos preços;
- robustez dos coeficientes de equivalência;
- confiabilidade das taxas de performance;
- precisão do overlap;
- qualidade do modelo de saturação;
- disponibilidade de dados de atribuição.

---

## 25. Ajustes e recalculabilidade

Cada parâmetro deverá preservar:

```text
valor original
valor calculado
valor ajustado
valor efetivo
responsável
justificativa
data e hora
```

Qualquer alteração relevante deverá provocar:

- recálculo seletivo;
- nova versão ou revisão registrada;
- comparação com a versão anterior;
- possibilidade de restauração.

---

## 26. Versionamento e estados

Exemplo de versionamento:

```text
Cenário A1 — versão 1
Cenário A1 — versão 2
Cenário A1 — versão 3
```

Estados canônicos:

```text
rascunho
configurado
calculado
com alertas
apto para comparação
comparado
em otimização
otimizado
selecionado
descartado
arquivado
```

Um cenário somente estará apto para comparação quando:

- os cálculos essenciais forem válidos;
- as premissas estiverem identificadas;
- os dados ausentes estiverem sinalizados;
- os alertas críticos estiverem resolvidos ou aceitos;
- a versão estiver congelada para aquela comparação.

---

## 27. Limites da etapa

A Simulação deve:

- quantificar arquiteturas;
- sugerir e reavaliar papéis;
- calcular indicadores;
- aplicar hipóteses;
- produzir cenários;
- construir curvas de frequência e pressão;
- converter métricas por equivalências;
- detectar alertas;
- registrar incertezas;
- permitir ajustes;
- preservar rastreabilidade.

A Simulação não deve:

- escolher definitivamente o melhor cenário;
- substituir o julgamento do planejador;
- consolidar automaticamente o plano;
- ocultar premissas;
- apagar métricas nativas;
- transformar estimativas em promessas;
- comparar cenários sem critérios estratégicos.

---

## 28. Contrato de entrada

A Simulação deverá receber, no mínimo:

- Arquitetura Candidata identificada e versionada;
- Perfil Estratégico de referência;
- meios, canais e inventários elegíveis;
- papéis arquitetônicos;
- públicos;
- praças;
- jornada e pontos de contato;
- orçamento disponível para mídia;
- preços e unidades de compra;
- dados de audiência e entrega;
- estratégia temporal;
- parâmetros de equivalência;
- parâmetros de overlap;
- parâmetros de saturação;
- taxas de performance;
- modelo de atribuição;
- restrições;
- confiança e fontes.

---

## 29. Contrato de saída para a Comparação

A Simulação deverá entregar:

```text
Cenário identificado e versionado
Arquitetura de origem
Configuração completa
Papéis arquitetônicos
Papéis sugeridos pela simulação
Papéis efetivos
Métricas nativas
Métricas equivalentes
Resultados calculados
Resultados normalizados
Curvas de frequência e pressão
Parâmetros estratégicos de referência
Alertas
Restrições atendidas e violadas
Confiança
Premissas
Rastreabilidade
```

A Comparação deverá utilizar esses dados para avaliar não apenas qual cenário produz valores maiores, mas qual atende melhor ao Perfil Estratégico de Mídia.

---

## 30. Formulação canônica

> A Simulação de Mídia é o processo estruturado que aplica valores orçamentários, comerciais, temporais, territoriais, de audiência, equivalência e performance a uma Arquitetura Candidata, produzindo um Cenário Simulado quantitativo, rastreável, editável, versionado e comparável.

A etapa deverá funcionar de forma integrada com Arquitetura, Comparação e Otimização, permitindo ciclos sucessivos de formulação, teste, diagnóstico e aperfeiçoamento.