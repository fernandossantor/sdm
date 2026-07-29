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

O princípio central é:

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

A Biblioteca de Inventários integra o Sistema de Bibliotecas do MediAd Planner.

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

Ela não é apenas uma tela de cadastro nem uma tabela de preços. É uma camada de conhecimento entre os catálogos e os motores de planejamento.

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

É o conjunto de vocabulários controlados usados para classificar os inventários:

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

É a combinação validada dos oito primeiros níveis da cadeia:

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

Exemplo:

```text
Tecnologia: Digital
Canal: Digital
Ambiente: Social
Estrutura: Direta
Formato: Feed
Modelo comercial: Mídia avulsa
Modalidade de compra: CPM
Unidade de compra: Mil impressões
```

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

### 4.4 Disponibilização do inventário

É o vínculo entre um inventário de referência e um meio concreto.

Responde:

> Este meio disponibiliza este inventário?

Exemplo:

```text
Inventário de referência: Feed — Social — CPM
Meio: Instagram
Nome comercial: Instagram Feed Ads
```

Um mesmo inventário de referência pode ser disponibilizado por vários meios.

### 4.5 Oferta comercial

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

### 4.6 KPI e métrica

KPI é o indicador utilizado para avaliar entrega, custo, qualidade ou resultado.

Métrica é a medida operacional ou calculada relacionada ao inventário, à oferta ou ao planejamento.

O KPI deve ser associado ao inventário completo, e não apenas ao meio.

---

## 5. Cadeia taxonômica

### 5.1 Tecnologia

Base técnica predominante que permite a produção, distribuição, exibição ou comercialização do inventário.

Exemplos:

- impressa;
- eletrônica;
- digital;
- programática.

Responsabilidade:

- delimitar os canais compatíveis.

Relação recomendada:

```text
Tecnologia ↔ Canal
```

Cardinalidade: N:N.

Um canal pode ser compatível com mais de uma tecnologia.

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

Responsabilidade:

- delimitar os ambientes compatíveis.

Relação recomendada:

```text
Canal ↔ Ambiente
```

Cardinalidade: N:N.

Pode existir um canal principal para navegação ou relatório, sem impedir vínculos secundários.

### 5.3 Ambiente

Contexto específico de circulação, exposição, reprodução ou interação no qual o inventário está disponível.

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

Responsabilidades:

- delimitar estruturas possíveis;
- delimitar formatos possíveis.

Relações:

```text
Ambiente ↔ Estrutura
Ambiente ↔ Formato
```

Cardinalidade: N:N.

### 5.4 Estrutura

Forma organizacional, editorial ou transacional pela qual o inventário é disponibilizado.

Valores atuais:

- Afiliada;
- Conteúdo;
- Direta;
- Patrocínio;
- Programática PG;
- Programática PMP;
- Programática Preferred;
- Programática RTB.

Famílias conceituais:

```text
Distribuição
├── Direta
└── Afiliada

Integração editorial
├── Conteúdo
└── Patrocínio

Acesso programático
├── PG
├── PMP
├── Preferred
└── RTB
```

Responsabilidade:

- restringir os formatos possíveis no ambiente selecionado.

Relação:

```text
Estrutura ↔ Formato
```

Cardinalidade: N:N.

A lista final de formatos deve ser obtida pela interseção:

```text
formatos compatíveis com o ambiente
∩
formatos compatíveis com a estrutura
```

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

O catálogo pode reunir formatos definidos por:

- duração;
- dimensão;
- posição;
- interface;
- configuração criativa;
- tipo de peça;
- tipo de ação;
- modelo de entrega.

Responsabilidade:

- restringir os modelos comerciais possíveis.

Relação:

```text
Formato ↔ Modelo comercial
```

Cardinalidade: N:N.

### 5.6 Modelo comercial

Natureza geral do produto, arranjo ou propriedade comercial oferecida.

Responde:

> O que está sendo comercializado?

Exemplos:

- Mídia avulsa;
- Comercial simples;
- Comercial duplo;
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

Responsabilidade:

- restringir as modalidades de compra possíveis.

Relação:

```text
Modelo comercial ↔ Modalidade de compra
```

Cardinalidade: N:N.

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

Famílias recomendadas:

```text
Por entrega ou resultado
├── CPM
├── CPC
├── CPA
├── CPV
└── CPP

Temporal
├── Diária
├── Semanal
├── Quinzenal
└── Mensal

Espacial ou estrutural
└── Circuito

Propriedade ou integração
├── Cota
├── Patrocínio
├── Exclusividade
└── Projeto especial

Negocial
├── Pacote
├── Tabela
└── Negociação
```

Responsabilidade:

- determinar as unidades de compra possíveis.

Relação:

```text
Modalidade de compra ↔ Unidade de compra
```

Cardinalidade: N:N.

### 5.8 Unidade de compra

Unidade na qual a quantidade contratada é expressa.

Exemplos:

- Mil impressões;
- Impressão;
- Clique;
- Ação;
- Lead;
- View;
- Inserção;
- Página;
- Exemplar;
- Face;
- Ponto;
- Programa;
- Sessão;
- Dia;
- Semana;
- Mês;
- Loja;
- Pessoa alcançada;
- Ponto de audiência.

A unidade completa a definição abstrata do inventário, mas não contém a quantidade.

Exemplo:

```text
Formato: Spot 30
Modalidade: Avulsa
Unidade: Inserção
Quantidade no planejamento: 20
```

---

## 6. Relações de compatibilidade

Devem existir relações explícitas entre níveis consecutivos e complementares.

Tabelas associativas recomendadas:

```text
tecnologias_canais
canais_ambientes
ambientes_estruturas
ambientes_formatos
estruturas_formatos
formatos_modelos_comerciais
modelos_comerciais_modalidades
modalidades_unidades_compra
```

A cadeia não deve apresentar opções incompatíveis apenas porque o item existe no catálogo.

### 6.1 Regra de interseção

Quando uma seleção depende de mais de uma relação, o sistema deve usar interseção.

Exemplo:

```text
Formatos disponíveis
=
formatos vinculados ao ambiente
∩
formatos vinculados à estrutura
```

### 6.2 Exceção controlada

Usuários autorizados podem cadastrar combinações ainda não previstas.

A exceção deve exigir:

- justificativa;
- identificação do responsável;
- registro de data;
- estado editorial;
- auditoria;
- possibilidade de revisão posterior.

### 6.3 Novo item de catálogo

Quando um novo item for criado durante o fluxo, o sistema deve solicitar suas relações mínimas.

Exemplos:

```text
Novo canal
→ selecionar tecnologias compatíveis

Novo ambiente
→ selecionar canais compatíveis

Nova estrutura
→ selecionar ambientes compatíveis

Novo formato
→ selecionar ambientes e estruturas compatíveis
```

---

## 7. Inventário de referência

### 7.1 Definição

O inventário de referência é a combinação validada dos oito níveis taxonômicos.

Ele representa uma classe reutilizável de oportunidade de mídia.

### 7.2 Campos recomendados

- `id`;
- `nome`;
- `descricao`;
- `tecnologia_id` ou relações derivadas;
- `canal_id` ou relações derivadas;
- `ambiente_id`;
- `estrutura_id`;
- `formato_id`;
- `modelo_comercial_id`;
- `modalidade_compra_id`;
- `unidade_compra_id`;
- `escopo`;
- `espaco_id`;
- `projeto_id`, quando aplicável;
- `origem_id`;
- `versao`;
- `estado_editorial`;
- `estado_operacional`;
- `ativo`;
- `criado_por`;
- `criado_em`;
- `atualizado_por`;
- `atualizado_em`.

### 7.3 Identidade

A identidade do inventário deve ser determinada pela combinação taxonômica e por eventuais atributos estruturais indispensáveis.

Não devem integrar sua identidade permanente:

- preço;
- desconto;
- fee;
- vigência;
- praça;
- fornecedor;
- disponibilidade;
- capacidade;
- quantidade contratada;
- investimento mínimo.

### 7.4 Nome sugerido

O sistema pode sugerir:

```text
[Formato] — [Ambiente] — [Modalidade]
```

Exemplos:

- Feed — Social — CPM;
- Spot 30 — FM — Avulsa;
- Vídeo 15 — DOOH — Diária;
- Página inteira — Revista — Avulsa.

O nome sugerido pode ser editado.

### 7.5 Duplicidade

Antes de salvar, o sistema deve verificar se já existe inventário com a mesma combinação taxonômica no mesmo escopo.

O usuário poderá:

- reutilizar o existente;
- criar derivação;
- justificar uma exceção;
- cancelar o cadastro.

---

## 8. Meios, plataformas e empresas

### 8.1 Definição

O meio é a entidade concreta que disponibiliza o inventário.

Na interface, a denominação recomendada é:

> Meio, plataforma ou empresa

O nome técnico existente `plataformas` pode ser preservado durante a transição, desde que sua definição seja ampliada.

### 8.2 Campos recomendados

- `id`;
- `nome`;
- `tipo`;
- `empresa`;
- `grupo_economico`;
- `descricao`;
- `site`;
- `pais`;
- `escopo`;
- `espaco_id`;
- `estado_editorial`;
- `ativo`;
- `criado_por`;
- `criado_em`;
- `atualizado_em`.

### 8.3 Tipos recomendados

- plataforma;
- veículo;
- emissora;
- publicação;
- rede;
- publisher;
- exibidora;
- empresa OOH;
- marketplace;
- varejista;
- operador;
- representante;
- grupo de mídia;
- outro.

---

## 9. Disponibilização do inventário

### 9.1 Entidade

Nome recomendado:

```text
disponibilizacoes_inventario
```

### 9.2 Responsabilidade

Registrar que um meio oferece determinado inventário de referência.

### 9.3 Campos recomendados

- `id`;
- `inventario_referencia_id`;
- `meio_id`;
- `nome_comercial`;
- `codigo_externo`;
- `descricao`;
- `url_documentacao`;
- `escopo`;
- `espaco_id`;
- `estado_editorial`;
- `estado_operacional`;
- `ativo`;
- `criado_por`;
- `criado_em`;
- `atualizado_em`.

### 9.4 Exemplo

```text
Inventário de referência:
Feed — Social — CPM

Meio:
Instagram

Disponibilização:
Instagram Feed Ads
```

---

## 10. Oferta comercial

### 10.1 Definição

Oferta comercial é o conjunto de condições sob as quais uma disponibilização pode ser contratada.

### 10.2 Campos recomendados

- `id`;
- `disponibilizacao_id`;
- `nome`;
- `moeda`;
- `valor_bruto_unitario`;
- `desconto_percentual`;
- `valor_liquido_unitario`;
- `quantidade_minima`;
- `investimento_minimo`;
- `capacidade_maxima`;
- `vigencia_inicio`;
- `vigencia_fim`;
- `modelo_negociacao`;
- `praca_id`;
- `abrangencia_geografica`;
- `segmentacao_disponivel`;
- `fonte`;
- `observacoes`;
- `estado_editorial`;
- `estado_operacional`;
- `ativo`;
- `criado_por`;
- `criado_em`;
- `atualizado_em`.

### 10.3 Fees

A oferta pode registrar:

- fee de tecnologia percentual;
- fee de tecnologia fixo;
- fee de dados percentual;
- fee de dados fixo;
- fee de verificação percentual;
- fee de verificação fixo;
- fee de operação percentual;
- fee de operação fixo;
- outros fees identificados.

A comissão de agência deve permanecer separada dos fees tecnológicos e operacionais.

### 10.4 Modelos de negociação

- Direto;
- Open auction;
- PMP;
- Preferred deal;
- Garantido;
- Tabela;
- Negociação;
- Contrato;
- Permuta;
- Bonificação.

### 10.5 Cálculos

Os valores calculados devem preservar memória de cálculo.

```text
Valor líquido unitário
=
valor bruto unitário
− desconto
+ fees aplicáveis
```

A interface deve indicar claramente quais componentes estão incluídos ou excluídos.

---

## 11. KPIs, métricas e medições

### 11.1 Relações

```text
Inventário de referência ↔ KPI
Disponibilização ↔ KPI
Oferta ↔ Medição
```

### 11.2 KPI principal

Cada inventário pode possuir:

- um KPI principal;
- vários KPIs secundários;
- métricas de diagnóstico;
- métricas de custo;
- métricas de entrega;
- métricas de resultado;
- métricas de qualidade;
- métricas de marca.

### 11.3 Associação conceitual

A relação inventário–KPI indica quais indicadores são aplicáveis àquele tipo de inventário.

### 11.4 Associação contextual

A disponibilização pode restringir ou ampliar KPIs conforme as capacidades de medição do meio.

### 11.5 Medições

Cada medição deve registrar, quando aplicável:

- inventário;
- disponibilização;
- oferta;
- período;
- praça;
- fonte;
- valor;
- unidade métrica;
- metodologia;
- nível de confiança;
- data da coleta;
- responsável;
- observações.

---

## 12. Escopos

A Biblioteca de Inventários adota os escopos definidos no Sistema de Bibliotecas.

### 12.1 Global

Disponível aos espaços autorizados.

Pode conter:

- inventários de referência padronizados;
- meios amplamente conhecidos;
- compatibilidades validadas;
- KPIs consolidados;
- ofertas públicas ou referenciais.

### 12.2 Espaço de trabalho

Disponível somente aos membros do espaço.

Pode conter:

- veículos locais;
- tabelas comerciais privadas;
- fornecedores específicos;
- preços negociados;
- formatos proprietários;
- inventários internos.

### 12.3 Projeto

Disponível somente no projeto.

Adequado para:

- inventário pontual;
- oferta excepcional;
- condição temporária;
- veículo utilizado apenas naquela campanha.

### 12.4 Pessoal ou rascunho

Área de preparação ainda não compartilhada.

Itens pessoais não participam dos motores compartilhados até serem promovidos.

---

## 13. Estados

Estado editorial e estado operacional devem ser separados.

### 13.1 Estado editorial

- Rascunho;
- Em revisão;
- Validado;
- Rejeitado;
- Arquivado.

### 13.2 Estado operacional do inventário

- Ativo;
- Inativo;
- Obsoleto.

### 13.3 Estado operacional da disponibilização

- Ativa;
- Suspensa;
- Encerrada.

### 13.4 Estado operacional da oferta

- Futura;
- Vigente;
- Expirada;
- Suspensa;
- Arquivada.

---

## 14. Versionamento

### 14.1 Objetos versionáveis

- inventário de referência;
- disponibilização;
- oferta;
- relações com KPIs;
- preços;
- vigências;
- compatibilidades taxonômicas.

### 14.2 Alterações que exigem nova versão

- mudança de combinação taxonômica;
- mudança de modalidade;
- mudança de unidade;
- mudança de meio;
- mudança relevante de preço;
- mudança de vigência;
- mudança de fees;
- mudança de mínimo comercial;
- mudança de capacidade;
- mudança de KPI principal;
- mudança de regra de mensuração.

### 14.3 Correções simples

Erros ortográficos e ajustes descritivos podem atualizar a mesma versão quando não alterarem o significado operacional.

### 14.4 Campos recomendados

- `versao`;
- `versao_anterior_id`;
- `motivo_alteracao`;
- `alterado_por`;
- `alterado_em`;
- `vigente_desde`;
- `vigente_ate`;
- `status_versao`.

---

## 15. Fluxo de criação

### 15.1 Escolher origem

O usuário pode:

- selecionar inventário existente;
- duplicar inventário;
- derivar inventário;
- criar do zero;
- importar inventário.

### 15.2 Compor a taxonomia

```text
Tecnologia
→ Canal compatível
→ Ambiente compatível
→ Estrutura compatível
→ Formato compatível
→ Modelo comercial compatível
→ Modalidade compatível
→ Unidade compatível
```

### 15.3 Validar a combinação

O sistema deve verificar:

- compatibilidade;
- duplicidade;
- ausência de relacionamento;
- combinação incomum;
- campos obrigatórios.

### 15.4 Criar ou selecionar o meio

O usuário seleciona:

- meio existente;
- novo meio do espaço;
- novo meio global, se autorizado.

### 15.5 Criar disponibilização

O usuário informa:

- nome comercial;
- código externo;
- descrição;
- documentação;
- estado operacional.

### 15.6 Cadastrar oferta

O usuário informa:

- preço;
- moeda;
- vigência;
- desconto;
- fees;
- mínimos;
- capacidade;
- praça;
- modelo de negociação.

### 15.7 Associar KPIs

O sistema sugere KPIs compatíveis.

O usuário define:

- KPI principal;
- KPIs secundários;
- métricas obrigatórias;
- fontes de medição.

### 15.8 Publicar

O objeto pode ser salvo como:

- rascunho pessoal;
- item do projeto;
- item do espaço;
- item global, se autorizado;
- submissão para revisão.

---

## 16. Busca e navegação

### 16.1 Filtros

- tecnologia;
- canal;
- ambiente;
- estrutura;
- formato;
- modelo comercial;
- modalidade;
- unidade;
- meio;
- KPI;
- praça;
- faixa de preço;
- vigência;
- escopo;
- estado;
- autor;
- espaço de trabalho.

### 16.2 Busca textual

Pesquisar em:

- nome;
- descrição;
- meio;
- empresa;
- código;
- formato;
- ambiente;
- observações;
- tags.

### 16.3 Visualizações

- Lista;
- Tabela;
- Cards;
- Árvore de composição;
- Comparação;
- Histórico de versões.

---

## 17. Card do inventário

Cada card deve apresentar:

```text
Nome do inventário

Tecnologia > Canal > Ambiente
Estrutura > Formato
Modelo > Modalidade > Unidade

Meio
Preço vigente
Praça
KPI principal
Escopo
Estado
Última atualização
```

Ações possíveis:

- usar no planejamento;
- visualizar;
- editar;
- duplicar;
- derivar;
- comparar;
- arquivar;
- promover;
- revisar histórico.

---

## 18. Uso no planejamento

Ao inserir um inventário em um planejamento, o sistema deve criar uma instância vinculada à versão utilizada.

A instância deve preservar:

- `inventario_id`;
- `inventario_versao_id`;
- `disponibilizacao_id`;
- `oferta_id`;
- snapshot do preço;
- snapshot das condições;
- quantidade;
- investimento;
- praça;
- período;
- papel estratégico;
- KPIs selecionados.

Alterações posteriores na Biblioteca não devem modificar silenciosamente planejamentos já salvos.

O sistema pode informar:

> Existe uma versão mais recente deste inventário. Deseja atualizar a instância do planejamento?

A atualização deve ser explícita e auditável.

---

## 19. Duplicação e derivação

### 19.1 Duplicação

Cria uma cópia independente, sem relação operacional obrigatória com a origem.

### 19.2 Derivação

Cria um novo objeto vinculado ao original.

A derivação deve preservar:

- item de origem;
- data;
- autor;
- diferenças;
- possibilidade de comparação;
- histórico de promoção.

Exemplo:

```text
Inventário global:
Spot 30 — FM — Inserção

Derivação do espaço:
Spot 30 — Rádio local X — pacote regional
```

---

## 20. Promoção

### 20.1 Fluxo

```text
Pessoal ou projeto
→ Espaço de trabalho
→ Submetido
→ Em revisão
→ Aprovado
→ Global
```

### 20.2 Critérios

- descrição suficiente;
- taxonomia válida;
- ausência de duplicidade;
- nomenclatura adequada;
- fonte identificada;
- compatibilidades verificadas;
- ausência de dados confidenciais;
- relevância para reutilização.

### 20.3 Separação entre estrutura e preço

A promoção de um inventário não implica a promoção de ofertas privadas.

Podem ser promovidos:

- inventário de referência;
- meio;
- compatibilidades;
- KPIs.

Sem promover automaticamente:

- preços negociados;
- descontos;
- fees;
- contratos;
- mínimos privados;
- condições confidenciais.

---

## 21. Auditoria

Devem ser registrados:

- criação;
- edição;
- duplicação;
- derivação;
- promoção;
- aprovação;
- rejeição;
- arquivamento;
- alteração de preço;
- alteração de vigência;
- alteração de compatibilidade;
- uso em planejamento;
- mudança de escopo;
- mudança de estado.

Campos mínimos:

- usuário;
- espaço;
- projeto, quando aplicável;
- data;
- ação;
- objeto;
- versão;
- valores anteriores;
- valores posteriores;
- justificativa.

---

## 22. Modelo lógico resumido

### 22.1 Catálogos e compatibilidades

```text
tecnologias
    ↕
tecnologias_canais
    ↕
canais
    ↕
canais_ambientes
    ↕
ambientes
    ↕
ambientes_estruturas
    ↕
estruturas
    ↕
estruturas_formatos
    ↕
formatos
    ↕
formatos_modelos_comerciais
    ↕
modelos_comerciais
    ↕
modelos_comerciais_modalidades
    ↕
modalidades_compra
    ↕
modalidades_unidades_compra
    ↕
unidades_compra
```

### 22.2 Inventário

```text
combinação taxonômica validada
        ↓
inventarios_referencia
```

### 22.3 Disponibilização

```text
inventarios_referencia
        ↓
disponibilizacoes_inventario
        ↑
meios
```

### 22.4 Oferta

```text
disponibilizacoes_inventario
        ↓
ofertas_inventario
        ↓
preços, vigências, fees, mínimos e capacidades
```

### 22.5 Mensuração

```text
inventarios_referencia
        ↔
inventarios_kpis
        ↔
kpis
```

```text
ofertas_inventario
        ↓
medicoes_inventario
```

---

## 23. Regras consolidadas

1. As dez tabelas do catálogo são preservadas.
2. A ordem hierárquica atual é preservada na interface.
3. A hierarquia representa composição assistida, não filiação ontológica exclusiva.
4. Relações N:N devem substituir vínculos exclusivos quando houver hibridismo real.
5. Ambiente e Estrutura devem restringir conjuntamente os formatos.
6. Modelo comercial responde o que é vendido.
7. Modalidade de compra responde como é contratado ou precificado.
8. Unidade de compra responde em que unidade a quantidade é expressa.
9. A quantidade pertence à oferta ou ao planejamento, não à unidade.
10. O inventário de referência é separado do meio que o disponibiliza.
11. A disponibilização é separada da oferta comercial.
12. Preço, desconto, fee, vigência, praça, mínimo e capacidade pertencem à oferta.
13. KPI deve ser associado ao inventário completo, não apenas ao meio.
14. Planejamentos preservam snapshots e versões utilizadas.
15. Promoção de inventário não publica automaticamente condições comerciais privadas.
16. Exceções são permitidas somente com justificativa e auditoria.
17. Novos itens de catálogo devem nascer com relações mínimas de compatibilidade.
18. Nenhuma alteração da Biblioteca deve modificar silenciosamente um planejamento salvo.

---

## 24. Decisão arquitetural consolidada

A Biblioteca de Inventários será estruturada em quatro camadas:

```text
1. Catálogos e compatibilidades
2. Inventários de referência
3. Disponibilizações por meios
4. Ofertas comerciais e mensuração
```

A ordem operacional permanecerá:

```text
Tecnologia
→ Canal
→ Ambiente
→ Estrutura
→ Formato
→ Modelo comercial
→ Modalidade de compra
→ Unidade de compra
→ Meio / Plataforma / Empresa
→ KPI
```

Internamente, porém, o sistema distinguirá:

```text
Os oito primeiros níveis definem o tipo de inventário.
O meio o disponibiliza.
A oferta estabelece as condições comerciais.
Os KPIs e métricas permitem sua mensuração.
O planejamento instancia e preserva a versão utilizada.
```

Essa é a configuração consolidada da Biblioteca de Inventários do MediAd Planner.
