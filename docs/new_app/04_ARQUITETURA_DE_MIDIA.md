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

```text
Campanha
    ↓
Briefing
    ↓
Tradução Estratégica
    ↓
Perfil Estratégico de Mídia
    ↓
Arquitetura de Mídia
    ↓
Arquiteturas Candidatas
    ↓
Simulações
    ↓
Comparação e Otimização
    ↓
Plano Consolidado
```

A adequação das mídias nunca é uma propriedade fixa dos meios. Ela é calculada dinamicamente a partir das variáveis do Briefing, dos pesos da Tradução Estratégica, das condições da campanha, das capacidades das alternativas e das relações entre públicos e inventários.

A revisão atual não substitui esse modelo. Ela acrescenta uma nova camada de informação ao cálculo já existente: a **qualificação público–inventário**.

---

## 2. Natureza do artefato

Uma Arquitetura Candidata de Mídia deverá conter, progressivamente:

- funções de mídia;
- públicos, segmentos, universos e praças vinculados;
- etapas da jornada;
- pontos de contato;
- meios e canais candidatos;
- papéis estratégicos;
- relações entre mídias;
- veículos, plataformas, programas, formatos e inventários elegíveis;
- modelos de compra;
- hipóteses de overlap;
- hipóteses de distribuição geográfica e temporal;
- critérios de seleção;
- índices de aderência;
- contribuições da qualificação público–inventário;
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
- qualificar meios, canais, veículos, plataformas, programas, formatos e inventários;
- incorporar a relação entre características dos públicos e propriedades das alternativas de mídia;
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

Esses cálculos pertencem ao Ambiente de Elaboração, sobretudo à Simulação, à Comparação e à Otimização.

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
- interesses e comportamentos relevantes;
- praças e territórios;
- etapas da jornada;
- pontos de contato e necessidades comunicacionais;
- período;
- verba disponível;
- restrições;
- tensões;
- graus de confiança;
- valores calculados, ajustados e efetivos.

Também deve consultar, conforme disponibilidade:

- proposta editorial e temas dos veículos, programas e ambientes;
- contextos e comportamentos de contato atendidos pelos inventários;
- funções de jornada compatíveis;
- segmentações disponíveis;
- cobertura territorial;
- afinidade observada e demais evidências empíricas;
- fontes, datas, metodologias e confiança dos dados.

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
Qualificação de veículos, plataformas, programas e formatos
        ↓
Qualificação público–inventário
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

A qualificação público–inventário é um componente da Arquitetura de Mídia. Não constitui um motor autônomo concorrente.

A seleção não deve começar diretamente pelo inventário. O movimento deve ser progressivo, da função estratégica à unidade comercial disponível.

---

## 6. Funções de mídia

A Arquitetura deve converter parâmetros estratégicos em funções de mídia, entre elas:

- construir alcance;
- ampliar cobertura territorial;
- gerar frequência;
- sustentar continuidade;
- acelerar a construção de alcance;
- produzir impacto;
- reforçar lembrança;
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

O antigo enunciado “gerar afinidade” deve ser interpretado como **selecionar alternativas com maior afinidade observada ou aderência estimada ao público**, e não como produzir afinidade como efeito automático da veiculação.

---

## 7. Jornada e pontos de contato

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

## 8. Qualificação das mídias

Cada alternativa deve ser qualificada por capacidades técnicas parametrizadas e por sua relação contextual com o público.

### 8.1 Capacidades técnicas

- potencial de alcance;
- potencial de frequência;
- cobertura geográfica;
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
- compatibilidade temporal.

### 8.2 Qualificação público–inventário

A qualificação público–inventário acrescenta ao cálculo de adequação as seguintes dimensões:

- aderência editorial ou temática;
- aderência comportamental;
- aderência à jornada;
- compatibilidade demográfica;
- compatibilidade territorial;
- adequação contextual;
- afinidade observada, quando disponível;
- confiabilidade das evidências.

Ela compara descrições estruturadas e compatíveis das Bibliotecas de Públicos e de Inventários.

```text
Interesses do público
↔ temas e proposta editorial

Comportamentos do público
↔ contextos de contato atendidos

Etapa da jornada
↔ funções possíveis do inventário

Território do público
↔ cobertura territorial

Características demográficas
↔ segmentação disponível ou audiência observada
```

Os atributos devem possuir valores, fontes, datas, unidades, escopo e graus de confiança.

---

## 9. Afinidade observada e aderência estimada

### 9.1 Afinidade observada

Afinidade observada é uma evidência empírica da presença proporcional de determinado público na audiência de um veículo, programa ou inventário, em comparação com um universo de referência.

Deve sempre registrar:

- público ou segmento;
- veículo, programa ou inventário;
- praça;
- período;
- universo de comparação;
- valor e unidade;
- fonte;
- metodologia;
- grau de confiança.

Ela não pertence isoladamente à Biblioteca de Públicos nem à Biblioteca de Inventários. É uma relação medida entre ambos.

### 9.2 Aderência estimada

Aderência estimada é a compatibilidade estratégica calculada pelo MediAd Planner a partir das características do público, das propriedades da alternativa de mídia e das condições da campanha.

Não deve ser apresentada como audiência medida.

---

## 10. Índice de aderência

A recomendação deve resultar da correlação entre:

```text
Perfil Estratégico
        ×
Capacidades da mídia
        ×
Qualificação público–inventário
        ×
Condições da campanha
```

O índice de aderência deverá considerar:

- pesos estratégicos;
- capacidades da alternativa;
- públicos e praças;
- interesses e comportamentos relevantes;
- jornada e pontos de contato;
- compatibilidades editorial, comportamental, demográfica, territorial e contextual;
- afinidade observada, quando houver;
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

```text
Meio
    ↓
Canal
    ↓
Veículo ou plataforma
    ↓
Programa, faixa, ambiente ou posicionamento
    ↓
Formato
    ↓
Inventário
```

Nem todo mercado exige todos os níveis, mas cada entidade deve possuir tipo e posição inequívocos.

A proposta editorial pode pertencer ao veículo, programa, publicação, ambiente ou conteúdo. A cobertura territorial pode pertencer ao veículo, rede, emissora, circuito, plataforma ou disponibilização. O inventário deve herdar essas propriedades quando aplicáveis, preservando sua origem.

---

## 12. Papéis estratégicos

Toda mídia selecionada deve poder receber um papel:

- Principal;
- Complementar;
- Apoio.

O papel é contextual e pode variar por:

- público;
- segmento;
- praça;
- etapa da jornada;
- objetivo;
- período.

A qualificação público–inventário contribui para a atribuição do papel, mas não a determina isoladamente.

Também devem ser considerados:

- objetivos;
- KPIs;
- orçamento;
- complementaridade;
- overlap;
- saturação;
- cobertura;
- restrições;
- disponibilidade;
- capacidade de mensuração.

---

## 13. Overlap

A Arquitetura registra hipóteses de overlap. A Simulação aplica valores quantitativos.

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

Regra metodológica:

```text
Mesma praça:
o overlap tende a contribuir principalmente para frequência.

Praças distintas:
a combinação tende a contribuir principalmente para alcance territorial.
```

Essa regra não elimina a modelagem da sobreposição real de audiências.

---

## 14. Inventário elegível

A elegibilidade deverá considerar:

- disponibilidade na praça;
- sobreposição entre território do público e cobertura do veículo;
- aderência às funções;
- compatibilidade com a jornada;
- aderência editorial e comportamental;
- compatibilidade demográfica;
- afinidade observada, quando houver;
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

## 15. Relação com a Simulação

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

Audiência, alcance, cobertura e frequência não pertencem à definição permanente do público. São propriedades ou resultados associados a veículos, inventários, disponibilizações, períodos e planos.

---

## 16. Rastreabilidade

Cada recomendação deve permitir reconstruir:

```text
Dado do Briefing
    ↓
Tradução Estratégica
    ↓
Peso ou restrição
    ↓
Capacidade da alternativa
    ↓
Qualificação público–inventário
    ↓
Índice de aderência
    ↓
Papel estratégico
    ↓
Arquitetura candidata
```

A interface deve apresentar justificativas legíveis, incluindo contribuições positivas, limitações, ausências de dados e graus de confiança.

---

## 17. Formulação consolidada

> A Arquitetura de Mídia já calcula dinamicamente a adequação das alternativas a partir das variáveis do Briefing e da Tradução Estratégica. A descrição comparável de públicos e inventários acrescenta uma nova camada de qualificação, tornando mais preciso o cálculo de adequação editorial, comportamental, territorial, demográfica, contextual e funcional, sem substituir os demais critérios do modelo.
