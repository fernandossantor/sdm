# Biblioteca de Inventários do MediAd Planner

**Documento:** `13_BIBLIOTECA_DE_INVENTARIOS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Inventários organiza, preserva e disponibiliza oportunidades de mídia reutilizáveis para os planejamentos do MediAd Planner.

Ela recebe, como referência estratégica, os pontos de contato definidos pela Biblioteca 16 e os desdobra em tipologias, meios, ambientes, formatos, disponibilizações, ofertas e inventários concretos.

```text
Ponto de contato
    ↓
Tipologia de mídia
    ↓
Inventários de referência
    ↓
Disponibilizações
    ↓
Ofertas comerciais
```

A Biblioteca não define jornadas, etapas, necessidades comunicacionais ou funções. Ela declara em quais tipologias e condições essas estruturas podem ser materializadas.

---

## 2. Posição na arquitetura

```text
Biblioteca 16
Jornadas, necessidades, funções e pontos de contato
    ↓
Biblioteca 13
Tipologias e inventários
    ↓
Arquitetura de Mídia
    ↓
Simulações
```

O ponto de contato é uma categoria de mídia. O inventário é uma oportunidade operacional e comercial mais específica.

---

## 3. Separações obrigatórias

```text
Ponto de contato ≠ formato
Ponto de contato ≠ ambiente
Ponto de contato ≠ veículo
Ponto de contato ≠ plataforma
Ponto de contato ≠ inventário
Formato ≠ inventário completo
Meio ≠ oferta comercial
Indicador ≠ atributo permanente do inventário
```

Exemplo:

```text
Ponto de contato: mídia digital
    ↓
Canal: social
    ↓
Ambiente: feed
    ↓
Formato: vídeo vertical
    ↓
Plataforma: rede social específica
    ↓
Inventário: oportunidade concreta de entrega
```

---

## 4. Princípio de composição

A composição pode utilizar:

```text
Ponto de contato
→ Tecnologia
→ Canal
→ Ambiente
→ Estrutura
→ Formato
→ Modelo comercial
→ Modalidade de compra
→ Unidade de compra
→ Inventário de referência
→ Meio / Veículo / Plataforma
→ Programa / Faixa / Posicionamento
→ Disponibilização
→ Oferta comercial
```

A ordem é progressiva na interface, mas relacional no banco de dados. Diversas compatibilidades são N:N.

---

## 5. Objetos fundamentais

### 5.1 Ponto de contato de origem

Categoria de mídia proveniente da Biblioteca 16, como televisão, rádio, jornal, revista, cinema, mídia exterior, mídia digital, ponto de venda, evento, atendimento, mídia própria ou no media.

### 5.2 Catálogos taxonômicos

Vocabulários controlados para classificar:

- tecnologias;
- canais;
- ambientes;
- estruturas;
- formatos;
- modelos comerciais;
- modalidades de compra;
- unidades de compra;
- meios, veículos e plataformas;
- programas, faixas, contextos e posicionamentos.

### 5.3 Inventário de referência

Combinação validada de atributos tipológicos que representa uma possibilidade estruturada de exposição, inserção, presença ou entrega.

### 5.4 Meio, veículo, plataforma ou empresa

Entidade concreta que disponibiliza, opera, publica, transmite, representa ou comercializa inventário.

### 5.5 Programa, faixa, publicação, ambiente ou posicionamento

Camada contextual na qual a exposição ocorre. Pode carregar proposta editorial, temas, gêneros, contexto de exposição, audiência e restrições próprias.

### 5.6 Disponibilização

Vínculo entre um inventário de referência e um meio concreto.

### 5.7 Oferta comercial

Conjunto de condições comerciais aplicadas a uma disponibilização, podendo variar por fornecedor, praça, período, moeda, preço, desconto, fees, mínimos, capacidade e negociação.

---

## 6. Tipologia de mídia

A Biblioteca deve permitir mapear cada ponto de contato para uma ou mais tipologias.

Exemplos de pontos de contato:

- televisão;
- rádio;
- jornal;
- revista;
- cinema;
- mídia exterior;
- mídia digital;
- ponto de venda;
- evento;
- atendimento;
- mídia própria;
- no media.

Exemplos de desdobramentos tipológicos:

- TV aberta e fechada;
- rádio AM, FM, streaming e podcast;
- OOH, DOOH e mobiliário urbano;
- search, social, display, vídeo, CTV, e-mail e retail media;
- gôndola, checkout, sampling e material de PDV.

Esses desdobramentos não alteram a definição do ponto de contato; apenas materializam sua tipologia.

---

## 7. Camada semântica e contextual

A Biblioteca deve descrever inventários por dimensões comparáveis às dos públicos e às estruturas comunicacionais:

- proposta editorial;
- temas e gêneros;
- contextos de contato;
- comportamentos de consumo atendidos;
- etapas de jornada compatíveis;
- necessidades comunicacionais que podem apoiar;
- funções comunicacionais que podem desempenhar;
- segmentações disponíveis;
- cobertura territorial;
- restrições editoriais e operacionais.

A relação com etapa, necessidade e função é contextual e não essencialista.

Um inventário não “é de conversão”, “é de alcance” ou “é de consideração” por natureza. Ele pode desempenhar determinados papéis quando utilizado em condições compatíveis.

---

## 8. Capacidades analíticas

Cada inventário ou disponibilização pode declarar:

- objetivos suportados;
- resultados suportados;
- indicadores compatíveis;
- indicadores projetáveis;
- indicadores calculáveis;
- indicadores posteriormente mensuráveis;
- requisitos de dados;
- fontes possíveis;
- unidades;
- limitações;
- grau de confiança.

O inventário não armazena KPI permanente. Um indicador torna-se KPI apenas quando priorizado em um planejamento.

---

## 9. Camada territorial

Devem ser registradas disponibilidade e cobertura por:

- país;
- estado;
- região;
- município;
- distrito;
- bairro;
- CEP;
- setor censitário;
- coordenada;
- raio;
- rota;
- ponto;
- polígono;
- área personalizada.

Cada registro deve preservar natureza da cobertura, fonte, data e confiança.

---

## 10. Dimensões compartilhadas

A Biblioteca deve utilizar catálogos compartilhados para:

- pontos de contato;
- etapas;
- necessidades comunicacionais;
- funções comunicacionais;
- interesses;
- comportamentos;
- contextos de contato;
- territórios;
- temas editoriais;
- indicadores;
- famílias de indicadores.

Não devem existir vocabulários redundantes e incompatíveis.

---

## 11. Audiência, cobertura, alcance e afinidade

Audiência é medida observada ou estimada de pessoas expostas em determinado contexto, período e praça.

Cobertura pode representar alcance técnico, área territorial, população potencialmente alcançável ou disponibilidade comercial, desde que sua natureza seja declarada.

Alcance e frequência são metas ou resultados projetados de cenários e planos. Não são atributos permanentes do inventário de referência.

Afinidade observada é uma relação medida entre público e mídia. Aderência estimada é cálculo estratégico da Arquitetura.

---

## 12. Relação com a Biblioteca 16

A Biblioteca 16 termina no ponto de contato.

A Biblioteca 13 inicia o desdobramento tipológico.

```text
Etapa
    ↓
Necessidade
    ↓
Função
    ↓
Ponto de contato
------------------------
Limite entre bibliotecas
------------------------
Tecnologia
    ↓
Canal
    ↓
Ambiente
    ↓
Formato
    ↓
Inventário
```

A relação função–ponto de contato pertence à Biblioteca 16.

A relação ponto de contato–tipologia–inventário pertence à Biblioteca 13.

---

## 13. Relação com a Arquitetura de Mídia

A Biblioteca fornece dados para que a Arquitetura avalie:

- compatibilidade com o ponto de contato;
- compatibilidade com etapa, necessidade e função;
- aderência editorial e comportamental;
- compatibilidade demográfica e territorial;
- afinidade observada;
- indicadores prioritários e capacidades analíticas;
- custo, disponibilidade e restrições;
- complementaridade, overlap e saturação;
- confiança das evidências.

Nenhuma relação isolada determina a recomendação final.

---

## 14. Escopos, versionamento e snapshot

Inventários e relações podem possuir escopo global, de espaço de trabalho, de projeto ou pessoal/rascunho.

Toda instância utilizada deve preservar:

- versão do inventário de referência;
- versão da disponibilização;
- versão da oferta;
- ponto de contato de origem;
- atributos tipológicos;
- propriedades editoriais e contextuais;
- capacidades analíticas;
- cobertura territorial;
- fontes e datas;
- ajustes locais;
- autoria.

Alterações futuras não modificam retroativamente planejamentos anteriores.

---

## 15. Modelo lógico mínimo

```text
pontos_contato
tecnologias
canais
ambientes
estruturas
formatos
modelos_comerciais
modalidades_compra
unidades_compra
inventarios_referencia
meios
contextos_midia
disponibilizacoes_inventario
ofertas_comerciais
pontos_contato_tipologias
inventarios_funcoes
inventarios_etapas
inventarios_necessidades
inventarios_indicadores
coberturas_inventario
inventarios_temas
inventarios_segmentacoes
medicoes_audiencia
afinidades_observadas
```

As relações devem preservar contexto, fonte, validade e confiança.

---

## 16. Princípio consolidado

> O ponto de contato é uma mídia; o inventário é sua materialização tipológica, operacional e comercial. A Biblioteca de Inventários não define a jornada nem cria necessidades e funções. Ela declara quais alternativas concretas podem materializar os pontos de contato e quais capacidades contextuais, territoriais e analíticas possuem.