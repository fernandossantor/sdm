# Biblioteca de Públicos e Segmentos do MediAd Planner

**Documento:** `14_BIBLIOTECA_DE_PUBLICOS_E_SEGMENTOS.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Consolidado  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Públicos e Segmentos organiza definições reutilizáveis de universos, públicos, segmentos e características relevantes para os planejamentos do MediAd Planner.

Seu objetivo é responder:

> Quem se pretende alcançar, por quais critérios esse conjunto é definido e em que território ele se encontra?

A Biblioteca descreve o público. Ela não descreve, por si só, a estratégia aplicada a esse público, a jornada selecionada, a necessidade comunicacional derivada, a função da mídia ou o ponto de contato recomendado.

O preenchimento ocorrerá predominantemente no contexto de cada projeto, com possibilidade de promoção posterior para o espaço de trabalho ou para a biblioteca global.

---

## 2. Escopo

A Biblioteca deve conter:

- universos de referência;
- públicos;
- segmentos;
- critérios demográficos e institucionais;
- interesses;
- comportamentos;
- necessidades humanas, funcionais ou de consumo;
- motivações;
- barreiras e tensões;
- ocasiões e situações de uso;
- critérios de decisão;
- contextos de vida, consumo e contato;
- territórios e praças;
- inclusões e exclusões;
- fontes, validade e confiança.

A Biblioteca não deve armazenar como atributos permanentes do público:

- jornada aplicada;
- etapa de jornada;
- necessidade comunicacional;
- função comunicacional da mídia;
- ponto de contato recomendado;
- arquitetura de mídia;
- audiência;
- alcance;
- cobertura;
- frequência;
- impactos;
- afinidade observada;
- aderência calculada a inventários.

Esses elementos surgem de relações contextuais estabelecidas no planejamento ou em outras bibliotecas.

---

## 3. Limite entre as Bibliotecas 14 e 16

A Biblioteca 14 descreve **quem é o público e em que contexto vive, decide, consome ou age**.

A Biblioteca 16 organiza **como esse público é interpretado em uma progressão comunicacional e quais respostas de mídia podem ser pertinentes**.

```text
Biblioteca 14
Público + características + contexto
                ↓
Aplicação no planejamento
                ↓
Biblioteca 16
Jornada + etapa + necessidade comunicacional
+ função + ponto de contato
```

### 3.1 Pertence à Biblioteca 14

- necessidade humana ou funcional;
- motivação pessoal ou de consumo;
- barreira percebida;
- tensão;
- problema vivido;
- ocasião de uso;
- situação de compra;
- critério de decisão;
- hábito de mídia ou comportamento de contato;
- nível de conhecimento observado, quando descrito como dado do público;
- território.

### 3.2 Pertence à Biblioteca 16

- modelo de jornada;
- etapa da jornada;
- necessidade comunicacional derivada;
- função comunicacional da mídia;
- ponto de contato possível;
- regras de transição entre etapas;
- adequação de uma função a uma combinação etapa–necessidade.

### 3.3 Relação contextual

A Biblioteca 14 fornece dados de contexto para a aplicação da Biblioteca 16, mas não deve duplicar seus objetos.

Exemplo:

```text
Biblioteca 14
Barreira do público: receio de risco financeiro

Biblioteca 16, no planejamento
Etapa: consideração
Necessidade comunicacional: reduzir incerteza
Função: explicar e comprovar
Pontos de contato possíveis: mídia digital, atendimento, evento
```

A barreira pertence ao público. A necessidade comunicacional, a função e os pontos de contato são derivados no planejamento.

---

## 4. Conceitos fundamentais

### 4.1 Universo

Universo é a população de referência dentro da qual um público é definido.

Exemplos:

- população residente em determinado município;
- pessoas com 15 anos ou mais;
- domicílios urbanos;
- estudantes de determinada instituição;
- clientes cadastrados de uma organização.

Um universo pode possuir valor populacional, desde que registre:

- território;
- unidade populacional;
- ano ou período;
- fonte;
- metodologia;
- data de atualização;
- grau de confiança.

Esse valor é populacional, não de audiência.

### 4.2 Público

Público é um conjunto de pessoas ou organizações definido por critérios relevantes para uma campanha, marca, produto, serviço ou problema de comunicação.

Pode ser:

- amplo ou específico;
- permanente ou temporário;
- global;
- do espaço de trabalho;
- exclusivo de um projeto;
- pessoal ou rascunho.

### 4.3 Segmento

Segmento é um recorte interno de um público, definido por critérios adicionais.

```text
Universo
    ↓
Público
    ↓
Segmento
```

Um mesmo público pode possuir vários segmentos. Prioridade e peso estratégico são atributos da aplicação do segmento no projeto, não necessariamente da sua definição mestre.

### 4.4 Persona

Persona é uma representação qualitativa ou narrativa criada para sintetizar características de um público.

Ela não substitui o público mensurável nem deve ser utilizada diretamente como unidade de cálculo sem critérios explícitos.

### 4.5 Target operacional

Target operacional é o recorte efetivamente utilizado em uma estratégia, compra ou simulação.

Ele deriva de um público ou segmento, mas pertence à instância do planejamento e deve preservar:

- critérios utilizados;
- plataforma ou fonte de segmentação;
- aproximações;
- limitações;
- versão do público de origem.

### 4.6 Audiência

Audiência é a população observada ou estimada de um veículo, programa, ambiente ou inventário em determinado período e praça.

Não pertence à Biblioteca 14.

---

## 5. Princípio de preenchimento contextual

A Biblioteca não deve exigir falsa precisão.

Para cada dimensão, o sistema deve admitir estados semanticamente distintos:

```text
NÃO_INFORMADO
SEM_RESTRIÇÃO
NÃO_APLICÁVEL
VALOR_DEFINIDO
FAIXA_DEFINIDA
HIPÓTESE
DADO_OBSERVADO
DADO_INFERIDO
```

O sistema deve permitir criar um público durante o Briefing e salvá-lo inicialmente no escopo do projeto.

```text
Projeto
    ↓
Seleciona público existente
ou cria público específico
    ↓
Preserva snapshot no projeto
    ↓
Opcionalmente promove ao espaço de trabalho
    ↓
Opcionalmente propõe publicação global
```

---

## 6. Estrutura mínima do público

Campos recomendados:

- identificador;
- nome;
- descrição;
- finalidade de definição;
- universo de referência;
- critérios de inclusão;
- critérios de exclusão;
- territórios;
- critérios demográficos ou institucionais;
- interesses;
- comportamentos;
- necessidades humanas, funcionais ou de consumo;
- motivações;
- barreiras e tensões;
- ocasiões e situações de uso;
- critérios de decisão;
- contextos de vida, consumo e contato;
- tamanho estimado, quando disponível;
- unidade populacional;
- fonte;
- metodologia;
- data de referência;
- período de validade;
- natureza dos dados;
- nível de confiança;
- escopo;
- estado editorial;
- autoria;
- versão.

Não são campos do cadastro mestre do público:

- jornada;
- etapa;
- necessidade comunicacional;
- função comunicacional;
- ponto de contato recomendado;
- prioridade estratégica no plano;
- peso no plano.

---

## 7. Critérios demográficos e institucionais

Podem incluir:

- faixa etária;
- sexo ou gênero, conforme a fonte;
- renda;
- classe econômica;
- escolaridade;
- ocupação;
- situação de trabalho;
- composição domiciliar;
- estado civil;
- presença de filhos;
- ciclo de vida;
- condição urbana ou rural;
- nacionalidade;
- idioma;
- vínculo institucional;
- setor de atividade;
- porte da organização;
- função profissional.

Cada critério deve permitir:

- operador;
- valor ou faixa;
- inclusão ou exclusão;
- fonte;
- data;
- confiança;
- observação metodológica.

---

## 8. Interesses e comportamentos

Interesses caracterizam temas, atividades, assuntos ou áreas de atenção relevantes para o público.

Comportamentos descrevem ações, hábitos, rotinas ou padrões relevantes, incluindo comportamentos de compra, consumo, deslocamento, informação e uso de mídia.

Cada vínculo deve preservar:

- item do vocabulário controlado;
- relevância;
- frequência ou intensidade;
- contexto;
- natureza;
- origem;
- fonte;
- validade;
- confiança.

Naturezas possíveis:

- declarado;
- observado;
- inferido;
- hipotético;
- fornecido pelo cliente;
- derivado de pesquisa;
- modelado.

Interesse não deve ser confundido com afinidade de mídia. Comportamento de uso de mídia não determina automaticamente um ponto de contato estratégico.

---

## 9. Necessidades, motivações, barreiras e contextos

Nesta Biblioteca, necessidade significa uma condição do público, e não uma necessidade comunicacional.

Exemplos:

- necessidade funcional;
- necessidade de informação observada;
- necessidade de segurança;
- necessidade de conveniência;
- necessidade de reconhecimento;
- problema a resolver;
- motivação de compra;
- barreira percebida;
- tensão;
- situação de uso;
- ocasião de consumo;
- critério de decisão.

Para evitar ambiguidade, recomenda-se utilizar no modelo de dados nomes explícitos, como:

```text
necessidades_do_publico
motivacoes_do_publico
barreiras_do_publico
contextos_do_publico
```

A expressão `necessidade_comunicacional` fica reservada exclusivamente à Biblioteca 16.

---

## 10. Territórios e praças

A geolocalização deve ser uma dimensão compartilhada entre públicos, inventários e projetos.

O público pode ser relacionado a:

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
- polígono;
- área personalizada.

Cada relação deve preservar fonte cartográfica, data, precisão, validade e confiança.

O mesmo catálogo territorial deve ser utilizado pela Biblioteca de Inventários para registrar cobertura e disponibilidade.

```text
Território do público
        ∩
Cobertura do inventário
        ↓
Compatibilidade territorial calculada
```

---

## 11. Relação com a Biblioteca 16

A Biblioteca 14 fornece à Biblioteca 16:

- público ou segmento selecionado;
- características relevantes;
- interesses;
- comportamentos;
- necessidades do público;
- motivações;
- barreiras;
- contextos;
- território;
- evidências e confiança.

A Biblioteca 16 aplica essas informações a um modelo de jornada em determinado planejamento.

```text
Público selecionado
        +
Objetivo e resultado pretendido
        +
Contexto do projeto
        ↓
Jornada aplicada
        ↓
Etapa contextual
        ↓
Necessidade comunicacional
        ↓
Função comunicacional
        ↓
Ponto de contato possível
```

A relação público–jornada deve existir na instância do planejamento ou em um modelo reutilizável da Biblioteca 21, nunca como atributo ontológico permanente do público.

---

## 12. Relação com a Biblioteca de Inventários

Públicos e inventários devem utilizar vocabulários compatíveis para permitir qualificações posteriores.

Dimensões compartilháveis:

- interesses e temas editoriais;
- comportamentos e contextos atendidos;
- variáveis demográficas e segmentações disponíveis;
- territórios e cobertura;
- idiomas;
- restrições de elegibilidade.

A relação público–inventário é calculada ou observada fora do cadastro do público.

```text
Características do público
        ↕
Propriedades do inventário
        ↓
Qualificação contextual
```

A qualificação pode produzir:

- aderência editorial ou temática;
- aderência comportamental;
- compatibilidade demográfica;
- compatibilidade territorial;
- adequação contextual;
- confiança das evidências.

Aderência à jornada depende também da Biblioteca 16 e não deve ser calculada apenas pela Biblioteca 14.

---

## 13. Afinidade observada e aderência estimada

### 13.1 Afinidade observada

Afinidade observada é uma relação empírica entre um público e a audiência de um veículo, programa ou inventário.

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

Ela não é campo permanente do público.

### 13.2 Aderência estimada

Aderência estimada é uma compatibilidade calculada a partir das características do público, das propriedades da alternativa e das condições do planejamento.

Não deve ser apresentada como audiência medida nem armazenada como essência do público ou do inventário.

---

## 14. Segmentos

Campos recomendados:

- identificador;
- nome;
- público de origem;
- descrição;
- critérios adicionais;
- exclusões;
- tamanho estimado, quando disponível;
- unidade;
- fonte;
- metodologia;
- data;
- confiança;
- escopo;
- estado;
- versão.

Prioridade, papel e peso estratégico pertencem à aplicação do segmento no projeto.

---

## 15. Escopos

### Global

Deve conter apenas estruturas e públicos amplamente reutilizáveis e metodologicamente estáveis.

### Espaço de trabalho

Contém públicos recorrentes de uma organização ou equipe.

### Projeto

Contém públicos criados ou adaptados para um planejamento específico. Deve ser o escopo predominante.

### Pessoal ou rascunho

Contém definições ainda em elaboração.

---

## 16. Versionamento e snapshot

Quando um público for utilizado em um projeto, o sistema deve preservar:

- versão da definição;
- critérios utilizados;
- universo de referência;
- território;
- fontes;
- datas;
- natureza dos dados;
- confiança;
- ajustes locais;
- autoria;
- data de seleção.

Alterações futuras no cadastro mestre não devem modificar retroativamente planejamentos anteriores.

---

## 17. Modelo lógico mínimo

Entidades principais:

```text
universos
publicos
segmentos
criterios_publico
interesses
comportamentos
necessidades_do_publico
motivacoes_do_publico
barreiras_do_publico
contextos_do_publico
territorios
publicos_criterios
publicos_interesses
publicos_comportamentos
publicos_necessidades
publicos_motivacoes
publicos_barreiras
publicos_contextos
publicos_territorios
publicos_exclusoes
```

Relações pertencentes à instância do planejamento:

```text
planejamento_publicos
planejamento_segmentos
planejamento_publicos_jornadas
planejamento_targets_operacionais
planejamento_prioridades_publico
```

Relações analíticas externas:

```text
afinidades_observadas
qualificacoes_publico_inventario
```

Não devem existir na Biblioteca 14 tabelas mestre como:

```text
publicos_jornadas
publicos_etapas_jornada
publicos_funcoes
publicos_pontos_contato
```

---

## 18. Separações ontológicas obrigatórias

```text
Necessidade do público ≠ necessidade comunicacional
Comportamento de mídia ≠ ponto de contato recomendado
Contexto do público ≠ etapa de jornada
Nível de conhecimento observado ≠ etapa atribuída
Público ≠ target operacional
Público ≠ audiência
Interesse ≠ afinidade de mídia
Território do público ≠ cobertura de inventário
Jornada aplicada ≠ atributo permanente do público
```

---

## 19. Princípio consolidado

> A Biblioteca de Públicos e Segmentos define quem se pretende alcançar, por quais critérios esse conjunto é caracterizado e em que território e contexto ele se encontra. Necessidades, motivações, barreiras e comportamentos descrevem o público; jornadas, etapas, necessidades comunicacionais, funções e pontos de contato são aplicados contextualmente pela Biblioteca 16. Audiência, afinidade e aderência surgem de relações analíticas e não pertencem isoladamente ao cadastro do público.