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
