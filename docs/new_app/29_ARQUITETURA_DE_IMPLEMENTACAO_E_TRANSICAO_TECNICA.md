# Arquitetura de Implementação e Transição Técnica

**Documento:** `29_ARQUITETURA_DE_IMPLEMENTACAO_E_TRANSICAO_TECNICA.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Diretriz para início da implementação  
**Natureza:** Arquitetura técnica e plano de transição  
**Última revisão:** 29/07/2026

---

## 1. Finalidade

Este documento estabelece a ponte entre a arquitetura conceitual já consolidada e a implementação do MediAd Planner.

Ele complementa, mas não integra internamente, o documento `25_CONTRATO_COMUM_DOS_MOTORES_ESPECIALISTAS.md`.

O documento 25 permanece como contrato normativo compartilhado dos motores. Este documento 29 trata de:

- organização interna do código;
- infraestrutura adotada;
- responsabilidades das camadas técnicas;
- integração entre Streamlit, aplicação, domínio e Supabase;
- estratégia de substituição do aplicativo atual;
- preservação, arquivamento e descarte controlado do legado;
- ordem de implementação;
- critérios de segurança para mudanças destrutivas.

A separação evita misturar regras estáveis de domínio com decisões técnicas que podem evoluir durante a implementação.

---

## 2. Relação com os documentos anteriores

A hierarquia documental será:

```text
Documentos 01 a 18B
→ definem campos, bibliotecas, conhecimentos e problemas

Documento 24
→ valida a economia e as fronteiras dos motores

Documento 25
→ define o contrato comum dos motores

Documentos 26, 27 e 28
→ especificam os três motores

Documento 29
→ define como esses contratos serão materializados no software
```

O documento 29 não poderá alterar silenciosamente:

- responsabilidades dos motores;
- campos de negócio;
- fórmulas ou regras metodológicas;
- classificações de entrada;
- estados de execução;
- contratos de saída;
- regras de confiança, rastreabilidade e reexecução.

Mudanças nesses elementos exigem revisão do documento de origem correspondente.

---

## 3. Infraestrutura mantida

A nova implementação reutilizará a infraestrutura já adotada pelo projeto:

```text
GitHub
+ GitHub Codespaces
+ Codex
+ Python
+ Streamlit
+ Supabase
```

### 3.1 GitHub

Responsável por:

- repositório principal;
- versionamento do código e da documentação;
- branches;
- commits;
- pull requests;
- histórico auditável;
- recuperação de versões anteriores.

### 3.2 GitHub Codespaces

Responsável por:

- ambiente de desenvolvimento em nuvem;
- execução do aplicativo;
- terminal;
- testes;
- migrações;
- ferramentas de qualidade;
- isolamento do ambiente local do usuário.

A implementação não deverá depender de instalação local.

### 3.3 Codex

Responsável por apoiar:

- criação e alteração de código;
- geração de testes;
- refatorações;
- análise de falhas;
- implementação incremental a partir dos documentos normativos.

O Codex deverá receber tarefas pequenas, verificáveis e vinculadas a documentos específicos. Não deverá receber instruções genéricas para reconstruir todo o sistema de uma vez.

### 3.4 Streamlit

Responsável pela camada de interface e composição visual.

Não deverá conter diretamente:

- fórmulas de negócio;
- regras dos motores;
- consultas SQL dispersas;
- decisões estratégicas;
- lógica de domínio duplicada;
- credenciais.

### 3.5 Supabase

Responsável por:

- persistência relacional;
- autenticação, quando aplicável;
- armazenamento de snapshots;
- bibliotecas versionadas;
- campanhas, cenários, execuções e resultados;
- rastreabilidade;
- controle de acesso;
- futuras integrações por API.

O Supabase não substitui o domínio. Restrições de banco reforçam integridade, mas regras decisórias permanecem na aplicação e nos objetos de conhecimento.

---

## 4. Decisão sobre o aplicativo atual

O mesmo repositório, Codespace e projeto Supabase poderão ser reutilizados, mas a substituição do aplicativo atual será tratada como uma transição controlada, não como exclusão imediata e irreversível.

A diretriz é:

```text
preservar
→ inventariar
→ arquivar
→ isolar
→ reconstruir
→ validar
→ somente então remover o legado desnecessário
```

Não se deve iniciar apagando arquivos, tabelas ou configurações sem uma referência recuperável.

---

## 5. Estratégia de preservação antes da substituição

Antes de qualquer remoção, deverão ser executadas as seguintes ações.

### 5.1 GitHub

1. registrar um commit final do aplicativo atual;
2. criar uma tag ou branch de preservação, por exemplo:

```text
legacy/pre-mediad-planner-v1
```

3. registrar no README ou em documento próprio o ponto de restauração;
4. confirmar que arquivos de configuração não contêm segredos versionados;
5. manter a documentação arquitetural na branch principal.

### 5.2 Supabase

Antes de excluir ou recriar tabelas:

- exportar o esquema atual;
- identificar tabelas reutilizáveis;
- identificar dados descartáveis;
- identificar dados que precisam ser migrados;
- preservar políticas de acesso relevantes;
- registrar funções, triggers e extensões existentes;
- gerar backup ou exportação lógica dos dados necessários;
- registrar as variáveis de ambiente utilizadas.

### 5.3 Codespace

O Codespace poderá ser reutilizado, mas não deverá ser tratado como fonte única de arquivos ou configurações. Tudo o que for necessário ao projeto deve estar:

- versionado no GitHub;
- documentado;
- ou armazenado como secret/configuração externa recuperável.

---

## 6. Opções de transição

### 6.1 Opção recomendada: substituição progressiva no mesmo repositório

```text
preservar branch do legado
→ criar estrutura nova
→ implementar módulos novos
→ redirecionar gradualmente o app.py
→ remover código legado somente após equivalência mínima
```

Vantagens:

- histórico contínuo;
- menor risco de perda;
- fácil comparação;
- rollback;
- possibilidade de validar partes novas antes da troca completa.

### 6.2 Substituição integral imediata

Só será aceitável quando:

- o legado estiver integralmente preservado em branch ou tag;
- o esquema do Supabase tiver backup;
- os secrets estiverem confirmados;
- a nova estrutura mínima estiver preparada;
- houver plano de restauração.

A reutilização do mesmo espaço não exige apagar o histórico.

---

## 7. Arquitetura de software proposta

A implementação seguirá camadas com dependências direcionadas.

```text
Streamlit / Interface
        ↓
Application / Casos de uso
        ↓
Motores / Orquestração de domínio
        ↓
Domínio / Contratos e entidades
        ↓
Portas e repositórios abstratos
        ↓
Infrastructure / Supabase e serviços externos
```

Dependências de domínio nunca deverão apontar para Streamlit ou Supabase.

---

## 8. Estrutura inicial de diretórios

Estrutura recomendada:

```text
app.py

frontend/
├── pages/
├── components/
├── presenters/
├── session/
└── navigation/

application/
├── commands/
├── queries/
├── use_cases/
├── dto/
├── services/
└── orchestration/

domain/
├── common/
├── campanha/
├── briefing/
├── traducao_estrategica/
├── arquitetura_cenarios/
├── simulacao/
├── bibliotecas/
├── conhecimento_tecnico/
├── problemas_tecnicos/
└── contracts/

engines/
├── base/
├── traducao_estrategica/
├── decisao_arquitetura_cenarios/
└── simulacao_tecnica_economica/

infrastructure/
├── supabase/
├── repositories/
├── cache/
├── logging/
├── configuration/
└── migrations/

reports/
visualization/
tests/
docs/
database/
```

A estrutura poderá ser ajustada durante a implementação, desde que preserve as fronteiras conceituais.

---

## 9. Estrutura interna comum de um motor

Cada motor deverá ser implementado como uma fachada de domínio coordenando componentes menores.

```text
MotorFacade
├── CommandHandler
├── ContextResolver
├── ProblemIdentifier
├── InputSelector
├── LocalValidator
├── ProcedureSelector
├── ProcedureExecutor
├── ResultComposer
├── ConfidenceEvaluator
├── ExplanationBuilder
├── TraceabilityRecorder
└── DependencyPlanner
```

Esses componentes não constituem novos motores. São responsabilidades internas reutilizáveis.

---

## 10. Contratos em Python

Os contratos do documento 25 deverão ser materializados preferencialmente por:

- enums para estados e classificações fechadas;
- dataclasses ou modelos equivalentes para comandos e saídas;
- tipos explícitos;
- validação de entrada;
- identificadores imutáveis;
- timestamps com fuso;
- referências versionadas;
- objetos de valor para unidades, dinheiro, percentuais e intervalos.

Os contratos não deverão depender de estruturas de sessão do Streamlit.

---

## 11. Fachada e orquestração

Cada motor terá uma fachada pública estável.

Exemplo conceitual:

```python
resultado = motor.executar(comando)
```

A fachada deverá:

1. validar o envelope do comando;
2. resolver o contexto;
3. selecionar apenas as entradas necessárias;
4. identificar problemas técnicos;
5. selecionar procedimentos;
6. executar os procedimentos aplicáveis;
7. compor a saída comum;
8. registrar confiança e rastreabilidade;
9. declarar dependências e reexecução.

A fachada não deverá conter todas as fórmulas ou regras em um único arquivo.

---

## 12. Procedimentos e bibliotecas

As Bibliotecas 17 e 18 deverão ser acessadas por provedores ou repositórios próprios.

```text
KnowledgeProvider
→ fornece objetos da Biblioteca 17

ProblemCatalogProvider
→ fornece problemas e gatilhos da Biblioteca 18
```

Os motores selecionam os objetos adequados, mas não mantêm cópias internas deles.

Procedimentos matemáticos deverão ser pequenos, testáveis e versionáveis.

---

## 13. Persistência no Supabase

A persistência deverá distinguir, no mínimo:

```text
cadastros mestres
configurações do projeto
snapshots
comandos
execuções
resultados
alertas
rastreabilidade
dependências
intervenções humanas
```

Não se deve usar uma única tabela genérica para todo o domínio quando isso eliminar integridade e clareza.

Também não se deve criar uma tabela para cada detalhe interno sem necessidade de consulta ou persistência própria.

A modelagem física será elaborada por migrações versionadas.

---

## 14. Migrações do banco

Toda mudança de esquema deverá ser implementada por script de migração versionado.

Regras:

- não alterar manualmente produção sem registrar a mudança;
- não depender de memória do desenvolvedor;
- permitir reconstrução do esquema em novo ambiente;
- separar criação, alteração, carga inicial e rollback quando aplicável;
- preservar dados antes de operações destrutivas;
- testar migrações em ambiente isolado ou esquema de desenvolvimento.

A exclusão de tabelas antigas deverá ocorrer apenas em migração própria e depois de confirmação de que não são mais utilizadas.

---

## 15. Configuração e secrets

Credenciais e tokens não deverão ser salvos no código ou em arquivos versionados.

Devem ser usados:

- Codespaces Secrets;
- variáveis de ambiente;
- Streamlit Secrets, quando necessário;
- configurações externas adequadas.

Variáveis mínimas esperadas incluem referências equivalentes a:

```text
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY, somente em contexto seguro
```

A aplicação deverá falhar com mensagem clara quando uma configuração obrigatória estiver ausente.

---

## 16. Streamlit como adaptador de interface

A camada Streamlit deverá:

- coletar comandos do usuário;
- apresentar estados e resultados;
- controlar navegação e sessão;
- solicitar confirmações de operações destrutivas;
- exibir explicações, alertas e confiança;
- chamar casos de uso da camada de aplicação.

Não deverá:

- acessar tabelas diretamente em cada página;
- recalcular indicadores;
- tomar decisões dos motores;
- armazenar estado durável apenas em `st.session_state`;
- alterar dados sem passar por casos de uso explícitos.

---

## 17. Cache e reexecução

O cache deverá utilizar chaves derivadas de:

```text
motor
modo
nível
snapshot
versões das bibliotecas
parâmetros efetivos
entradas consumidas
```

Uma alteração deverá invalidar somente resultados dependentes.

O cache não pode ocultar mudança de versão, intervenção humana ou alteração de parâmetro.

---

## 18. Registro e observabilidade

Cada execução deverá registrar:

- identificador;
- comando;
- motor e modo;
- início e término;
- estado;
- entradas efetivamente consumidas;
- versões utilizadas;
- procedimentos executados;
- alertas;
- falhas;
- dependências;
- duração;
- uso de cache.

Logs técnicos e rastreabilidade de domínio são relacionados, mas não idênticos.

---

## 19. Estratégia de testes

A implementação deverá possuir:

### 19.1 Testes unitários

Para:

- objetos de valor;
- validações;
- seletores;
- fórmulas;
- procedimentos;
- confiança;
- propagação de dependências.

### 19.2 Testes de contrato

Para garantir que os motores respeitem:

- envelope de comando;
- estados;
- saída comum;
- classificação das entradas;
- rastreabilidade;
- reexecução.

### 19.3 Testes de integração

Para:

- Supabase;
- repositórios;
- migrações;
- cache;
- execução entre motores.

### 19.4 Testes de fluxo

Para os casos mínimos definidos nos documentos 26, 27 e 28.

---

## 20. Ordem de implementação

A ordem recomendada é:

```text
1. fundação técnica comum
2. contratos compartilhados
3. persistência mínima e migrações
4. Motor de Tradução Estratégica
5. Motor de Simulação Técnica e Econômica
6. Motor de Decisão de Arquitetura e Cenários
7. integração completa na interface
8. remoção final do legado não utilizado
```

O Motor de Decisão será implementado depois do Motor de Simulação porque depende de chamadas quantitativas para avaliar e ajustar cenários.

---

## 21. Primeira etapa de implementação

O primeiro ciclo técnico deverá produzir somente:

- estrutura de diretórios;
- configuração de ambiente;
- conexão testável com Supabase;
- tipos comuns;
- envelope de comando;
- envelope de saída;
- enums comuns;
- interface base dos motores;
- repositórios abstratos;
- implementação mínima de persistência;
- testes da fundação.

Ainda não deverão ser implementados algoritmos completos dos três motores nesse primeiro ciclo.

---

## 22. Uso do Codex

As tarefas enviadas ao Codex deverão seguir o padrão:

```text
contexto documental
→ objetivo pequeno
→ arquivos permitidos
→ contratos que não podem mudar
→ critérios de aceite
→ testes obrigatórios
→ comando de verificação
```

Exemplo de sequência:

1. criar enums comuns;
2. criar modelos de comando e saída;
3. criar protocolo base de motor;
4. criar testes de contrato;
5. criar adaptador de configuração;
6. criar repositório Supabase mínimo;
7. integrar sem regra de negócio avançada.

O Codex não deverá excluir o legado ou alterar o esquema do Supabase de forma destrutiva sem instrução específica e confirmação.

---

## 23. Critérios para remover o legado

Código, tabelas ou configurações antigas somente poderão ser removidos quando:

- houver cópia recuperável;
- o novo fluxo correspondente estiver implementado;
- os testes estiverem aprovados;
- não existirem importações ou consultas dependentes;
- a migração estiver documentada;
- a remoção estiver em commit próprio;
- houver caminho de rollback ou restauração.

A remoção deverá ser separada da implementação funcional sempre que possível, facilitando revisão e reversão.

---

## 24. Critérios de prontidão para a implementação dos motores

A fundação estará pronta quando:

- o projeto executar no Codespace;
- o Streamlit abrir sem erro;
- a configuração do Supabase for validada;
- os contratos comuns estiverem testados;
- um motor fictício puder receber e devolver envelopes válidos;
- logs e identificadores de execução forem gerados;
- os testes puderem ser executados por comando único;
- nenhuma regra de domínio depender diretamente da interface.

---

## 25. Decisão consolidada

O documento 25 deve permanecer enxuto e normativo, contendo o contrato compartilhado dos motores. A arquitetura interna, a infraestrutura e a transição do aplicativo atual pertencem a este documento 29 porque possuem ciclo de mudança diferente.

A infraestrutura atual será mantida, mas o aplicativo existente será substituído de forma controlada no mesmo ecossistema:

```text
mesmo GitHub
mesmo Codespace
mesmo Supabase
mesma tecnologia de interface
nova arquitetura de aplicação
novo domínio implementado progressivamente
legado preservado antes da remoção
```

> Reutilizar os mesmos espaços não significa reutilizar a estrutura inadequada nem apagar o passado. A nova implementação deverá preservar o histórico, reconstruir o software sobre contratos claros e remover o legado apenas depois que a substituição estiver comprovadamente funcional e recuperável.
