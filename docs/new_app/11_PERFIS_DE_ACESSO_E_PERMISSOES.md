# Perfis de Acesso, Permissões e Governança de Bibliotecas

## 1. Finalidade

Este documento define o modelo de identidade, acesso, autoridade, colaboração e governança de dados do **MediAd Planner**.

Ele estabelece:

- quem pode acessar o sistema;
- em qual contexto o acesso ocorre;
- quais papéis podem ser exercidos;
- quais recursos cada papel pode consultar ou modificar;
- quais decisões cada papel pode tomar;
- como funcionam autoria, aprovação e rastreabilidade;
- como são administradas as bibliotecas do sistema;
- quem pode incluir, editar, validar, publicar, arquivar ou excluir informações dessas bibliotecas.

O controle de acesso deve preservar simultaneamente:

- isolamento entre espaços de trabalho;
- princípio do menor privilégio;
- clareza de autoria;
- integridade metodológica;
- rastreabilidade das decisões;
- separação entre conteúdo global e conteúdo privado;
- possibilidade de uso profissional e didático.

Formulação central:

> O acesso ao MediAd Planner é determinado pela identidade do usuário, por sua membresia em um espaço de trabalho, pelo papel exercido nesse espaço e pelas permissões associadas aos recursos e ações disponíveis.

---

## 2. Escopo funcional

O sistema é um ambiente de planejamento de mídia.

O fluxo principal termina na elaboração e consolidação do plano:

```text
Perfil Estratégico
        ↓
Arquitetura de Mídia
        ↓
Simulação
        ↓
Comparação
        ↓
Otimização
        ↓
Seleção
        ↓
Plano Consolidado
        ├── Cronograma de Mídia
        └── Mapa de Veiculação
```

Os perfis e permissões definidos neste documento incidem sobre esse fluxo e sobre os recursos que o sustentam, especialmente:

- projetos;
- briefings;
- perfis estratégicos;
- arquiteturas;
- cenários;
- simulações;
- comparações;
- otimizações;
- planos consolidados;
- cronogramas;
- mapas de veiculação;
- relatórios;
- bibliotecas;
- catálogos;
- parâmetros;
- membros e espaços de trabalho.

O sistema não contempla permissões relativas à execução posterior da campanha, tais como comprovação de veiculação, faturamento, pagamento ou avaliação de resultados realizados.

---

## 3. Princípios do modelo de acesso

### 3.1 Identidade não é papel

A identidade representa a pessoa autenticada.

O papel representa a autoridade que essa pessoa possui em determinado contexto.

```text
Usuário
   ↓
Perfil pessoal
   ↓
Membresia
   ↓
Espaço de trabalho
   ↓
Papel no espaço
   ↓
Permissões
```

Uma mesma pessoa pode possuir papéis diferentes em espaços distintos.

Exemplo:

```text
Usuário A
├── Espaço Agência Alfa → PROPRIETÁRIO
├── Espaço Disciplina 2026 → EDITOR
└── Espaço Cliente Beta → LEITOR
```

### 3.2 O espaço de trabalho é a unidade de isolamento

Projetos, planejamentos, artefatos e bibliotecas privadas pertencem a um espaço de trabalho.

Nenhum usuário comum deve acessar dados de outro espaço sem membresia válida.

### 3.3 Permissão deve ser explícita

A ausência de autorização explícita implica negação.

### 3.4 Menor privilégio

Cada usuário deve receber apenas as permissões necessárias para sua atuação.

### 3.5 Autoria e decisão não podem ser apagadas

O sistema deve registrar:

- quem criou;
- quem alterou;
- quem revisou;
- quem aprovou;
- quem publicou;
- quando cada ação ocorreu;
- qual versão foi afetada.

### 3.6 Administração não equivale a autoria metodológica

Um administrador pode intervir tecnicamente, mas não deve aparecer como autor de uma decisão estratégica sem ter realizado essa ação no fluxo normal do planejamento.

### 3.7 Bibliotecas exigem governança própria

Consultar uma biblioteca não implica poder alterá-la.

Usar um item em um planejamento não implica poder editar sua fonte.

Propor uma contribuição não implica poder publicá-la globalmente.

---

## 4. Entidades de identidade e acesso

### 4.1 Usuário

Representa a identidade autenticada.

Campos conceituais mínimos:

```text
usuario
├── id
├── nome
├── email
├── ativo
├── criado_em
├── ultimo_acesso
├── trocar_senha
└── administrador_global
```

### 4.2 Perfil pessoal

Contém informações da pessoa, preferências e metadados que não definem, por si sós, autorização sobre espaços.

### 4.3 Espaço de trabalho

É o domínio organizacional no qual projetos e bibliotecas privadas são mantidos.

Pode representar:

- agência;
- empresa;
- cliente;
- equipe;
- disciplina;
- turma;
- laboratório;
- projeto institucional;
- ambiente individual.

### 4.4 Membresia

É a relação entre usuário e espaço.

```text
membresia
├── usuario_id
├── espaco_id
├── papel
├── ativo
├── convidado_por
├── criado_em
└── encerrado_em
```

### 4.5 Papel

Define o conjunto básico de prerrogativas.

Papéis principais:

```text
ADMINISTRADOR
PROPRIETARIO
EDITOR
LEITOR
```

O papel `ADMINISTRADOR` é global.

Os papéis `PROPRIETARIO`, `EDITOR` e `LEITOR` são exercidos dentro de uma membresia em um espaço.

---

## 5. Papéis de acesso

## 5.1 ADMINISTRADOR

Papel global do sistema.

### Prerrogativas

Pode:

- criar, ativar, inativar e administrar contas;
- redefinir acesso e senha temporária;
- criar, ativar, inativar e administrar espaços;
- atribuir ou substituir proprietários;
- acessar espaços para suporte, auditoria, manutenção ou recuperação;
- administrar configurações sistêmicas;
- administrar catálogos globais;
- administrar bibliotecas globais;
- validar e publicar contribuições globais;
- arquivar ou retirar de publicação itens globais;
- consultar trilhas de auditoria;
- executar operações administrativas excepcionais;
- corrigir vínculos inválidos ou restaurar acesso.

### Limites

Não deve:

- alterar silenciosamente conteúdo metodológico de um planejamento;
- assumir autoria de decisões produzidas por outro usuário;
- publicar contribuições sem rastreabilidade;
- usar acesso excepcional sem registro de motivo;
- transformar conteúdo privado em global sem processo de revisão;
- remover definitivamente conteúdo referenciado por planejamentos sem preservar histórico.

### Acesso a espaços

O administrador pode acessar espaços ativos para fins administrativos, mas toda intervenção deve ser identificada como ação administrativa excepcional.

---

## 5.2 PROPRIETARIO

Responsável pela administração de um espaço de trabalho.

### Prerrogativas gerais

Pode:

- editar as configurações do espaço;
- convidar membros;
- ativar ou remover membresias;
- atribuir os papéis `EDITOR` e `LEITOR`;
- atribuir outro `PROPRIETARIO`, conforme regras do sistema;
- criar, editar, duplicar, arquivar e excluir projetos;
- acessar todos os projetos do espaço;
- restaurar itens arquivados;
- administrar bibliotecas privadas do espaço;
- consolidar e aprovar planos;
- exportar artefatos;
- consultar autoria e histórico;
- transferir propriedade do espaço, quando permitido;
- definir regras locais de contribuição para bibliotecas;
- encaminhar itens privados como proposta de inclusão global.

### Limites

Não pode:

- administrar contas globais;
- acessar espaços dos quais não seja membro;
- alterar parâmetros sistêmicos protegidos;
- publicar diretamente em bibliotecas globais;
- conceder o papel global de administrador;
- remover a rastreabilidade de contribuições;
- transformar um item global em privado;
- editar a fonte de um item global apenas porque o utilizou em um projeto.

---

## 5.3 EDITOR

Perfil responsável pela elaboração e manutenção do planejamento.

### Prerrogativas de planejamento

Pode:

- criar e editar projetos;
- elaborar briefings;
- construir Perfis Estratégicos;
- elaborar Arquiteturas de Mídia;
- criar cenários;
- executar simulações;
- comparar alternativas;
- propor e aplicar otimizações;
- selecionar cenários;
- elaborar o Plano Consolidado;
- gerar Cronograma de Mídia;
- gerar Mapa de Veiculação;
- duplicar projetos e artefatos;
- criar versões;
- exportar relatórios permitidos;
- consultar bibliotecas globais e privadas autorizadas;
- utilizar itens de biblioteca em planejamentos;
- criar itens em bibliotecas privadas, conforme política do espaço;
- propor alterações ou novos itens para revisão do proprietário;
- encaminhar contribuições candidatas à biblioteca global, quando permitido.

### Limites

Não pode:

- administrar membros;
- alterar propriedade do espaço;
- excluir o espaço;
- modificar configurações globais;
- publicar diretamente em biblioteca global;
- aprovar a própria contribuição global quando revisão independente for exigida;
- alterar itens globais em uso por outros espaços;
- excluir definitivamente itens privados referenciados por planejamentos consolidados;
- conceder permissões;
- acessar projetos de outros espaços.

---

## 5.4 LEITOR

Perfil de consulta.

### Prerrogativas

Pode:

- visualizar projetos autorizados;
- consultar briefings e Perfis Estratégicos;
- visualizar Arquiteturas de Mídia;
- consultar cenários, simulações e comparações;
- visualizar otimizações e decisões registradas;
- consultar Planos Consolidados;
- visualizar Cronogramas e Mapas de Veiculação;
- consultar bibliotecas permitidas;
- visualizar metadados e fontes dos itens de biblioteca;
- exportar relatórios quando essa ação estiver habilitada;
- navegar por versões existentes.

### Limites

Não pode:

- criar ou editar projetos;
- recalcular simulações;
- selecionar cenários;
- consolidar ou aprovar planos;
- criar, editar, publicar ou excluir itens de biblioteca;
- administrar membros;
- alterar parâmetros;
- arquivar ou excluir conteúdo;
- transformar uma visualização em nova versão oficial.

---

## 6. Papéis metodológicos

Papéis metodológicos descrevem a função exercida no processo, mas não substituem os papéis de acesso.

Exemplos:

```text
PLANEJADOR
REVISOR
APROVADOR
OBSERVADOR
DOCENTE
ESTUDANTE
CLIENTE
CONSULTOR
```

Esses rótulos podem ser atribuídos a membros ou participantes de um projeto.

Exemplos:

- um docente pode ser `PROPRIETARIO` do espaço e `APROVADOR` do projeto;
- um estudante pode ser `EDITOR` do espaço e `PLANEJADOR` do projeto;
- um cliente pode ser `LEITOR` do espaço e `APROVADOR` do plano;
- um consultor pode ser `EDITOR` e `REVISOR`.

Regra:

```text
papel de acesso = autoridade sistêmica
papel metodológico = função no processo
```

---

## 7. Recursos protegidos

As permissões devem incidir sobre os seguintes grupos de recursos:

### 7.1 Administração

- usuários;
- perfis;
- espaços;
- membresias;
- convites;
- configurações;
- trilhas de auditoria.

### 7.2 Planejamento

- projetos;
- briefings;
- Perfis Estratégicos;
- Arquiteturas;
- cenários;
- simulações;
- comparações;
- otimizações;
- seleções;
- Planos Consolidados;
- Cronogramas;
- Mapas de Veiculação;
- relatórios;
- versões.

### 7.3 Bibliotecas e catálogos

- meios;
- canais;
- veículos;
- inventários;
- formatos;
- unidades comerciais;
- públicos;
- segmentos;
- universos;
- praças;
- jornadas;
- pontos de contato;
- funções de mídia;
- objetivos;
- KPIs;
- parâmetros;
- coeficientes;
- custos de referência;
- regras comerciais;
- cenários-modelo;
- templates;
- fontes e evidências.

---

## 8. Ações normalizadas

As ações devem ser tratadas de forma consistente:

```text
CONSULTAR
CRIAR
EDITAR
DUPLICAR
SIMULAR
COMPARAR
OTIMIZAR
SELECIONAR
CONSOLIDAR
APROVAR
EXPORTAR
PUBLICAR
ARQUIVAR
RESTAURAR
EXCLUIR
ADMINISTRAR
PROPOR
REVISAR
VALIDAR
```

Nem todo recurso aceita todas as ações.

Exemplo:

- uma biblioteca aceita `PROPOR`, `REVISAR`, `VALIDAR` e `PUBLICAR`;
- uma simulação aceita `CRIAR`, `EXECUTAR`, `DUPLICAR` e `CONSULTAR`;
- um espaço aceita `ADMINISTRAR`, `ARQUIVAR` e `TRANSFERIR`.

---

## 9. Matriz geral de permissões

Legenda:

```text
✓ permitido
C condicionado
— não permitido
```

| Recurso ou ação | Administrador | Proprietário | Editor | Leitor |
|---|---:|---:|---:|---:|
| Administrar contas | ✓ | — | — | — |
| Criar espaço | ✓ | C | — | — |
| Administrar espaço | ✓ | ✓ | — | — |
| Administrar membros | ✓ | ✓ | — | — |
| Criar projeto | ✓ | ✓ | ✓ | — |
| Editar projeto | ✓ | ✓ | ✓ | — |
| Arquivar projeto | ✓ | ✓ | C | — |
| Excluir projeto | ✓ | ✓ | C | — |
| Criar briefing | ✓ | ✓ | ✓ | — |
| Criar Perfil Estratégico | ✓ | ✓ | ✓ | — |
| Criar Arquitetura | ✓ | ✓ | ✓ | — |
| Simular | ✓ | ✓ | ✓ | — |
| Comparar | ✓ | ✓ | ✓ | — |
| Otimizar | ✓ | ✓ | ✓ | — |
| Selecionar cenário | ✓ | ✓ | ✓ | — |
| Consolidar plano | ✓ | ✓ | C | — |
| Aprovar plano | ✓ | ✓ | C | — |
| Visualizar plano | ✓ | ✓ | ✓ | ✓ |
| Exportar | ✓ | ✓ | ✓ | C |
| Consultar biblioteca global | ✓ | ✓ | ✓ | ✓ |
| Publicar em biblioteca global | ✓ | — | — | — |
| Propor item global | ✓ | ✓ | ✓ | — |
| Administrar biblioteca privada | ✓ | ✓ | C | — |
| Criar item privado | ✓ | ✓ | ✓ | — |
| Editar item privado | ✓ | ✓ | ✓ | — |
| Excluir item privado | ✓ | ✓ | C | — |

As condições específicas devem ser configuradas por política do espaço e estado do recurso.

---

## 10. Governança das bibliotecas

## 10.1 Conceito

Bibliotecas são conjuntos estruturados de informações reutilizáveis que sustentam o planejamento.

Elas não são simples listas auxiliares.

Podem conter dados com diferentes níveis de autoridade, origem, validade e compartilhamento.

Toda entrada de biblioteca deve responder:

```text
Quem criou?
Qual é a fonte?
A quem pertence?
Quem pode usar?
Quem pode editar?
Quem validou?
Qual é a validade?
Qual é o estado?
Em quais planejamentos foi utilizada?
```

---

## 10.2 Escopos de biblioteca

### Biblioteca global

Disponível para todos os espaços autorizados.

Contém itens institucionais, metodológicos ou de referência comum.

Exemplos:

- categorias de meios;
- tipos de canais;
- KPIs oficiais;
- unidades padronizadas;
- funções de mídia;
- classificações comuns;
- fórmulas protegidas;
- templates oficiais;
- parâmetros sistêmicos;
- inventários de referência publicados.

### Biblioteca privada do espaço

Pertence a um espaço específico.

Pode conter:

- veículos locais;
- inventários próprios;
- tabelas de preço;
- públicos internos;
- coeficientes locais;
- cenários-modelo;
- templates do espaço;
- regras comerciais;
- parâmetros privados;
- fornecedores;
- dados de pesquisa;
- fontes licenciadas.

### Biblioteca de projeto

Contém itens criados ou adaptados para um projeto específico.

Esses itens podem permanecer restritos ao projeto ou ser promovidos à biblioteca privada do espaço mediante aprovação.

### Biblioteca pessoal temporária

Pode existir como área de rascunho individual, sem autoridade institucional.

Itens pessoais não devem ser usados como referência oficial sem promoção explícita para projeto ou espaço.

---

## 10.3 Hierarquia de escopos

```text
Biblioteca Global
        ↓ disponível para consulta
Biblioteca do Espaço
        ↓ reutilizável internamente
Biblioteca do Projeto
        ↓ contextual
Rascunho Pessoal
```

A hierarquia não implica edição ascendente automática.

Um usuário pode copiar ou derivar um item global para um contexto privado quando a política permitir, mas não altera a fonte global.

---

## 10.4 Estados dos itens de biblioteca

```text
RASCUNHO
PROPOSTO
EM_REVISAO
VALIDADO
PUBLICADO
REJEITADO
SUSPENSO
ARQUIVADO
SUBSTITUIDO
```

### RASCUNHO

Visível apenas ao autor e a perfis autorizados do mesmo contexto.

### PROPOSTO

Encaminhado para revisão.

### EM_REVISAO

Submetido a análise metodológica, técnica ou administrativa.

### VALIDADO

Aprovado quanto ao conteúdo, mas ainda não necessariamente publicado.

### PUBLICADO

Disponível para uso no escopo correspondente.

### REJEITADO

Não aprovado. Deve preservar justificativa e autoria.

### SUSPENSO

Temporariamente indisponível para novos usos.

### ARQUIVADO

Mantido para histórico, sem oferta padrão em novas seleções.

### SUBSTITUIDO

Preservado porque já foi utilizado, mas vinculado a uma versão sucessora.

---

## 10.5 Prerrogativas sobre bibliotecas globais

### Administrador

Pode:

- criar itens globais;
- revisar contribuições;
- validar;
- publicar;
- suspender;
- arquivar;
- substituir;
- corrigir metadados;
- administrar taxonomias;
- definir campos obrigatórios;
- definir políticas de validade;
- controlar versões;
- vincular fontes;
- resolver duplicidades.

### Proprietário

Pode:

- consultar;
- utilizar;
- copiar para o espaço quando permitido;
- propor novo item global;
- propor correção;
- propor atualização;
- acompanhar a revisão;
- retirar uma proposta ainda não analisada.

Não pode publicar diretamente.

### Editor

Pode:

- consultar;
- utilizar;
- propor novo item;
- propor correção;
- anexar fonte;
- responder a pedidos de ajuste;
- acompanhar o estado da proposta.

Não pode validar ou publicar a própria contribuição global.

### Leitor

Pode consultar itens publicados e seus metadados.

Não pode propor ou editar.

---

## 10.6 Prerrogativas sobre bibliotecas privadas do espaço

### Proprietário

Pode:

- criar;
- editar;
- revisar;
- validar;
- publicar no espaço;
- suspender;
- arquivar;
- excluir quando não houver dependência;
- promover item de projeto para o espaço;
- encaminhar item como proposta global;
- definir quem pode contribuir;
- definir revisão obrigatória;
- transferir responsabilidade por uma biblioteca.

### Editor

Pode, por padrão:

- criar item privado;
- editar itens próprios em rascunho;
- propor publicação no espaço;
- utilizar itens publicados;
- copiar itens permitidos;
- anexar fontes;
- atualizar validade;
- propor substituição.

Pode editar itens publicados somente quando a política do espaço permitir e sem sobrescrever versões já utilizadas.

### Leitor

Pode consultar e utilizar apenas por meio dos planejamentos aos quais tenha acesso.

Não pode contribuir.

### Administrador

Pode intervir para suporte, recuperação ou integridade, com registro de ação excepcional.

---

## 10.7 Inclusão de informações nas bibliotecas

Toda inclusão deve exigir, conforme o tipo de item:

- título ou nome;
- categoria;
- escopo;
- descrição;
- origem;
- fonte;
- data de referência;
- data de validade;
- território;
- público aplicável;
- unidade;
- metodologia;
- responsável;
- grau de confiança;
- restrições de uso;
- situação de licenciamento;
- estado editorial;
- versão.

Fluxo recomendado:

```text
Criação
   ↓
Rascunho
   ↓
Proposta
   ↓
Revisão
   ↓
Validação
   ↓
Publicação
   ↓
Uso em planejamentos
   ↓
Atualização ou substituição
```

Nenhum item deve ser publicado globalmente sem:

- fonte identificada;
- autor identificado;
- revisão registrada;
- escopo definido;
- validade definida quando aplicável;
- ausência de conflito evidente;
- versionamento.

---

## 10.8 Separação entre criar, validar e publicar

As ações devem ser independentes:

```text
CRIAR ≠ VALIDAR ≠ PUBLICAR
```

Um mesmo usuário pode acumular ações em bibliotecas privadas pequenas, conforme política do espaço.

Nas bibliotecas globais, recomenda-se separação mínima entre autoria e publicação.

Exemplo:

```text
Editor cria proposta
        ↓
Proprietário revisa o contexto
        ↓
Administrador valida e publica globalmente
```

---

## 10.9 Uso de itens de biblioteca em planejamentos

Quando um item é utilizado em um planejamento, o sistema deve registrar uma referência versionada.

```text
Item de biblioteca
        ↓
Versão utilizada
        ↓
Referência no planejamento
```

A atualização posterior do item não deve alterar silenciosamente um planejamento já consolidado.

O sistema pode oferecer:

- manter a versão usada;
- revisar a atualização;
- substituir conscientemente;
- recalcular artefatos afetados;
- registrar a decisão.

---

## 10.10 Edição, exclusão e dependências

Um item referenciado não deve ser apagado fisicamente de modo a destruir a reprodutibilidade.

Regras:

- item sem uso pode ser excluído conforme permissão;
- item em uso deve ser arquivado ou substituído;
- correções relevantes geram nova versão;
- alteração de fórmula ou unidade exige versão nova;
- alteração apenas editorial pode manter versão, conforme política;
- dependências devem ser exibidas antes da ação;
- exclusão global exige privilégio administrativo;
- exclusão privada exige proprietário ou autorização específica.

---

## 10.11 Proveniência e confiança

Cada item deve registrar sua proveniência.

```text
proveniencia
├── fonte
├── autor_da_fonte
├── coletado_por
├── data_de_coleta
├── metodo
├── territorio
├── periodo
├── licenca
├── confianca
└── observacoes
```

A confiança pode ser representada por classificação, escala ou combinação de critérios.

Exemplos:

- oficial;
- auditada;
- declarada pelo fornecedor;
- estimada;
- modelada;
- sem validação externa.

O nível de confiança não substitui a fonte.

---

## 10.12 Bibliotecas globais protegidas

Algumas bibliotecas devem possuir proteção reforçada.

Exemplos:

- fórmulas oficiais;
- unidades;
- categorias estruturais;
- regras de cálculo;
- tipos de KPI;
- taxonomias centrais;
- estados do fluxo;
- políticas de acesso.

Esses itens podem ser consultados por todos, mas alterados apenas por administração autorizada e mediante nova versão sistêmica.

---

## 11. Aprovação e autoridade decisória

A capacidade de editar não implica necessariamente poder aprovar.

O sistema deve permitir distinguir:

```text
autor
editor
revisor
aprovador
proprietário
```

A aprovação pode ser configurável por espaço ou projeto.

Exemplos:

- espaço individual: proprietário cria e aprova;
- equipe profissional: editor elabora, proprietário aprova;
- ambiente didático: estudante elabora, docente aprova;
- trabalho para cliente: planejador elabora, cliente consulta e registra aceite.

O aceite metodológico não deve alterar o papel de acesso.

---

## 12. Regras de autoria e versionamento

Toda entidade relevante deve registrar:

```text
criado_por
criado_em
alterado_por
alterado_em
versao
estado
origem
```

Ações críticas devem registrar também:

```text
motivo
antes
Depois
contexto
```

A consolidação de um plano deve congelar referências essenciais.

Edições posteriores devem gerar nova versão ou reabrir o estado de elaboração.

---

## 13. Estados do planejamento e prerrogativas

Estados recomendados:

```text
RASCUNHO
EM_ELABORACAO
SIMULADO
COMPARADO
OTIMIZADO
SELECIONADO
CONSOLIDADO
APROVADO
ARQUIVADO
```

Regras gerais:

- leitores apenas consultam;
- editores atuam até a consolidação conforme política;
- proprietários podem consolidar, aprovar e reabrir;
- administradores só intervêm excepcionalmente;
- um plano aprovado não deve ser alterado sem nova versão;
- arquivamento não elimina histórico.

---

## 14. Cadastro, convite e ativação

O sistema não deve possuir cadastro público irrestrito por padrão.

Formas previstas:

- criação administrativa;
- convite por proprietário;
- criação vinculada a instituição;
- importação controlada de turma ou equipe.

Fluxo:

```text
Convite ou criação
        ↓
Conta pendente
        ↓
Senha temporária ou definição inicial
        ↓
Troca obrigatória de senha
        ↓
Ativação
        ↓
Membresia válida
```

Contas inativas não acessam recursos privados.

---

## 15. Seleção de espaço ativo

Após autenticação:

- um único espaço pode ser selecionado automaticamente;
- múltiplos espaços exigem escolha;
- o contexto deve ser revalidado;
- troca de espaço limpa seleções privadas anteriores;
- projeto, briefing, plano e resultados derivados não devem permanecer em memória após troca;
- o identificador do espaço deve ser imposto pelo contexto autorizado, não pelo payload do usuário.

---

## 16. Perda ou encerramento de acesso

Quando uma membresia é encerrada:

- o usuário perde acesso imediato ao espaço;
- sua autoria histórica permanece;
- seus itens não são transferidos silenciosamente;
- rascunhos podem ser reassociados conforme política;
- propostas pendentes permanecem identificadas;
- sessões ativas devem ser invalidadas ou revalidadas;
- arquivos exportados anteriormente não podem ser recolhidos pelo sistema.

A remoção de um usuário não apaga suas contribuições históricas.

---

## 17. Transferência de propriedade

A transferência de propriedade deve:

- exigir proprietário atual ou administrador;
- garantir ao menos um proprietário ativo;
- registrar origem, destino, data e motivo;
- preservar histórico;
- não alterar autoria de projetos e bibliotecas;
- revogar prerrogativas anteriores conforme decisão explícita.

---

## 18. Exclusão, arquivamento e restauração

Preferência:

```text
arquivar antes de excluir
```

### Arquivamento

Mantém histórico, referências e rastreabilidade.

### Exclusão lógica

Remove da operação comum sem apagar dependências.

### Exclusão física

Deve ser restrita a:

- dados sem dependência;
- dados de teste;
- exigência legal;
- operação administrativa controlada.

---

## 19. Compartilhamento e exportação

Compartilhar dentro do sistema deve respeitar espaços e papéis.

Exportar produz uma cópia externa que deixa de ser controlada pelo sistema.

O sistema deve registrar:

- quem exportou;
- qual artefato;
- qual versão;
- quando;
- em qual formato.

Itens de biblioteca com restrição de licenciamento podem impedir exportação ou exigir aviso.

---

## 20. Auditoria

A trilha de auditoria deve registrar ações críticas, especialmente:

- login e logout;
- criação e inativação de conta;
- criação e transferência de espaço;
- alteração de papel;
- acesso administrativo excepcional;
- criação, revisão e publicação de item de biblioteca;
- alteração de fórmula ou parâmetro;
- consolidação e aprovação de plano;
- arquivamento e exclusão;
- exportação de artefato.

A auditoria deve ser consultável por administradores e, em seu próprio espaço, por proprietários conforme política.

---

## 21. Regras de segurança

- autenticação obrigatória para conteúdo privado;
- ausência de cadastro público por padrão;
- tokens isolados por sessão;
- invalidação no logout;
- renovação controlada;
- bloqueio de contas inativas;
- troca obrigatória de senha temporária;
- proibição de autopromoção;
- isolamento por espaço;
- validação do contexto em todas as operações;
- negação por padrão;
- proteção reforçada para bibliotecas globais;
- impossibilidade de mudar registro entre espaços sem operação autorizada;
- preservação de autoria.

---

## 22. Regras para implementação futura das bibliotecas

A construção das bibliotecas deverá respeitar este modelo desde o início.

Requisitos mínimos:

1. todo item possui `escopo`;
2. todo item possui `estado`;
3. todo item possui `autor`;
4. todo item possui `fonte` quando aplicável;
5. todo item possui `versao`;
6. todo item possui política de leitura e escrita;
7. itens globais não são editados por usuários comuns;
8. contribuições globais entram como propostas;
9. itens privados pertencem a um espaço;
10. itens de projeto não se tornam institucionais automaticamente;
11. itens utilizados em planos mantêm referência versionada;
12. exclusões respeitam dependências;
13. publicação e validação são ações distintas;
14. a origem de uma cópia ou derivação é preservada;
15. alterações relevantes geram nova versão.

---

## 23. Estrutura conceitual consolidada

```text
MediAd Planner
├── Identidade
│   ├── Usuário
│   ├── Perfil
│   └── Sessão
├── Colaboração
│   ├── Espaço
│   ├── Membresia
│   ├── Papel de acesso
│   └── Papel metodológico
├── Planejamento
│   ├── Projeto
│   ├── Artefatos
│   ├── Versões
│   ├── Consolidação
│   └── Aprovação
├── Bibliotecas
│   ├── Global
│   ├── Espaço
│   ├── Projeto
│   ├── Rascunho pessoal
│   ├── Contribuição
│   ├── Revisão
│   ├── Validação
│   └── Publicação
└── Governança
    ├── Permissões
    ├── Autoria
    ├── Auditoria
    ├── Proveniência
    ├── Versionamento
    └── Segurança
```

---

## 24. Decisões consolidadas

1. O isolamento será realizado por espaço de trabalho.
2. Usuário e papel são conceitos distintos.
3. Os papéis de acesso principais são `ADMINISTRADOR`, `PROPRIETARIO`, `EDITOR` e `LEITOR`.
4. `ADMINISTRADOR` é global; os demais papéis pertencem a membresias.
5. Papéis metodológicos não substituem permissões sistêmicas.
6. O proprietário administra o espaço e suas bibliotecas privadas.
7. O editor elabora planejamentos e pode contribuir com bibliotecas privadas.
8. O leitor possui acesso de consulta.
9. Apenas administração autorizada publica diretamente em bibliotecas globais.
10. Proprietários e editores podem propor contribuições globais.
11. Criar, validar e publicar são ações distintas.
12. Bibliotecas possuem escopo, estado, autoria, fonte e versão.
13. Itens usados em planejamentos devem permanecer referenciáveis.
14. Atualizações de biblioteca não alteram silenciosamente planos consolidados.
15. Exclusão deve preservar histórico e dependências.
16. Ações administrativas excepcionais devem ser auditadas.
17. O sistema deve aplicar negação por padrão e menor privilégio.
18. O modelo deve suportar uso profissional, institucional e didático sem converter categorias como docente, estudante ou cliente em papéis rígidos de acesso.

---

## 25. Síntese normativa

> O MediAd Planner organiza o acesso por identidade, membresia e papel em espaços de trabalho. Administradores governam o sistema e as bibliotecas globais; proprietários governam seus espaços e bibliotecas privadas; editores elaboram planejamentos e contribuem com informações; leitores consultam os conteúdos autorizados. A inclusão de informações em bibliotecas deve preservar escopo, fonte, autoria, revisão, validade, versionamento e rastreabilidade, impedindo que contribuições privadas ou não validadas sejam convertidas automaticamente em referências globais.