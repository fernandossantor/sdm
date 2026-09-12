# Checkpoint — 12/09/2026

Registro operacional de continuidade, sem força normativa. A única fonte normativa é `docs/new_app/`, observando a precedência do documento 30 e `AGENTS.md`. Este checkpoint sucede `CHECKPOINT_2026-09-06.md`, que conserva os detalhes das entregas.

## Estado salvo

- Branch: `main`.
- Última entrega de código: `8ba41bd` — Permite vincular objetivos declarados a públicos e praças.
- Entrega anterior: `ef975ef` — Amplia diagnósticos de prioridades para objetivos e públicos.
- Os dois commits de implementação são locais e ainda não foram enviados ao GitHub. Este checkpoint será salvo em um terceiro commit local.
- Última revisão remota conferida nesta sessão: `aceb960`, com CI aprovado em https://github.com/fernandossantor/sdm/actions/runs/34055062384. Isso não valida remotamente as duas novas entregas.
- A revisão publicada no Streamlit permanece sem confirmação.

## Entregas concluídas

1. **Diagnósticos de prioridades:** Marketing, Comunicação e Públicos são avaliados separadamente quanto a prioridades iguais e múltiplas máximas sem justificativa. Máxima corresponde a 5 na escala existente; ausência não é tratada como valor. Os avisos chegam às subetapas e à revisão pelo resumo calculado no domínio.
2. **Vínculos dos Objetivos:** cada Objetivo de Marketing ou Comunicação já cadastrado permite salvar, alterar e retirar Públicos e Praças relacionados. As referências são opcionais e pertencem ao mesmo Briefing. Os demais campos do Objetivo são preservados. Remover uma entidade ainda vinculada exige retirar explicitamente a referência; conflitos preservam os dados salvos.

A revisão continua parcial e somente de leitura. A persistência continua usando o repositório em memória existente; nenhuma tabela ou migração foi acrescentada. A reabertura testada ocorre nessa infraestrutura, sem representar persistência após reiniciar o aplicativo.

## Validação e escopo deste checkpoint

- Última entrega de código: **538 testes aprovados** em cópia limpa dos arquivos preparados para a entrega; compilação de `app.py`, `mediad_planner` e `tests` aprovada.
- As duas entregas acrescentaram, respectivamente, 35 e 55 testes.
- Arquivos deste encerramento: `docs/CHECKPOINT_2026-09-12.md` e `tests/test_clean_foundation.py`.
- O teste estrutural admite especificamente este novo checkpoint, mantendo a lista restrita de documentação permitida.
- Validação deste encerramento: teste estrutural de documentação executado e aprovado (**1 teste**); `git diff --check` aprovado.
- Aceite deste encerramento: checkpoint recuperável por commit, estado local/remoto e pendências explícitos, teste estrutural de documentação aprovado e diff sem erros de whitespace.

## Estado local a preservar

`supabase/` permanece não rastreado e fora das entregas. Não consultar ou imprimir seu conteúdo, não versionar dados de conexão e não presumir migrações autorizadas.

Há resíduos locais fora da estrutura ativa. A suíte completa foi executada em cópia limpa para preservar esses resíduos; a verificação de ausência de diretórios operacionais antigos não passa na pasta original. Não consultar, restaurar ou reutilizar código legado. Nenhuma limpeza destrutiva foi realizada.

## Próxima retomada

1. Conferir `git status -sb`, os commits locais e a revisão remota antes de alterar ou enviar arquivos.
2. Resolver o envio dos commits locais ao GitHub e verificar o CI da revisão enviada. Confirmar separadamente a revisão publicada no Streamlit; obter endereço/configuração se necessário.
3. Próximo recorte funcional sugerido: avaliar os diagnósticos de Público prioritário sem Objetivo e Objetivo prioritário sem Público ou Praça, conforme §13.3 de `02_BRIEFING.md`. Os vínculos já existem; os novos apontamentos ainda não. Explicitar o recorte de prioridade antes de implementar, sem inventar limiares normativos.
4. Manter explícitos os limites atuais: ordenação de Jornada avaliada para múltiplas etapas de máxima prioridade (5), avaliação incompleta de coerência/suficiência e demais diagnósticos da seção 13.3 ainda pendentes.
5. Permanecem pendentes reconhecimento explícito de alertas, histórico/comparação de versões, conclusão do Briefing e transição para Tradução Estratégica. Revisar também as incoerências territoriais atualmente rejeitadas na entrada à luz das validações sem bloqueio indevido.

O usuário solicitou pausa com novo checkpoint. Não iniciar nova implementação funcional sem retomada do trabalho.
