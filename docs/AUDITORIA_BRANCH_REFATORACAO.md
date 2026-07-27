# Auditoria da branch `refactor/sdm-finalizacao`

Data da triagem: 27 de julho de 2026.

## Objetivo

A branch possui histórico independente da linha atual e foi avaliada como fonte
de ideias, sem merge ou cherry-pick indiscriminado. A decisão considera o plano
mestre e as decisões metodológicas vigentes.

## Resultado

| Grupo de mudanças | Decisão | Motivo |
|---|---|---|
| Forecast tolerante a métricas nulas (`bf7f053`) | Portado seletivamente | Ausência de métricas deve produzir lacunas, não erro técnico. |
| Validação e compatibilidade de briefing (`dc1e09a`, `cd9b5cd`, `bf7f053`) | Já atendido | O serviço atual valida o briefing e preserva compatibilidade com o fluxo persistido. |
| Ranking centralizado no score (`cce94d9`, `07b9d4d`) | Superado | O pipeline atual separa elegibilidade, restrições duras e score. A versão antiga ainda inclui defaults e bônus incompatíveis. |
| Reordenação e desacoplamento do planejador (`6de82a6`, `27ebfae`) | Não portado | A arquitetura alternativa não contém os contratos atuais de custos, comparabilidade, proveniência e restrições. |
| Teste offline do pipeline (`cea2b94`) | Já atendido | A suíte atual cobre engines, serviços e o fluxo completo até a exportação. |
| Compatibilidade de imports e páginas (`6526254`, `7672f1b`, `ad01e8a`) | Não necessária | Os módulos ativos importam e compilam sem os wrappers legados. |
| Normalização de payloads e metadados (`00ec81b`, `4f19da1`) | Adiado | Depende do modelo de propriedade e repositories autenticados das Fases 4 e 5. |
| Campanhas, workspace e cadastros de mídia (`9b4dfd4`, `91b9dc5` e relacionados) | Adiado | São insumos para as Fases 5 e 6, não correções dos engines da Fase 2. |

## Conclusão

Não há base segura para mesclar os históricos. O único comportamento ainda
necessário à Fase 2 foi reimplementado sobre a arquitetura atual. Itens adiados
deverão ser reavaliados contra o modelo multiusuário antes de qualquer porte.
