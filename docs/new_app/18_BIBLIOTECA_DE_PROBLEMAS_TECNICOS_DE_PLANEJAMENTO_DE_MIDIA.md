# Biblioteca de Problemas Técnicos de Planejamento de Mídia

**Documento:** `18_BIBLIOTECA_DE_PROBLEMAS_TECNICOS_DE_PLANEJAMENTO_DE_MIDIA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Estrutura inicial consolidada  
**Última revisão:** 29/07/2026  
**Natureza:** Documento normativo

---

## 1. Finalidade

A Biblioteca de Problemas Técnicos de Planejamento de Mídia organiza situações decisórias, analíticas, comparativas, econômicas, operacionais e de validação que podem ser resolvidas pelos motores especialistas do MediAd Planner.

Sua unidade principal não é uma fórmula, um indicador, um cálculo ou um algoritmo. É uma pergunta técnica orientada a uma decisão.

A Biblioteca responde:

> Que problema o planejador precisa resolver, quais conhecimentos são aplicáveis, quais procedimentos podem ser utilizados e em que condições cada solução é válida?

Ela constitui a camada heurística do sistema e faz a ponte entre a Biblioteca 17 — Conhecimento Técnico — e os motores especialistas.

---

## 2. Princípio fundamental

Um problema técnico deve ser definido pelo objetivo decisório, e não pelas ferramentas utilizadas para resolvê-lo.

Exemplos:

```text
Problema estável
COMPARAR_ALTERNATIVAS_DE_MIDIA

Conhecimentos evolutivos
CPM, CPP, afinidade, cobertura, qualidade, viewability,
overlap, saturação, confiança e outros.
```

```text
Problema estável
DISTRIBUIR_ORCAMENTO

Procedimentos evolutivos
regras proporcionais, cenários, heurísticas,
otimização matemática ou métodos híbridos.
```

O surgimento de uma nova métrica, fórmula ou técnica não deve exigir a redefinição do problema. Deve produzir nova relação com a Biblioteca 17 ou novo procedimento de resolução.

---

## 3. Posição na arquitetura

```text
Bibliotecas ontológicas
13 a 16
    ↓
Biblioteca 17
Conhecimento Técnico
    ↓
Biblioteca 18
Problemas Técnicos
    ↓
Motores especialistas
    ↓
Simulação, comparação, otimização e explicação
    ↓
Plano de mídia
```

A Biblioteca 17 descreve o que o especialista sabe.

A Biblioteca 18 descreve como esse conhecimento pode ser mobilizado diante de uma situação decisória.

Os motores executam, combinam ou coordenam procedimentos no contexto de um projeto.

---

## 4. Definições

### 4.1 Problema técnico

Situação que exige uma resposta fundamentada em conhecimento de planejamento de mídia e que possui objetivo decisório, entradas, condições, saídas e critérios de conclusão identificáveis.

### 4.2 Gatilho

Condição que indica a existência ou a necessidade de resolução de um problema.

Exemplos:

- objetivo de mídia validado;
- necessidade de selecionar inventários;
- orçamento insuficiente;
- ausência de comparabilidade;
- frequência projetada acima do limite;
- duas arquiteturas candidatas;
- dado obrigatório ausente.

### 4.3 Conhecimento aplicável

Objeto da Biblioteca 17 que contribui para compreender, calcular, validar, comparar ou interpretar aspectos do problema.

### 4.4 Procedimento de resolução

Sequência estruturada de operações e decisões que pode produzir uma resposta para o problema.

Um mesmo problema pode admitir vários procedimentos.

### 4.5 Critério de escolha

Condição usada para selecionar um procedimento entre alternativas possíveis.

Pode considerar:

- disponibilidade e qualidade dos dados;
- inventários envolvidos;
- território;
- horizonte temporal;
- precisão exigida;
- custo computacional;
- nível de automação;
- regras metodológicas;
- necessidade de explicação;
- confiança mínima.

### 4.6 Resposta técnica

Resultado produzido pela resolução do problema, acompanhado de justificativa, nível de confiança, limitações, hipóteses e rastreabilidade.

### 4.7 Subproblema

Problema que integra a resolução de outro problema mais amplo, preservando identidade e possibilidade de reutilização.

Exemplo:

```text
SELECIONAR_INVENTARIOS
    ↓ depende de
VALIDAR_ELEGIBILIDADE
COMPARAR_ALTERNATIVAS_DE_MIDIA
VERIFICAR_VIABILIDADE_ORCAMENTARIA
ESTIMAR_SOBREPOSICAO
```

---

## 5. Estrutura do Objeto de Problema Técnico

Cada problema deve possuir, quando aplicável:

```text
id
codigo
nome
pergunta_orientadora
descricao
objetivo_decisorio
categoria
dominio
momento_do_planejamento
gatilhos
entradas
saidas
pre_condicoes
restricoes
subproblemas
problemas_dependentes
conhecimentos_aplicaveis
procedimentos_possiveis
criterios_de_escolha
criterios_de_conclusao
nivel_de_automacao
intervencao_humana
exigencia_de_explicabilidade
tratamento_de_incerteza
estados_de_resultado
fontes
versao
status_editorial
```

Nem todos os campos precisam estar presentes em todos os problemas, mas objetivo decisório, entradas, saídas, conhecimentos aplicáveis, critérios de conclusão, versão e status são obrigatórios.

---

## 6. Identidade do problema

### 6.1 Código

Código estável, único e orientado à ação.

Padrão recomendado:

```text
VERBO_NO_INFINITIVO + OBJETO
```

Exemplos:

```text
ESTIMAR_ALCANCE
COMPARAR_ALTERNATIVAS_DE_MIDIA
DISTRIBUIR_ORCAMENTO
VALIDAR_COMPARABILIDADE
CONTROLAR_SATURACAO
SELECIONAR_INVENTARIOS
```

### 6.2 Nome

Título legível para usuários e documentação.

### 6.3 Pergunta orientadora

Formulação do problema em linguagem natural.

Exemplo:

```text
Código: ESTIMAR_ALCANCE
Pergunta: Quantas pessoas distintas do público poderão ser atingidas?
```

### 6.4 Objetivo decisório

Explicita para que a resposta será utilizada.

O objetivo não deve ser apenas “calcular um valor”. Deve declarar a decisão ou avaliação que o valor sustenta.

---

## 7. Taxonomia inicial de problemas

A taxonomia é expansível e não implica hierarquia rígida.

### 7.1 Problemas estratégicos

Relacionados à transformação de intenções em direções de planejamento.

Exemplos preliminares:

```text
VALIDAR_OBJETIVOS_DECLARADOS
CLASSIFICAR_OBJETIVOS
DERIVAR_OBJETIVOS_DE_COMUNICACAO
DERIVAR_OBJETIVOS_DE_MIDIA
PRIORIZAR_RESULTADOS_PRETENDIDOS
SELECIONAR_JORNADA
IDENTIFICAR_NECESSIDADE_COMUNICACIONAL
DEFINIR_FUNCAO_COMUNICACIONAL
```

A presença desses problemas na Biblioteca 18 não transfere para ela as ontologias ou regras dos Documentos 03, 15 e 16. Ela apenas registra situações resolvidas pelos motores mediante consulta a essas estruturas.

### 7.2 Problemas de dimensionamento e projeção

Relacionados à estimativa de grandezas e efeitos de mídia.

Exemplos preliminares:

```text
ESTIMAR_AUDIENCIA
ESTIMAR_ALCANCE
ESTIMAR_ALCANCE_INCREMENTAL
ESTIMAR_FREQUENCIA
ESTIMAR_IMPACTOS
ESTIMAR_PRESSAO_DE_MIDIA
ESTIMAR_COBERTURA_TERRITORIAL
ESTIMAR_SOBREPOSICAO
ESTIMAR_SATURACAO
```

### 7.3 Problemas comparativos

Relacionados à comparação entre objetos ou alternativas.

Exemplos preliminares:

```text
COMPARAR_MEIOS
COMPARAR_VEICULOS
COMPARAR_INVENTARIOS
COMPARAR_PLANOS
COMPARAR_ARQUITETURAS
COMPARAR_CENARIOS
AVALIAR_AFINIDADE
AVALIAR_EFICIENCIA_RELATIVA
```

### 7.4 Problemas de seleção e composição

Relacionados à escolha e combinação de componentes.

Exemplos preliminares:

```text
SELECIONAR_PONTOS_DE_CONTATO
SELECIONAR_TIPOLOGIAS_DE_MIDIA
SELECIONAR_INVENTARIOS
DEFINIR_PAPEL_ESTRATEGICO_DOS_CANAIS
COMPOR_ARQUITETURA_DE_MIDIA
DEFINIR_MIX_DE_MIDIA
PRIORIZAR_ALTERNATIVAS
```

### 7.5 Problemas econômicos

Relacionados a orçamento, custo e retorno projetado.

Exemplos preliminares:

```text
VALIDAR_VIABILIDADE_ORCAMENTARIA
DISTRIBUIR_ORCAMENTO
CALCULAR_INVESTIMENTO_BRUTO
CALCULAR_INVESTIMENTO_LIQUIDO
CALCULAR_COMISSAO_DE_AGENCIA
AVALIAR_EFICIENCIA_DE_CUSTO
MINIMIZAR_DESPERDICIO
OTIMIZAR_DISTRIBUICAO_DE_RECURSOS
```

### 7.6 Problemas temporais e operacionais

Relacionados à organização da presença de mídia no tempo e às condições de execução.

Exemplos preliminares:

```text
DEFINIR_FLIGHT
DEFINIR_CONTINUIDADE
DISTRIBUIR_INSERCOES_NO_TEMPO
CONTROLAR_FREQUENCIA
CONTROLAR_SATURACAO
VERIFICAR_DISPONIBILIDADE
COMPATIBILIZAR_PRAZOS
```

### 7.7 Problemas de validação

Relacionados à elegibilidade, consistência e validade metodológica.

Exemplos preliminares:

```text
VALIDAR_DADOS_DE_ENTRADA
VALIDAR_COMPARABILIDADE
VALIDAR_IDENTIDADE_DE_UNIVERSO
VALIDAR_IDENTIDADE_TEMPORAL
VALIDAR_IDENTIDADE_TERRITORIAL
VALIDAR_IDENTIDADE_DE_UNIDADE
VALIDAR_ELEGIBILIDADE_DE_INVENTARIO
DETECTAR_INCONSISTENCIAS
DETECTAR_DADOS_AUSENTES
DISTINGUIR_ZERO_DE_AUSENCIA
```

### 7.8 Problemas de explicação e diagnóstico

Relacionados à interpretação e comunicação das decisões.

Exemplos preliminares:

```text
EXPLICAR_RECOMENDACAO
JUSTIFICAR_SELECAO
DIAGNOSTICAR_LIMITACAO
IDENTIFICAR_FATOR_DE_RISCO
IDENTIFICAR_CAUSA_DE_INVIABILIDADE
COMPARAR_CONTRIBUICOES
EXPRESSAR_NIVEL_DE_CONFIANCA
```

---

## 8. Relação entre problema e conhecimento técnico

A relação é N:N.

```text
Problema técnico
    ↕
Objeto de Conhecimento Técnico
```

Cada vínculo deve possuir, quando aplicável:

```text
papel
obrigatoriedade
prioridade
contexto
ordem_logica
condicao_de_uso
alternatividade
dependencia
nivel_de_confianca
versao
```

Papéis iniciais recomendados:

```text
DEFINE
FUNDAMENTA
CALCULA
CONVERTE
VALIDA
COMPARA
RESTRINGE
INTERPRETA
EXPLICA
COMPLEMENTA
```

Obrigatoriedade inicial:

```text
OBRIGATORIO
CONDICIONAL
ALTERNATIVO
COMPLEMENTAR
```

Um conhecimento não pertence exclusivamente a um problema.

Exemplo:

```text
GRP
    ↓ participa de
ESTIMAR_PRESSAO_DE_MIDIA
COMPARAR_PLANOS
AVALIAR_EFICIENCIA_DE_CUSTO
DEFINIR_FLIGHT
```

---

## 9. Procedimentos de resolução

### 9.1 Separação obrigatória

```text
Problema ≠ procedimento
Procedimento ≠ fórmula
Procedimento ≠ motor
```

O problema declara o que precisa ser resolvido.

O procedimento declara um caminho possível.

A fórmula é um componente técnico que pode integrar o procedimento.

O motor seleciona, executa e coordena procedimentos.

### 9.2 Estrutura mínima do procedimento

```text
id
codigo
nome
problema_id
descricao
aplicabilidade
entradas_obrigatorias
entradas_opcionais
pre_condicoes
conhecimentos_utilizados
regras_aplicadas
sequencia_de_operacoes
validacoes
saidas
tratamento_de_excecoes
criterios_de_sucesso
nivel_de_automacao
explicacao_gerada
versao
status
```

### 9.3 Vários procedimentos para o mesmo problema

Exemplo conceitual:

```text
Problema: ESTIMAR_ALCANCE

Procedimento A
usar dado observado ou fornecido por fonte de audiência

Procedimento B
estimar por modelo matemático validado

Procedimento C
usar proxy de cobertura ou penetração

Procedimento D
declarar não operacionalização por ausência de dados
```

A escolha depende dos dados, do contexto, da validade metodológica e da confiança exigida.

---

## 10. Dependências entre problemas

Problemas podem formar grafos de dependência.

Tipos iniciais de relação:

```text
DEPENDE_DE
ANTECede
HABILITA
DECOMPOE_EM
COMPÕE
VALIDA
RESTRINGE
ALIMENTA
RETROALIMENTA
```

A grafia canônica do valor deverá ser normalizada na implementação, sem acentos, por exemplo `ANTECEDE` e `COMPOE`.

Exemplo:

```text
COMPOR_ARQUITETURA_DE_MIDIA
    ↓ depende de
SELECIONAR_PONTOS_DE_CONTATO
SELECIONAR_INVENTARIOS
VALIDAR_ELEGIBILIDADE_DE_INVENTARIO
VALIDAR_VIABILIDADE_ORCAMENTARIA
ESTIMAR_SOBREPOSICAO
CONTROLAR_SATURACAO
```

A existência de dependência não implica execução obrigatoriamente linear. Problemas podem ser resolvidos iterativamente ou em paralelo quando não houver conflito lógico.

---

## 11. Entradas e saídas

### 11.1 Entradas

Uma entrada deve declarar:

```text
nome
tipo
unidade
origem
obrigatoriedade
validacao
tratamento_de_ausencia
confianca
```

Origens possíveis:

```text
BRIEFING
BIBLIOTECA
PROJETO
FONTE_EXTERNA
CALCULO_PREVIO
PARAMETRO
USUARIO
OUTRO_PROBLEMA
```

### 11.2 Saídas

Uma saída pode ser:

- valor numérico;
- classificação;
- ranking;
- recomendação;
- conjunto de alternativas;
- alerta;
- diagnóstico;
- inviabilidade;
- necessidade de dado;
- solicitação de decisão humana;
- justificativa;
- nível de confiança.

A saída deve preservar sua natureza:

```text
OBSERVADA
FORNECIDA
CALCULADA
ESTIMADA
PROJETADA
DERIVADA
INFERIDA
PROXY
QUALITATIVA_ESTRUTURADA
NAO_OPERACIONALIZADA
```

---

## 12. Estados de resolução

Estados iniciais recomendados:

```text
NAO_INICIADO
AGUARDANDO_DADOS
PRONTO_PARA_RESOLUCAO
EM_PROCESSAMENTO
RESOLVIDO
RESOLVIDO_COM_RESSALVAS
RESOLVIDO_POR_PROXY
DEPENDENTE_DE_DECISAO_HUMANA
INCONCLUSIVO
NAO_APLICAVEL
NAO_OPERACIONALIZADO
INVALIDADO
```

O estado de resolução não substitui o status editorial do objeto de problema.

---

## 13. Níveis de automação

Classificação inicial:

```text
MANUAL_ESTRUTURADO
ASSISTIDO
SEMI_AUTOMATICO
AUTOMATICO_COM_VALIDACAO
AUTOMATICO
```

### 13.1 Manual estruturado

O sistema organiza dados, perguntas e critérios, mas a decisão é humana.

### 13.2 Assistido

O sistema produz análises e alternativas, mas não seleciona a resposta final.

### 13.3 Semiautomático

O sistema executa parte significativa da resolução e solicita decisões em pontos definidos.

### 13.4 Automático com validação

O sistema produz uma resposta, mas exige aprovação humana antes de incorporá-la ao plano.

### 13.5 Automático

O sistema pode concluir o problema sem intervenção, desde que todas as condições e níveis mínimos de confiança sejam atendidos.

O nível de automação deve ser definido por procedimento e contexto, não apenas pelo problema.

---

## 14. Intervenção humana

A Biblioteca deve declarar quando a intervenção humana é:

```text
NAO_NECESSARIA
OPCIONAL
RECOMENDADA
OBRIGATORIA
```

A intervenção é obrigatória quando, por exemplo:

- há conflito entre objetivos sem regra de prioridade;
- a resposta depende de juízo ético ou estratégico;
- faltam dados essenciais e não existe proxy validado;
- há alternativas tecnicamente equivalentes;
- a confiança está abaixo do mínimo definido;
- uma regra institucional exige aprovação.

---

## 15. Incerteza e confiança

Todo problema deve definir como tratar:

- dados ausentes;
- dados incompatíveis;
- estimativas;
- proxies;
- hipóteses;
- intervalos;
- divergências de fonte;
- sensibilidade a parâmetros;
- resultados inconclusivos.

A confiança não deve ser apresentada como precisão estatística quando for apenas avaliação qualitativa.

Estrutura inicial possível:

```text
ALTA
MEDIA
BAIXA
INDETERMINADA
```

A implementação poderá utilizar escalas mais detalhadas, desde que a metodologia seja explícita.

---

## 16. Explicabilidade

Toda resolução deve permitir responder:

```text
Qual problema foi identificado?
Por que ele precisava ser resolvido?
Quais dados foram utilizados?
Quais conhecimentos foram consultados?
Qual procedimento foi selecionado?
Por que esse procedimento foi escolhido?
Quais regras e restrições foram aplicadas?
Quais alternativas foram descartadas?
Qual foi a resposta?
Qual é o nível de confiança?
Quais são as limitações?
```

A explicação deve distinguir:

- dado de entrada;
- cálculo;
- regra;
- inferência;
- hipótese;
- proxy;
- decisão humana;
- recomendação do sistema.

---

## 17. Exemplo estrutural inicial

### 17.1 Problema

```text
codigo: COMPARAR_ALTERNATIVAS_DE_MIDIA
nome: Comparar alternativas de mídia
pergunta: Qual alternativa apresenta melhor adequação ao problema de planejamento?
categoria: COMPARATIVO
objetivo_decisorio: apoiar seleção ou priorização de alternativas
```

### 17.2 Entradas possíveis

- público;
- território;
- objetivo de mídia;
- resultado pretendido;
- indicadores prioritários;
- inventários candidatos;
- custos;
- audiência ou entrega;
- alcance;
- frequência;
- afinidade;
- restrições;
- qualidade e confiança dos dados.

### 17.3 Conhecimentos possíveis

- CPM;
- CPP;
- afinidade;
- cobertura;
- alcance;
- frequência;
- GRP ou TRP;
- overlap;
- saturação;
- viewability;
- comparabilidade;
- normalização;
- análise multicritério.

### 17.4 Procedimentos possíveis

```text
COMPARACAO_DIRETA_POR_INDICADOR
COMPARACAO_NORMALIZADA_MULTICRITERIO
COMPARACAO_POR_REGRAS_DE_ELEGIBILIDADE
COMPARACAO_POR_CENARIOS
COMPARACAO_ASSISTIDA_POR_JULGAMENTO
```

### 17.5 Saída

- ranking;
- alternativas dominantes;
- empates técnicos;
- alternativas inelegíveis;
- justificativa;
- confiança;
- ressalvas.

---

## 18. Inventário preliminar de problemas prioritários

O primeiro ciclo de formalização deverá priorizar problemas diretamente relacionados aos objetos já inventariados na Biblioteca 17.

### Núcleo A — Validade dos dados

```text
VALIDAR_DADOS_DE_ENTRADA
VALIDAR_COMPARABILIDADE
VALIDAR_IDENTIDADE_DE_UNIVERSO
VALIDAR_IDENTIDADE_DE_UNIDADE
VALIDAR_IDENTIDADE_TEMPORAL
VALIDAR_IDENTIDADE_TERRITORIAL
DISTINGUIR_ZERO_DE_AUSENCIA
```

### Núcleo B — Entrega e pressão

```text
ESTIMAR_AUDIENCIA
ESTIMAR_ALCANCE
ESTIMAR_FREQUENCIA
ESTIMAR_IMPACTOS
ESTIMAR_PRESSAO_DE_MIDIA
ESTIMAR_SOBREPOSICAO
CONTROLAR_SATURACAO
```

### Núcleo C — Comparação

```text
AVALIAR_AFINIDADE
AVALIAR_EFICIENCIA_DE_CUSTO
COMPARAR_INVENTARIOS
COMPARAR_PLANOS
COMPARAR_ARQUITETURAS
```

### Núcleo D — Composição

```text
SELECIONAR_PONTOS_DE_CONTATO
SELECIONAR_INVENTARIOS
DEFINIR_PAPEL_ESTRATEGICO_DOS_CANAIS
COMPOR_ARQUITETURA_DE_MIDIA
```

### Núcleo E — Orçamento e tempo

```text
VALIDAR_VIABILIDADE_ORCAMENTARIA
DISTRIBUIR_ORCAMENTO
DEFINIR_FLIGHT
DEFINIR_CONTINUIDADE
DISTRIBUIR_INSERCOES_NO_TEMPO
```

### Núcleo F — Explicação

```text
EXPLICAR_RECOMENDACAO
JUSTIFICAR_SELECAO
DIAGNOSTICAR_LIMITACAO
EXPRESSAR_NIVEL_DE_CONFIANCA
```

Este inventário é preliminar. A inclusão não significa que o problema já esteja formalizado ou implementado.

---

## 19. Estados editoriais

Estados recomendados para os objetos da Biblioteca 18:

```text
IDENTIFICADO
EM_MODELAGEM
EM_REVISAO
VALIDADO
PUBLICADO
SUSPENSO
SUBSTITUIDO
ARQUIVADO
REJEITADO
```

Para procedimentos:

```text
PROPOSTO
EM_TESTE
VALIDADO
PUBLICADO
DEPRECIADO
SUBSTITUIDO
ARQUIVADO
```

---

## 20. Versionamento e rastreabilidade

Problemas e procedimentos possuem versionamento independente.

Uma nova técnica pode gerar:

- nova relação problema–conhecimento;
- novo procedimento;
- nova versão de procedimento;
- alteração dos critérios de escolha;
- alteração do nível de automação;
- alteração da explicação.

Não deve exigir, por padrão, nova identidade para o problema.

Cada resolução registrada no projeto deve preservar:

```text
versao_do_problema
versao_dos_conhecimentos
versao_do_procedimento
parametros
entradas
regras
resultado
confianca
justificativa
data
responsavel
```

---

## 21. Limites da Biblioteca

A Biblioteca 18 não deve:

- duplicar objetivos, resultados ou indicadores da Biblioteca 15;
- duplicar jornadas, necessidades, funções ou pontos de contato da Biblioteca 16;
- armazenar fórmulas isoladas da Biblioteca 17;
- armazenar preços e condições comerciais da Biblioteca 19;
- absorver regras transversais da Biblioteca 20;
- substituir modelos reutilizáveis da Biblioteca 21;
- executar diretamente cálculos;
- incorporar decisões específicas de um projeto ao cadastro mestre;
- confundir problema com tela, módulo ou função de software;
- confundir procedimento com motor.

---

## 22. Papel no sistema especialista

O MediAd Planner deve raciocinar segundo a sequência:

```text
Identificar a situação
    ↓
Classificar o problema técnico
    ↓
Verificar pré-condições
    ↓
Recuperar conhecimentos aplicáveis
    ↓
Recuperar procedimentos possíveis
    ↓
Aplicar regras e restrições
    ↓
Selecionar ou combinar procedimentos
    ↓
Executar pelos motores
    ↓
Validar a resposta
    ↓
Explicar resultado, confiança e limitações
```

A Biblioteca 18 não torna o sistema inteligente por si só. Ela fornece uma estrutura explícita e auditável para que os motores possam mobilizar conhecimento sem acoplamento rígido a fórmulas ou algoritmos específicos.

---

## 23. Princípio consolidado

> A Biblioteca 18 organiza as perguntas técnicas do planejamento de mídia. Cada problema é definido por seu objetivo decisório, relacionado a conhecimentos e procedimentos versionados e resolvido pelos motores segundo dados, contexto, regras e confiança. Problemas permanecem estáveis; conhecimentos e métodos podem evoluir. Essa separação permite que o MediAd Planner funcione como sistema especialista explicável, extensível e rastreável.
