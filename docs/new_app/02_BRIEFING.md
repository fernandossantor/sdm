# Briefing de Mídia

**Documento:** `02_BRIEFING.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

Este documento estabelece a definição canônica do **Briefing de Mídia** no MediAd Planner.

O Briefing de Mídia recebe o contexto administrativo criado na Campanha e o transforma em um **Objeto Contextual Estruturado**, sem produzir interpretação estratégica, objetivo de mídia, arquitetura de mídia ou plano.

Seu papel é registrar e estruturar:

- a situação do anunciante, da marca, do produto ou serviço;
- a situação do mercado, da categoria e da concorrência;
- os objetivos declarados de marketing e de comunicação;
- a estrutura territorial e populacional da campanha;
- os segmentos e públicos declarados;
- a jornada associada aos públicos;
- o período pretendido;
- a verba disponível;
- as prioridades;
- as restrições;
- as pretensões declaradas pelo anunciante.

O Briefing não confirma a viabilidade das pretensões, não formula o problema estratégico e não define a solução de mídia.

---

## 2. Posição no fluxo metodológico

```text
Campanha
    ↓
Objeto Administrativo
    ↓
Briefing de Mídia
    ↓
Objeto Contextual Estruturado
    ↓
Tradução Estratégica
    ↓
Objeto Interpretativo
    ↓
Arquitetura de Mídia
    ↓
Simulação
    ↓
Plano Consolidado
```

A Campanha cria a unidade de trabalho e identifica:

- Anunciante;
- Marca, quando houver;
- Produto ou Serviço, quando houver;
- Planejador Responsável;
- Equipe da Campanha, quando houver;
- Código da Campanha;
- metadados iniciais.

Esses dados são herdados pelo Briefing e não devem ser solicitados novamente como conteúdo metodológico.

---

## 3. Natureza epistemológica

O Briefing é um objeto predominantemente declaratório e descritivo.

Ele registra:

- fatos informados;
- indicadores disponíveis;
- condições existentes;
- escolhas declaradas;
- prioridades declaradas;
- restrições declaradas;
- pretensões do anunciante.

O Briefing não deve:

- diagnosticar causas;
- formular o problema estratégico;
- corrigir automaticamente as declarações do anunciante;
- definir objetivo de mídia;
- selecionar KPIs;
- definir alcance;
- definir frequência;
- definir flight;
- selecionar pontos de contato;
- selecionar meios;
- selecionar canais;
- selecionar veículos;
- selecionar inventários;
- atribuir papéis estratégicos;
- propor distribuição de verba;
- produzir cenários;
- calcular resultados.

Quando houver inconsistências, insuficiências ou tensões, o sistema deve identificá-las e apresentá-las como análise, sem alterar silenciosamente o conteúdo declarado.

---

## 4. Princípios de modelagem dos campos

O Briefing não deve ser tratado como um formulário longo de texto livre.

Campos decisórios e classificatórios devem ser preferencialmente parametrizados.

A ordem preferencial de modelagem é:

1. seleção única;
2. seleção múltipla;
3. intensidade;
4. prioridade;
5. ordenação;
6. valor quantitativo;
7. texto complementar.

Texto livre deve ser usado apenas quando:

- não houver taxonomia adequada;
- for necessário justificar uma escolha;
- for necessário registrar uma observação específica;
- for necessário contextualizar um indicador;
- for necessário informar uma condição não prevista.

Toda lista parametrizada deve permitir criação controlada de nova opção, preservando governança terminológica.

Cada campo deve possuir, quando aplicável:

- conceito;
- finalidade;
- tipo de entrada;
- cardinalidade;
- opções;
- relação com outros campos;
- regra de coerência;
- necessidade de fonte;
- possibilidade de complementação textual.

---

## 5. Estrutura consolidada do Briefing

O Briefing de Mídia é composto pelos seguintes domínios:

1. Contexto herdado da Campanha;
2. Situação mercadológica e competitiva;
3. Objetivos declarados;
4. Estrutura territorial e populacional;
5. Jornada;
6. Período pretendido;
7. Verba;
8. Prioridades;
9. Restrições;
10. Pretensões declaradas.

A avaliação de coerência e suficiência não constitui um domínio de preenchimento. Ela é produzida pelo aplicativo sobre o conjunto estruturado.

---

## 6. Contexto herdado da Campanha

O Briefing deve exibir como referência:

- Código da Campanha;
- Nome da Campanha;
- Anunciante;
- Marca, quando houver;
- Produto ou Serviço, quando houver;
- Planejador Responsável;
- Equipe da Campanha, quando houver.

Esses elementos:

- não são redefinidos no Briefing;
- não constituem campos metodológicos do Briefing;
- permanecem vinculados à Campanha;
- devem manter snapshot histórico.

---

## 7. Situação mercadológica e competitiva

### 7.1 Finalidade

Registrar a posição do anunciante em relação ao mercado, à categoria e à concorrência.

A análise histórica relevante deve estar incorporada aos indicadores desses elementos, e não em um bloco autônomo de histórico de campanhas.

A relação central é:

```text
Situação do Anunciante
        ×
Situação do Mercado
        ×
Situação da Categoria
        ×
Situação da Concorrência
```

### 7.2 Situação do anunciante, marca, produto ou serviço

Campos estruturados podem contemplar, conforme disponibilidade:

- posição no mercado;
- participação de mercado;
- penetração;
- notoriedade;
- lembrança;
- imagem;
- preferência;
- fidelização;
- desempenho comercial;
- distribuição;
- presença geográfica;
- ciclo de vida;
- tendência de desempenho.

Tipos de entrada possíveis:

- seleção única;
- seleção múltipla;
- intensidade;
- valor quantitativo;
- série temporal;
- texto complementar.

### 7.3 Situação do mercado e da categoria

Campos estruturados podem contemplar:

- dimensão do mercado;
- crescimento;
- estabilidade;
- retração;
- sazonalidade;
- concentração;
- maturidade;
- tendência da categoria;
- nível de competição;
- mudanças relevantes;
- índices disponíveis.

### 7.4 Situação competitiva

Campos estruturados podem contemplar:

- concorrentes relevantes;
- posição relativa;
- participação dos concorrentes;
- intensidade competitiva;
- presença territorial;
- presença de comunicação;
- investimento de mídia, quando disponível;
- Share of Voice, quando disponível;
- vantagens percebidas;
- desvantagens percebidas;
- tendências competitivas.

### 7.5 Relações e coerência

O sistema deve permitir comparar:

- anunciante versus mercado;
- anunciante versus categoria;
- anunciante versus concorrentes;
- evolução do anunciante;
- evolução do mercado;
- evolução dos concorrentes.

O aplicativo deve sinalizar:

- ausência de fonte;
- ausência de período de referência;
- indicadores incomparáveis;
- unidades distintas;
- séries temporais incompatíveis;
- concorrente sem indicador correspondente;
- afirmação qualitativa sem evidência, quando a evidência for necessária.

---

## 8. Objetivos declarados

### 8.1 Princípio

O Briefing registra apenas:

- objetivo de marketing declarado;
- objetivo de comunicação declarado.

O objetivo de mídia não pertence ao Briefing. Ele será produzido na Tradução Estratégica.

A relação canônica é:

```text
Objetivo de Marketing declarado
              ↓
Objetivo de Comunicação declarado
              ↓
Tradução Estratégica
              ↓
Objetivo de Mídia
```

### 8.2 Objetivo de Marketing

O campo deve ser parametrizado e admitir seleção múltipla com prioridade.

Categorias canônicas iniciais:

- Branding;
- Posicionamento;
- Segmentação;
- Diferenciação;
- Crescimento;
- Participação de mercado;
- Fidelização;
- Penetração;
- Desenvolvimento de produto;
- Diversificação.

Quando aplicável, o objetivo pode ser relacionado às dimensões do composto de marketing:

- Produto;
- Preço;
- Praça;
- Promoção.

Para cada objetivo selecionado, o usuário pode informar:

- prioridade;
- intensidade;
- público relacionado;
- praça relacionada;
- justificativa complementar.

### 8.3 Objetivo de Comunicação

O campo deve ser parametrizado e admitir seleção múltipla com prioridade.

Categorias canônicas iniciais:

- notoriedade;
- conhecimento;
- lembrança;
- compreensão;
- imagem;
- posicionamento percebido;
- diferenciação percebida;
- persuasão;
- preferência;
- consideração;
- engajamento;
- experimentação;
- ação;
- relacionamento;
- fidelização;
- recomendação;
- defesa da marca.

Para cada objetivo selecionado, o usuário pode informar:

- prioridade;
- intensidade;
- público relacionado;
- praça relacionada;
- etapa da jornada relacionada;
- justificativa complementar.

### 8.4 Relação entre Marketing e Comunicação

Objetivos de Marketing e Comunicação não podem ser tratados como escolhas independentes e fortuitas.

O aplicativo deve avaliar:

- compatibilidade;
- complementaridade;
- insuficiência;
- possível contradição;
- ausência de relação explícita;
- excesso de objetivos simultâneos;
- conflito de prioridades.

A avaliação não altera automaticamente as escolhas do usuário.

---

## 9. Estrutura territorial e populacional

### 9.1 Relação canônica

```text
Praça
   ↓
Universo
   ↓
Critérios de Segmentação
   ↓
Segmentos
   ↓
Públicos
```

Esses elementos não podem ser tratados como listas independentes.

### 9.2 Praça

A Praça delimita territorialmente o planejamento.

Tipo de entrada:

- seleção múltipla em biblioteca;
- criação controlada de nova praça;
- agrupamento de praças.

Cada praça pode possuir:

- tipo territorial;
- abrangência;
- código oficial, quando houver;
- população de referência;
- fonte;
- data de referência;
- observação complementar.

Praça não é sinônimo de cobertura.

### 9.3 Universo

O Universo representa a população de referência existente na praça.

Cada universo deve estar vinculado a uma ou mais praças.

Campos possíveis:

- nome;
- definição;
- valor populacional;
- unidade;
- fonte;
- data de referência;
- critérios de inclusão;
- critérios de exclusão.

O universo não é público-alvo e não é audiência.

### 9.4 Critérios de Segmentação

Seleção múltipla estruturada.

Categorias canônicas iniciais:

- geográfica;
- demográfica;
- socioeconômica;
- psicográfica;
- comportamental;
- consumo;
- relacionamento com a categoria;
- relacionamento com a marca;
- jornada;
- intenção;
- contexto.

### 9.5 Segmentos

Segmento é um subconjunto do universo construído a partir de critérios de segmentação.

Cada segmento deve preservar:

- universo de origem;
- praça ou praças;
- critérios aplicados;
- definição;
- tamanho estimado, quando disponível;
- fonte;
- data de referência.

### 9.6 Públicos

Público é o segmento ou conjunto de segmentos selecionado para a campanha.

Cada público pode receber:

- nome;
- segmento ou segmentos de origem;
- praça ou praças;
- prioridade;
- intensidade de importância;
- tamanho estimado;
- papel declarado na campanha;
- justificativa complementar.

Distinção obrigatória:

- Universo: população de referência;
- Segmento: subconjunto identificável do universo;
- Público: segmento ou combinação de segmentos selecionados para a campanha.

### 9.7 Regras de coerência

O sistema deve sinalizar:

- praça sem universo;
- universo sem fonte;
- segmento sem universo de origem;
- segmento sem critério de segmentação;
- público sem segmento de origem;
- público associado a praça incompatível;
- tamanho de segmento superior ao universo;
- soma de segmentos interpretada incorretamente quando houver sobreposição;
- público duplicado;
- público sem prioridade quando houver múltiplos públicos.

---

## 10. Jornada

### 10.1 Finalidade

Registrar o percurso do público em relação à categoria, à marca, ao produto, ao serviço ou à decisão.

A jornada pertence ao Briefing porque descreve o contexto comportamental do público.

Pontos de contato não pertencem ao Briefing.

A relação canônica é:

```text
Público
   ↓
Jornada
   ↓
Etapas
```

Posteriormente:

```text
Jornada
   ↓
Tradução Estratégica e Arquitetura
   ↓
Pontos de Contato
   ↓
Meios, Canais e Inventários
```

### 10.2 Modelo de jornada

O sistema deve permitir:

- seleção de jornada em biblioteca;
- criação controlada de nova jornada;
- adaptação local por campanha;
- jornadas distintas para públicos distintos.

Não deve haver um único modelo universal obrigatório.

### 10.3 Etapas da jornada

Categorias iniciais possíveis:

- descoberta;
- conhecimento;
- consideração;
- avaliação;
- decisão;
- compra;
- experiência;
- recompra;
- fidelização;
- recomendação.

Para cada etapa, o usuário pode informar:

- existência;
- relevância;
- intensidade;
- prioridade;
- público associado;
- situação atual;
- situação pretendida;
- observação complementar.

### 10.4 Regras de coerência

O aplicativo deve sinalizar:

- jornada sem público associado;
- público sem jornada, quando a jornada for necessária;
- etapa sem relação com objetivo de comunicação;
- múltiplas etapas prioritárias sem ordenação;
- jornada incompatível com a natureza declarada do produto ou serviço;
- uso de modelo genérico sem adaptação quando houver diferenças relevantes entre públicos.

---

## 11. Período pretendido

### 11.1 Princípio

Em mídia, o Briefing registra o período pretendido de veiculação.

Não existe, neste documento, distinção autônoma entre período e temporalidade.

O Briefing não define flight.

### 11.2 Campos

- data inicial pretendida;
- data final pretendida;
- duração;
- datas críticas;
- sazonalidades;
- eventos condicionantes;
- períodos obrigatórios;
- períodos vedados;
- observação complementar.

### 11.3 Regras de coerência

O aplicativo deve sinalizar:

- data final anterior à inicial;
- período incompatível com evento declarado;
- período obrigatório fora do intervalo principal;
- sazonalidade informada sem correspondência temporal;
- duração ausente quando as datas não estiverem definidas;
- período incompatível com restrição declarada.

Flight, continuidade, pulsação, ondas e concentração pertencem às etapas posteriores.

---

## 12. Verba

### 12.1 Finalidade

Registrar os recursos financeiros declarados como disponíveis para mídia.

### 12.2 Campos

- valor total disponível;
- moeda;
- natureza do limite;
- margem de flexibilidade;
- valor mínimo, quando declarado;
- valor máximo, quando declarado;
- parcela já comprometida, quando aplicável;
- observação complementar.

### 12.3 Natureza do limite

Seleção única:

- rígido;
- flexível;
- estimado;
- ainda não definido.

### 12.4 Regras de coerência

O aplicativo deve sinalizar:

- verba ausente;
- valor máximo inferior ao mínimo;
- parcela comprometida superior ao total;
- limite declarado como rígido com margem de flexibilidade incompatível;
- moeda ausente;
- verba não definida diante de pretensões quantitativamente exigentes.

A distribuição da verba não pertence ao Briefing.

---

## 13. Prioridades

### 13.1 Princípio

Prioridade não deve ser tratada como um texto genérico isolado.

Ela deve ser aplicada às entidades relevantes do Briefing:

- objetivos de marketing;
- objetivos de comunicação;
- praças;
- segmentos;
- públicos;
- etapas da jornada;
- períodos;
- pretensões;
- restrições, quando aplicável.

### 13.2 Escala canônica

- muito baixa;
- baixa;
- média;
- alta;
- muito alta.

Quando necessário, o sistema também deve permitir ordenação explícita.

### 13.3 Regras de coerência

O aplicativo deve sinalizar:

- todos os itens marcados com a mesma prioridade;
- múltiplas prioridades máximas sem justificativa;
- conflito entre prioridade e intensidade;
- público prioritário sem objetivo relacionado;
- objetivo prioritário sem público ou praça relacionado;
- pretensão prioritária incompatível com restrição rígida.

---

## 14. Restrições

### 14.1 Finalidade

Registrar condições declaradas que limitam o planejamento.

O Briefing registra a restrição. A Tradução Estratégica avaliará sua natureza técnica, compatibilidade e possíveis compensações.

### 14.2 Categorias iniciais

- geográfica;
- populacional;
- público;
- segmento;
- período;
- orçamentária;
- legal;
- ética;
- institucional;
- mercadológica;
- competitiva;
- operacional;
- disponibilidade;
- mensuração;
- outra restrição controlada.

Não devem ser introduzidas aqui restrições já formuladas como escolha técnica de meio, canal, veículo ou inventário, salvo quando forem imposições externas declaradas.

### 14.3 Campos por restrição

- categoria;
- descrição estruturada;
- entidade afetada;
- intensidade;
- prioridade;
- origem;
- justificativa;
- documento ou fonte, quando houver;
- observação complementar.

### 14.4 Regras de coerência

O aplicativo deve sinalizar:

- restrição sem entidade afetada;
- restrição legal sem fundamento informado;
- restrição incompatível com período;
- restrição incompatível com praça;
- restrição incompatível com público;
- restrição contraditória com objetivo declarado;
- restrição sem justificativa quando de alta intensidade.

A classificação técnica entre restrição rígida e flexível pertence à Tradução Estratégica.

---

## 15. Pretensões declaradas

### 15.1 Finalidade

Registrar o que o anunciante espera da campanha sem converter essa expectativa em objetivo técnico de mídia, KPI ou parâmetro de cálculo.

As pretensões substituem a entrada indevida, no Briefing, de:

- objetivo de mídia;
- KPI;
- alcance;
- frequência;
- flight;
- pressão;
- distribuição de mídia.

### 15.2 Categorias iniciais

- ampliar presença;
- alcançar novos públicos;
- reforçar presença entre públicos atuais;
- aumentar conhecimento;
- melhorar lembrança;
- apoiar lançamento;
- apoiar vendas;
- estimular experimentação;
- gerar tráfego;
- ampliar presença territorial;
- concentrar esforços em públicos prioritários;
- acompanhar etapas específicas da jornada;
- responder à pressão competitiva;
- recuperar presença;
- manter liderança;
- sustentar presença;
- gerar rápida visibilidade;
- outra pretensão controlada.

### 15.3 Campos por pretensão

- categoria;
- prioridade;
- intensidade;
- público associado;
- praça associada;
- etapa da jornada associada;
- período associado;
- flexibilidade declarada;
- justificativa complementar.

### 15.4 Relação com etapas posteriores

```text
Pretensões declaradas
        ↓
Tradução Estratégica
        ↓
Objetivo de Mídia
        ↓
KPIs e prioridades técnicas
        ↓
Arquitetura de Mídia
        ↓
Simulação
        ↓
Alcance, Frequência, Flight e Resultados
```

---

## 16. Avaliação produzida pelo aplicativo

A avaliação do Briefing não constitui um bloco de preenchimento.

O aplicativo deve produzir e disponibilizar, separadamente:

- completude;
- suficiência;
- coerência entre objetivos de marketing e comunicação;
- coerência entre praça, universo, segmentos e públicos;
- coerência entre públicos e jornadas;
- coerência entre objetivos, pretensões, prioridades, período, verba e restrições;
- lacunas;
- conflitos;
- incompatibilidades;
- dados sem fonte;
- dados sem período de referência;
- escolhas que exigem justificativa;
- riscos de interpretação;
- dependências para a Tradução Estratégica.

Essa avaliação deve explicar os motivos de cada alerta.

O sistema não deve:

- alterar escolhas sem consentimento;
- substituir objetivos declarados;
- formular automaticamente o objetivo de mídia dentro do Briefing;
- tratar ausência de informação como valor neutro;
- ocultar inconsistências.

---

## 17. Interface

O Briefing não deve ser exibido em uma única tela extensa.

A interface deve ser progressiva e organizada em subetapas:

```text
1. Situação mercadológica e competitiva
2. Objetivos declarados
3. Praça e universo
4. Segmentos e públicos
5. Jornada
6. Período e verba
7. Prioridades, restrições e pretensões
8. Revisão do Briefing
```

A interface deve oferecer:

- resumo permanente;
- salvamento progressivo;
- possibilidade de retorno;
- indicação de pendências;
- explicação conceitual dos campos;
- visualização das relações entre entidades;
- criação controlada de novas opções;
- histórico de versões;
- comparação entre versões;
- validações sem bloqueio indevido;
- distinção visual entre declaração do usuário e análise do sistema.

---

## 18. Versionamento

O Briefing pertence à Campanha e deve possuir versionamento próprio.

Exemplos:

```text
Briefing v1
Briefing v2
Briefing v3
```

Uma nova versão deve ser criada quando houver alteração relevante em:

- situação mercadológica;
- objetivos;
- praça;
- universo;
- segmentos;
- públicos;
- jornada;
- período;
- verba;
- prioridades;
- restrições;
- pretensões.

Cada versão deve preservar:

- autor;
- data e hora;
- motivo da alteração;
- campos alterados;
- valores anteriores;
- valores novos;
- análise de impacto;
- estado da versão.

O Código da Campanha não é alterado.

---

## 19. Estados do Briefing

Valores canônicos:

- Rascunho;
- Em preenchimento;
- Em revisão;
- Concluído;
- Substituído.

### Rascunho

Briefing criado, ainda sem conteúdo suficiente.

### Em preenchimento

Briefing em construção, com campos e relações ainda incompletos.

### Em revisão

Conteúdo preenchido e submetido à revisão de coerência e suficiência.

### Concluído

Objeto Contextual Estruturado apto a seguir para a Tradução Estratégica, ainda que contenha alertas explicitamente aceitos.

### Substituído

Versão anterior preservada após a conclusão de nova versão.

---

## 20. Critérios de conclusão

O Briefing pode ser concluído quando possuir, no mínimo:

- contexto herdado válido;
- situação mercadológica e competitiva registrada;
- ao menos um objetivo de marketing;
- ao menos um objetivo de comunicação;
- relação explícita entre objetivos;
- ao menos uma praça;
- universo correspondente;
- ao menos um público;
- vínculo entre público, segmento e universo;
- jornada vinculada aos públicos, quando aplicável;
- período pretendido;
- verba ou indicação explícita de verba ainda não definida;
- prioridades mínimas;
- restrições registradas ou declaração de inexistência;
- pretensões declaradas;
- fontes registradas quando houver indicadores quantitativos;
- pendências e alertas apresentados ao usuário.

A existência de alerta não impede automaticamente a conclusão.

O sistema deve exigir reconhecimento explícito quando o usuário decidir prosseguir com lacunas ou incompatibilidades relevantes.

---

## 21. Contrato de entrada

### 21.1 Pré-condições

- Campanha criada;
- Anunciante vinculado;
- Planejador Responsável válido;
- usuário autorizado;
- Etapa Atual igual a `Briefing`.

### 21.2 Entradas herdadas

- Código da Campanha;
- Nome da Campanha;
- Anunciante;
- Marca, quando houver;
- Produto ou Serviço, quando houver;
- Planejador Responsável;
- Equipe da Campanha, quando houver.

### 21.3 Entradas metodológicas

- situação mercadológica e competitiva;
- objetivos de marketing;
- objetivos de comunicação;
- praças;
- universos;
- critérios de segmentação;
- segmentos;
- públicos;
- jornadas;
- período pretendido;
- verba;
- prioridades;
- restrições;
- pretensões.

---

## 22. Contrato de saída

O Briefing concluído produz um **Objeto Contextual Estruturado** contendo:

- vínculos herdados da Campanha;
- snapshot das entidades reutilizadas;
- situação mercadológica e competitiva;
- objetivos declarados de marketing;
- objetivos declarados de comunicação;
- relações entre objetivos;
- praças;
- universos;
- critérios de segmentação;
- segmentos;
- públicos;
- jornadas;
- período pretendido;
- verba;
- prioridades;
- restrições;
- pretensões;
- fontes;
- pendências;
- alertas;
- versão;
- metadados.

O contrato de saída não inclui:

- problema estratégico;
- objetivo de mídia;
- KPIs;
- pontos de contato;
- alcance;
- frequência;
- flight;
- arquitetura de mídia;
- meios;
- canais;
- veículos;
- inventários;
- papéis estratégicos;
- distribuição de verba;
- resultados calculados.

Esses elementos pertencem às etapas posteriores.

---

## 23. Transição para a Tradução Estratégica

Quando o Briefing for concluído:

```text
Situação da Campanha: Em andamento
Etapa Atual: Tradução Estratégica
```

A Tradução Estratégica recebe o Objeto Contextual Estruturado e deverá:

- interpretar a situação;
- formular o problema estratégico;
- relacionar objetivos e pretensões;
- produzir objetivo de mídia;
- definir prioridades técnicas;
- selecionar KPIs;
- identificar tensões;
- classificar restrições;
- produzir pesos e compatibilidades;
- preparar a Arquitetura de Mídia.

---

## 24. Regras canônicas de separação entre etapas

### Pertence ao Briefing

- situação mercadológica e competitiva;
- objetivos de marketing;
- objetivos de comunicação;
- praça;
- universo;
- segmentação;
- segmentos;
- públicos;
- jornada;
- período;
- verba;
- prioridades;
- restrições;
- pretensões.

### Pertence à Tradução Estratégica

- problema estratégico;
- objetivo de mídia;
- KPIs;
- pesos;
- compatibilidades;
- tensões;
- prioridades técnicas;
- classificação de restrições;
- compensações.

### Pertence à Arquitetura de Mídia

- pontos de contato;
- meios;
- canais;
- veículos;
- inventários;
- papéis estratégicos;
- adequações.

### Pertence à Simulação

- alcance;
- frequência;
- cobertura;
- impactos;
- pressão;
- flight;
- custos;
- distribuição de verba;
- sobreposição;
- saturação;
- resultados calculados.

---

## 25. Decisão canônica

O Briefing de Mídia do MediAd Planner é definido como:

> Um Objeto Contextual Estruturado que organiza a situação mercadológica, os objetivos declarados, a estrutura territorial e populacional, os públicos, a jornada, o período, a verba, as prioridades, as restrições e as pretensões do anunciante, sem antecipar decisões técnicas de mídia.

Qualquer implementação que introduza no Briefing objetivo de mídia, KPIs, pontos de contato, alcance, frequência, flight, meios, canais, inventários ou resultados calculados deverá ser considerada incompatível com esta especificação.
