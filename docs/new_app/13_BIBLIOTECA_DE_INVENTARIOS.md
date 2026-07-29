# Biblioteca de Inventários do MediAd Planner

**Documento:** `13_BIBLIOTECA_DE_INVENTARIOS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Inventários organiza, preserva e disponibiliza oportunidades reutilizáveis de veiculação, exposição, presença ou entrega publicitária.

Ela recebe os pontos de contato definidos pela Biblioteca 16 e os desdobra em estruturas operacionais e comerciais concretas, sem redefinir jornadas, necessidades ou funções.

```text
Ponto de contato
    ↓
Meio e tipologia
    ↓
Ambiente, veículo e propriedade
    ↓
Inventário
    ↓
Formatos compatíveis
    ↓
Disponibilização
    ↓
Modalidade de comercialização
    ↓
Oferta comercial
```

---

## 2. Definição normativa de inventário

> Inventário de mídia é a capacidade identificável e disponibilizável de veiculação ou exposição publicitária em determinado ambiente, propriedade, veículo, posição, período e condição técnica.

Inventário não é:

- audiência;
- preço;
- formato criativo;
- campanha;
- pacote;
- cota;
- patrocínio;
- projeto especial;
- estimativa de impactos.

Esses elementos podem qualificar, utilizar, agrupar, comercializar ou medir o inventário, mas não o substituem conceitualmente.

---

## 3. Posição na arquitetura

```text
Biblioteca 16
Jornadas, necessidades, funções e pontos de contato
    ↓
Biblioteca 13
Meios, ambientes, inventários, formatos e comercialização
    ↓
Arquitetura de Mídia
    ↓
Plano Consolidado
    ↓
Mapa de Veiculação
```

O ponto de contato descreve a situação de relação entre público e mensagem. O meio descreve uma categoria técnica e comunicacional. O inventário descreve a capacidade concreta de inserção ou exposição.

---

## 4. Separações obrigatórias

```text
Ponto de contato ≠ meio
Meio ≠ veículo
Veículo ≠ proprietário
Veículo ≠ propriedade
Propriedade ≠ ambiente
Ambiente ≠ inventário
Inventário ≠ formato
Formato ≠ especificação técnica
Inventário ≠ produto comercial
Produto comercial ≠ modalidade de compra
Unidade de compra ≠ unidade de mensuração
Audiência ≠ inventário
Cobertura territorial ≠ alcance
Fluxo ≠ audiência
Impacto declarado ≠ impacto tecnicamente validado
```

---

## 5. Camadas fundamentais

### 5.1 Proprietário ou grupo

Entidade econômica ou institucional que controla uma ou mais empresas, marcas, veículos ou plataformas.

### 5.2 Veículo ou plataforma

Entidade concreta que publica, transmite, distribui, exibe ou opera conteúdo e publicidade.

### 5.3 Propriedade

Contexto editorial, programático, espacial ou experiencial reconhecível, como programa, editoria, podcast, evento, campeonato, sessão, estação ou circuito.

### 5.4 Ambiente

Local ou situação técnica de exposição, como intervalo, feed, página de matéria, sala de cinema, foyer, vagão, estação, shopping, rua, edifício ou ponto de venda.

### 5.5 Inventário

Capacidade disponibilizável dentro de uma propriedade e ambiente.

### 5.6 Formato publicitário

Configuração expressiva ou material da mensagem que pode ocupar inventário compatível.

### 5.7 Especificação técnica

Requisitos de dimensão, duração, proporção, peso, arquivo, resolução, áudio, comportamento ou produção.

### 5.8 Disponibilização

Vínculo entre inventário de referência e entidade concreta que o oferece em determinado território, período e condição.

### 5.9 Produto comercial

Configuração padronizada de inventário, formato, quantidade, período e condições de entrega.

### 5.10 Oferta comercial

Aplicação de preço, validade, mínimos, descontos, fees, bonificações, disponibilidade, faturamento e regras de negociação a uma disponibilização ou produto comercial.

---

## 6. Hierarquia recomendada

```text
GRUPO_OU_PROPRIETARIO
    ↓
VEICULO_OU_PLATAFORMA
    ↓
PROPRIEDADE
    ↓
AMBIENTE
    ↓
INVENTARIO
    ↓
FORMATOS_COMPATIVEIS
    ↓
DISPONIBILIZACAO
    ↓
PRODUTO_COMERCIAL
    ↓
OFERTA_COMERCIAL
```

A hierarquia deve ser relacional, não uma cadeia rígida. Um inventário pode pertencer a circuitos, redes, pacotes e agregações diferentes.

---

## 7. Agregação e composição de inventários

A Biblioteca deve permitir relações entre inventários:

```text
CONTEM
PERTENCE_A
AGRUPA
DISTRIBUI_EM
SUBSTITUI
COMPARTILHA_CAPACIDADE_COM
INCOMPATIVEL_COM
```

Exemplos:

- rede de emissoras contendo emissoras locais;
- circuito de DOOH contendo telas ou faces;
- complexo de cinema contendo salas;
- pacote regional contendo praças;
- ROS contendo páginas elegíveis;
- propriedade multiplataforma contendo entregas de TV, digital, áudio e evento.

Um circuito ou pacote não deve apagar os inventários que o compõem.

---

## 8. Formato, especificação e experiência

A Biblioteca deve separar:

```text
FORMATO_PUBLICITARIO
ESPECIFICACAO_TECNICA
COMPORTAMENTO_DO_FORMATO
EXPERIENCIA_PUBLICITARIA
```

Exemplo:

```text
Formato: vídeo
Especificação: vertical 9:16, até 15 segundos
Comportamento: autoplay, sem áudio inicial, pulável
Experiência: in-stream, out-stream ou interstitial
```

O inventário deve declarar formatos aceitos, especificações, comportamentos permitidos e restrições. Não se deve criar um novo inventário para cada combinação técnica possível.

---

## 9. Unidades de comercialização

As unidades devem ser extensíveis e classificadas por natureza.

```text
ESPACO
TEMPO
ENTREGA
PERIODO
COBERTURA
COMPOSTA
```

Exemplos:

- segundo;
- inserção;
- centímetro-coluna;
- página ou fração;
- linha;
- lâmina de encarte;
- face;
- tela;
- sala;
- sessão;
- diária;
- semana;
- mês;
- CPM;
- pacote;
- circuito;
- cota;
- patrocínio;
- projeto.

A unidade de comercialização não deve ser confundida com unidade de entrega ou mensuração.

---

## 10. Compra, entrega e mensuração

Cada disponibilização ou oferta deve preservar, quando aplicável:

```text
unidade_de_compra
unidade_de_entrega
unidade_de_mensuracao
```

Exemplo:

```text
Compra: patrocínio mensal
Entrega: vinhetas + inserções + presença editorial
Mensuração: audiência, impactos, reproduções e retenção
```

O custo somente pode ser comparado corretamente quando a base de compra estiver declarada.

---

## 11. Produtos compostos, cotas e projetos

Produtos compostos podem reunir inventários e entregas heterogêneas.

```text
produto_composto
    entregas[]
    inventarios[]
    direitos[]
    restricoes[]
    exclusividades[]
    servicos[]
    metricas_por_entrega[]
    periodo
    valor_total
```

Categorias internas possíveis:

```text
PRODUTO_PADRONIZADO
PACOTE
CIRCUITO
COTA
PATROCINIO
PROJETO_ESPECIAL
```

Essas categorias descrevem a comercialização. Não substituem a natureza do inventário.

Entregas compostas devem poder ser classificadas como:

```text
ENTREGA_DE_MIDIA
ENTREGA_DE_CONTEUDO
SERVICO_DE_PRODUCAO
DIREITO_DE_ASSOCIACAO
ATIVACAO
TECNOLOGIA
DADOS
```

Somente entregas de mídia elegíveis entram automaticamente nos cálculos de pressão.

---

## 12. Segmentação

A Biblioteca 14 define quem é o público. A Biblioteca 13 registra como o inventário permite selecioná-lo.

Campos mínimos:

```text
segmentacao_disponivel
tipo_de_segmentacao
fonte_do_dado
unidade_de_identidade
custo_adicional
restricoes
```

Pessoa, conta, cookie, dispositivo e domicílio não devem ser tratados como unidades idênticas.

---

## 13. Posição, duração e condições técnicas

Posição e duração são atributos operacionais e comerciais reais.

O inventário ou produto pode registrar:

```text
posicao
posicao_determinada
prioridade
break
pagina
secao
pre_roll_mid_roll_post_roll
altura
distancia
sentido
iluminacao
duracao_padrao
fator_de_conversao_por_duracao
regra_para_duracao_nao_padrao
```

Não se deve presumir proporcionalidade linear de preço ou efeito entre durações.

---

## 14. Cobertura e alcance

A Biblioteca deve distinguir:

```text
cobertura_territorial_do_inventario
abrangencia_da_programacao
alcance_de_audiencia
```

Cobertura territorial descreve onde o inventário existe. Abrangência da programação descreve o subconjunto contratado. Alcance descreve unidades distintas atingidas ao menos uma vez.

O termo `cobertura` nunca deve ser usado sem qualificador.

---

## 15. Audiência e período de referência

Toda audiência deve preservar:

```text
unidade
universo
territorio
periodo_de_referencia
janela_de_acumulacao
fonte
metodologia
natureza_do_valor
```

Estados para a natureza do valor:

```text
GARANTIDO
ESTIMADO
PROJETADO
HISTORICO
POTENCIAL
NAO_GARANTIDO
```

Audiência institucional, público histórico e capacidade instalada não equivalem automaticamente à entrega de uma campanha.

---

## 16. Fluxo, OTS e contatos em OOH

A cadeia conceitual deve ser preservada:

```text
FLUXO_BRUTO
    ↓
OPORTUNIDADE_DE_VER_OU_CONTATO
    ↓
PROBABILIDADE_DE_VER_OU_CONTATO
    ↓
CONTATO_AJUSTADO
    ↓
ALCANCE_E_FREQUENCIA_ESTIMADOS
```

Características de visibilidade podem incluir posição, sentido, velocidade, altura, tamanho, inclinação, iluminação, distância, tempo de exposição e ambiente.

Fluxo não deve ser armazenado como sinônimo de audiência ou impactos.

---

## 17. Tipologia de impactos e exposições

Valores comerciais chamados de `impactos` devem ser qualificados.

```text
IMPACTO_CALCULADO_POR_AUDIENCIA
CONTATO_AJUSTADO
OPORTUNIDADE_DE_CONTATO
IMPACTO_DECLARADO_PELO_FORNECEDOR
IMPRESSAO_SERVIDA
IMPRESSAO_VALIDA
IMPRESSAO_VISIVEL
EXPOSICAO_ESTIMADA
```

Cada valor deve preservar:

```text
metrica_original
nome_comercial
metodologia
fonte
periodo
universo
auditabilidade
grau_de_confianca
```

A terminologia do fornecedor deve ser preservada, mas sua equivalência técnica precisa ser validada pela Biblioteca 17.

---

## 18. Afinidade, composição e penetração

Devem permanecer distintas:

```text
composicao_da_audiencia
penetracao_no_target
afinidade
alcance_no_target
```

Afinidade exige comparação com a presença do target no universo de referência. A concentração do perfil no veículo, isoladamente, não constitui índice de afinidade.

---

## 19. Qualidade da exposição

Dimensões como visibilidade, audibilidade, duração, completude, contexto, atenção e interação devem ser registradas separadamente.

```text
dimensao_de_qualidade
metrica
valor
fonte
metodo
confianca
```

Não deve existir multiplicador universal de qualidade ou atenção sem metodologia específica e validada.

---

## 20. Condições comerciais e negociação

A negociação não se reduz a desconto.

```text
preco_de_lista
coeficientes
acrescimos
desconto
bonificacao
entregas_adicionais
custos_adicionais
condicao_de_pagamento
regra_de_cancelamento
substituicao_de_inventario
valor_negociado
```

A oferta deve admitir custos fixos, variáveis, por entrega, por período e por produto composto.

---

## 21. Capacidades analíticas

Cada inventário ou disponibilização pode declarar:

- objetivos e resultados suportados;
- indicadores compatíveis;
- indicadores projetáveis;
- indicadores calculáveis;
- indicadores posteriormente mensuráveis;
- requisitos de dados;
- fontes possíveis;
- limitações;
- grau de confiança.

O inventário não armazena KPI permanente. Um indicador torna-se KPI quando priorizado no planejamento.

---

## 22. Modelo lógico mínimo revisado

```text
proprietarios_midia
veiculos_plataformas
propriedades_midia
ambientes_midia
inventarios_referencia
inventarios_relacoes
formatos_publicitarios
especificacoes_tecnicas
comportamentos_formato
experiencias_publicitarias
inventarios_formatos
disponibilizacoes_inventario
produtos_comerciais
produtos_entregas
produtos_inventarios
modalidades_compra
unidades_comercializacao
ofertas_comerciais
condicoes_negociadas
segmentacoes_disponiveis
coberturas_territoriais
medicoes_audiencia
medicoes_exposicao
qualificadores_exposicao
afinidades_observadas
fontes_metodologias
```

As relações devem preservar contexto, fonte, validade, período, universo e confiança.

---

## 23. Relação com o Mapa de Veiculação

A Biblioteca descreve o que pode ser comprado. O Mapa de Veiculação registra o que foi selecionado, negociado e programado.

```text
Biblioteca 13
    ↓
Inventário + produto + oferta
    ↓
Condição negociada
    ↓
Linha de programação
    ↓
Ocorrências
    ↓
Mapa de Veiculação
```

O Mapa deve preservar os identificadores e versões das entidades utilizadas.

---

## 24. Princípio consolidado

> O ponto de contato descreve a relação; o meio descreve a categoria; o inventário descreve a capacidade disponível; o formato descreve a configuração da mensagem; o produto comercial organiza a venda; a oferta aplica condições; e o Mapa de Veiculação registra a decisão programada. Essas camadas podem se combinar, mas não devem ser confundidas.