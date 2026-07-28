# Sistema de Bibliotecas do MediAd Planner

## 1. Finalidade

O Sistema de Bibliotecas organiza os conhecimentos reutilizáveis que sustentam o planejamento de mídia no MediAd Planner.

Seu objetivo é evitar que cada projeto reconstrua do zero conceitos, parâmetros, referências, classificações, inventários, públicos, objetivos, métricas, custos e modelos de planejamento.

As bibliotecas não substituem o julgamento do planejador. Elas fornecem objetos estruturados, versionados e rastreáveis para apoiar:

- o Perfil Estratégico;
- a Tradução Estratégica;
- a Arquitetura de Mídia;
- as Simulações;
- a Comparação de Cenários;
- a Otimização;
- o Plano Consolidado;
- o Cronograma;
- o Mapa de Veiculação.

O princípio geral é:

```text
Base de conhecimento fornece referências.
Motores processam relações.
Usuários tomam decisões.
Planos preservam as versões utilizadas.
```

---

## 2. Posição na arquitetura

```text
Catálogos
   ↓
Bibliotecas
   ↓
Relações e parâmetros
   ↓
Motores de planejamento
   ↓
Artefatos do projeto
```

O Sistema de Bibliotecas é transversal a todos os ambientes do aplicativo.

Ele não constitui uma etapa isolada do planejamento. Seus objetos são consultados, selecionados, adaptados e instanciados ao longo de todo o fluxo.

---

## 3. Distinções fundamentais

### 3.1 Catálogo

Catálogo é um vocabulário controlado utilizado para classificar objetos.

Exemplos:

- tecnologia;
- canal;
- ambiente;
- formato;
- modalidade de compra;
- unidade comercial;
- tipo de objetivo;
- categoria de KPI;
- etapa de jornada;
- unidade métrica.

Catálogos devem possuir estruturas simples, estáveis e normalizadas.

### 3.2 Biblioteca

Biblioteca é uma coleção de objetos reutilizáveis e contextualizados.

Exemplos:

- inventários;
- públicos;
- modelos de jornada;
- objetivos;
- KPIs;
- parâmetros;
- fórmulas;
- regras;
- benchmarks;
- modelos de arquitetura.

Bibliotecas podem possuir versões, fontes, escopos, validade, autoria, confiança e relações com outros objetos.

### 3.3 Relação de conhecimento

Relação de conhecimento conecta dois ou mais objetos.

Exemplos:

- inventário aderente a objetivo;
- interesse afim a ambiente;
- KPI compatível com objetivo;
- ponto de contato atendido por meio;
- formato compatível com ambiente;
- unidade compatível com modalidade de compra.

Relações não devem ser tratadas automaticamente como verdades universais. Quando necessário, devem admitir contexto, fonte, versão, território, período e nível de confiança.

### 3.4 Parâmetro

Parâmetro é um valor utilizado por regras, fórmulas ou motores.

Exemplos:

- peso de aderência;
- limite de saturação;
- frequência desejada;
- faixa de confiança;
- coeficiente de equivalência;
- tolerância de orçamento;
- fator de sobreposição.

### 3.5 Instância de projeto

Uma instância de projeto é a cópia contextual de um objeto da biblioteca utilizada em um planejamento específico.

A instância pode manter vínculo com a origem, mas deve preservar os dados efetivamente utilizados no projeto.

```text
Objeto da biblioteca
        ↓
Seleção
        ↓
Instância no projeto
        ↓
Adaptação contextual
        ↓
Uso no planejamento
```

---

## 4. Núcleos do Sistema de Bibliotecas

O sistema será composto pelos seguintes núcleos:

1. Biblioteca de Inventários de Mídia;
2. Biblioteca de Públicos e Audiências;
3. Biblioteca de Objetivos, Resultados e KPIs;
4. Biblioteca de Jornadas, Pontos de Contato e Funções;
5. Biblioteca de Parâmetros, Métricas e Fórmulas;
6. Biblioteca de Custos e Condições Comerciais;
7. Biblioteca de Regras, Restrições e Referências Metodológicas;
8. Biblioteca de Modelos e Componentes Reutilizáveis.

Cada núcleo possuirá entidades próprias. Não será criada uma tabela genérica única para armazenar todos os tipos de biblioteca.

---

## 5. Escopos

Todo objeto reutilizável deve possuir um escopo explícito.

### 5.1 Global

Disponível para todos os espaços de trabalho autorizados.

É governado pela administração do sistema.

Exemplos:

- taxonomias centrais;
- definições metodológicas;
- fórmulas oficiais;
- inventários de referência geral;
- KPIs padronizados;
- modelos validados.

### 5.2 Espaço de trabalho

Disponível apenas aos membros do espaço de trabalho ao qual pertence.

É governado pelo proprietário do espaço, respeitadas as permissões dos editores.

Exemplos:

- inventários locais;
- tabelas comerciais privadas;
- públicos proprietários;
- parâmetros internos;
- modelos da organização;
- referências de uso restrito.

### 5.3 Projeto

Disponível apenas dentro de um projeto específico.

É utilizado para informações contextuais que não devem integrar automaticamente uma biblioteca permanente.

Exemplos:

- público criado exclusivamente para uma campanha;
- inventário pontual;
- regra excepcional;
- parâmetro temporário;
- arquitetura específica.

### 5.4 Pessoal ou rascunho

Área de preparação ainda não compartilhada.

Pode ser utilizada para elaboração de propostas antes de sua submissão ao espaço ou à biblioteca global.

Itens pessoais não participam dos motores compartilhados até serem promovidos a um escopo autorizado.

---

## 6. Estados editoriais

Os objetos de biblioteca devem possuir estado editorial separado de seu estado operacional.

Estados recomendados:

```text
RASCUNHO
PROPOSTO
EM_REVISAO
VALIDADO
PUBLICADO
SUSPENSO
SUBSTITUIDO
ARQUIVADO
REJEITADO
```

### Rascunho

Objeto ainda em elaboração e visível apenas aos responsáveis autorizados.

### Proposto

Objeto submetido para avaliação.

### Em revisão

Objeto sob análise editorial, técnica ou metodológica.

### Validado

Objeto considerado consistente, mas ainda não necessariamente disponibilizado aos usuários finais.

### Publicado

Objeto liberado para utilização no escopo correspondente.

### Suspenso

Objeto temporariamente indisponível para novos usos, sem perder seu histórico.

### Substituído

Objeto sucedido por uma nova versão ou por outro objeto.

### Arquivado

Objeto preservado apenas para histórico e rastreabilidade.

### Rejeitado

Proposta não aceita. Deve permanecer rastreável quando houver necessidade de auditoria.

---

## 7. Princípio de separação de responsabilidades

A governança das bibliotecas deve preservar a distinção:

```text
CRIAR ≠ REVISAR ≠ VALIDAR ≠ PUBLICAR
```

O sistema pode permitir que uma mesma pessoa exerça mais de uma dessas ações quando suas prerrogativas autorizarem, mas as ações devem permanecer semanticamente distintas e registradas separadamente.

---

## 8. Papéis e prerrogativas

As permissões seguem o documento `11_PERFIS_DE_ACESSO_E_PERMISSOES.md`.

### 8.1 Administrador

Pode:

- criar, editar, revisar, validar, publicar, suspender, substituir e arquivar objetos globais;
- administrar catálogos globais;
- definir regras de governança;
- revisar propostas de promoção ao escopo global;
- resolver duplicidades e conflitos globais;
- executar correções administrativas auditáveis;
- administrar integrações e importações globais.

Não deve alterar silenciosamente itens já utilizados por planos consolidados.

### 8.2 Proprietário

Pode, dentro de seu espaço:

- criar e editar objetos privados;
- validar e publicar objetos na biblioteca do espaço;
- revisar contribuições de editores;
- suspender, substituir e arquivar objetos do espaço;
- promover itens de projeto para a biblioteca do espaço;
- encaminhar propostas à biblioteca global;
- definir quais membros podem atuar como revisores internos;
- administrar fontes privadas e restrições de uso.

Não pode publicar diretamente na biblioteca global, salvo quando também possuir papel administrativo global.

### 8.3 Editor

Pode, dentro de seu espaço:

- criar objetos em rascunho;
- editar objetos próprios ou objetos liberados para colaboração;
- propor novos itens para a biblioteca do espaço;
- propor atualizações ou correções;
- duplicar objetos permitidos;
- criar instâncias de projeto;
- utilizar objetos publicados;
- encaminhar sugestões de promoção global por meio do fluxo do espaço.

Não pode, por padrão:

- publicar globalmente;
- validar sua própria proposta quando a política exigir revisão independente;
- alterar catálogos globais;
- excluir definitivamente objetos utilizados;
- promover diretamente um item privado para o escopo global.

### 8.4 Leitor

Pode:

- consultar objetos publicados aos quais tenha acesso;
- utilizar objetos permitidos em relatórios ou exportações autorizadas;
- visualizar fontes, versões e notas metodológicas quando não houver restrição;
- comparar versões publicadas.

Não pode:

- criar;
- editar;
- validar;
- publicar;
- suspender;
- substituir;
- arquivar;
- promover objetos.

---

## 9. Inclusão de informações nas bibliotecas

Toda inclusão deve declarar, no mínimo:

- tipo de objeto;
- nome ou título;
- escopo;
- autor da inclusão;
- estado editorial;
- fonte, quando aplicável;
- data da fonte;
- território ou praça, quando aplicável;
- período de validade, quando aplicável;
- unidade, quando aplicável;
- natureza do dado;
- nível de confiança;
- restrições de uso;
- observações metodológicas.

O sistema deve impedir a publicação de itens que não atendam aos campos obrigatórios de seu domínio.

---

## 10. Natureza dos dados

Os valores associados aos objetos devem indicar sua natureza.

Categorias recomendadas:

- observado;
- declarado;
- fornecido comercialmente;
- benchmark;
- estimado;
- calculado;
- convertido;
- modelado;
- inferido;
- recomendado;
- padrão do sistema.

A natureza do dado deve acompanhar o valor até seu uso em uma simulação ou plano.

---

## 11. Proveniência

Proveniência representa a origem e o percurso do conhecimento.

Cada objeto ou versão deve poder registrar:

- fonte original;
- responsável pela coleta;
- método de coleta;
- data de obtenção;
- documento ou referência de suporte;
- transformações realizadas;
- unidades originais;
- conversões;
- revisor;
- validador;
- publicador;
- data de publicação.

Quando um valor for derivado, sua linhagem deve apontar para os dados de origem e para a regra ou fórmula utilizada.

---

## 12. Confiança

Objetos e valores podem possuir um nível de confiança.

A confiança não deve ser confundida com aderência ou desempenho.

Ela informa a qualidade esperada da informação com base em fatores como:

- autoridade da fonte;
- atualidade;
- completude;
- método;
- consistência;
- possibilidade de verificação;
- abrangência territorial;
- compatibilidade temporal.

O modelo poderá utilizar:

- escala categórica;
- escala numérica;
- justificativa textual;
- critérios decomponíveis.

A definição final da escala será tratada na Biblioteca de Parâmetros, Métricas e Fórmulas.

---

## 13. Versionamento

Objetos publicados não devem ser sobrescritos de forma destrutiva.

Alterações relevantes devem gerar nova versão.

Uma versão deve registrar:

- identificador do objeto;
- número ou código da versão;
- estado;
- vigência;
- autor;
- motivo da alteração;
- versão anterior;
- diferenças relevantes;
- data de publicação.

Correções meramente ortográficas podem seguir política simplificada, desde que não alterem o sentido ou os valores utilizados.

---

## 14. Vigência e temporalidade

Objetos sujeitos a mudança devem permitir:

- início de vigência;
- fim de vigência;
- data de referência;
- data da coleta;
- periodicidade esperada de revisão.

Exemplos:

- preços;
- audiências;
- benchmarks;
- taxas;
- limites regulatórios;
- condições comerciais;
- parâmetros de mercado.

Um objeto vencido pode permanecer consultável, mas deve ser sinalizado e não deve ser selecionado automaticamente sem justificativa.

---

## 15. Territorialidade

Objetos podem possuir abrangência:

- global;
- nacional;
- regional;
- estadual;
- municipal;
- por praça;
- por cobertura de veículo;
- por área personalizada.

A abrangência territorial deve ser separada do escopo de acesso.

Um objeto pode ser global quanto ao acesso e municipal quanto à validade territorial.

---

## 16. Compartilhamento e promoção

A promoção entre escopos deve seguir fluxo controlado.

```text
Rascunho pessoal
        ↓
Projeto
        ↓
Biblioteca do espaço
        ↓
Proposta global
        ↓
Revisão administrativa
        ↓
Biblioteca global
```

A promoção não precisa mover o objeto original. Pode gerar cópia vinculada ou nova versão com proveniência preservada.

O objeto promovido deve indicar:

- origem;
- responsável pela promoção;
- adaptações realizadas;
- escopo anterior;
- escopo novo;
- data;
- decisão editorial.

---

## 17. Duplicação, equivalência e conflitos

O sistema deve apoiar a identificação de:

- duplicatas exatas;
- duplicatas prováveis;
- sinônimos;
- variações regionais;
- objetos relacionados;
- objetos substitutos;
- versões concorrentes.

Objetos semelhantes não devem ser fundidos automaticamente quando diferenças contextuais forem relevantes.

A resolução pode resultar em:

- manutenção separada;
- vinculação como equivalentes;
- definição de sinônimo;
- substituição;
- fusão editorial;
- rejeição da proposta.

---

## 18. Arquivamento e exclusão

A regra geral é:

```text
Objeto utilizado não é apagado; é versionado, suspenso, substituído ou arquivado.
```

A exclusão física deve ser restrita a:

- rascunhos sem dependências;
- registros criados por engano;
- dados de teste;
- situações administrativas excepcionais.

Qualquer exclusão física relevante deve gerar registro de auditoria.

---

## 19. Preservação nos planejamentos

Quando um objeto de biblioteca for utilizado em um planejamento, o sistema deve preservar:

- identificador do objeto de origem;
- versão utilizada;
- valores efetivamente aplicados;
- parâmetros modificados no projeto;
- data da seleção;
- responsável pela seleção.

Mudanças posteriores na biblioteca não devem alterar silenciosamente planejamentos existentes.

O sistema poderá oferecer atualização assistida, com comparação entre a versão utilizada e a versão mais recente.

---

## 20. Relação entre objeto-base e adaptação de projeto

O uso de um item de biblioteca não deve impedir adaptação contextual.

```text
Objeto publicado
        ↓
Instância do projeto
        ↓
Ajustes autorizados
        ↓
Registro das diferenças
```

A instância deve indicar se está:

- idêntica à origem;
- parcialmente adaptada;
- desvinculada;
- substituída por objeto próprio do projeto.

---

## 21. Pesquisa, filtros e descoberta

Todas as bibliotecas devem oferecer mecanismos compatíveis de descoberta:

- busca textual;
- filtros por categoria;
- filtros por escopo;
- filtros por estado;
- filtros por território;
- filtros por vigência;
- filtros por fonte;
- filtros por confiança;
- ordenação;
- favoritos;
- itens recentes;
- itens mais utilizados;
- relações sugeridas.

A relevância dos resultados deve considerar contexto, sem ocultar a origem e o escopo dos itens.

---

## 22. Importação e exportação

O sistema poderá admitir:

- inclusão manual;
- importação tabular;
- importação por integração;
- duplicação controlada;
- publicação administrativa;
- exportação de catálogos e bibliotecas.

Toda importação deve passar por:

1. validação estrutural;
2. normalização;
3. identificação de duplicidades;
4. verificação de obrigatoriedade;
5. atribuição de proveniência;
6. definição de estado editorial;
7. revisão antes da publicação, quando necessária.

---

## 23. Auditoria

Devem ser auditáveis:

- criação;
- edição;
- proposta;
- revisão;
- validação;
- publicação;
- suspensão;
- substituição;
- arquivamento;
- promoção de escopo;
- alteração de fonte;
- alteração de vigência;
- mudança de confiança;
- uso em planejamento;
- exclusão excepcional.

O registro deve identificar usuário, data, ação, objeto, versão e contexto.

---

## 24. Relação com os motores

Os motores devem consumir apenas objetos:

- acessíveis no espaço ativo;
- compatíveis com o contexto;
- publicados ou explicitamente autorizados;
- vigentes ou selecionados com justificativa;
- tecnicamente completos;
- vinculados à versão utilizada.

O motor não deve transformar automaticamente uma sugestão, um rascunho ou uma proposta não validada em referência geral.

---

## 25. Transparência das recomendações

Quando uma recomendação depender de objetos das bibliotecas, o sistema deve ser capaz de explicar:

- quais objetos foram utilizados;
- quais versões;
- quais relações;
- quais parâmetros;
- quais fontes;
- quais valores foram adaptados;
- quais restrições foram aplicadas.

A explicabilidade deve acompanhar o resultado sem expor dados privados a usuários não autorizados.

---

## 26. Princípios de interface

A interface das bibliotecas deve distinguir claramente:

- consultar;
- usar no projeto;
- duplicar;
- editar;
- propor alteração;
- publicar;
- arquivar.

Também deve sinalizar:

- escopo;
- estado;
- vigência;
- fonte;
- confiança;
- versão;
- restrição de uso;
- existência de versão mais recente.

---

## 27. Critérios comuns de qualidade

Um objeto de biblioteca deve ser avaliado, conforme seu domínio, por:

- clareza;
- unicidade;
- completude;
- consistência;
- atualidade;
- rastreabilidade;
- compatibilidade;
- utilidade;
- reprodutibilidade;
- adequação territorial;
- adequação temporal.

---

## 28. Dependências entre bibliotecas

As bibliotecas não são independentes.

```text
Objetivos e KPIs
        ↓
Jornadas e funções
        ↓
Públicos e audiências
        ↓
Inventários
        ↓
Custos, métricas e parâmetros
        ↓
Regras e modelos
```

As relações devem ser explícitas e normalizadas, evitando duplicação de definições em núcleos diferentes.

---

## 29. Limites

O Sistema de Bibliotecas:

- não substitui a elaboração estratégica;
- não transforma benchmarks em metas universais;
- não converte relações contextuais em verdades absolutas;
- não atualiza silenciosamente planos existentes;
- não permite que usuários publiquem além de suas prerrogativas;
- não mistura escopo de acesso com abrangência territorial;
- não confunde catálogo, biblioteca, relação e parâmetro;
- não acompanha resultados posteriores à execução da campanha.

---

## 30. Síntese

```text
Catálogos definem a linguagem.
Bibliotecas preservam objetos reutilizáveis.
Relações conectam conhecimentos.
Parâmetros orientam cálculos.
Motores processam alternativas.
Usuários decidem.
Projetos preservam o contexto e a versão utilizada.
```

Este documento estabelece as regras transversais. Cada biblioteca específica deverá detalhar suas entidades, relações, campos obrigatórios, fluxos editoriais, permissões, usos nos motores e critérios próprios de qualidade.
