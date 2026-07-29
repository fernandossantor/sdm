# Biblioteca de Públicos e Segmentos do MediAd Planner

## 1. Finalidade

A Biblioteca de Públicos e Segmentos organiza definições reutilizáveis de públicos, universos, segmentos e territórios relevantes para os planejamentos do MediAd Planner.

Seu objetivo é responder:

> Quem se pretende alcançar, por quais características esse conjunto é definido e em que território ele se encontra?

A Biblioteca deve ser deliberadamente restrita. Ela não precisa nascer com grande quantidade de públicos previamente cadastrados. Deve oferecer estruturas, campos e vocabulários controlados para que cada projeto registre apenas as informações necessárias ao seu caso.

O preenchimento ocorrerá predominantemente no contexto de cada campanha, com possibilidade de promoção posterior para o espaço de trabalho ou para a biblioteca global.

---

## 2. Escopo

A Biblioteca deve conter:

- universos de referência;
- públicos;
- segmentos;
- critérios demográficos;
- interesses;
- comportamentos;
- necessidades e motivações;
- etapas da jornada;
- pontos de contato relevantes;
- territórios e praças;
- exclusões;
- fontes, validade e confiança.

A Biblioteca não deve armazenar como atributos permanentes do público:

- audiência;
- alcance;
- cobertura;
- frequência;
- impactos;
- afinidade observada.

Essas variáveis dependem da relação entre o público e uma alternativa de mídia em determinado território, período e metodologia.

---

## 3. Distinções fundamentais

### 3.1 Universo

Universo é a população de referência dentro da qual um público é definido.

Exemplos:

- população residente em São Borja;
- pessoas com 15 anos ou mais;
- domicílios urbanos;
- estudantes de determinada instituição;
- clientes cadastrados de uma empresa.

Um universo pode possuir valor populacional, desde que registre:

- território;
- unidade populacional;
- ano ou período;
- fonte;
- metodologia;
- data de atualização;
- grau de confiança.

Esse valor é populacional, não de audiência.

### 3.2 Público

Público é um conjunto de pessoas definido por critérios relevantes para uma campanha, marca, produto, serviço ou problema de comunicação.

Pode ser:

- amplo ou específico;
- permanente ou temporário;
- global;
- do espaço de trabalho;
- exclusivo de um projeto;
- pessoal ou rascunho.

### 3.3 Segmento

Segmento é um recorte interno de um público, definido por critérios adicionais.

```text
Universo
    ↓
Público
    ↓
Segmento
```

Um mesmo público pode possuir vários segmentos. Um segmento pode receber prioridade ou peso estratégico diferente conforme a campanha.

### 3.4 Persona

Persona é uma representação qualitativa ou narrativa criada para sintetizar características de um público.

Ela não deve substituir o público mensurável nem ser usada diretamente como unidade de cálculo sem critérios explícitos.

### 3.5 Target operacional

Target operacional é o recorte efetivamente utilizado em uma estratégia, compra ou simulação.

Pode derivar de um público ou segmento, mas deve preservar os critérios utilizados e as limitações da plataforma ou veículo.

### 3.6 Audiência

Audiência é a população observada ou estimada de um veículo, programa, ambiente ou inventário em determinado período e praça.

Não pertence a esta Biblioteca.

---

## 4. Princípio de preenchimento contextual

A Biblioteca não deve exigir falsa precisão.

Para cada campo, o sistema deve admitir estados semanticamente distintos:

```text
Não informado
Sem restrição
Não aplicável
Valor definido
Faixa definida
Hipótese
Dado observado
```

O sistema deve permitir criar um público durante o Briefing e salvá-lo inicialmente no escopo do projeto.

```text
Campanha
    ↓
Seleciona público existente
ou
Cria público específico
    ↓
Salva no projeto
    ↓
Opcionalmente promove para o espaço de trabalho
    ↓
Opcionalmente propõe publicação global
```

---

## 5. Estrutura do público

Campos mínimos recomendados:

- nome;
- descrição;
- finalidade;
- universo de referência;
- praça ou território;
- critérios demográficos;
- interesses;
- comportamentos;
- necessidades e motivações;
- etapas da jornada;
- pontos de contato relevantes;
- exclusões;
- fonte;
- data de referência;
- período de validade;
- natureza dos dados;
- nível de confiança;
- escopo;
- estado editorial;
- autoria.

O sistema não deve obrigar o preenchimento de todas as dimensões. A obrigatoriedade deve variar conforme o uso pretendido.

---

## 6. Variáveis demográficas

As variáveis demográficas permanecem na Biblioteca como critérios de definição de públicos e segmentos.

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
- condição institucional ou profissional.

Cada critério deve permitir:

- operador;
- valor ou faixa;
- inclusão ou exclusão;
- fonte;
- data;
- confiança;
- observação metodológica.

---

## 7. Interesses

Interesses caracterizam temas, atividades, assuntos ou áreas de atenção relevantes para o público.

Exemplos:

- esportes;
- tecnologia;
- gastronomia;
- política;
- música;
- saúde;
- viagens;
- automóveis;
- educação;
- sustentabilidade.

Cada vínculo entre público e interesse deve registrar:

- interesse;
- relevância;
- intensidade;
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

Interesse não deve ser confundido com afinidade de mídia.

---

## 8. Comportamentos

Comportamentos descrevem ações, hábitos, rotinas ou padrões relevantes.

Exemplos:

- compra online;
- compra presencial;
- frequência de compra;
- consumo de streaming;
- deslocamento diário;
- uso de transporte coletivo;
- visita a shopping;
- consumo de rádio;
- pesquisa de preço;
- uso de aplicativos;
- consumo fora do lar;
- resposta a promoções;
- compartilhamento de conteúdo;
- uso simultâneo de telas;
- comparação antes da compra.

Cada vínculo deve registrar:

- comportamento;
- frequência ou intensidade;
- contexto;
- origem;
- fonte;
- validade;
- confiança.

A ausência de fonte deve reduzir a confiança, mas não impedir o registro de uma hipótese explicitamente marcada.

---

## 9. Necessidades, motivações e barreiras

O público pode ser descrito por:

- necessidades;
- motivações;
- barreiras;
- tensões;
- ocasiões;
- situações de uso;
- critérios de decisão;
- necessidades informacionais.

Essas informações são especialmente úteis para relacionar o público à jornada, aos pontos de contato e às funções de mídia.

Devem ser tratadas como dados qualitativos estruturados, com fonte e confiança.

---

## 10. Jornada e pontos de contato

A Biblioteca pode associar públicos e segmentos a:

- etapas da jornada;
- necessidades comunicacionais;
- momentos de decisão;
- ocasiões de contato;
- pontos de contato preferenciais ou relevantes.

Esses vínculos não determinam automaticamente os meios. Eles fornecem informações para a Tradução Estratégica e para a Arquitetura de Mídia.

```text
Público
    ↓
Etapa da jornada
    ↓
Necessidade
    ↓
Ponto de contato possível
```

O detalhamento metodológico das jornadas, pontos de contato e funções pertence ao documento 16.

---

## 11. Territórios e praças

A geolocalização deve ser uma camada compartilhada entre públicos e inventários.

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

Campos recomendados:

- nome da praça;
- tipo territorial;
- código oficial;
- país;
- unidade federativa;
- município;
- bairro;
- CEP;
- latitude;
- longitude;
- raio;
- geometria;
- fonte cartográfica;
- data de atualização;
- grau de confiança.

A praça não deve ser apenas texto livre.

O mesmo catálogo territorial deve ser utilizado pela Biblioteca de Inventários para registrar cobertura e disponibilidade.

A Arquitetura de Mídia poderá comparar:

```text
Território do público
∩
Cobertura do veículo ou inventário
```

A implementação pode evoluir por níveis:

1. correspondência administrativa;
2. abrangência parcial por bairros ou distritos;
3. coordenadas e raio;
4. polígonos e interseção geoespacial.

---

## 12. Dimensões compartilhadas com a Biblioteca de Inventários

Públicos e inventários devem usar vocabulários compatíveis para permitir comparação.

Catálogos compartilhados:

- interesses;
- comportamentos;
- contextos de consumo e contato;
- etapas da jornada;
- pontos de contato;
- funções;
- variáveis demográficas;
- territórios;
- temas editoriais.

Exemplo lógico:

```text
interesses
    ↕
publicos_interesses

comportamentos
    ↕
publicos_comportamentos

etapas_jornada
    ↕
publicos_etapas_jornada

territorios
    ↕
publicos_territorios
```

As relações devem preservar relevância, origem, fonte, validade e confiança.

---

## 13. Qualificação público–inventário

A Biblioteca fornece uma das entradas do componente de qualificação da Arquitetura de Mídia.

```text
Interesses do público
↔ proposta editorial e temas

Comportamentos do público
↔ contextos de contato atendidos

Etapa da jornada
↔ funções possíveis do inventário

Território do público
↔ cobertura territorial

Características demográficas
↔ segmentações disponíveis ou audiência observada
```

A qualificação pode gerar dimensões como:

- aderência editorial ou temática;
- aderência comportamental;
- aderência à jornada;
- compatibilidade demográfica;
- compatibilidade territorial;
- adequação contextual;
- confiança das evidências.

Essa qualificação não substitui objetivos, KPIs, custos, restrições, overlap, saturação, complementaridade ou demais variáveis da Arquitetura de Mídia.

---

## 14. Afinidade observada e aderência estimada

### 14.1 Afinidade observada

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

Ela não é um campo permanente do público.

### 14.2 Aderência estimada

Aderência estimada é a compatibilidade calculada pela Arquitetura de Mídia a partir das características do público, das propriedades da alternativa e das condições da campanha.

Não deve ser apresentada como audiência medida.

---

## 15. Segmentos

Campos recomendados:

- nome;
- público de origem;
- descrição;
- critérios adicionais;
- exclusões;
- prioridade;
- peso estratégico;
- tamanho estimado, quando disponível;
- unidade;
- fonte;
- data;
- confiança;
- escopo;
- estado.

O tamanho estimado de um segmento é opcional e deve indicar fonte e metodologia. Não deve ser confundido com audiência.

---

## 16. Escopos

### Global

Deve conter apenas estruturas e públicos amplamente reutilizáveis e metodologicamente estáveis.

Exemplos:

- população geral;
- adultos 18+;
- domicílios;
- empresas;
- estudantes;
- consumidores.

### Espaço de trabalho

Públicos recorrentes de uma organização.

Exemplos:

- consumidores atuais;
- clientes de determinada marca;
- comunidade acadêmica;
- moradores de uma região;
- compradores de uma categoria.

### Projeto

Públicos criados especificamente para uma campanha. Deve ser o escopo predominante.

### Pessoal ou rascunho

Públicos ainda em elaboração.

---

## 17. Versionamento e snapshot

Quando um público for utilizado em um projeto, o sistema deve preservar:

- versão da definição;
- critérios usados;
- universo de referência;
- território;
- fontes;
- datas;
- natureza dos dados;
- confiança;
- ajustes locais;
- autoria;
- data de seleção.

Alterações futuras na biblioteca não devem modificar retroativamente campanhas anteriores.

---

## 18. Modelo lógico mínimo

Entidades principais:

```text
universos
publicos
segmentos
criterios_demograficos
interesses
comportamentos
necessidades
motivacoes
barreiras
territorios
publicos_demografia
publicos_interesses
publicos_comportamentos
publicos_jornadas
publicos_pontos_contato
publicos_territorios
publicos_exclusoes
```

Relações externas:

```text
afinidades_observadas
qualificacoes_publico_inventario
```

Essas relações externas não devem ser confundidas com atributos permanentes do público.

---

## 19. Princípio consolidado

> A Biblioteca de Públicos e Segmentos define quem se pretende alcançar, por quais critérios esse conjunto é caracterizado e em que território ele se encontra. Audiência, alcance, cobertura, frequência e afinidade observada surgem da relação entre públicos e alternativas de mídia, e não pertencem isoladamente ao cadastro do público.
