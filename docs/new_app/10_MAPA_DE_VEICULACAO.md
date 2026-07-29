# Mapa de Veiculação

**Documento:** `10_MAPA_DE_VEICULACAO.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Especificação funcional e operacional

---

## 1. Finalidade

O **Mapa de Veiculação** é a visão técnica, operacional e detalhada do Plano Consolidado de Mídia.

Ele registra o que foi selecionado, em qual veículo ou plataforma, em qual propriedade e inventário, com qual formato, período, quantidade, unidade comercial, condição negociada, audiência, função estratégica e estado operacional.

Pergunta orientadora:

> O que exatamente será veiculado, quando, onde, em qual inventário e formato, para qual público, com qual finalidade, entrega prevista, custo e condição operacional?

O Mapa deriva da mesma base do Plano e do Cronograma. Não é uma planilha paralela.

```text
Plano Consolidado
    ↓
Inventários e produtos aprovados
    ↓
Condições negociadas
    ↓
Linhas de programação
    ↓
Ocorrências de veiculação
    ↓
Mapa de Veiculação
    ↓
Autorização ou PI
    ↓
Checking e pós-compra
```

---

## 2. Natureza do artefato

O Mapa funciona como:

- grade de programação;
- memória de cálculo;
- controle orçamentário;
- registro técnico;
- base de execução;
- referência para autorização ou pedido de inserção;
- base de checking;
- fonte do Cronograma;
- base para indicadores e conciliação.

O Mapa não substitui contrato, autorização ou PI, mas deve conter dados suficientes para alimentá-los.

---

## 3. Níveis de domínio

### 3.1 Inventário

Capacidade concreta e disponibilizável de veiculação ou exposição em determinado ambiente, propriedade, posição, período e condição técnica.

### 3.2 Produto comercial

Configuração de inventário, formato, quantidade, período e condições de entrega. Pode ser simples ou composto.

### 3.3 Condição negociada

Resultado específico da negociação aplicada à oferta: preço, desconto, bonificação, entregas, pagamento, cancelamento, posição, exclusividade ou substituição.

### 3.4 Linha de programação

Agrupamento de ocorrências homogêneas.

Exemplo:

```text
Rádio X
Programa Y
Faixa 07h–09h
Spot de 30 segundos
Peça A
Praça São Borja
Condição negociada Z
```

### 3.5 Ocorrência

Concretização temporal da linha.

```text
10/08/2026
08h15
1 inserção
programada
```

Uma linha pode possuir várias ocorrências. Uma ocorrência pode representar o início de uma exposição por período, como outdoor, diária digital, encarte ou patrocínio.

---

## 4. Estrutura normalizada

A base interna deve ser vertical e normalizada.

| linha_programacao_id | data_inicio | data_fim | hora_faixa | quantidade | unidade | estado |
|---|---|---|---|---:|---|---|
| TV-JORNAL-A-30 | 05/08/2026 | 05/08/2026 | 19h30 | 1 | inserção | programada |
| OOH-CIRCUITO-B | 05/08/2026 | 18/08/2026 | contínuo | 1 | período | programada |

Grades mensais ou semanais são formas de apresentação, não a estrutura primária.

```text
Base normalizada
    ↓
Mapa mensal
Mapa semanal
Mapa por fase
Mapa por veículo
Mapa por praça
Mapa por fornecedor
Mapa por meio
```

---

## 5. Cabeçalho

Cada Mapa deve registrar:

- plano e versão de origem;
- campanha;
- anunciante;
- produto, serviço ou unidade de negócio;
- período geral;
- moeda;
- responsável;
- data de geração;
- estado;
- filtros aplicados;
- versão do Mapa.

---

## 6. Identificação da linha de programação

Campos estruturais:

```text
linha_programacao_id
meio
tipologia
proprietario_ou_grupo
veiculo_ou_plataforma
propriedade
ambiente
inventario_id
inventario_pai_ou_circuito
produto_comercial_id
fornecedor
praca
territorio
```

Esses campos preservam a separação entre grupo, veículo, propriedade, ambiente, inventário e produto comercial.

---

## 7. Formato e material

Cada linha pode registrar:

```text
formato_publicitario
experiencia_publicitaria
especificacao_tecnica
comportamento_do_formato
peca
material_id
duracao
dimensao
proporcao
cor
audio
posicao
posicao_determinada
```

Formato não deve ser confundido com inventário. A linha deve validar a compatibilidade entre ambos.

---

## 8. Campos estratégicos

Cada linha deve poder vincular:

- objetivo;
- resultado esperado;
- público ou segmento;
- fase da campanha;
- etapa da jornada;
- necessidade;
- função comunicacional;
- ponto de contato;
- papel estratégico do meio;
- praça;
- prioridade.

Esses campos podem ficar ocultos em uma impressão operacional, mas devem permanecer na base.

---

## 9. Compra, entrega e mensuração

A linha deve separar:

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

Campos mínimos:

```text
modalidade_de_compra
unidade_comercial
quantidade_planejada
quantidade_garantida
entrega_prevista
natureza_da_entrega
criterio_de_comprovacao
```

---

## 10. Produtos compostos

Pacotes, circuitos, cotas, patrocínios e projetos especiais devem ser decompostos em entregas.

```text
produto_composto
    ↓
entrega_1: mídia
entrega_2: conteúdo
entrega_3: produção
entrega_4: direito de associação
entrega_5: ativação
```

Cada entrega deve informar:

```text
tipo_de_entrega
inventario_associado
quantidade
unidade
periodo
valor_alocado
metrica_elegivel
```

Somente entregas elegíveis de mídia entram automaticamente nos cálculos de pressão.

---

## 11. Campos da ocorrência

Cada ocorrência deve registrar:

- linha de origem;
- data inicial;
- data final;
- dia da semana;
- hora ou faixa;
- duração da exposição;
- quantidade;
- unidade consumida;
- peça e material;
- responsável;
- estado;
- comprovante;
- observação.

Estados possíveis:

```text
RASCUNHO
RESERVADA
NEGOCIADA
APROVADA
AUTORIZADA
PROGRAMADA
VEICULADA
COMPROVADA
COMPENSADA
CANCELADA
DIVERGENTE
```

---

## 12. Campos financeiros

Cada linha ou entrega deve admitir:

```text
preco_de_tabela
coeficiente_de_formato
coeficiente_de_duracao
acrescimo_de_posicao
outros_acrescimos
preco_ajustado
desconto
bonificacao
entregas_adicionais
preco_negociado
custo_unitario
quantidade
custo_bruto
custo_liquido_do_veiculo
comissao_ou_fee
taxas
impostos
producao
tecnologia
dados
outros_custos
custo_total
base_financeira
```

A negociação não deve ser representada apenas por desconto.

O sistema deve admitir:

- custos fixos;
- custos variáveis;
- custos por entrega;
- custos por período;
- pacotes;
- valor único com alocação entre entregas.

---

## 13. Modelos de remuneração

O Mapa deve registrar, quando aplicável:

```text
DESCONTO_PADRAO
COMISSAO
FEE_DE_MIDIA
FEE_GLOBAL
FTE
HORA_HOMEM
SUCCESS_FEE
SEM_INTERMEDIACAO
OUTRO
```

Valor de mídia, remuneração de agência, produção, tecnologia e dados devem permanecer distinguíveis, ainda que faturados conjuntamente.

---

## 14. Audiências e exposições nativas

O Mapa deve preservar a métrica original de cada meio.

Campos obrigatórios por medição:

```text
metrica_original
valor_original
unidade_original
universo
unidade_de_identidade
territorio
periodo_de_referencia
janela_de_acumulacao
fonte
metodologia
natureza_do_valor
auditabilidade
confianca
```

Natureza do valor:

```text
GARANTIDO
ESTIMADO
PROJETADO
HISTORICO
POTENCIAL
NAO_GARANTIDO
```

Audiência institucional ou público histórico não deve ser apresentado como entrega garantida.

---

## 15. Tipologia de impactos

Valores chamados de `impactos` devem ser qualificados:

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

A terminologia comercial deve ser preservada, mas a equivalência técnica deve ser validada.

---

## 16. OOH e DOOH

O Mapa deve manter separados:

```text
fluxo_bruto
OTS
PTS_ou_probabilidade_de_contato
contato_ajustado
alcance_estimado
frequencia_estimada
```

Campos típicos:

- exibidora;
- circuito;
- face ou tela;
- endereço, rota ou área;
- posição, sentido e altura;
- estático ou digital;
- duração da peça;
- loop;
- inserções por dia;
- número de cotas;
- período;
- auditoria de inventário;
- comprovação de campanha.

Fluxo não deve ser usado como sinônimo de audiência ou impactos.

---

## 17. Audiências equivalentes e pontos de pressão

Ao lado da métrica nativa, o Mapa pode registrar:

```text
camada_de_comparacao
metodo_de_conversao
valor_convertido
qualificador_da_exposicao
estado_de_equivalencia
estado_de_deduplicacao
confianca
ressalvas
```

Estados de equivalência:

```text
EQUIVALENCIA_DIRETA
EQUIVALENCIA_APOS_CONVERSAO
EQUIVALENCIA_CONDICIONADA
NAO_EQUIVALENTE
DADOS_INSUFICIENTES
```

Pontos de pressão não substituem a métrica nativa e não devem ser apresentados como alcance deduplicado, pessoas únicas, atenção ou efeito.

---

## 18. Deduplicação

Estados possíveis:

```text
DEDUPLICADO_POR_IDENTIDADE
DEDUPLICADO_POR_PAINEL
DEDUPLICADO_POR_MODELO
ESTIMADO_POR_PROXY
NAO_DEDUPLICADO
INDETERMINADO
```

Uma programação multiplataforma pode somar custos e entregas compatíveis, mas não pode somar pessoas únicas sem método de deduplicação válido.

---

## 19. Cobertura

O Mapa deve distinguir:

```text
cobertura_territorial_do_inventario
abrangencia_da_programacao
alcance_de_audiencia
```

Exemplo: uma rede pode ter cobertura nacional, enquanto a programação utiliza apenas determinadas praças e produz alcance inferior ao universo dessas praças.

---

## 20. Afinidade e perfil

Devem permanecer distintos:

```text
composicao_da_audiencia
penetracao_no_target
afinidade
alcance_no_target
```

Afinidade somente deve ser calculada quando houver universo de referência compatível.

---

## 21. Totais e consolidações

O Mapa deve calcular:

- total da linha;
- total da entrega;
- total do produto composto;
- total do veículo;
- total do fornecedor;
- total do meio;
- total da praça;
- total do período;
- total do Mapa;
- verba aprovada;
- verba alocada;
- diferença;
- comissão ou fee;
- saldo.

Métricas somente podem ser agregadas quando unidade, universo, período e metodologia forem compatíveis.

---

## 22. Relação com autorização e PI

A saída operacional deve possuir dados suficientes para:

```text
anunciante
agencia
veiculo_ou_fornecedor
produto_comercial
inventario
formato
quantidade
periodo
datas
valor
condicoes
faturamento
observacoes
termos_aplicaveis
```

O Mapa é a fonte estruturada. A autorização ou PI é um documento transacional derivado.

---

## 23. Checking e conciliação

O Mapa deve permitir comparar:

```text
planejado
negociado
autorizado
programado
veiculado
comprovado
faturado
```

Divergências possíveis:

- data;
- horário;
- quantidade;
- posição;
- formato;
- duração;
- praça;
- entrega;
- audiência;
- custo;
- faturamento;
- compensação.

---

## 24. Versionamento e rastreabilidade

Cada linha deve preservar:

- versão do inventário;
- versão do produto comercial;
- versão da oferta;
- condição negociada;
- fonte e data das audiências;
- método de equivalência;
- versão do Plano;
- autoria;
- histórico de alterações.

Alterações futuras da Biblioteca não devem modificar Mapas anteriores.

---

## 25. Princípio consolidado

> O Mapa de Veiculação é a materialização operacional do Plano. Ele deve preservar a diferença entre inventário, formato, produto, compra, entrega e mensuração; registrar a condição negociada; manter métricas nativas e equivalências qualificadas; e fornecer a base única para programação, autorização, checking e conciliação.