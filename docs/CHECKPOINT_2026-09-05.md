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
