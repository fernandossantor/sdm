# Inventário técnico do legado

Data: 29/07/2026
Commit inventariado: `544fbdabed9c247700624402f6097c94cb1b1557`
Preservação local: tag anotada `legacy-pre-mediad-planner-v1`

## Estado inicial

O `main` foi atualizado somente por fast-forward. Antes da implementação já existiam
dois itens não rastreados, preservados e fora do escopo: `docs/PLANO_EVOLUCAO_INTEGRADO.md`
e `docs/materials/`. A suíte existente falhava durante a coleta porque `scipy`, embora
declarado no `requirements.txt`, não estava instalado no ambiente.

## Árvore resumida e classificação

| Componente | Conteúdo atual | Classificação | Diretriz |
|---|---|---|---|
| `app.py` | Entrada Streamlit, configuração inicial e navegação | ADAPTAR | Manter executável; redirecionar progressivamente |
| `pages/` | 22 páginas funcionais do SDM | ISOLAR | Preservar até haver equivalência validada |
| `components/` | Componentes Streamlit, sessão e fluxo | ADAPTAR | Reaproveitar apenas apresentação genérica |
| `application/services/` | Serviços de briefing, planejamento, cenários, forecast, autenticação e colaboração | ADAPTAR | Extrair regras para domínio/casos de uso |
| `application/admin/` | Administração de contas | REUTILIZAR | Manter fronteira administrativa |
| `domain/models/` | Briefing, forecast, plano, realizado e workflow | ADAPTAR | Migrar incrementalmente aos contratos novos |
| `domain/*.py` | Custos, métricas, catálogo e restrições | ADAPTAR | Validar contra Bibliotecas 13, 17 e 18 |
| `engine/` | Motores históricos de alocação, forecast, score, recomendação, comparação e otimização | ISOLAR | Não promovê-los automaticamente aos três novos motores |
| `infrastructure/database/` | Clientes Supabase tardios e contexto de workspace | REUTILIZAR | Centralizar configuração sem conexão no import |
| `infrastructure/repositories/` | Repositórios concretos do legado | ADAPTAR | Fazer depender de portas explícitas |
| `supabase/migrations/` | Migrações versionadas e RLS | REUTILIZAR | Fonte principal do esquema inferível |
| `database/sql/` | Espelhos/atalhos SQL históricos | INDETERMINADO | Conferir divergências antes de consolidar |
| `tests/` | Testes unitários, integração, arquitetura e SQL | REUTILIZAR | Manter; separar falhas preexistentes |
| `scripts/` | Seed, auditoria, health check, backup e homologação | ADAPTAR | Classificar escrita/leitura antes de executar |
| `data/` | Seeds CSV de inventários | ADAPTAR | Tratar como carga versionada, não verdade do runtime |
| `docs/new_app/` | Especificação normativa MediAd Planner | REUTILIZAR | Aplicar precedência do documento 30 |
| `projeto.zip` | Snapshot binário do projeto | REMOVER_DEPOIS | Só após confirmar finalidade e backup |

## Ponto de entrada e páginas

O ponto de entrada é `app.py`. Ele importa Streamlit, carrega configuração de ambiente
e compõe a experiência existente. As páginas cobrem briefing, catálogos, guia,
papéis, inventários, planejamento, forecast, dashboard, exportação, diagnóstico,
comparação, cenários, otimização, insights, públicos, universos, segmentos,
cronograma, administração, colaboração, atribuição e qualidade/localização.

## Dependências e configuração

O projeto usa `requirements.txt`: Streamlit, Supabase/PostgREST, pandas, NumPy,
SciPy, openpyxl, matplotlib, Pydantic 2, dotenv, HTTPX, dateutil, pytest e ferramentas
de qualidade. Há também `package.json`, usado para tooling do Supabase.

Configurações relevantes: `.env.example`, `.devcontainer/devcontainer.json`,
`.github/workflows/ci.yml`, `.gitignore` e `supabase/config.toml`.

## Reuso e conflitos

Reuso provável:

- inicialização tardia dos clientes Supabase;
- autenticação, workspace, compartilhamento e RLS;
- migrações versionadas;
- componentes visuais genéricos;
- testes de segurança, backup e isolamento;
- modelos e procedimentos quantitativos após validação metodológica.

Conflitos com a arquitetura nova:

- `engine/` expressa muitos motores históricos, enquanto a arquitetura normativa
  possui somente três motores especialistas;
- regras aparecem em páginas, serviços e engines e precisarão ser desacopladas;
- comparação e otimização não podem permanecer como motores autônomos;
- nomes SDM, PlanOS e MCP são históricos e devem ser substituídos progressivamente;
- fórmulas existentes não devem ser copiadas sem vínculo versionado à Biblioteca 17.

## Riscos

1. O banco remoto não pôde ser confrontado com as migrações.
2. Migrações e `database/sql/` podem divergir.
3. O ambiente atual não reproduz integralmente o `requirements.txt`.
4. Há lógica de domínio distribuída na interface e nos serviços.
5. Arquivos não rastreados preexistentes não estão cobertos pela tag de preservação.
6. Alterar o ponto de entrada agora elevaria o risco sem benefício para a fundação.

Nenhum componente foi removido ou substituído neste inventário.
