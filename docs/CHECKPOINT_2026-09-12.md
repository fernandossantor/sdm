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

## Retomada — 12/09/2026

- Retomada solicitada pelo usuário. Os três commits locais até `75e1b6b` foram enviados à `main` no GitHub.
- CI de `75e1b6b` aprovado: https://github.com/fernandossantor/sdm/actions/runs/34717800573. O log confirma **538 testes aprovados** e compilação de `app.py`, `mediad_planner` e `tests` aprovada.
- Nenhuma nova implementação funcional nesta retomada. O §13.3 exige diagnósticos para entidades prioritárias, mas não define um limiar numérico. Foi solicitada ao usuário a definição do recorte antes de implementar esses apontamentos.
- A revisão publicada no Streamlit continua sem confirmação; endereço e configuração de deploy foram solicitados ao usuário.
- Escopo desta entrega: atualização deste checkpoint operacional. Aceite: envio anterior e CI comprovados, pendências preservadas e diff sem erros de whitespace. Verificação estrutural de documentação aprovada em cópia limpa dos arquivos rastreados (**1 teste**); `git diff --check` aprovado.
- `supabase/` permanece não rastreado, sem consulta ao conteúdo ou alterações.

## Entrega da retomada — vínculos de entidades prioritárias

- O usuário definiu explicitamente **4 e 5** como recorte para os dois novos diagnósticos do §13.3. A definição foi incorporada a `docs/new_app/02_BRIEFING.md`, mantendo a fonte normativa única.
- Público de prioridade alta (4) ou muito alta (5) sem vínculo explícito com Objetivo de Marketing ou Comunicação gera aviso. Qualquer objetivo vinculado atende à relação, independentemente de sua prioridade. Relação por praça comum ou por outro objetivo não cria vínculo implícito.
- Objetivos de Marketing e Comunicação com prioridade 4 ou 5 recebem avisos separados para falta de Público e falta de Praça. Salvar ou retirar um vínculo recalcula os apontamentos; os avisos não impedem salvar e não alteram as declarações.
- Os apontamentos são calculados no domínio e chegam às subetapas de Objetivos e Públicos e à Revisão pela infraestrutura existente. A revisão permanece parcial e a persistência continua em memória.
- Arquivos afetados: `docs/new_app/02_BRIEFING.md`, `mediad_planner/domain/briefing/revisao.py`, `tests/test_diagnosticos_prioridades.py`, `tests/test_diagnosticos_vinculos_prioritarios.py`, `tests/test_frontoffice_diagnosticos_vinculos.py` e este checkpoint.
- Aceite: prioridades 4 e 5 avaliadas; prioridades 1–3 e ausência não geram os novos avisos; vínculos explícitos respeitam identidades; recálculo após salvar/retirar vínculos, editar prioridade do Público e remover Objetivo; avisos consistentes nas subetapas e na revisão; avaliação somente de leitura.
- Validação: **612 testes aprovados** em cópia limpa da entrega (**74 novos testes**); compilação de `app.py`, `mediad_planner` e `tests` aprovada. Os testes anteriores de igualdade/máximas passaram a verificar especificamente essas mensagens, permitindo coexistência dos novos diagnósticos.
- Limite adicional verificado: a aplicação ainda não oferece edição da prioridade dos Objetivos já cadastrados. O recorte dos Objetivos foi testado no domínio em todos os valores existentes; não foi criado fluxo de edição nesta entrega.
- O serviço de assinatura recusou o commit com `403 | Author is invalid`, inclusive após conferir a identidade autenticada. O usuário autorizou explicitamente criar apenas este commit sem assinatura, enviar e verificar o CI, preservando a configuração de assinatura do repositório.
- Este registro acompanha a entrega preparada para envio. O resultado do CI da revisão enviada deve ser consultado no GitHub; o CI aprovado de `75e1b6b` não valida este código novo.
- Próximos passos após envio e CI: confirmar separadamente o deploy no Streamlit. Continuam pendentes os demais diagnósticos do §13.3, reconhecimento de alertas, histórico/comparação de versões, conclusão e transição do Briefing. A regra de ordenação da Jornada permanece restrita às múltiplas máximas (5). A falha de assinatura permanece pendente para futuros commits.
