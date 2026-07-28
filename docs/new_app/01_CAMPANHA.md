# Campanha

**Documento:** `01_CAMPANHA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 27/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

Este documento estabelece a definição canônica da entidade **Campanha** e da etapa **Abertura da Campanha** no MediAd Planner.

A Campanha é a unidade central do sistema. Todo o planejamento, suas decisões, versões, simulações, consolidações, aprovações, acompanhamento e resultados pertencem obrigatoriamente a uma Campanha.

Em caso de divergência entre este documento, implementações, interfaces, documentação auxiliar ou código-fonte, esta especificação prevalece até que uma nova decisão seja formalmente registrada no Registro de Decisões.

---

## 2. Finalidade da Abertura da Campanha

A Abertura da Campanha cria o contexto inicial de um novo planejamento.

A etapa deve:

- criar a Campanha;
- identificar o Anunciante;
- identificar a Marca, quando aplicável;
- identificar o Produto ou Serviço, quando aplicável;
- registrar o Planejador Responsável;
- registrar a Equipe da Campanha, quando houver;
- gerar o Código da Campanha;
- registrar os metadados iniciais;
- preparar a transição para o Briefing.

A Abertura da Campanha não executa atividades de planejamento de mídia e não aciona motores de cálculo.

Não pertencem a esta etapa:

- objetivos;
- metas;
- públicos;
- universos;
- segmentos;
- jornadas;
- praças;
- períodos;
- orçamento;
- restrições;
- KPIs;
- arquitetura de mídia;
- inventários;
- cronogramas;
- simulações;
- comparações;
- otimizações;
- consolidação do plano;
- acompanhamento de resultados.

---

## 3. Conceitos do domínio

### 3.1 Campanha

Entidade central e raiz lógica do domínio.

Todo objeto de planejamento deve pertencer a uma Campanha.

### 3.2 Anunciante

Organização, instituição, empresa, órgão público, projeto ou pessoa responsável pela comunicação.

### 3.3 Marca

Identidade mercadológica ou institucional vinculada ao Anunciante.

### 3.4 Produto ou Serviço

Oferta específica vinculada ao Anunciante ou à Marca.

### 3.5 Planejador Responsável

Usuário responsável pela condução da Campanha.

### 3.6 Equipe da Campanha

Conjunto de usuários autorizados a colaborar na Campanha.

### 3.7 Código da Campanha

Identificador legível, único, permanente e imutável da Campanha.

### 3.8 Nome

Atributo descritivo da Campanha. Não constitui entidade ou conceito independente do domínio.

---

## 4. Papel da Campanha na arquitetura

A Campanha constitui a raiz lógica do fluxo metodológico.

```text
Campanha
├── Briefing
├── Tradução Estratégica
├── Arquitetura de Mídia
├── Simulações
├── Comparações
├── Otimizações
├── Insights
├── Plano Consolidado
├── Validações e Aprovações
└── Acompanhamento e Resultados
```

Os objetos internos não possuem existência autônoma fora de uma Campanha.

---

## 5. Modelo conceitual

A relação canônica é:

```text
Anunciante
└── Marca
    └── Produto ou Serviço
```

O sistema também deve admitir:

- campanhas institucionais;
- campanhas corporativas;
- campanhas sem Marca;
- campanhas sem Produto ou Serviço.

Regras estruturais:

- Anunciante é obrigatório;
- Marca é opcional;
- Produto ou Serviço é opcional;
- Marca deve pertencer ao Anunciante selecionado;
- Produto ou Serviço deve pertencer ao Anunciante ou à Marca selecionada.

---

## 6. Campos da Campanha

### 6.1 Campos obrigatórios informados pelo usuário

- Nome;
- Anunciante;
- Planejador Responsável.

### 6.2 Campos opcionais informados pelo usuário

- Marca;
- Produto ou Serviço;
- Equipe da Campanha;
- Observação Inicial.

### 6.3 Campos gerados ou controlados pelo sistema

- ID técnico;
- Código da Campanha;
- Criado por;
- Data e hora de criação;
- Data e hora da última atualização;
- Situação;
- Etapa Atual;
- Campanha Derivada de, quando aplicável.

---

## 7. Código da Campanha

Toda Campanha recebe um Código da Campanha no momento de sua criação.

### 7.1 Formato

```text
MP-AAAAMM-NNNN
```

Onde:

- `MP` identifica o MediAd Planner;
- `AAAAMM` representa o ano e o mês de criação;
- `NNNN` representa um sequencial global, crescente, único e não reutilizável.

Exemplos:

```text
MP-202607-0001
MP-202607-0002
MP-202608-0003
```

### 7.2 Regras do código

O Código da Campanha:

- é obrigatório;
- é gerado automaticamente;
- é único;
- é permanente;
- é imutável;
- não pode ser editado pelo usuário;
- não pode ser reutilizado;
- não é alterado pela Situação;
- não é alterado pela Etapa Atual;
- não é alterado por revisões ou versões internas;
- deve acompanhar telas, relatórios, exportações, históricos e registros de auditoria.

### 7.3 Sequencial global

O sequencial não é reiniciado a cada mês.

Exemplo:

```text
MP-202607-0001
MP-202607-0002
MP-202608-0003
MP-202608-0004
```

A parte temporal informa a data de criação. O sequencial informa a ordem histórica global de criação.

---

## 8. Código e versionamento

O Código da Campanha identifica a Campanha.

O versionamento identifica estados sucessivos dos objetos internos.

Exemplos:

- Briefing v1, v2, v3;
- Arquitetura de Mídia v1, v2;
- Plano Consolidado v1, v2;
- Simulação 1, 2, 3 ou A, B, C.

Briefing, Arquitetura, Simulação, Plano e demais objetos não recebem novos códigos primários independentes.

A evolução desses objetos nunca altera o Código da Campanha.

---

## 9. Situação da Campanha

A Situação representa a condição administrativa geral da Campanha.

Valores canônicos:

- Rascunho;
- Em andamento;
- Concluída;
- Cancelada;
- Arquivada.

A Situação inicial é:

```text
Rascunho
```

### 9.1 Significados

**Rascunho**  
Campanha criada, mas cuja Abertura ainda não foi concluída.

**Em andamento**  
Campanha aberta e com trabalho ativo em alguma etapa.

**Concluída**  
Campanha encerrada após o cumprimento do fluxo previsto.

**Cancelada**  
Campanha interrompida antes de sua conclusão.

**Arquivada**  
Campanha retirada da operação corrente, com preservação integral do histórico.

---

## 10. Etapa Atual

A Etapa Atual indica onde o trabalho se encontra no fluxo do Plano Mestre.

Valores canônicos:

- Abertura;
- Briefing;
- Tradução Estratégica;
- Arquitetura de Mídia;
- Simulação;
- Consolidação do Plano;
- Validação e Aprovação;
- Acompanhamento e Resultados.

A Etapa Atual inicial é:

```text
Abertura
```

Situação e Etapa Atual são dimensões distintas.

Exemplo:

```text
Situação: Em andamento
Etapa Atual: Simulação
```

A Etapa Atual não substitui os estados próprios dos objetos internos.

---

## 11. Estados dos objetos internos

Cada objeto interno poderá possuir seu próprio ciclo de estados.

Esses estados serão definidos nas respectivas especificações.

Exemplos de objetos com estados próprios:

- Briefing;
- Simulação;
- Plano Consolidado;
- Aprovação;
- Resultado.

Estados internos não devem ser incorporados à lista de Situações da Campanha.

---

## 12. Snapshot histórico

Na criação da Campanha, o sistema deve preservar uma fotografia dos principais vínculos.

Devem ser registrados, no mínimo:

- nome do Anunciante;
- nome da Marca, quando houver;
- nome do Produto ou Serviço, quando houver;
- identificação do Planejador Responsável;
- data e hora da criação.

A Campanha deve manter simultaneamente:

- a referência viva à entidade atual;
- o snapshot histórico do momento da criação.

Alterações posteriores nos cadastros não podem eliminar o contexto histórico da Campanha.

---

## 13. Campanhas derivadas e duplicação

Uma Campanha pode ser duplicada para originar outra Campanha.

A duplicação:

- cria uma nova Campanha;
- gera novo ID técnico;
- gera novo Código da Campanha;
- preserva a Campanha original;
- registra o vínculo com a Campanha de origem.

Campo canônico:

```text
Campanha Derivada de
```

A Campanha original não recebe nova versão nem tem seu código alterado.

A definição precisa de quais objetos internos podem ser copiados será estabelecida na especificação da duplicação.

---

## 14. Contrato de entrada

### 14.1 Pré-condições

- usuário autenticado;
- usuário autorizado a criar Campanhas;
- Anunciante disponível ou cadastrado no fluxo;
- Planejador Responsável válido.

### 14.2 Entradas obrigatórias

- Nome;
- Anunciante;
- Planejador Responsável.

### 14.3 Entradas opcionais

- Marca;
- Produto ou Serviço;
- Equipe da Campanha;
- Observação Inicial;
- Campanha Derivada de.

---

## 15. Contrato de saída

A Abertura produz uma Campanha contendo, no mínimo:

- ID técnico;
- Código da Campanha;
- Nome;
- vínculos informados;
- Planejador Responsável;
- Equipe da Campanha, quando houver;
- snapshots iniciais;
- Situação igual a `Rascunho`;
- Etapa Atual igual a `Abertura`;
- metadados de criação e atualização.

Quando a Abertura é concluída e o usuário prossegue para o Briefing:

```text
Situação: Em andamento
Etapa Atual: Briefing
```

A saída desta etapa habilita imediatamente o início do Briefing.

---

## 16. Regras de negócio

1. Toda Campanha pertence obrigatoriamente a um Anunciante.
2. Marca deve pertencer ao Anunciante selecionado.
3. Produto ou Serviço deve pertencer ao Anunciante ou à Marca selecionada.
4. Campanhas podem existir sem Marca.
5. Campanhas podem existir sem Produto ou Serviço.
6. Nome é obrigatório, mas não precisa ser único.
7. O Código da Campanha é obrigatório, automático, único, permanente e imutável.
8. O Código da Campanha nunca é reutilizado.
9. Alterações de Anunciante, Marca, Produto ou Serviço não modificam o Código da Campanha.
10. Alterações em Briefing, Estratégia, Simulações, Plano ou Resultados não modificam o Código da Campanha.
11. A duplicação cria uma nova Campanha e um novo Código da Campanha.
12. A duplicação preserva vínculo explícito com a Campanha de origem.
13. O Planejador Responsável recebe acesso automaticamente.
14. A Equipe da Campanha é opcional.
15. Nenhum motor de cálculo é executado na Abertura da Campanha.
16. Campanhas com histórico não devem ser excluídas diretamente.
17. O encerramento operacional deve ocorrer por Conclusão, Cancelamento ou Arquivamento.
18. A remoção física somente poderá ocorrer por procedimento administrativo controlado e auditável.

---

## 17. Interface

A interface da Abertura da Campanha deve permanecer simples e progressiva.

### 17.1 Bloco de identificação

- Nome;
- Anunciante;
- Marca;
- Produto ou Serviço.

### 17.2 Bloco de responsáveis

- Planejador Responsável;
- Equipe da Campanha.

### 17.3 Bloco de organização

- Observação Inicial.

### 17.4 Ações

- Cancelar;
- Salvar como Rascunho;
- Criar Campanha e iniciar Briefing.

### 17.5 Comportamento progressivo

```text
Seleciona Anunciante
↓
Libera Marcas vinculadas
↓
Seleciona Marca
↓
Libera Produtos ou Serviços vinculados
```

O cadastro contextual de Anunciante, Marca e Produto ou Serviço deve ocorrer sem abandonar a tela, preferencialmente por modal, painel lateral ou componente equivalente.

### 17.6 Identificação visível

Forma completa:

```text
[Código] Nome — Marca ou Anunciante
```

Forma compacta:

```text
[Código] Nome
```

---

## 18. Auditoria e rastreabilidade

A Campanha deve registrar, no mínimo:

- usuário criador;
- data e hora de criação;
- usuário da última alteração;
- data e hora da última alteração;
- Código da Campanha;
- Campanha de origem, quando houver;
- mudanças de Situação;
- mudanças de Etapa Atual;
- alterações de responsáveis e equipe.

O histórico não pode depender exclusivamente do estado atual das entidades relacionadas.

---

## 19. Impactos no sistema

A Abertura da Campanha influencia diretamente:

- organização do trabalho;
- permissões;
- colaboração;
- histórico;
- relatórios;
- exportações;
- filtros;
- rastreabilidade;
- restauração de contexto.

A Abertura não influencia diretamente:

- pesos estratégicos;
- seleção de meios;
- alcance;
- frequência;
- distribuição de verba;
- otimização;
- resultados calculados.

---

## 20. Decisões consolidadas

- **DEC-011 — Campanha como entidade central.**  
  A Campanha é a raiz lógica de todo o fluxo do MediAd Planner.

- **DEC-012 — Anunciante obrigatório.**  
  Toda Campanha deve pertencer a um Anunciante.

- **DEC-013 — Marca e Produto ou Serviço opcionais.**  
  O sistema admite campanhas institucionais e corporativas sem esses vínculos.

- **DEC-014 — Separação entre Abertura e Briefing.**  
  A Abertura cria o contexto; o Briefing reúne as informações de planejamento.

- **DEC-015 — Situação inicial igual a Rascunho.**

- **DEC-016 — Etapa Atual inicial igual a Abertura.**

- **DEC-017 — Preservação por snapshots.**  
  A Campanha mantém referências vivas e registros históricos dos vínculos iniciais.

- **DEC-018 — Nenhum motor é executado na Abertura.**

- **DEC-019 — Interface progressiva.**  
  Marca e Produto ou Serviço são filtrados conforme os vínculos selecionados.

- **DEC-020 — Exclusão controlada.**  
  Campanhas com histórico devem ser concluídas, canceladas ou arquivadas, e não simplesmente excluídas.

- **DEC-021 — Código permanente da Campanha.**  
  Toda Campanha possui um único código canônico durante toda a sua existência.

- **DEC-022 — Separação entre Situação, Etapa Atual e estados internos.**  
  Essas dimensões não devem ser representadas por uma única lista de status.

- **DEC-023 — Nome como atributo da Campanha.**  
  Nome não constitui entidade ou conceito autônomo do domínio.

- **DEC-024 — Código no formato `MP-AAAAMM-NNNN`.**  
  O prefixo identifica o MediAd Planner, a parte temporal registra a criação e o sequencial é global, crescente, único e não reutilizável.

---

## 21. Limites desta especificação

Este documento não define em detalhe:

- permissões e papéis de colaboração;
- regras de duplicação parcial;
- políticas de retenção e remoção física;
- versionamento detalhado dos objetos internos;
- estados próprios do Briefing, Simulação, Plano e Aprovação;
- implementação técnica do gerador de códigos.

Esses temas serão definidos em documentos específicos, preservando as decisões estabelecidas aqui.
