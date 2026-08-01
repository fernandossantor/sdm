# Prompt Inicial para o Codex no Codespace

**Documento:** `31_PROMPT_INICIAL_PARA_CODEX_NO_CODESPACE.md`  
**Plano Mestre:** MediAd Planner  
**Status:** Execução inicial concluída; preservado como registro histórico
**Natureza:** Instrução operacional de implementação  
**Última revisão:** 01/08/2026

---

## Uso atual

A execução inicial descrita abaixo foi concluída. Não repita inventário, preservação ou fundação. O legado está arquivado conforme `docs/implementation/05_DECISAO_ARQUIVAMENTO_LEGADO.md`; o novo aplicativo deve evoluir exclusivamente a partir de `docs/new_app`.

Para retomar, use:

```text
Você está trabalhando no repositório `fernandossantor/sdm`, na branch `main`, dentro do Codespace configurado.

Desenvolva exclusivamente o novo MediAd Planner. Leia `docs/new_app/30_AUDITORIA_FINAL_DE_CONSISTENCIA_DOCUMENTAL.md` e aplique sua precedência sobre todo o corpo de `docs/new_app`. Consulte `docs/implementation/05_DECISAO_ARQUIVAMENTO_LEGADO.md` para a decisão sobre o legado.

O aplicativo legado está arquivado: não o restaure à navegação, não o use como contrato funcional e não exija paridade com ele. Preserve a tag `legacy-pre-mediad-planner-v1` e o histórico Git. Qualquer remoção física de código, tabela ou dado exige etapa controlada, backup e autorização específica.

Implemente o próximo incremento verificável do fluxo novo, com domínio independente de Streamlit e Supabase, testes proporcionais ao risco e documentação do estado real. Não marque funcionalidades futuras como concluídas e não invente regras ausentes dos documentos normativos.

Nunca exponha secrets, tokens, chaves ou senhas. Não faça force push nem reescreva o histórico. Preserve os itens do usuário que estejam fora do escopo.
```

## Prompt original preservado

O texto abaixo permanece para auditoria da primeira execução e não deve ser reutilizado:


```text
Você está trabalhando no repositório GitHub `fernandossantor/sdm`, na branch `main`, dentro de um GitHub Codespace já configurado.

O objetivo é iniciar a reconstrução controlada do aplicativo atual como o novo MediAd Planner, mantendo a infraestrutura existente:

- GitHub;
- GitHub Codespaces;
- Codex;
- Python;
- Streamlit;
- Supabase.

As credenciais, secrets e autorizações já existentes no ambiente devem ser reutilizados apenas por seus mecanismos normais. NUNCA exiba valores de secrets, tokens, chaves, senhas ou URLs sensíveis no terminal, em logs, respostas, arquivos ou commits. Você pode verificar apenas se uma variável existe, sem imprimir seu conteúdo.

## 1. Fonte de verdade

Antes de alterar código, leia integralmente o diretório `docs/new_app`.

Use especialmente, nesta ordem:

1. `docs/new_app/30_AUDITORIA_FINAL_DE_CONSISTENCIA_DOCUMENTAL.md`;
2. `docs/new_app/29_ARQUITETURA_DE_IMPLEMENTACAO_E_TRANSICAO_TECNICA.md`;
3. `docs/new_app/25_CONTRATO_COMUM_DOS_MOTORES_ESPECIALISTAS.md`;
4. `docs/new_app/26_MOTOR_DE_TRADUCAO_ESTRATEGICA.md`;
5. `docs/new_app/27_MOTOR_DE_DECISAO_DE_ARQUITETURA_E_CENARIOS.md`;
6. `docs/new_app/28_MOTOR_DE_SIMULACAO_TECNICA_E_ECONOMICA.md`;
7. `docs/new_app/23_MAPA_DE_NECESSIDADE_E_FRONTEIRAS_DOS_MOTORES.md`;
8. `docs/new_app/24_CASOS_DE_USO_E_VALIDACAO_DA_ECONOMIA_DE_MOTORES.md`;
9. documentos 01–18 e respectivos complementos;
10. `docs/new_app/PLANO_MESTRE_MEDIAD_PLANNER.md` como visão geral.

Aplique a precedência definida no documento 30. Não implemente formulações históricas incompatíveis com documentos específicos mais recentes.

O arquivo `MODELO DE PLANEJAMENTO CROSS MEDIA.md` é referência metodológica, não contrato normativo superior.

## 2. Regra principal desta primeira execução

NÃO reconstrua o sistema inteiro de uma vez.

Esta primeira execução deve produzir apenas:

1. inventário técnico do legado;
2. preservação recuperável do estado atual;
3. diagnóstico do Supabase sem alterações destrutivas;
4. proposta concreta de transição;
5. fundação mínima da nova arquitetura;
6. testes da fundação;
7. relatório final do que foi feito e do que ficou pendente.

Não implemente ainda os três motores completos.

## 3. Segurança e preservação obrigatórias

Estamos trabalhando diretamente na branch `main`, por decisão do proprietário do projeto. Antes de qualquer exclusão ou substituição:

1. confirme que o working tree está limpo ou registre claramente alterações existentes;
2. identifique o commit atual de `main`;
3. crie uma referência de preservação recuperável do legado, preferencialmente:
   - tag anotada `legacy-pre-mediad-planner-v1`, ou
   - branch `legacy/pre-mediad-planner-v1`;
4. não force push;
5. não reescreva histórico;
6. não apague arquivos, tabelas, funções, políticas ou dados nesta primeira execução;
7. não altere secrets;
8. não remova dependências antes de mapear seu uso.

Caso a tag ou branch já exista, não a sobrescreva silenciosamente. Informe e proponha outro nome versionado.

## 4. Inventário do repositório atual

Examine o repositório e gere um relatório em:

`docs/implementation/00_INVENTARIO_TECNICO_DO_LEGADO.md`

O relatório deve incluir:

- árvore resumida de diretórios;
- ponto de entrada do Streamlit;
- páginas existentes;
- módulos de domínio;
- serviços de aplicação;
- infraestrutura;
- acesso atual ao Supabase;
- testes existentes;
- scripts utilitários;
- arquivos de configuração;
- dependências do `requirements.txt`, `pyproject.toml` ou equivalentes;
- arquivos aparentemente obsoletos;
- código potencialmente reutilizável;
- código que conflita com a nova arquitetura;
- referências a nomes antigos;
- riscos técnicos observados.

Classifique cada componente como:

- REUTILIZAR;
- ADAPTAR;
- ISOLAR;
- SUBSTITUIR;
- REMOVER_DEPOIS;
- INDETERMINADO.

Não remova nada nessa etapa.

## 5. Diagnóstico do Supabase

Use a conexão existente apenas para leitura e diagnóstico.

Não imprima credenciais.

Verifique, quando as ferramentas disponíveis permitirem:

- conectividade;
- tabelas existentes;
- colunas principais;
- chaves e relacionamentos;
- views;
- funções;
- triggers;
- políticas RLS;
- extensões relevantes;
- migrações já existentes;
- dados que parecem estruturais;
- dados de teste ou descartáveis.

Gere:

`docs/implementation/01_INVENTARIO_SUPABASE_ATUAL.md`

Classifique os objetos como:

- PRESERVAR;
- MIGRAR;
- REUTILIZAR;
- SUBSTITUIR;
- REMOVER_SOMENTE_APOS_BACKUP;
- INDETERMINADO.

Não execute `DROP`, `TRUNCATE`, exclusões em massa ou migrações destrutivas.

Caso não seja possível consultar o Supabase por falta de CLI ou biblioteca, não instale ferramentas arbitrariamente sem necessidade. Primeiro identifique a forma de conexão já usada pelo projeto e produza um diagnóstico do impedimento.

## 6. Estrutura nova a preparar

Com base no documento 29, prepare ou ajuste incrementalmente a estrutura abaixo, sem destruir o legado:

```text
app.py
frontend/
application/
domain/
engines/
infrastructure/
reports/
visualization/
tests/
database/
docs/implementation/
```

Subestruturas esperadas:

```text
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
```

Crie apenas diretórios e arquivos necessários à fundação. Evite arquivos vazios sem finalidade. Use `__init__.py` quando necessário ao empacotamento.

## 7. Fundação de domínio a implementar

Implemente contratos comuns mínimos derivados do documento 25.

Crie tipos explícitos para, no mínimo:

- níveis de execução: `PREVIA`, `PADRAO`, `DETALHADA`;
- estados de execução;
- classificações de entrada;
- resultados de validação;
- severidades;
- naturezas do valor;
- estados de deduplicação;
- estados de equivalência;
- níveis de confiança, se definidos de forma fechada;
- identificadores e referências versionadas;
- envelope comum de comando;
- envelope comum de saída;
- validação local;
- alerta;
- restrição;
- rastreabilidade;
- dependência e plano de reexecução.

Escolha entre `dataclasses`, Pydantic ou solução equivalente após verificar as dependências atuais. Prefira a alternativa mais simples, tipada e compatível com o projeto.

Regras obrigatórias:

- domínio não depende de Streamlit;
- domínio não depende do cliente Supabase;
- objetos devem ser serializáveis;
- timestamps devem possuir fuso;
- ausência não pode virar zero;
- valores informados, herdados, calculados, estimados e inferidos devem ser distinguíveis;
- contratos devem preservar versões e origens.

## 8. Interface base dos motores

Implemente apenas a base compartilhada, sem regras completas dos motores.

Crie uma interface ou protocolo para:

```python
resultado = motor.executar(comando)
```

A fundação deve permitir:

- validação do envelope;
- resolução futura de contexto;
- seleção futura de procedimentos;
- composição da saída comum;
- registro de confiança;
- rastreabilidade;
- dependências e reexecução.

Crie placeholders tipados ou abstrações para:

- `ContextResolver`;
- `ProblemIdentifier`;
- `ProcedureSelector`;
- `ProcedureExecutor`;
- `ConfidenceEvaluator`;
- `ExplanationBuilder`;
- `TraceabilityRecorder`;
- `DependencyPlanner`;
- `KnowledgeProvider`;
- `ProblemCatalogProvider`.

Não transforme cada item em novo motor ou microsserviço.

## 9. Portas de persistência

Crie interfaces abstratas, não implementações completas, para repositórios essenciais, por exemplo:

- campanhas;
- snapshots;
- comandos;
- execuções;
- resultados;
- bibliotecas versionadas;
- objetos de conhecimento;
- problemas técnicos.

Implemente apenas uma configuração central segura para o cliente Supabase, reutilizando o mecanismo atual de variáveis de ambiente.

A importação de módulos não deve abrir conexão automaticamente.

## 10. Streamlit

Não redesenhe ainda todas as telas.

Apenas garanta que:

- o ponto de entrada atual continue executável ou seja isolado de forma reversível;
- a nova fundação não dependa de estado de sessão;
- nenhuma regra de domínio seja adicionada diretamente a páginas;
- seja possível criar posteriormente uma navegação progressiva.

Caso precise modificar `app.py`, faça a menor alteração reversível possível e mantenha o legado acessível até a substituição validada.

## 11. Testes

Crie testes automatizados para a fundação, incluindo no mínimo:

1. criação válida de comando;
2. rejeição de comando inválido;
3. serialização e desserialização;
4. timestamps com fuso;
5. distinção entre ausência e zero;
6. saída parcial;
7. saída não executável;
8. validação com alerta;
9. plano de reexecução;
10. interface base de motor com implementação falsa;
11. domínio sem dependência de Streamlit;
12. configuração Supabase sem exposição de secrets.

Execute os testes existentes e os novos.

Se testes antigos falharem antes das alterações, registre isso separadamente. Não masque falhas removendo testes.

## 12. Qualidade

Respeite as ferramentas já existentes no projeto. Verifique antes de introduzir novas dependências.

Execute, conforme disponível:

- testes;
- lint;
- formatação;
- checagem de tipos;
- importação do aplicativo;
- inicialização mínima do Streamlit sem interação destrutiva.

Não adicione uma ferramenta pesada quando uma solução já existente resolver o problema.

## 13. Commits

Trabalhe em etapas pequenas na própria `main`, conforme solicitado, mas faça commits claros e recuperáveis.

Sugestão:

1. `chore: preserva estado legado e registra inventário inicial`
2. `docs: registra inventário técnico e diagnóstico do Supabase`
3. `refactor: cria fundação arquitetural do MediAd Planner`
4. `test: adiciona testes dos contratos e da base dos motores`

Antes de cada commit:

- mostre o resumo das alterações;
- execute os testes pertinentes;
- confirme que nenhum secret entrou no diff.

Não faça push forçado.

## 14. Entregáveis desta execução

Ao terminar, devem existir:

- referência Git recuperável do legado;
- `docs/implementation/00_INVENTARIO_TECNICO_DO_LEGADO.md`;
- `docs/implementation/01_INVENTARIO_SUPABASE_ATUAL.md`;
- `docs/implementation/02_PLANO_DE_TRANSICAO_EXECUTAVEL.md`;
- estrutura mínima das novas camadas;
- contratos comuns implementados;
- interface base dos motores;
- portas de persistência;
- configuração segura do Supabase;
- testes da fundação;
- relatório final.

O plano de transição deve separar:

- ações já executadas;
- ações seguras para a próxima etapa;
- ações destrutivas que exigem confirmação do proprietário;
- itens do legado reutilizáveis;
- itens candidatos à remoção futura;
- migrações necessárias no Supabase.

## 15. Restrições absolutas

Não faça nesta execução:

- implementação integral dos motores 26, 27 e 28;
- criação de fórmulas não documentadas;
- invenção de tabelas definitivas sem diagnóstico;
- remoção do legado;
- exclusão de dados;
- alteração destrutiva do Supabase;
- exposição de secrets;
- mudança de infraestrutura;
- migração para framework diferente do Streamlit;
- criação de bibliotecas ou motores adicionais;
- duplicação de fórmulas entre comparação, otimização e simulação;
- alteração silenciosa da documentação normativa.

## 16. Forma de trabalhar e responder

Primeiro faça o diagnóstico. Depois apresente um plano curto e execute por etapas.

Não peça confirmação para leituras, inventários, criação de arquivos novos não destrutivos, testes ou estruturação reversível.

Pare e peça confirmação antes de:

- apagar arquivos existentes;
- substituir de forma irreversível o ponto de entrada;
- remover dependências;
- excluir ou alterar destrutivamente tabelas;
- migrar dados;
- alterar políticas RLS;
- alterar autenticação;
- renomear objetos persistidos usados pelo app atual.

Ao final, responda com:

1. estado inicial encontrado;
2. referência de preservação criada;
3. arquivos criados e alterados;
4. testes executados e resultados;
5. diagnóstico do Supabase;
6. decisões técnicas tomadas;
7. riscos ainda existentes;
8. próxima tarefa recomendada;
9. lista explícita de ações destrutivas ainda não realizadas.

Comece agora pela leitura dos documentos e pelo inventário. Não apague nem substitua nada antes de concluir e registrar o diagnóstico.
```
