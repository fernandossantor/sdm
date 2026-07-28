# Arquitetura de Mídia

**Documento:** `04_ARQUITETURA_DE_MIDIA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 28/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Arquitetura de Mídia recebe o **Perfil Estratégico de Mídia** produzido pela Tradução Estratégica e o converte em funções, pontos de contato, meios, canais, papéis estratégicos, relações e inventários candidatos.

Seu resultado principal é uma ou mais **Arquiteturas Candidatas de Mídia**, tecnicamente justificadas, editáveis, versionadas e aptas à simulação.

Fluxo canônico:

```text
Campanha
    ↓
Briefing
    ↓
Tradução Estratégica
Perfil Estratégico de Mídia
    ↓
Arquitetura de Mídia
Arquiteturas Candidatas
    ↓
Simulações
    ↓
Comparação e Otimização
    ↓
Plano Consolidado
```

A Arquitetura de Mídia integra o **Ambiente de Elaboração**, composto por quatro capacidades codependentes:

```text
Arquitetar
Simular
Comparar
Otimizar
```

Essas capacidades não formam uma sequência rígida. O sistema deve permitir ciclos sucessivos de construção, teste, comparação, ajuste e nova simulação.

---

## 2. Natureza do artefato

O artefato da etapa será denominado:

```text
Arquitetura Candidata de Mídia
```

Uma arquitetura candidata deverá conter, progressivamente:

- funções de mídia;
- públicos, segmentos e praças vinculados;
- etapas da jornada;
- pontos de contato;
- meios e canais candidatos;
- papéis estratégicos;
- relações entre mídias;
- veículos, plataformas, formatos e inventários elegíveis;
- modelos de compra;
- hipóteses de overlap;
- hipóteses de distribuição geográfica e temporal;
- critérios de seleção;
- índices de aderência;
- restrições;
- graus de confiança;
- alterações do planejador;
- rastreabilidade;
- versão e estado.

A Arquitetura não é ainda uma grade final de veiculação, uma compra de mídia ou um plano consolidado.

---

## 3. Limites da Arquitetura

A Arquitetura deve:

- transformar parâmetros estratégicos em funções de mídia;
- relacionar jornada e pontos de contato;
- relacionar objetivos e pretensões com resultados observáveis e KPIs;
- qualificar meios, canais, veículos, plataformas, formatos e inventários;
- classificar mídias como principal, complementar ou de apoio;
- registrar relações entre mídias;
- sugerir alternativas elegíveis;
- produzir arquiteturas candidatas;
- fornecer configurações iniciais para simulação;
- permitir inclusão, exclusão e ajuste pelo planejador.

A Arquitetura não deve, isoladamente:

- calcular resultados finais de alcance ou frequência;
- calcular GRP, TRP, CPM, CPP, CTR, CPC, CPA ou ROAS;
- determinar quantidades finais de inserções ou impressões;
- fechar a distribuição definitiva da verba;
- executar a otimização final;
- consolidar o plano.

Esses cálculos e decisões pertencem ao Ambiente de Elaboração, sobretudo à Simulação, à Comparação e à Otimização.

---

## 4. Contrato de entrada

A Arquitetura deve consumir o Perfil Estratégico de Mídia vigente, especialmente:

- dimensões técnicas;
- intensidades requeridas;
- pesos estratégicos;
- prioridades;
- condições de atendimento;
- objetivos de mídia derivados;
- públicos, segmentos e universos;
- praças;
- etapas da jornada;
- período;
- verba disponível;
- restrições;
- tensões;
- graus de confiança;
- valores calculados, ajustados e efetivos.

Nenhuma recomendação deve ser produzida sem vínculo explícito com parâmetros do Perfil Estratégico ou regras metodológicas versionadas.

---

## 5. Processo canônico

```text
Perfil Estratégico de Mídia
        ↓
Funções de mídia requeridas
        ↓
Pontos de contato possíveis
        ↓
Capacidades técnicas necessárias
        ↓
Qualificação de meios e canais
        ↓
Qualificação de veículos, plataformas e formatos
        ↓
Elegibilidade de inventários
        ↓
Classificação dos papéis estratégicos
        ↓
Construção de relações entre mídias
        ↓
Geração de arquiteturas candidatas
        ↓
Configurações iniciais para simulação
```

A seleção não deve começar diretamente pelo inventário. O movimento deve ser progressivo, da função estratégica à unidade comercial disponível.

---

## 6. Funções de mídia

A Arquitetura deve converter os parâmetros estratégicos em funções de mídia.

Biblioteca inicial de funções:

- construir alcance;
- ampliar cobertura territorial;
- gerar frequência;
- sustentar continuidade;
- acelerar a construção de alcance;
- produzir impacto;
- reforçar lembrança;
- gerar afinidade;
- alcançar segmentos específicos;
- sustentar presença territorial;
- acompanhar etapas da jornada;
- gerar tráfego;
- estimular resposta;
- apoiar conversão;
- permitir retargeting;
- gerar dados;
- apoiar mensuração;
- responder à pressão competitiva;
- reforçar diferenciação;
- integrar mídia e ponto de venda.

Uma função pode ser atendida por várias mídias. Uma mesma mídia pode exercer várias funções.

Cada função deverá registrar:

- identificador;
- origem no Perfil Estratégico;
- intensidade requerida;
- peso;
- prioridade;
- condição;
- públicos vinculados;
- praças vinculadas;
- etapas da jornada vinculadas;
- grau de confiança.

---

## 7. Jornada e pontos de contato

A jornada pertence ao Briefing. Os pontos de contato são identificados e estruturados na Arquitetura.

Relação canônica:

```text
Público
    ↓
Etapa da jornada
    ↓
Necessidade comunicacional
    ↓
Ponto de contato possível
    ↓
Meios e canais aptos
```

O ponto de contato representa uma situação de encontro entre o público e a comunicação. Não deve ser confundido com meio, canal, veículo ou plataforma.

Cada ponto de contato deverá registrar:

- público;
- segmento;
- praça;
- etapa da jornada;
- situação de contato;
- necessidade comunicacional;
- relevância;
- intensidade;
- meios e canais compatíveis;
- limitações;
- grau de confiança.

---

## 8. Pretensões, objetivos e KPIs

As pretensões do Briefing são traduzidas em objetivos de mídia e parâmetros na etapa anterior. Na Arquitetura, esses parâmetros são relacionados a resultados observáveis e a KPIs adequados.

Relação canônica:

```text
Pretensão declarada
    ↓
Objetivo de mídia derivado
    ↓
Função de mídia
    ↓
Resultado observável
    ↓
KPI aplicável
```

O KPI não deve ser escolhido apenas porque existe no catálogo. Sua aplicabilidade depende de:

- objetivo;
- função;
- meio ou canal;
- modelo de compra;
- disponibilidade de dados;
- capacidade real de mensuração;
- modelo de atribuição.

A definição da meta e o cálculo do resultado ocorrerão no Ambiente de Elaboração.

---

## 9. Qualificação das mídias

Cada alternativa deve ser qualificada por capacidades técnicas parametrizadas.

Biblioteca inicial de atributos:

- alcance;
- frequência;
- cobertura geográfica;
- afinidade;
- seletividade;
- impacto;
- continuidade;
- velocidade de entrega;
- segmentação;
- contextualidade;
- capacidade audiovisual;
- interatividade;
- capacidade de resposta;
- capacidade de conversão;
- mensurabilidade;
- rastreabilidade;
- flexibilidade de compra;
- flexibilidade criativa;
- capacidade de otimização;
- custo relativo;
- disponibilidade;
- risco de saturação;
- compatibilidade com a jornada;
- compatibilidade territorial;
- compatibilidade temporal.

Os atributos devem possuir valores, fontes, datas, unidades, escopo e graus de confiança.

---

## 10. Índice de aderência

A recomendação deve resultar da correlação entre:

```text
Perfil Estratégico
        ×
Capacidades da mídia
        ×
Condições da campanha
```

O índice de aderência deverá considerar:

- pesos estratégicos;
- capacidades da alternativa;
- públicos e praças;
- jornada e pontos de contato;
- período;
- verba e preços;
- restrições;
- disponibilidade;
- confiança dos dados;
- penalizações por incompatibilidade ou saturação prevista.

O sistema deverá preservar:

- fórmula aplicada;
- versão da fórmula;
- contribuições por dimensão;
- penalizações;
- valor calculado;
- valor ajustado;
- valor efetivo;
- justificativa do ajuste.

O índice orienta a recomendação, mas não substitui a decisão do planejador.

---

## 11. Hierarquia de seleção

A ontologia geral será:

```text
Meio
    ↓
Canal
    ↓
Veículo ou plataforma
    ↓
Formato
    ↓
Inventário
```

A estrutura deve acomodar diferenças entre mercados de mídia sem apagar os níveis conceituais.

Exemplos:

```text
TV aberta
    ↓
Emissora
    ↓
Programa ou faixa
    ↓
Inserção
```

```text
Mídia social
    ↓
Plataforma
    ↓
Posicionamento
    ↓
Formato
    ↓
Impressões compradas
```

```text
OOH
    ↓
Operador
    ↓
Circuito
    ↓
Tipo de ativo
    ↓
Face ou período
```

Nem todo meio exige todos os níveis, mas cada entidade deve possuir tipo e posição inequívocos na hierarquia.

---

## 12. Papéis estratégicos

Toda mídia selecionada deve poder receber um papel estratégico:

- Principal;
- Complementar;
- Apoio.

O papel é contextual. Não é uma propriedade permanente do meio.

### 12.1 Principal

Assume a maior responsabilidade pelo atendimento dos objetivos e parâmetros prioritários da arquitetura.

Pode responder por:

- função central;
- maior contribuição esperada para alcance ou pressão;
- principal relação com o público prioritário;
- maior responsabilidade territorial ou temporal;
- maior proteção na alocação de verba.

Não deve ser definido apenas pelo maior investimento.

### 12.2 Complementar

Amplia, qualifica ou corrige limitações do principal.

Pode:

- estender alcance;
- elevar frequência;
- cobrir públicos ou praças adicionais;
- atuar em outras etapas da jornada;
- elevar afinidade;
- acrescentar mensurabilidade;
- reduzir lacunas temporais ou territoriais.

### 12.3 Apoio

Executa funções específicas, pontuais ou localizadas.

Pode:

- reforçar datas críticas;
- ativar pontos de contato;
- apoiar conversão;
- integrar mídia e PDV;
- atender públicos secundários;
- gerar dados ou retargeting;
- sustentar presença local.

---

## 13. Papel geral e papel contextual

O sistema deverá admitir:

- papel geral;
- papel por público;
- papel por segmento;
- papel por praça;
- papel por etapa da jornada;
- papel por objetivo;
- papel por período.

Exemplo:

```text
Canal A
Papel geral: Principal
Público 1: Principal
Público 2: Complementar
Praça central: Principal
Praça secundária: Apoio
```

Os papéis poderão receber coeficientes configuráveis. Valores iniciais ilustrativos não devem ser tratados como universais.

O papel poderá influenciar:

- prioridade de verba;
- participação mínima;
- proteção contra cortes;
- ordem de otimização;
- tolerância a substituições;
- avaliação da contribuição.

---

## 14. Relações entre mídias

A Arquitetura deve registrar como as mídias se articulam.

Tipos iniciais de relação:

- complementaridade;
- reforço;
- extensão de alcance;
- extensão territorial;
- extensão temporal;
- extensão de jornada;
- redundância intencional;
- redundância indesejada;
- dependência;
- sequenciamento;
- ativação;
- retargeting;
- transferência de atenção;
- captura de demanda;
- apoio à conversão.

Cada relação deverá conter:

- origem;
- destino;
- tipo;
- função;
- público;
- praça;
- etapa da jornada;
- período;
- intensidade;
- condição;
- confiança.

---

## 15. Overlap

O overlap pertence ao Ambiente de Elaboração porque depende das mídias combinadas.

A Arquitetura registra a hipótese. A Simulação aplica o valor quantitativo.

Para cada par de canais ou inventários, o sistema deverá permitir:

- overlap sugerido;
- overlap ajustado;
- overlap efetivo;
- público;
- praça;
- período;
- fonte;
- confiança;
- justificativa.

Regra metodológica já consolidada:

```text
Mesma praça:
o overlap tende a contribuir principalmente para frequência.

Praças distintas:
a combinação tende a contribuir principalmente para alcance territorial.
```

Essa regra não elimina a modelagem da sobreposição real de audiências.

---

## 16. Inventário elegível

A elegibilidade deverá considerar:

- disponibilidade na praça;
- cobertura do público;
- aderência às funções;
- compatibilidade com a jornada;
- preço;
- modelo de compra;
- período;
- restrições;
- formato;
- mensurabilidade;
- limites operacionais;
- dados suficientes para simulação.

Estados possíveis:

- Sugerido;
- Elegível;
- Selecionado para simulação;
- Rejeitado;
- Indisponível;
- Substituído.

A rejeição ou substituição deverá preservar justificativa e autoria.

---

## 17. Preços e modelos de compra

A Arquitetura consulta preços para verificar viabilidade e elegibilidade. A Simulação utiliza preços e quantidades para calcular resultados.

Modelos de compra iniciais:

- inserção;
- espaço;
- face;
- diária;
- período;
- pacote;
- patrocínio;
- audiência;
- GRP;
- impressão;
- CPM;
- clique;
- CPC;
- visualização;
- CPV;
- lead;
- CPL;
- aquisição ou conversão;
- CPA.

Cada preço deverá registrar:

- unidade comercial;
- preço bruto;
- desconto;
- preço líquido;
- comissão da agência;
- encargos aplicáveis;
- quantidade mínima;
- vigência;
- praça;
- disponibilidade;
- fonte;
- confiança.

---

## 18. Arquiteturas candidatas

O sistema poderá gerar várias arquiteturas a partir do mesmo Perfil Estratégico.

Tipos iniciais de orientação:

- alcance;
- frequência;
- equilíbrio;
- continuidade;
- impacto;
- afinidade;
- performance;
- eficiência;
- presença territorial;
- personalizada.

Cada arquitetura é uma hipótese distinta de articulação das mídias e deve poder originar uma ou mais simulações.

O sistema deve distinguir:

- sugestão do sistema;
- seleção do planejador;
- seleção efetiva.

---

## 19. Relação com a Simulação

A Arquitetura define:

- funções;
- pontos de contato;
- meios e canais;
- papéis;
- relações;
- inventários candidatos;
- modelos de compra;
- hipóteses de overlap;
- critérios e restrições;
- configurações iniciais.

A Simulação calcula:

- quantidades;
- investimento;
- audiência;
- impactos;
- alcance;
- cobertura;
- frequência;
- GRP;
- TRP;
- CPM;
- CPP;
- CTR;
- CPC;
- CPA;
- conversões;
- ROAS;
- saturação;
- contribuição marginal;
- distribuição geográfica e temporal.

Uma mesma arquitetura poderá originar várias configurações de simulação.

```text
Arquitetura
    +
Configuração de simulação
    =
Resultado simulado
```

---

## 20. Catálogo de métricas do Ambiente de Elaboração

As métricas não pertencem todas à Arquitetura, mas deverão estar disponíveis no Ambiente de Elaboração.

### 20.1 Audiência e exposição

- audiência;
- impactos;
- alcance;
- cobertura;
- frequência;
- GRP;
- TRP;
- afinidade;
- ICP;
- ISP;
- Share of Voice;
- impressões;
- visualizações;
- taxa de conclusão.

### 20.2 Custo e eficiência

- investimento bruto;
- líquido de veículos;
- comissão da agência;
- CPM;
- CPP;
- custo por alcance;
- custo por frequência incremental;
- CPC;
- CPV;
- CPL;
- CPA;
- custo por conversão;
- custo incremental.

### 20.3 Resposta e performance

- cliques;
- CTR;
- visitas;
- sessões;
- leads;
- conversões;
- taxa de conversão;
- receita;
- ROAS;
- resposta direta;
- engajamento, quando tecnicamente aplicável.

### 20.4 Distribuição

- verba por meio;
- verba por canal;
- verba por praça;
- verba por público;
- verba por período;
- impactos por praça;
- alcance por público;
- pressão por período;
- participação de cada mídia.

### 20.5 Qualidade da arquitetura

- aderência estratégica;
- atendimento das funções;
- cobertura da jornada;
- cobertura dos pontos de contato;
- complementaridade;
- redundância;
- diversidade;
- mensurabilidade;
- flexibilidade;
- risco;
- confiança.

---

## 21. Fórmulas canônicas iniciais

As fórmulas somente devem ser aplicadas quando houver entradas válidas e escopo explícito.

### 21.1 GRP

```text
GRP = alcance percentual × frequência média
```

Também poderá ser obtido pela soma das audiências percentuais das inserções, conforme a fonte disponível.

### 21.2 TRP

```text
TRP = alcance percentual no público-alvo × frequência média no público-alvo
```

### 21.3 CPM

```text
CPM = investimento ÷ impressões × 1.000
```

O tipo de investimento utilizado deverá ser informado.

### 21.4 CPP

```text
CPP = investimento ÷ pontos de audiência
```

### 21.5 CTR

```text
CTR = cliques ÷ impressões × 100
```

### 21.6 CPC

```text
CPC = investimento ÷ cliques
```

### 21.7 CPA

```text
CPA = investimento ÷ conversões
```

### 21.8 ROAS

Conforme decisão metodológica já consolidada no projeto:

```text
ROAS = (receita - investimento) ÷ investimento × 100
```

Cada cálculo deverá registrar:

- universo de referência;
- público;
- praça;
- período;
- mídia ou conjunto de mídias;
- investimento considerado;
- fonte dos dados;
- fórmula e versão;
- confiança.

---

## 22. Construção assistida e manual

A Arquitetura deve permitir simultaneamente:

### 22.1 Construção assistida

O sistema sugere:

- funções;
- pontos de contato;
- meios;
- canais;
- veículos;
- plataformas;
- formatos;
- inventários;
- papéis;
- relações;
- modelos de compra.

### 22.2 Construção manual

O planejador pode:

- incluir alternativas não sugeridas;
- excluir sugestões;
- alterar papéis;
- modificar relações;
- substituir inventários;
- restringir ou ampliar o conjunto elegível;
- ajustar parâmetros;
- justificar decisões.

O valor sugerido nunca deve ser apagado pelo ajuste manual.

---

## 23. Versionamento e estados

Toda alteração relevante deverá produzir nova versão ou revisão auditável.

Estados possíveis:

- Gerada;
- Em edição;
- Apta para simulação;
- Simulada;
- Comparada;
- Otimizada;
- Selecionada;
- Descartada;
- Incorporada ao plano.

Cada versão deverá manter:

- arquitetura de origem;
- Perfil Estratégico utilizado;
- parâmetros vigentes;
- alterações;
- responsável;
- data e hora;
- justificativas;
- resultados associados.

---

## 24. Contrato de saída

A saída mínima da Arquitetura deverá conter:

```text
Identificador e versão
Perfil Estratégico de origem
Funções de mídia
Objetivos vinculados
Públicos, segmentos e universos
Praças
Etapas da jornada
Pontos de contato
Meios e canais
Veículos, plataformas e formatos candidatos
Papéis estratégicos
Relações entre mídias
Inventários elegíveis
Modelos de compra
Hipóteses de overlap
Hipóteses geográficas e temporais
Critérios de avaliação
Restrições
Índices de aderência
Graus de confiança
Valores sugeridos, ajustados e efetivos
Histórico de alterações
Estado da arquitetura
```

---

## 25. Critérios de conclusão

Uma arquitetura estará apta para simulação quando:

- possuir ao menos uma função de mídia válida;
- possuir público e praça vinculados;
- relacionar funções a meios ou canais elegíveis;
- possuir papéis estratégicos definidos;
- possuir inventários ou classes de inventário simuláveis;
- possuir preços ou parâmetros de custo suficientes;
- registrar restrições aplicáveis;
- indicar parâmetros ausentes ou incertos;
- preservar rastreabilidade;
- passar pelas validações estruturais.

A ausência de dados não deve ser ocultada. O sistema deverá sinalizar limitações e reduzir o grau de confiança quando necessário.

---

## 26. Formulação canônica

A Arquitetura de Mídia é o processo estruturado que converte o Perfil Estratégico de Mídia em funções, pontos de contato, meios, canais, papéis, relações e inventários candidatos, produzindo alternativas tecnicamente justificadas e aptas à simulação.

A classificação **Principal, Complementar e Apoio** pertence à Arquitetura. Os cálculos de **GRP, TRP, CPM, CPP, CTR, CPC, CPA, ROAS** e demais resultados pertencem ao Ambiente de Elaboração e são produzidos principalmente pelas Simulações, sendo depois mobilizados pela Comparação e pela Otimização.
