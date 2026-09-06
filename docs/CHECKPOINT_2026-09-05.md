# Checkpoint — 05/09/2026

Registro operacional de continuidade, sem força normativa. A única fonte normativa continua sendo `docs/new_app/`, conforme a precedência do documento 30 e as regras de `AGENTS.md`.

## Estado entregue

- Branch: `main`, sincronizada com `origin/main` no encerramento da entrega de código.
- Commit enviado: `0b020e8` — Implementa periodo verba e condicoes declaradas no Briefing.
- Commit anterior: `9b5ca15` — Implementa segmentacao publicos e jornada no Briefing.
- O push ao GitHub foi confirmado. A publicação efetiva no Streamlit permanece sem confirmação; não afirmar que o deploy terminou.

## Escopo e arquivos afetados

A entrega acrescenta período/verba e gerenciamento de prioridades, restrições e pretensões declaradas no Briefing, conforme `docs/new_app/02_BRIEFING.md`.

Foram enviados 18 arquivos: módulos `periodo_verba.py` e `condicoes_declaradas.py` em domínio, DTOs, casos de uso e apresentação; integração em entidades, resumo/mapeamento, serviço de aplicação, composição e navegação do Briefing; quatro arquivos de testes:

- `tests/test_periodo_verba.py`
- `tests/test_frontoffice_periodo_verba.py`
- `tests/test_condicoes_declaradas.py`
- `tests/test_frontoffice_condicoes_declaradas.py`

Critérios de aceite verificados: registrar período e verba, gerenciar condições declaradas, validar referências e preservar permissões, com cobertura de domínio/aplicação e telas. Isso não equivale a certificar a completude de todo o Briefing normativo.

## Validação

- Cópia limpa dos arquivos preparados para o commit: **368 testes aprovados**, executando `python -m pytest -q`.
- `python -m compileall -q app.py mediad_planner tests`: aprovado.
- `git diff --cached --check`: aprovado antes do commit.
- Na pasta original, foram 367 testes aprovados e uma falha em `test_diretorios_operacionais_legados_nao_estao_na_raiz`, pela existência do diretório local `application`. A cópia limpa passou sem alterar ou consultar código legado.
- A assinatura automática do commit falhou com erro de autor inválido. O commit foi criado sem assinatura, usando opção restrita ao comando, e enviado com sucesso.
- A consulta ao GitHub imediatamente após o push não retornou execução de CI; resultado remoto ainda não confirmado.

## Estado local a preservar

`supabase/` permanece não rastreado e contém arquivos temporários locais. Não foi incluído na entrega. Não imprimir seu conteúdo, versionar dados de conexão ou tratar esses arquivos como migrações autorizadas.

Existem diretórios locais residuais fora da estrutura ativa. Não consultar, restaurar ou reutilizar código do aplicativo anterior. Nenhuma limpeza destrutiva foi realizada nesta sessão.

## Retomada

1. Conferir `git status -sb` e o commit remoto antes de novas alterações.
2. Verificar o CI do commit `0b020e8` e confirmar no Streamlit qual revisão está em execução. Obter o endereço/configuração do app se necessário.
3. Conferir a experiência das novas subetapas e a coerência do resumo de progresso: a tela ainda lista Jornada e Prioridades/restrições/pretensões como “Não iniciada” de forma fixa. Tratar como ponto de revisão, não como correção já entregue.
4. Antes de continuar a implementação, confrontar o Briefing atual com `02_BRIEFING.md`, especialmente revisão, diagnósticos e condições de conclusão. A revisão do Briefing aparece como subetapa pendente; não presumir autorização para ampliar motores ou regras.
5. Definir a próxima entrega pequena com escopo, arquivos, critérios de aceite e testes explícitos, mantendo as regras de `AGENTS.md`.

O usuário solicitou uma pausa com checkpoint. Não iniciar nova implementação a partir deste registro sem retomada do trabalho.

## Retomada — 06/09/2026

Retomada autorizada pelo usuário. Esta seção atualiza o registro operacional acima e continua sem força normativa.

- Confirmado que o remoto estava em `ccd2a01`. A consulta ao GitHub não retornou execução de CI para a entrega anterior; Streamlit ainda não confirmado.
- Commit local `ae23b21`: resumo de progresso em ordem e estados derivados dos registros de Jornada e Condições declaradas; teste estrutural passou a admitir especificamente este checkpoint. Validação em cópia limpa: 368 testes aprovados.

### Entrega: revisão parcial do Briefing

Base normativa: `02_BRIEFING.md`, seções 7.5, 8.4, 9.7, 10.4, 11–12, 14.4, 16, 17 e 20, respeitando a precedência do documento 30.

Escopo: disponibilizar a subetapa Revisão do Briefing com avaliação somente de leitura, recalculada a partir dos dados salvos. Aponta domínios ausentes, fontes e referências temporais ausentes, praça sem universo, comunicação sem vínculo a marketing, prioridades ausentes entre múltiplos públicos e jornada sem vínculo ao público ou ao objetivo de comunicação. A ausência de jornada solicita verificar aplicabilidade; não a presume obrigatória. Reutiliza os diagnósticos locais de período, verba e restrições. Verba explicitamente ainda não definida passa a ser distinguida de verba ausente, conforme a seção 20.

Arquivos afetados:

- `mediad_planner/domain/briefing/revisao.py` e `periodo_verba.py`;
- `mediad_planner/application/dto/revisao_briefing.py`, `dto/briefing.py` e `mappers/briefing.py`;
- `mediad_planner/presentation/revisao_briefing.py` e `briefings.py`;
- `tests/test_revisao_briefing.py`, `test_frontoffice_revisao_briefing.py` e `test_periodo_verba.py`;
- este checkpoint operacional.

Critérios de aceite: revisão acessível pela navegação, mensagens ligadas à subetapa e entidade, referência normativa no DTO, alertas recalculados após edição, preservação das declarações e do estado, distinção entre zero/ausência/verba ainda não definida e indicação explícita de avaliação parcial. Nenhuma transição de estado ou autorização de conclusão foi acrescentada.

Validação: **379 testes aprovados** em cópia limpa dos arquivos da entrega; compilação de `app.py`, `mediad_planner` e `tests` aprovada; `git diff --cached --check` aprovado. Na pasta original, a execução anterior aos dois últimos testes teve 376 aprovações e somente a falha estrutural por diretório residual `application`. Entrega preparada para commit local; envio ao GitHub e publicação não realizados nesta retomada.

### Pendências confirmadas pela revisão

- A avaliação ainda não cobre integralmente coerência, suficiência e relações cruzadas da seção 16; ausência de apontamentos não certifica conclusão.
- Falta registrar declaração explícita de inexistência de restrições e aplicabilidade da jornada.
- Faltam reconhecimento explícito de pendências relevantes, submissão à revisão, conclusão e transição para Tradução Estratégica.
- Faltam histórico e comparação entre versões e preservação dos metadados de alteração previstos na seção 18.
- Algumas incoerências territoriais são rejeitadas na entrada atual; revisar esse comportamento à luz das validações sem bloqueio indevido antes de certificar a conclusão.
- Próxima entrega sugerida: declaração de inexistência de restrições, com coexistência/edição coerente dos registros e testes próprios, antes de ampliar o fluxo de conclusão.

Os resíduos locais e `supabase/` continuam preservados e fora da entrega. Não foram consultados nem reutilizados.

### Continuação: declaração de inexistência de restrições

Continuação autorizada pelo usuário após a entrega da revisão parcial, commit local `131eb32`.

Base normativa: `02_BRIEFING.md`, seções 16, 17, 19 e 20. Implementada declaração explícita e reversível de inexistência de restrições, distinta da ausência de registros. A declaração integra o resumo do Briefing, o progresso da subetapa e a revisão. Declarar e retirar mantêm o Briefing em preenchimento e atualizam os metadados de edição existentes.

Escolha de interface e integridade para esta entrega: declaração de inexistência e registros de restrição não coexistem. A tentativa conflitante é recusada sem alterar os dados salvos. O usuário pode retirar explicitamente a declaração para cadastrar restrições; havendo registros, deve revisá-los antes de declarar inexistência. Remover o último registro mantém a situação não declarada. Isso não classifica tecnicamente restrições nem amplia os critérios de conclusão.

Arquivos afetados:

- `mediad_planner/domain/briefing/entidades.py` e `revisao.py`;
- `mediad_planner/application/dto/briefing.py`, `dto/condicoes_declaradas.py`, `mappers/briefing.py`, `use_cases/condicoes_declaradas.py` e `services/aplicacao_briefings.py`;
- `mediad_planner/presentation/briefings.py`, `condicoes_declaradas.py` e `revisao_briefing.py`;
- `tests/test_inexistencia_restricoes.py` e `test_frontoffice_inexistencia_restricoes.py`;
- este checkpoint operacional.

Critérios de aceite: declaração e retirada explícitas; reabertura preserva o valor; revisão elimina apenas a lacuna de restrições ao declarar e a restaura ao retirar; progresso considera a declaração; conflitos preservam dados; somente os papéis de edição já autorizados alteram a declaração; isolamento por espaço e campanha; validação de estado, autor, data e booleano estrito. Testes de interface cobrem navegação, declaração, retirada, restrição existente e remoção do último registro.

Esta entrega resolve a pendência de declaração de inexistência registrada acima. Permanecem as demais lacunas da avaliação completa, histórico/versionamento, reconhecimento de pendências e conclusão. Próxima entrega sugerida: declaração da aplicabilidade da jornada por público, observando as seções 10.4 e 20, antes de implementar a conclusão do Briefing.

Validação: **406 testes aprovados** em cópia limpa dos arquivos da entrega; compilação de `app.py`, `mediad_planner` e `tests` e `git diff --cached --check` aprovados. Os resíduos locais continuam fora da entrega. Envio ao GitHub e publicação no Streamlit não realizados nesta continuação.

### Continuação: aplicabilidade da Jornada por Público

Continuação autorizada pelo usuário após a declaração de inexistência de restrições, commit local `3820c2b`.

Base normativa: `02_BRIEFING.md`, seções 10.4, 16, 17 e 20. A aplicabilidade é uma declaração por Público, com três possibilidades: não informada, aplicável ou não aplicável. A interface permite salvar e retirar a declaração. Não informada continua como valor ausente; a existência de uma Jornada vinculada não preenche a declaração automaticamente.

A revisão distingue Público sem Jornada cuja aplicabilidade ainda precisa ser verificada, Público com Jornada declarada aplicável ainda sem vínculo e Público para o qual a Jornada foi declarada não aplicável. Apenas neste último caso a declaração dispensa o apontamento de Jornada ausente. A declaração também aparece separadamente na revisão e conta no progresso da subetapa.

Escolha de integridade desta entrega: não aplicável e Jornada vinculada ao mesmo Público não coexistem; conflitos solicitam revisar vínculos ou declaração e preservam os dados salvos. Jornadas podem continuar compartilhadas entre Públicos. Editar outros dados do Público preserva a aplicabilidade; remover a Jornada não altera a declaração; remover um Público sem vínculos remove junto sua declaração, sem deixar referência órfã.

Arquivos afetados:

- `mediad_planner/domain/briefing/praca_universo.py`, `entidades.py` e `revisao.py`;
- `mediad_planner/application/dto/jornada.py`, `dto/publicos.py`, `mappers/briefing.py`, `use_cases/jornada.py`, `use_cases/publicos.py` e `services/aplicacao_briefings.py`;
- `mediad_planner/composition/briefings.py`;
- `mediad_planner/presentation/jornada.py`, `briefings.py` e `revisao_briefing.py`;
- `tests/test_aplicabilidade_jornada.py` e `test_frontoffice_aplicabilidade_jornada.py`;
- este checkpoint operacional.

Critérios de aceite: três valores distintos por Público; reabertura e edição preservam a declaração; revisão e progresso refletem o valor salvo; conflitos na criação/edição de Jornadas e na declaração preservam vínculos; permissões de edição, isolamento de espaço/campanha/público e validações de estado, autor e data respeitados. Testes de interface incluem troca entre Públicos, retirada da declaração, filtro de Públicos disponíveis e rejeição de declaração conflitante.

Esta entrega resolve a pendência de aplicabilidade da Jornada. Permanecem avaliação completa de coerência e suficiência, reconhecimento explícito de pendências, versionamento/histórico e conclusão. Próxima entrega sugerida: revisar e ampliar os diagnósticos objetivos de prioridades e ordenação previstos nas seções 10.4 e 13.3, preservando a fronteira com interpretações estratégicas.

Validação: **428 testes aprovados** em cópia limpa dos arquivos da entrega; compilação de `app.py`, `mediad_planner` e `tests` e `git diff --cached --check` aprovados. Resíduos locais preservados e fora da entrega. Envio ao GitHub e publicação no Streamlit não realizados nesta continuação.

### Continuação: diagnósticos de prioridades contextuais e ordenação

Continuação autorizada pelo usuário após a aplicabilidade da Jornada, commit local `cba9d3e`.

Base normativa: `02_BRIEFING.md`, seções 10.4, 13.3, 16 e 17. Os três diagnósticos antes calculados nas telas agora são produzidos pelo domínio e transportados pelo resumo existente à revisão consolidada e às subetapas:

- todas as prioridades contextuais com o mesmo valor, quando houver mais de um item;
- múltiplas prioridades contextuais máximas com justificativa ausente, identificando cada item sem justificativa; corrigido o caso em que somente uma entre as máximas está sem justificativa;
- múltiplas etapas de máxima prioridade (5) na mesma Jornada, com ordenação ausente em ao menos uma delas, identificando a Jornada.

Mantido o recorte já usado pela interface para etapas de máxima prioridade (5). Esta entrega não define novos limiares para o termo “prioritária” nem certifica cobertura integral das seções 10.4 e 13.3. As prioridades contextuais são avaliadas no conjunto já exibido nessa aba. Diagnósticos de conflito com intensidade e de relações estratégicas continuam pendentes.

Arquivos afetados: `mediad_planner/domain/briefing/revisao.py`; `mediad_planner/presentation/condicoes_declaradas.py` e `jornada.py`; `tests/test_diagnosticos_prioridades.py`, `test_frontoffice_diagnosticos_prioridades.py`, `test_frontoffice_condicoes_declaradas.py` e `test_frontoffice_jornada.py`; este checkpoint operacional.

Critérios de aceite: mesmas mensagens nas subetapas e revisão, sem duplicar cálculos na apresentação; referências normativas e identificação de entidade preservadas; nenhum alerta coletivo para item único; justificativa ausente identificada mesmo quando as demais máximas estão justificadas; ordenação avaliada por Jornada; alertas recalculados após edição, justificativa e remoção; declarações e metadados preservados pela avaliação. Os testes de presença de texto nas telas foram substituídos, para esses alertas, por testes de comportamento da interface.

Próxima entrega sugerida: avaliar o mesmo diagnóstico de prioridades iguais e justificativas de máximas nos demais conjuntos que já possuem esses campos, especialmente objetivos declarados e Públicos, observando a seção 13.3. Conclusão, histórico/versionamento e reconhecimento de pendências continuam não implementados.

Validação: **448 testes aprovados** em cópia limpa dos arquivos da entrega; compilação de `app.py`, `mediad_planner` e `tests` e `git diff --cached --check` aprovados. Resíduos locais preservados. Envio ao GitHub e publicação no Streamlit não realizados nesta continuação.
