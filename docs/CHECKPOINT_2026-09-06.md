# Checkpoint — 06/09/2026

Registro operacional de continuidade, sem força normativa. A única fonte normativa é `docs/new_app/`, com a precedência do documento 30. Este checkpoint sucede `CHECKPOINT_2026-09-05.md`, que conserva os detalhes das entregas.

## Estado salvo

- Branch: `main`.
- Última entrega de código: `fa4c978`.
- Os cinco commits de implementação e o checkpoint inicial `a9da400` foram enviados à `main` do GitHub; push de `ccd2a01` até `a9da400` confirmado.
- Este registro foi atualizado após o envio para servir como novo checkpoint de encerramento, preservando o histórico anterior.
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
2. Verificar o CI da revisão final enviada e confirmar separadamente qual revisão está publicada no Streamlit.
3. Próxima entrega funcional sugerida: ampliar os diagnósticos objetivos de prioridades iguais e justificativas de máximas para objetivos declarados e Públicos, conforme a seção 13.3 de `02_BRIEFING.md`.
4. Manter explícito o recorte atual: ordenação avaliada para múltiplas etapas de máxima prioridade (5), por Jornada. Isso não certifica cobertura integral das seções 10.4 e 13.3.
5. Permanecem pendentes avaliação completa de coerência e suficiência, reconhecimento explícito de alertas, histórico/comparação de versões, conclusão do Briefing e transição para Tradução Estratégica.
6. Revisar as incoerências territoriais atualmente rejeitadas na entrada à luz das validações sem bloqueio indevido antes de certificar a conclusão.

O usuário solicitou commit e novo checkpoint. Nenhuma nova implementação funcional faz parte deste encerramento.

## Retomada — 12/09/2026: prioridades de objetivos e públicos

Retomada autorizada pelo usuário. Confirmados `main` local/remota em `aceb960` e CI aprovado dessa revisão: https://github.com/fernandossantor/sdm/actions/runs/34055062384. A revisão publicada no Streamlit permanece sem confirmação.

Entrega baseada em `02_BRIEFING.md`, seções 8.2–8.4 e 13.1–13.3: diagnósticos de prioridades iguais e múltiplas máximas sem justificativa ampliados para Objetivos de Marketing, Objetivos de Comunicação e Públicos. Cada conjunto é avaliado separadamente. Máxima corresponde a 5 na escala existente. Igualdade exige mais de um item e prioridade informada em todos; ausência continua como lacuna, sem ser convertida em valor. Havendo múltiplas máximas, cada item sem justificativa é identificado, inclusive quando os demais estão justificados.

Os diagnósticos são calculados no domínio e chegam às subetapas e à revisão pelo resumo existente. A avaliação permanece somente de leitura e parcial, sem alterar declarações, metadados, permissões ou estados.

Arquivos afetados:

- `mediad_planner/domain/briefing/revisao.py`;
- `mediad_planner/presentation/objetivos_declarados.py` e `segmentos.py`;
- `tests/test_diagnosticos_prioridades.py` e `test_frontoffice_diagnosticos_prioridades.py`;
- este checkpoint operacional.

Critérios de aceite verificados: conjuntos independentes; nenhum alerta coletivo para conjunto vazio ou item único; ausência distinta de igualdade; identificação das justificativas ausentes com referência normativa e entidade; preservação dos dados pela avaliação; mesmos avisos na subetapa e revisão; recálculo após remoção nos três conjuntos e após edição de prioridade/justificativa de Públicos.

Validação: **483 testes aprovados** em cópia limpa dos arquivos rastreados com as alterações desta entrega; compilação de `app.py`, `mediad_planner` e `tests` aprovada; `git diff --check` aprovado. Foram acrescentados 35 testes. Os testes de interface completam a renderização após a remoção, cujo `st.rerun` pode deixar elementos anteriores no resultado intermediário do AppTest.

Continuam pendentes os demais diagnósticos da seção 13.3, avaliação completa de coerência/suficiência, reconhecimento de alertas, histórico/versionamento e conclusão/transição do Briefing. Próximo recorte sugerido: confrontar os vínculos de objetivos com Públicos e Praças com as seções 8.2–8.3, antes de implementar diagnósticos que dependam desses vínculos.

`supabase/` e resíduos locais permanecem preservados e fora da entrega. Nenhum conteúdo legado foi consultado ou reutilizado. Esta retomada prepara commit local; não inclui envio ao GitHub nem confirmação de publicação no Streamlit.

## Continuação — 12/09/2026: vínculos dos Objetivos com Públicos e Praças

Continuação autorizada pelo usuário após o commit local `ef975ef`. Conferido que a revisão remota permanecia em `aceb960` antes desta implementação.

Base normativa: `02_BRIEFING.md`, seções 8.2, 8.3 e 17, respeitando a precedência do documento 30. A entrega permite salvar, substituir e retirar Públicos e Praças relacionados a cada Objetivo de Marketing ou Comunicação já cadastrado. Os vínculos são opcionais, usam identidades do Briefing atual e aparecem na lista dos objetivos salvos. Os seletores distinguem Públicos com nomes iguais e explicam a diferença entre Praça territorial e a dimensão Praça do composto de Marketing.

Recorte de interface: o usuário cria o objetivo pelo formulário existente e pode retornar ao objetivo salvo para preencher os vínculos, inclusive depois de cadastrar Praças e Públicos nas subetapas seguintes. As seleções só são aplicadas ao salvar o formulário de vínculos. Desmarcar e salvar retira explicitamente as referências. Vincular um Público não preenche automaticamente suas Praças no Objetivo nem transfere vínculos entre Marketing e Comunicação.

Integridade: IDs precisam existir no mesmo Briefing, ser UUIDs e não se repetir na mesma coleção. A tentativa de remover Público ou Praça ainda relacionado a Objetivo é recusada, com orientação para retirar o vínculo; os dados salvos são preservados. Remover um Objetivo remove suas próprias referências, preservando os Públicos e Praças. A edição de um Público preserva o vínculo por identidade. Permanecem os controles existentes de papel, espaço, campanha, estado, autor e data. As alterações mantêm o Briefing em preenchimento e atualizam os metadados de edição existentes.

Arquivos afetados:

- `mediad_planner/domain/briefing/objetivos_declarados.py` e `entidades.py`;
- `mediad_planner/application/dto/objetivos_declarados.py`, `use_cases/objetivos_declarados.py`, `mappers/briefing.py` e `services/aplicacao_briefings.py`;
- `mediad_planner/composition/briefings.py`;
- `mediad_planner/presentation/objetivos_declarados.py`;
- `tests/test_vinculos_objetivos.py` e `test_frontoffice_vinculos_objetivos.py`;
- este checkpoint operacional.

Critérios de aceite verificados: vínculos opcionais e múltiplos nos dois tipos de Objetivo; salvamento, alteração, retirada e reabertura pelo repositório em memória existente; preservação dos demais campos e do outro Objetivo; escolhas não salvas distintas dos dados declarados; isolamento de referências, inclusive quando a entidade existe em outra Campanha; permissões de edição, estados, autoria e data; rejeição de duplicatas, IDs inválidos e referências inexistentes; proteção contra remoções que deixariam vínculos órfãos; manutenção dos vínculos após editar Público.

Validação: **538 testes aprovados** em cópia limpa dos arquivos preparados para a entrega, incluindo **55 novos testes**; compilação de `app.py`, `mediad_planner` e `tests` aprovada; `git diff --cached --check` aprovado. A persistência utilizada continua sendo a infraestrutura em memória existente; esta entrega não acrescenta tabelas ou migrações.

Os diagnósticos de ausência desses vínculos ainda não foram acrescentados. Próximo recorte sugerido: avaliar os apontamentos de Público prioritário sem Objetivo e Objetivo prioritário sem Público ou Praça da seção 13.3, explicitando o recorte de prioridade antes de implementar. Permanecem as lacunas de avaliação completa, reconhecimento de alertas, histórico/versionamento e conclusão/transição. A entrega não certifica completude dos Objetivos declarados nem do Briefing.

Esta continuação prepara um novo commit local. Não houve envio ao GitHub ou confirmação da revisão publicada no Streamlit. `supabase/` e resíduos locais continuam preservados, sem consulta ou reutilização de legado e fora da entrega.
