# Ponto de situação e retomada

Data do fechamento: 30/07/2026

Branch: `main`

Último commit funcional antes deste checkpoint: `0a643f2`

## Estado do Git

- `origin/main`: `544fbda`;
- `main` estava 8 commits à frente do remoto antes deste checkpoint;
- tag recuperável da versão anterior:
  `legacy-pre-mediad-planner-v1` em `544fbda`;
- nenhum push foi realizado;
- não existe branch de implementação pendente de merge;
- `docs/PLANO_EVOLUCAO_INTEGRADO.md` e `docs/materials/` são itens do usuário,
  não rastreados e deliberadamente não incluídos nos commits.

## Decisão sobre a versão anterior

“Versão anterior” ou “legado” significa o aplicativo anterior e seus arquivos.
Esses arquivos permanecem no repositório apenas como memória recuperável, mas não
estão acessíveis pela navegação nova.

O contexto e as informações que precisam persistir entre telas da nova aplicação
não são legado. Eles pertencem ao novo MediAd Planner e deverão ser preservados
em sessão e em armazenamento durável conforme sua natureza.

Não criar adaptadores de compatibilidade ou integrações com serviços antigos sem
necessidade funcional comprovada.

## Entregas concluídas

1. Inventário técnico da versão anterior e do Supabase.
2. Plano de transição executável.
3. Tag local recuperável da versão anterior.
4. Fundação de contratos comuns dos motores.
5. Portas abstratas e configuração segura do Supabase.
6. Domínio canônico inicial de Campanha e Briefing.
7. Casos de uso de abertura da Campanha e início do Briefing.
8. Fachada falsa de Tradução Estratégica, sempre honesta e parcial.
9. Nova entrada Streamlit e navegação inicial:
   - Visão Geral;
   - Abertura da Campanha;
   - Briefing de mídia.
10. Migração local `20260730010000_campanhas_briefings_mediad.sql`.
11. Rollback local correspondente.
12. Adaptador Supabase novo para Campanha/Briefing.

## Estado da interface

- `app.py` aponta apenas para a nova camada `presentation`;
- páginas da versão anterior não possuem rota na nova navegação;
- os formulários de Campanha ainda estão desabilitados;
- não há autenticação, seleção de espaço ou gravação conectadas à interface nova;
- nenhuma regra de domínio foi colocada nas páginas.

## Estado da persistência

A migração `20260730010000` cria:

- `campanhas_mediad`;
- `campanhas_mediad_equipe`;
- `briefings_mediad`;
- políticas RLS por espaço;
- RPC transacional de abertura da Campanha;
- RPC transacional de início do Briefing;
- bloqueio de escrita direta para `anon` e `authenticated`;
- validações de autoria, membresia, equipe e imutabilidade do espaço.

O adaptador `UnidadeTrabalhoCampanhaSupabase`:

- recebe cliente autenticado e espaço por injeção;
- não importa clientes, serviços ou repositórios da versão anterior;
- usa uma RPC por transição atômica;
- reconstitui Campanha e equipe a partir das tabelas novas.

## Estado do Supabase no fechamento

- 25 migrações locais;
- 24 migrações remotas;
- `20260730010000` existe somente localmente;
- dois `db push --dry-run` confirmaram que apenas essa migração seria enviada;
- nenhuma migração foi aplicada;
- nenhuma tabela, função, política ou dado remoto foi alterado nesta etapa.

## Validações aprovadas

- suíte completa: `191 passed, 3 skipped`;
- Black: aprovado;
- Flake8: aprovado nos arquivos novos;
- `compileall`: aprovado;
- `git diff --check`: aprovado;
- varredura de segredos: aprovada;
- inicialização Streamlit por `AppTest`: aprovada;
- `supabase db push --linked --dry-run`: aprovado.

O SQL ainda não foi executado contra um banco isolado porque o ambiente atual não
possui Docker/Postgres local. O `dry-run` valida a fila da migração, mas não
substitui a execução controlada do SQL.

## Ponto exato de retomada

Retomar pela revisão e aplicação controlada da migração
`20260730010000_campanhas_briefings_mediad.sql`.

Sequência recomendada:

1. confirmar `git status -sb`;
2. executar `python -m pytest -q`;
3. executar `npx supabase migration list --linked` em modo somente leitura;
4. revisar a migração e o rollback;
5. preferencialmente executar a migração em Supabase local ou ambiente isolado;
6. obter confirmação explícita antes de aplicar no Supabase conectado;
7. após a aplicação, validar tabelas, funções, RLS e acesso entre espaços;
8. somente então conectar autenticação, espaço ativo e formulário de Campanha;
9. preservar o ID da Campanha e do espaço entre as telas da nova aplicação;
10. implementar o Briefing progressivamente, uma seção normativa por fatia.

## Ações que continuam proibidas sem confirmação

- aplicar a migração no Supabase conectado;
- executar o rollback;
- remover arquivos ou tabelas da versão anterior;
- alterar dados existentes;
- executar `DROP`, `TRUNCATE` ou exclusões em massa;
- fazer push dos commits ou publicar a tag;
- incluir os arquivos não rastreados do usuário em commits.

## Commits desta transição

- `f1ec450` — inventário e plano de transição;
- `236518c` — fundação arquitetural;
- `536823b` — testes da fundação;
- `b2031c6` — diagnóstico conectado do Supabase;
- `6285ff1` — primeira fatia de Campanha/Briefing;
- `da6852d` — fachada falsa de Tradução Estratégica;
- `9ad637e` — nova navegação do MediAd Planner;
- `0a643f2` — persistência local de Campanha/Briefing.
