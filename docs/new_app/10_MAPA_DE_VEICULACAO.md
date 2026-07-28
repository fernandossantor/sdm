# Mapa de Veiculação

O **Mapa de Veiculação** é a visão técnica, operacional e detalhada do Plano Consolidado de Mídia. Ele registra o que será veiculado, em qual veículo ou plataforma, em que formato, data, horário, quantidade, unidade comercial, custo, audiência, função estratégica e estado operacional.

Sua pergunta orientadora é:

> O que exatamente será veiculado, quando, onde, em qual formato, para qual público, com qual finalidade, audiência, custo e condição operacional?

O Mapa deriva da mesma base do Cronograma, mas preserva a granularidade necessária à compra, programação, execução, comprovação e auditoria.

```text
Plano Consolidado
        ↓
Inventários aprovados
        ↓
Linhas de Programação
        ↓
Ocorrências de Veiculação
        ↓
Mapa de Veiculação
```

## 1. Natureza do artefato

O Mapa deve funcionar simultaneamente como:

- grade de programação;
- memória de cálculo;
- controle orçamentário;
- registro técnico;
- base de execução;
- referência de comprovação;
- fonte do Cronograma;
- base para indicadores.

Ele não deve ser uma planilha paralela preenchida manualmente e desconectada do Plano.

## 2. Estrutura geral

O Mapa deve combinar:

```text
Identificação técnica do inventário
            +
Distribuição temporal das ocorrências
            +
Custos
            +
Audiências e indicadores
            +
Relações estratégicas
            +
Controle operacional
```

Estrutura conceitual:

```text
Mapa de Veiculação
├── Identificação do Plano
├── Campanha e período
├── Meio e praça
├── Linhas de programação
├── Ocorrências por data
├── Unidades comerciais
├── Custos unitários e totais
├── Audiências nativas
├── Audiências equivalentes
├── Indicadores
├── Jornada e pontos de contato
├── Funções e papéis
├── Materiais
├── Estados operacionais
├── Totais
├── Saldos
├── Observações
└── Versionamento
```

## 3. Três níveis de domínio

O Mapa exige a separação entre inventário, linha e ocorrência.

### 3.1 Inventário

É a oferta comercial disponível.

Exemplos:

- programa de TV;
- faixa de rádio;
- página de jornal;
- edição de revista;
- roteiro de OOH;
- sessão de cinema;
- conjunto de anúncios;
- pacote de impressões;
- espaço em PDV.

### 3.2 Linha de Programação

Agrupa ocorrências homogêneas.

Exemplo:

```text
Rádio X
Programa Y
07h–09h
Spot 30 segundos
Peça A
Praça São Borja
```

### 3.3 Ocorrência de Veiculação

É a concretização temporal da linha.

Exemplo:

```text
10/08/2026
08h15
1 inserção
programada
```

Uma linha pode possuir várias ocorrências.

## 4. Estrutura normalizada

A base interna deve ser vertical e normalizada.

Exemplo:

| linha_programacao_id | data | hora/faixa | quantidade | estado |
|---|---|---|---:|---|
| TV-JORNAL-A-30 | 05/08/2026 | 19h30 | 1 | programada |
| TV-JORNAL-A-30 | 07/08/2026 | 19h30 | 1 | programada |
| TV-JORNAL-A-30 | 12/08/2026 | 19h30 | 2 | programada |

A grade mensal com dias em colunas deve ser uma forma de apresentação, não a estrutura primária do banco.

```text
Base normalizada
       ↓
Mapa mensal
Mapa semanal
Mapa por fase
Mapa por veículo
Mapa por praça
Mapa por fornecedor
```

## 5. Cabeçalho do Mapa

Cada Mapa deve registrar:

- Plano de origem;
- versão do Plano;
- campanha;
- cliente;
- produto ou unidade;
- meio;
- praça;
- período;
- moeda;
- responsável;
- data de geração;
- estado;
- filtros aplicados.

## 6. Campos gerais da linha de programação

Cada linha pode conter:

- identificador;
- meio;
- canal;
- veículo ou empresa;
- plataforma;
- fornecedor;
- programa, seção, roteiro, ambiente ou posicionamento;
- horário ou faixa;
- formato;
- peça;
- duração;
- dimensão;
- praça;
- público;
- fase;
- período;
- objetivo;
- etapa da jornada;
- ponto de contato;
- função de mídia;
- papel estratégico;
- unidade comercial;
- quantidade planejada;
- observações.

## 7. Campos da ocorrência

Cada ocorrência deve registrar:

- linha de origem;
- data;
- dia da semana;
- hora ou faixa;
- data de início;
- data de término;
- duração da exposição;
- quantidade;
- unidade consumida;
- peça;
- material;
- responsável;
- estado;
- comprovante;
- observação.

Isso permite representar meios em que a data marcada é apenas o início de uma exposição mais longa.

## 8. Campos financeiros

Cada linha ou ocorrência deve poder registrar:

- preço de tabela;
- coeficiente de formato;
- preço ajustado;
- desconto;
- bonificação;
- preço negociado;
- custo unitário;
- quantidade;
- custo bruto;
- custo líquido do veículo;
- comissão;
- taxas;
- impostos;
- custo associado;
- custo total elegível;
- base financeira utilizada.

Forma básica:

```text
Custo da linha = quantidade de unidades comerciais × custo unitário negociado
```

O sistema deve admitir custos fixos, variáveis e pacotes.

## 9. Totais financeiros

O Mapa deve calcular:

- total da linha;
- total do veículo;
- total do fornecedor;
- total do meio;
- total da praça;
- total do período;
- total do Mapa;
- verba aprovada;
- verba alocada;
- diferença;
- comissão;
- saldo.

Nenhum total deve depender de fórmula externa não registrada.

## 10. Audiências nativas

O Mapa deve preservar as métricas próprias de cada meio.

Exemplos:

### TV e rádio

- audiência percentual;
- impactos;
- GRP;
- CPP.

### Jornal e revista

- circulação;
- leitores;
- audiência;
- CPM;
- GRP.

### OOH

- fluxo;
- impactos;
- alcance;
- CPM;
- GRP.

### Digital

- impressões;
- alcance;
- cliques;
- CTR;
- conversões;
- CPC;
- CPA;
- frequência.

### Cinema, PDV e No Media

- sessões;
- público;
- fluxo;
- contatos;
- ativações;
- participação;
- unidade específica do inventário.

## 11. Audiências equivalentes

Ao lado da métrica nativa, o Mapa deve registrar:

```text
métrica nativa
valor nativo
unidade nativa
fonte
método de equivalência
coeficientes
audiência equivalente
impactos equivalentes
confiança
```

A métrica equivalente não substitui a métrica nativa.

## 12. Relação com jornada e pontos de contato

Cada linha deve estar vinculada a:

- objetivo;
- etapa da jornada;
- ponto de contato;
- função de mídia;
- papel do meio;
- público;
- praça;
- fase.

Exemplo:

```text
TV — Jornal local — filme 30 segundos
Jornada: conhecimento
Ponto de contato: consumo de notícia no início da noite
Função: gerar alcance
Papel: principal
```

Esses campos podem ficar ocultos em uma impressão operacional simplificada, mas devem existir na base.

## 13. Relação com flight e pressão

O Mapa é a materialização detalhada do flight.

```text
Flight planejado
        ↓
Linhas de programação
        ↓
Ocorrências distribuídas
        ↓
Pressão por data e período
        ↓
Cronograma
```

Cada alteração de data, quantidade, veículo ou duração pode modificar a pressão e deve provocar recálculo.

## 14. Especificidades por meio

O sistema não deve impor exatamente as mesmas colunas a todos os meios.

### 14.1 TV

Campos típicos:

- emissora;
- programa;
- horário;
- formato;
- duração;
- peça;
- data;
- inserções;
- custo unitário;
- custo total;
- audiência;
- CPP;
- GRP.

Uma linha tende a representar:

```text
veículo + programa + horário + duração + peça + praça
```

### 14.2 Rádio

Campos típicos:

- emissora;
- programa;
- horário ou faixa;
- formato;
- duração;
- peça;
- data;
- inserções;
- custo unitário;
- custo total;
- audiência;
- CPP;
- GRP.

### 14.3 Jornal

Campos típicos:

- veículo;
- edição;
- seção;
- formato;
- dimensão;
- cor;
- data;
- quantidade;
- custo;
- circulação;
- leitores;
- CPM;
- audiência;
- GRP.

### 14.4 Revista

Campos típicos:

- título;
- edição;
- seção;
- posição;
- formato;
- dimensão;
- data de circulação;
- quantidade;
- custo;
- leitores;
- CPM;
- audiência;
- GRP.

### 14.5 OOH

Campos típicos:

- empresa;
- formato;
- roteiro;
- circuito;
- endereço ou área;
- data inicial;
- data final;
- duração;
- faces;
- custo;
- fluxo;
- impactos;
- CPM;
- alcance;
- GRP.

A ocorrência pode ser marcada no dia inicial e representar uma unidade comercial de vários dias.

### 14.6 Cinema

Campos típicos:

- rede;
- complexo;
- sala;
- sessão ou faixa;
- filme;
- formato;
- duração;
- período;
- sessões;
- público estimado;
- custo.

### 14.7 Digital

Uma linha pode representar:

```text
plataforma
campanha
conjunto de anúncios
objetivo
segmentação
formato
peça
período
orçamento diário ou total
modelo de compra
```

Campos típicos:

- plataforma;
- conta;
- campanha;
- conjunto;
- anúncio;
- objetivo;
- público;
- posicionamento;
- formato;
- início;
- fim;
- orçamento;
- bid;
- impressões;
- alcance;
- cliques;
- conversões;
- custos.

O sistema não deve forçar o digital a uma falsa unidade de inserção pontual.

### 14.8 PDV e No Media

Campos possíveis:

- local;
- ação;
- formato;
- equipe;
- material;
- período;
- quantidade;
- público estimado;
- contatos;
- custo;
- comprovação.

## 15. Campos obrigatórios por tipo

A obrigatoriedade deve depender do meio.

| Campo | TV | Rádio | Jornal | Revista | OOH | Digital |
|---|---:|---:|---:|---:|---:|---:|
| Veículo/empresa | Sim | Sim | Sim | Sim | Sim | Sim |
| Programa | Sim | Sim | Não | Não | Não | Não |
| Horário/faixa | Sim | Sim | Eventual | Eventual | Eventual | Eventual |
| Formato | Sim | Sim | Sim | Sim | Sim | Sim |
| Roteiro/local | Não | Não | Eventual | Eventual | Sim | Segmentação |
| Duração/período | Sim | Sim | Edição | Edição | Sim | Sim |
| Data/ocorrência | Sim | Sim | Sim | Sim | Início/fim | Período |

As regras devem ser configuráveis.

## 16. Estados operacionais

```text
planejado
cotado
reservado
contratado
confirmado
material solicitado
material recebido
material aprovado
programado
ativo
veiculado
comprovado
validado
compensado
cancelado
```

O estado da linha e o estado de cada ocorrência podem ser diferentes.

## 17. Materiais e peças

Cada linha deve poder vincular:

- peça;
- versão;
- formato;
- duração;
- dimensão;
- idioma;
- público;
- validade;
- aprovação;
- arquivo;
- especificação técnica;
- prazo de entrega.

Uma peça incompatível com o inventário deve gerar alerta.

## 18. Comprovação

Cada ocorrência pode possuir:

- comprovante;
- tipo de comprovante;
- data de recebimento;
- fonte;
- responsável;
- validação;
- divergência;
- compensação;
- observação.

Exemplos:

- checking;
- relatório de plataforma;
- print;
- fotografia;
- áudio;
- vídeo;
- declaração do veículo;
- log de exibição;
- auditoria externa.

## 19. Programado, contratado e realizado

O Mapa deve manter camadas separadas:

```text
planejado
reservado
contratado
programado
realizado
```

Deve ser possível comparar:

- quantidade;
- datas;
- horários;
- custos;
- audiência;
- entrega;
- estado.

O realizado não pode substituir o planejado.

## 20. Desvios

Cada linha e ocorrência pode registrar desvios:

- de data;
- de horário;
- de formato;
- de quantidade;
- de duração;
- de custo;
- de audiência;
- de entrega;
- de material;
- de comprovação.

Cada desvio relevante deve conter causa, impacto, responsável, tratamento, compensação e aceite.

## 21. Bonificações e compensações

O Mapa deve distinguir:

- unidade comprada;
- unidade bonificada;
- unidade compensatória;
- unidade adicional não faturada;
- unidade cancelada.

A bonificação não deve ser confundida com desconto financeiro.

## 22. Dependências

Uma linha ou ocorrência pode depender de:

- contratação;
- disponibilidade;
- criação;
- produção;
- aprovação jurídica;
- envio de material;
- configuração de plataforma;
- confirmação do veículo;
- pagamento;
- integração técnica.

Dependências atrasadas devem produzir alertas.

## 23. Regras de substituição

O Mapa pode registrar inventários substitutos previamente homologados.

Cada substituição deve conter:

- item original;
- substituto;
- equivalência funcional;
- diferença de custo;
- diferença de audiência;
- impacto na pressão;
- condição de acionamento;
- aprovação necessária.

## 24. Totais e fechamentos

Cada Mapa deve apresentar, quando aplicável:

- total de inserções ou unidades;
- total de audiência nativa;
- total de impactos equivalentes;
- total de GRP ou métrica equivalente;
- custo total;
- comissão;
- saldo;
- diferença para a verba;
- confiança média;
- alertas.

Os totais agregados devem respeitar overlap e regras de equivalência quando não forem simples somas.

## 25. Relação com o Cronograma

O Cronograma é gerado pela agregação do Mapa.

```text
Ocorrências detalhadas
        ↓
Agregação por período e dimensão
        ↓
Cálculo da pressão
        ↓
Cronograma de Mídia
```

Uma célula do Cronograma deve permitir acesso às linhas e ocorrências que a compõem.

## 26. Relação com custos e indicadores

Os indicadores devem nascer de bases declaradas.

Exemplos:

- CPM pela base de investimento selecionada;
- CPP pelo custo e audiência apropriados;
- GRP pelas audiências da linha;
- CPA pelo investimento elegível e conversões;
- ROAS pela política financeira do Plano.

O Mapa não deve inventar ou alterar fórmulas para fechar resultados.

## 27. Alertas

O sistema deve alertar para:

- linha sem veículo;
- ocorrência fora do período;
- horário incompatível;
- peça incompatível;
- preço sem validade;
- quantidade abaixo do pacote mínimo;
- custo divergente;
- audiência sem fonte;
- equivalência sem método;
- baixa confiança;
- duplicidade;
- sobreposição indevida;
- falta de material;
- falta de aprovação;
- ausência de responsável;
- saldo negativo;
- divergência com o Cronograma.

## 28. Validação

Antes da emissão, o sistema deve verificar:

- campos obrigatórios por meio;
- datas válidas;
- ocorrências dentro da campanha;
- unidade comercial definida;
- custos fechados;
- métricas com fonte;
- relações estratégicas preenchidas;
- materiais previstos;
- responsáveis atribuídos;
- totais coerentes;
- correspondência com o Plano;
- correspondência com o Cronograma;
- versão identificada.

Resultados possíveis:

```text
Mapa válido
Mapa válido com ressalvas
Mapa inconsistente
Mapa incompleto
Mapa inviável
```

## 29. Exportações

O Mapa deve poder ser exportado como:

- planilha por meio;
- planilha consolidada;
- PDF;
- ordem de inserção;
- pedido de compra;
- relatório técnico;
- arquivo para fornecedor;
- base de execução;
- base de auditoria.

A exportação pode adotar grade mensal, semanal, por fase ou formato vertical.

## 30. Versionamento

Cada Mapa deve registrar:

- Plano de origem;
- versão do Plano;
- período;
- meio;
- filtros;
- data de geração;
- responsável;
- estado.

Mudanças em linhas, ocorrências, custos, métricas ou materiais devem invalidar versões derivadas desatualizadas.

## 31. Contrato de entrada

O Mapa recebe:

- Plano Consolidado;
- inventários aprovados;
- linhas de programação;
- ocorrências;
- unidades comerciais;
- preços;
- negociações;
- públicos;
- praças;
- fases;
- jornada;
- pontos de contato;
- funções;
- papéis;
- métricas nativas;
- equivalências;
- materiais;
- responsáveis;
- estados;
- regras de comprovação.

## 32. Contrato de saída

O Mapa entrega:

- programação detalhada;
- ocorrências por data;
- quantidades;
- unidades comerciais;
- custos;
- audiências nativas;
- audiências equivalentes;
- indicadores;
- vínculos estratégicos;
- materiais;
- responsáveis;
- estados;
- totais;
- saldos;
- alertas;
- base para o Cronograma;
- base para execução e comprovação.

## 33. Limites

O Mapa deve:

- detalhar tecnicamente a veiculação;
- respeitar especificidades dos meios;
- relacionar inserções com jornada e pontos de contato;
- preservar métricas nativas e equivalentes;
- registrar custos e bases financeiras;
- servir à execução e auditoria;
- alimentar o Cronograma;
- manter rastreabilidade.

Ele não deve:

- ser uma base separada do Plano;
- forçar todos os meios à mesma granularidade;
- confundir linha com ocorrência;
- confundir data inicial com duração total;
- tratar planejado como contratado;
- substituir o Cronograma;
- sobrescrever valores realizados sobre planejados;
- ocultar fórmulas ou fontes.

## 34. Formulação canônica

O **Mapa de Veiculação** é a representação técnica, operacional e detalhada do Plano Consolidado, organizada por linhas de programação e ocorrências, capaz de indicar com precisão o que será veiculado, onde, quando, em qual formato, quantidade, unidade comercial, custo, audiência, função estratégica, etapa da jornada, ponto de contato e estado de execução.

Ele responde:

```text
qual inventário será usado
qual peça será veiculada
em qual veículo ou plataforma
em qual data e horário
por quanto tempo
quantas unidades serão consumidas
quanto custará
qual audiência produzirá
que função cumprirá
como será comprovado
```
