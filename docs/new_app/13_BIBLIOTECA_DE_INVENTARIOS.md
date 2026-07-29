# Biblioteca de Inventários do MediAd Planner

## 1. Finalidade

A Biblioteca de Inventários organiza, preserva e disponibiliza oportunidades de mídia reutilizáveis para os planejamentos do MediAd Planner.

Seu objetivo é permitir que usuários encontrem, selecionem, adaptem, cadastrem, comparem e utilizem inventários estruturados sem reconstruir, em cada projeto, todas as classificações, relações, condições comerciais e métricas necessárias.

A Biblioteca deve sustentar:

- a seleção de inventários na Arquitetura de Mídia;
- a composição de cenários;
- a alocação de investimento;
- a projeção de resultados;
- a comparação entre alternativas;
- a consolidação do plano;
- o cronograma;
- o mapa de veiculação;
- a rastreabilidade das versões utilizadas.

```text
A taxonomia define.
O inventário combina.
O meio disponibiliza.
A oferta comercializa.
Os KPIs mensuram.
O planejamento preserva a versão utilizada.
```

---

## 2. Posição na arquitetura

```text
Catálogos taxonômicos
        ↓
Relações de compatibilidade
        ↓
Inventários de referência
        ↓
Disponibilizações por meios
        ↓
Ofertas comerciais
        ↓
KPIs, métricas e medições
        ↓
Instâncias nos planejamentos
```

A Biblioteca não é apenas uma tela de cadastro nem uma tabela de preços. É uma camada de conhecimento entre os catálogos e os motores de planejamento.

---

## 3. Princípio de composição

O inventário é construído por uma cadeia hierárquica de refinamento:

```text
Tecnologia
→ Canal
→ Ambiente
→ Estrutura
→ Formato
→ Modelo comercial
→ Modalidade de compra
→ Unidade de compra
→ Inventário de referência
→ Meio / Plataforma / Empresa
→ Oferta comercial
→ KPIs e métricas
```

Essa cadeia representa a ordem operacional de composição na interface.

Ela não exige filiação exclusiva entre todos os níveis. Em vários pontos, as relações são de compatibilidade N:N.

Portanto, a hierarquia é simultaneamente:

- sequencial na experiência do usuário;
- relacional no banco de dados;
- multidimensional no domínio;
- contextual nos planejamentos.

---

## 4. Objetos fundamentais

### 4.1 Catálogo taxonômico

Vocabulários controlados utilizados para classificar inventários:

1. tecnologias;
2. canais;
3. ambientes;
4. estruturas;
5. formatos;
6. modelos comerciais;
7. modalidades de compra;
8. unidades de compra;
9. meios, plataformas ou empresas;
10. KPIs.

Os itens dos catálogos não são, isoladamente, inventários comercializáveis.

### 4.2 Inventário de referência

É a combinação validada dos oito primeiros níveis:

```text
Tecnologia
Canal
Ambiente
Estrutura
Formato
Modelo comercial
Modalidade de compra
Unidade de compra
```

Representa uma possibilidade estruturada de exposição, inserção, presença ou entrega de mídia.

O inventário de referência ainda não precisa informar quem o oferece, qual é o preço ou em quais praças está disponível.

### 4.3 Meio, plataforma ou empresa

É a entidade concreta que disponibiliza, opera, representa, publica, transmite ou comercializa o inventário.

Pode representar:

- plataforma tecnológica;
- veículo editorial;
- emissora;
- publicação;
- rede;
- publisher;
- exibidora;
- empresa de OOH ou DOOH;
- marketplace;
- varejista;
- operador de retail media;
- grupo de comunicação;
- representante comercial.

### 4.4 Programa, faixa, publicação, ambiente ou posicionamento

É a camada contextual na qual a exposição ocorre.

Pode representar:

- programa de televisão ou rádio;
- faixa horária;
- editoria;
- seção;
- podcast;
- episódio;
- canal de streaming;
- posicionamento digital;
- circuito;
- ambiente físico;
- conteúdo adjacente.

Essa camada pode carregar proposta editorial, temas, gêneros, contexto de exposição e evidências específicas de audiência.

### 4.5 Disponibilização do inventário

É o vínculo entre um inventário de referência e um meio concreto.

Responde:

> Este meio disponibiliza este inventário?

Uma disponibilização pode herdar atributos do meio, do programa, do ambiente ou do posicionamento, preservando a origem de cada informação.

### 4.6 Oferta comercial

É o conjunto de condições comerciais aplicado a uma disponibilização.

Pode variar por:

- fornecedor;
- praça;
- período;
- moeda;
- preço;
- desconto;
- fees;
- quantidade mínima;
- investimento mínimo;
- capacidade;
- modelo de negociação;
- contrato;
- segmento;
- condição especial.

Uma disponibilização pode possuir várias ofertas simultâneas ou históricas.

### 4.7 KPI e métrica

KPI é o indicador utilizado para avaliar entrega, custo, qualidade ou resultado.

Métrica é a medida operacional ou calculada relacionada ao inventário, à oferta ou ao planejamento.

O KPI deve ser associado ao inventário completo e ao contexto em que é mensurável, e não apenas ao meio.

---

## 5. Cadeia taxonômica

### 5.1 Tecnologia

Base técnica predominante que permite produção, distribuição, exibição ou comercialização.

Exemplos:

- impressa;
- eletrônica;
- digital;
- programática.

### 5.2 Canal

Grande campo de distribuição, exposição ou atuação midiática.

Exemplos:

- digital;
- eletrônica;
- impressa;
- OOH;
- PDV;
- programática;
- no media.

### 5.3 Ambiente

Contexto específico de circulação, exposição, reprodução ou interação.

Exemplos:

- Social;
- Search;
- Sites;
- TV aberta;
- FM;
- Podcast;
- Streaming de vídeo;
- CTV;
- Outdoor;
- DOOH;
- Shopping;
- Aeroporto;
- Gôndola;
- Checkout.

### 5.4 Estrutura

Forma organizacional, editorial ou transacional pela qual o inventário é disponibilizado.

Exemplos:

- Afiliada;
- Conteúdo;
- Direta;
- Patrocínio;
- Programática PG;
- Programática PMP;
- Programática Preferred;
- Programática RTB.

### 5.5 Formato

Configuração concreta da peça, espaço, inserção, ação ou entrega publicitária.

Exemplos:

- Feed;
- Stories;
- Reels;
- Banner;
- Texto;
- Responsivo;
- In-stream;
- Bumper;
- Spot 30;
- Página inteira;
- Dupla página;
- LED;
- Sampling;
- Wobbler.

### 5.6 Modelo comercial

Natureza geral do produto, arranjo ou propriedade comercial oferecida.

Exemplos:

- Mídia avulsa;
- Comercial simples;
- Patrocínio;
- Cota;
- Pacote comercial;
- Projeto especial;
- Branded content;
- Publieditorial;
- Ação promocional;
- Testemunhal;
- Permuta;
- Bonificação.

### 5.7 Modalidade de compra

Lógica pela qual o inventário é contratado, precificado ou negociado.

Exemplos:

- CPM;
- CPC;
- CPA;
- CPV;
- CPP;
- Diária;
- Semanal;
- Quinzenal;
- Mensal;
- Circuito;
- Avulsa;
- Cota;
- Patrocínio;
- Exclusividade;
- Projeto especial;
- Pacote;
- Tabela;
- Negociação.

### 5.8 Unidade de compra

Quantidade ou unidade operacional contratada.

Exemplos:

- inserção;
- mil impressões;
- clique;
- visualização;
- conversão;
- diária;
- face;
- circuito;
- espaço;
- cota;
- período.

---

## 6. Camada semântica e contextual

A estrutura operacional do inventário é necessária, mas insuficiente para qualificar sua adequação a públicos e objetivos.

A Biblioteca deve permitir descrever meios, programas, ambientes, disponibilizações e inventários por dimensões comparáveis às da Biblioteca de Públicos e Segmentos.

Essas descrições alimentam a qualificação público–inventário da Arquitetura de Mídia.

### 6.1 Perfil editorial ou temático

Pode registrar:

- proposta editorial;
- temas principais;
- gêneros de conteúdo;
- assuntos recorrentes;
- tom editorial;
- tipo de conteúdo adjacente;
- classificação etária;
- contexto de marca segura;
- restrições editoriais.

A proposta editorial tende a pertencer ao veículo, programa, publicação, ambiente ou conteúdo. O inventário pode herdar esses atributos quando a exposição ocorre nesse contexto.

### 6.2 Contextos de contato

Podem ser associados ao inventário:

- consumo em deslocamento;
- consumo doméstico;
- uso simultâneo de telas;
- busca ativa;
- descoberta passiva;
- permanência em local;
- consumo individual;
- consumo coletivo;
- interação;
- compartilhamento;
- resposta imediata;
- compra por impulso;
- comparação antes da compra.

Esses campos não afirmam que o inventário “possui comportamentos”. Eles descrevem comportamentos de contato ou consumo que o ambiente pode atender.

### 6.3 Funções de jornada

O inventário pode ser relacionado a:

- descoberta;
- reconhecimento;
- consideração;
- comparação;
- intenção;
- conversão;
- fidelização;
- recomendação.

Também pode desempenhar funções como:

- gerar notoriedade;
- explicar;
- demonstrar;
- lembrar;
- direcionar;
- converter;
- reforçar;
- acompanhar;
- retargetear.

### 6.4 Segmentações disponíveis

Devem ser registradas as capacidades reais de segmentação, como:

- geográfica;
- demográfica;
- contextual;
- comportamental;
- por interesse;
- por dispositivo;
- por horário;
- por audiência proprietária;
- por lista ou CRM;
- por retargeting.

Segmentação disponível não deve ser confundida com audiência efetivamente medida.

### 6.5 Público editorial pretendido

Pode ser registrado quando declarado pelo veículo ou publisher.

Deve ser distinguido de audiência observada:

```text
Público editorial pretendido
≠
Audiência efetivamente medida
```

---

## 7. Camada territorial

A Biblioteca deve registrar onde o meio, programa, rede, circuito, plataforma, disponibilização ou inventário está disponível ou possui cobertura.

Tipos de representação:

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

Campos recomendados:

- território;
- tipo de cobertura;
- cobertura total ou parcial;
- latitude e longitude;
- raio;
- geometria;
- código oficial;
- fonte cartográfica;
- data de atualização;
- grau de confiança.

A comparação territorial ocorre na Arquitetura de Mídia:

```text
Território do público
∩
Cobertura da alternativa de mídia
```

O resultado pode indicar:

- compatibilidade total;
- compatibilidade parcial;
- ausência de cobertura;
- necessidade de validação;
- percentual estimado de sobreposição geográfica.

---

## 8. Dimensões compartilhadas

A Biblioteca de Inventários deve usar os mesmos catálogos controlados da Biblioteca de Públicos e Segmentos para:

- interesses;
- comportamentos;
- contextos de contato;
- etapas da jornada;
- pontos de contato;
- funções;
- territórios;
- temas editoriais.

Não devem existir listas incompatíveis e redundantes em cada biblioteca.

Exemplo lógico:

```text
interesses
    ↕
inventarios_interesses

comportamentos
    ↕
inventarios_contextos_comportamentais

etapas_jornada
    ↕
inventarios_etapas_jornada

territorios
    ↕
coberturas_inventarios
```

Cada relação deve registrar intensidade, tipo de associação, fonte, validade e confiança.

---

## 9. Audiência, cobertura, alcance e afinidade

### 9.1 Audiência

Audiência é uma medida observada ou estimada de pessoas expostas a um veículo, programa, ambiente ou inventário em determinado período e praça.

Não é atributo permanente do público.

### 9.2 Cobertura

Cobertura pode representar:

- alcance técnico de sinal ou distribuição;
- área territorial atendida;
- população potencialmente alcançável;
- disponibilidade comercial em determinada praça.

Deve registrar sua natureza, fonte e metodologia.

### 9.3 Alcance e frequência

Alcance e frequência são resultados de veiculação, cenário ou plano. Não devem ser armazenados como atributos permanentes do público ou do inventário de referência.

Podem existir benchmarks e capacidades estimadas, desde que identificados como tais.

### 9.4 Afinidade observada

Afinidade observada é uma relação medida entre público e veículo, programa ou inventário.

Deve registrar:

- público ou segmento;
- entidade de mídia;
- praça;
- período;
- universo de comparação;
- índice ou percentual;
- fonte;
- metodologia;
- confiança.

Ela não deve ser tratada como atributo isolado do inventário.

### 9.5 Aderência estimada

Aderência estimada é calculada pela Arquitetura de Mídia a partir da comparação entre características do público, propriedades da alternativa e condições da campanha.

---

## 10. Qualificação público–inventário

A Biblioteca fornece dados para que a Arquitetura de Mídia avalie:

- aderência editorial ou temática;
- aderência comportamental;
- aderência à jornada;
- compatibilidade demográfica;
- compatibilidade territorial;
- adequação contextual;
- afinidade observada;
- confiança das evidências.

Essa qualificação é apenas uma das dimensões do cálculo de adequação.

Também permanecem relevantes:

- objetivos;
- KPIs;
- orçamento;
- custos;
- disponibilidade;
- complementaridade;
- overlap;
- saturação;
- restrições;
- mensurabilidade.

---

## 11. Escopos

Os inventários e suas relações podem possuir escopo:

- global;
- espaço de trabalho;
- projeto;
- pessoal ou rascunho.

Inventários locais, ofertas comerciais privadas e informações proprietárias devem respeitar o escopo e as permissões correspondentes.

---

## 12. Versionamento e snapshot

Toda instância utilizada em planejamento deve preservar:

- versão do inventário de referência;
- versão da disponibilização;
- versão da oferta comercial;
- atributos editoriais e contextuais usados;
- cobertura territorial usada;
- fontes e datas;
- ajustes locais;
- autoria;
- data de seleção.

Alterações futuras na biblioteca não devem modificar retroativamente planos anteriores.

---

## 13. Modelo lógico mínimo

Entidades principais:

```text
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
coberturas_inventario
inventarios_temas
inventarios_contextos_comportamentais
inventarios_etapas_jornada
inventarios_segmentacoes
medicoes_audiencia
afinidades_observadas
```

As tabelas relacionais devem preservar contexto, fonte, validade e confiança.

---

## 14. Princípio consolidado

> A Biblioteca de Inventários descreve tanto a estrutura operacional da oportunidade de mídia quanto, quando aplicável, suas propriedades editoriais, contextuais, funcionais e territoriais. Essas informações não definem sozinhas a adequação do inventário. Elas são comparadas com os públicos e com o Perfil Estratégico pela Arquitetura de Mídia.
