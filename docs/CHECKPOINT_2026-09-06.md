# Checkpoint — 06/09/2026

Registro operacional de continuidade, sem força normativa. A única fonte normativa é `docs/new_app/`, com a precedência do documento 30. Este checkpoint sucede `CHECKPOINT_2026-09-05.md`, que conserva os detalhes das entregas.

## Estado salvo

- Branch: `main`.
- Última entrega de código: `fa4c978`.
- Cinco commits locais desde `ccd2a01`, antes deste checkpoint; nenhum deles foi enviado ao GitHub nesta retomada.
- CI remoto e revisão publicada no Streamlit continuam sem confirmação. Não afirmar que houve publicação.

## Entregas concluídas

| Commit | Entrega |
| --- | --- |
| `ae23b21` | Ordem e estados do resumo de progresso do Briefing corrigidos. |
| `131eb32` | Revisão parcial com lacunas e alertas recalculados a partir dos dados salvos. |
| `3820c2b` | Declaração explícita e reversível de inexistência de restrições. |
| `cba9d3e` | Aplicabilidade da Jornada por Público: não informada, aplicável ou não aplicável. |
| `fa4c978` | Diagnósticos de prioridades contextuais e ordenação centralizados no domínio e apresentados nas subetapas e na revisão. |

A revisão é somente de leitura. Declarações, conflitos e lacunas não são corrigidos silenciosamente. As declarações de inexistência de restrições e de Jornada não aplicável exigem revisão explícita dos registros/vínculos conflitantes.

## Validação e escopo deste checkpoint

- Última entrega: **448 testes aprovados** em cópia limpa dos arquivos rastreados, com compilação de `app.py`, `mediad_planner` e `tests` aprovada.
- O teste estrutural de documentação foi atualizado para admitir especificamente este novo checkpoint operacional, preservando a lista restrita de documentos permitidos; teste executado e aprovado (**1 teste**). `git diff --check` aprovado.
- Arquivos desta entrega: este documento e `tests/test_clean_foundation.py`.
- Aceite: checkpoint recuperável por commit, entregas e pendências explícitas, teste estrutural compatível com o novo arquivo e ausência de arquivos locais de conexão no commit.

## Estado local a preservar

`supabase/` permanece não rastreado e fora da entrega. Não consultar ou imprimir seu conteúdo, não versionar dados de conexão e não presumir migrações autorizadas.

Há diretórios residuais locais fora da estrutura ativa. A verificação de ausência de legado na raiz falha nessa pasta por detectar `application`; os testes da entrega passam na cópia limpa. Nenhuma limpeza destrutiva foi realizada. Não consultar, restaurar ou reutilizar código do aplicativo anterior.

## Pendências e retomada

1. Conferir `git status -sb` e os commits locais/remotos antes de alterações ou envio.
2. Enviar os commits ao GitHub quando solicitado e verificar o CI; confirmar separadamente qual revisão está publicada no Streamlit.
3. Próxima entrega funcional sugerida: ampliar os diagnósticos objetivos de prioridades iguais e justificativas de máximas para objetivos declarados e Públicos, conforme a seção 13.3 de `02_BRIEFING.md`.
4. Manter explícito o recorte atual: ordenação avaliada para múltiplas etapas de máxima prioridade (5), por Jornada. Isso não certifica cobertura integral das seções 10.4 e 13.3.
5. Permanecem pendentes avaliação completa de coerência e suficiência, reconhecimento explícito de alertas, histórico/comparação de versões, conclusão do Briefing e transição para Tradução Estratégica.
6. Revisar as incoerências territoriais atualmente rejeitadas na entrada à luz das validações sem bloqueio indevido antes de certificar a conclusão.

O usuário solicitou commit e novo checkpoint. Nenhuma nova implementação funcional faz parte deste encerramento.
