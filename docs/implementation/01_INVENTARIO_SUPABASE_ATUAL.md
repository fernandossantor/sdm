# Inventário do Supabase atual

Data: 29/07/2026
Modo: diagnóstico conectado, somente leitura

## Estado da conexão

As credenciais foram carregadas em memória pelo mecanismo seguro do Codespace, sem
impressão ou persistência dos valores. A CLI foi vinculada ao projeto já documentado
e confirmou conectividade com o banco remoto.

Foram executadas apenas operações de leitura:

- inspeção de estatísticas das tabelas;
- health check das tabelas críticas;
- auditoria de acesso público e administrativo;
- testes de integração;
- comparação das migrações locais e remotas.

Não houve migração, escrita, alteração de política ou consulta a conteúdo sensível.

## Estado remoto confirmado

- 94 tabelas no esquema público;
- 46 tabelas com linhas estimadas e 48 sem linhas estimadas;
- 2.286 linhas estimadas no total — valor estatístico, não contagem transacional;
- 20 tabelas críticas aprovadas no health check;
- acesso público bloqueado e acesso administrativo válido nas tabelas auditadas;
- 24 migrações locais e remotas sincronizadas;
- última migração: `20260727090000`.

## Estado local posterior ao diagnóstico

Em 30/07/2026 foi preparada a migração local `20260730010000`, ainda não
aplicada. Uma nova consulta somente leitura confirmou:

- 25 migrações locais;
- 24 migrações remotas;
- `20260730010000` presente apenas localmente.

O estado remoto descrito neste inventário não foi alterado.

## Objetos confirmados e inferidos das migrações

| Grupo | Objetos principais | Classificação |
|---|---|---|
| Identidade e acesso | `perfis_usuarios`, `espacos_trabalho`, `membros_espacos`, `projetos_membros` | PRESERVAR |
| Campanha e trabalho | `projetos`, `briefings_v3`, `planejamentos`, `cenarios_v3`, `artefatos_workflow` | MIGRAR |
| Bibliotecas | inventários, objetivos, KPIs, métricas, públicos, segmentos, interesses, jornadas, universos | REUTILIZAR |
| Mensuração | `unidades_metricas`, `metricas_catalogo`, `formulas_metricas`, `conversoes_metricas`, `valores_metricas`, `medicoes_inventario` | REUTILIZAR |
| Versionamento | `versoes_planejamento`, identificadores e contadores | PRESERVAR |
| Comercial | preços, condições comerciais, modalidades e unidades de compra | REUTILIZAR |
| Auditoria | `logs_auditoria` | PRESERVAR |
| Legado com sufixo `_v3` | tabelas de catálogo, briefing e inventário | INDETERMINADO |
| Legado anterior e nomes em inglês | `campaigns`, `briefings`, `audiences`, `media_*` e estruturas históricas | REMOVER_SOMENTE_APOS_BACKUP |

As migrações também definem `pgcrypto`, funções de autorização e códigos,
triggers de integridade/auditoria/imutabilidade e um conjunto amplo de políticas RLS.
Não foram identificadas views nas migrações pela inspeção textual. A confirmação
exaustiva de views, funções, triggers e extensões remotas depende de exportação do
catálogo.

## Relacionamentos e controles relevantes

- projetos, briefings, planejamentos, artefatos e versões são associados a espaços;
- membros e proprietários condicionam leitura e edição;
- inventários admitem escopo global/privado;
- versões de planejamento possuem proteção de imutabilidade;
- códigos originais e de cópia são gerados por funções/triggers;
- RLS está habilitada para objetos de negócio e bibliotecas.

## Dados e legado

As maiores estruturas por linhas estimadas são catálogos e relações estruturais,
especialmente afinidades, formatos e modalidades de compra. Há também poucos
registros operacionais em projetos, briefings, planejamentos, inventários,
workspaces, versões e auditoria.

As estatísticas não permitem classificar linhas individuais como teste ou
descartáveis. Os CSVs em `data/` continuam sendo candidatos a sementes
estruturais, sem substituir a verificação de proveniência.

## Limitação remanescente

O export lógico somente do esquema foi tentado, mas a CLI exige Docker para essa
operação e o contêiner atual não o disponibiliza. Não foi instalada infraestrutura
adicional para contornar a limitação.

Antes de qualquer migração destrutiva:

1. exportar o catálogo ou esquema remoto em ambiente com Docker/`pg_dump`;
2. confrontar colunas, PKs, FKs, views, funções, triggers, extensões e políticas;
3. gerar e testar backup lógico;
4. identificar proveniência e uso das linhas legadas;
5. obter confirmação explícita para qualquer remoção.

Até essa confrontação, objetos ativos prevalecem como `PRESERVAR`, `REUTILIZAR`
ou `INDETERMINADO`; estruturas legadas são apenas candidatas a
`REMOVER_SOMENTE_APOS_BACKUP`.
