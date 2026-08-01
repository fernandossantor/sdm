# Decisão de arquitetura — arquivamento do aplicativo legado

Data: 1º de agosto de 2026 (UTC).

## Decisão

O aplicativo anterior cumpriu sua função como etapa de aprendizado e transição. Ele não será retomado como produto, não voltará à navegação e não constitui referência funcional para o novo MediAd Planner.

O novo aplicativo será desenvolvido exclusivamente a partir do corpo normativo de `docs/new_app`, aplicando a precedência definida em `30_AUDITORIA_FINAL_DE_CONSISTENCIA_DOCUMENTAL.md`.

## Significado de arquivamento

- preservar a tag recuperável `legacy-pre-mediad-planner-v1`, no commit `544fbda`;
- manter o histórico Git auditável;
- retirar o legado do caminho de evolução e da experiência do usuário;
- não exigir equivalência funcional entre o legado e o novo aplicativo;
- reutilizar código ou estrutura somente quando forem compatíveis com `docs/new_app`;
- remover código, tabelas ou dados obsoletos apenas em etapa controlada, após inventário, backup e autorização específica.

Arquivamento não significa exclusão imediata nem autoriza operações destrutivas.

## Consequências para implementação

1. `app.py` continuará apontando para a experiência nova.
2. Novas funcionalidades seguirão o fluxo Campanha → Briefing → Tradução Estratégica → Arquitetura e Cenários → Simulação → Plano Consolidado.
3. Os três motores serão implementados incrementalmente segundo os documentos 25 a 29.
4. Telas, serviços e tabelas do legado não serão reintroduzidos apenas para satisfazer o roteiro antigo de homologação.
5. Cada incremento do novo app terá critérios próprios, testes e evidências de homologação.

## Consequências para o piloto

O piloto será progressivo. A versão candidata somente será avaliada pelas capacidades efetivamente implementadas no novo app. Funcionalidades futuras permanecerão como gates de etapas posteriores, sem serem marcadas como falhas ou como concluídas antecipadamente.
