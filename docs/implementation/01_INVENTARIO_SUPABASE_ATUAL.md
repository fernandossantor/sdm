# Inventário do Supabase atual

Data: 29/07/2026
Modo: somente leitura documental

## Limitação do diagnóstico

`SUPABASE_URL`, `SUPABASE_KEY` e `SUPABASE_SERVICE_KEY` não estavam presentes no
processo e a CLI Supabase não está instalada. Nenhum valor sensível foi consultado
ou impresso. Não houve conexão remota, instalação de ferramenta, migração ou escrita.
Assim, este inventário descreve o estado **versionado**, não confirma o estado remoto.

## Objetos inferidos das migrações

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

As migrações também definem `pgcrypto`, funções de autorização e códigos,
triggers de integridade/auditoria/imutabilidade e um conjunto amplo de políticas RLS.
Não foram identificadas views nas migrações pela inspeção textual.

## Relacionamentos e controles relevantes

- projetos, briefings, planejamentos, artefatos e versões são associados a espaços;
- membros e proprietários condicionam leitura e edição;
- inventários admitem escopo global/privado;
- versões de planejamento possuem proteção de imutabilidade;
- códigos originais e de cópia são gerados por funções/triggers;
- RLS está habilitada para objetos de negócio e bibliotecas.

## Dados

Sem conexão não é possível classificar linhas como estruturais, teste ou descartáveis.
Os CSVs em `data/` parecem sementes estruturais, mas não comprovam o conteúdo remoto.

## Próximo diagnóstico seguro

Quando a configuração estiver disponível:

1. verificar conectividade com chave pública;
2. exportar catálogo de tabelas, colunas, PKs, FKs, views, funções, triggers,
   extensões e políticas;
3. comparar o remoto às migrações;
4. contar e amostrar apenas metadados necessários;
5. gerar backup lógico antes de qualquer migração destrutiva.

Objetos somente poderão ser classificados como `SUBSTITUIR` ou
`REMOVER_SOMENTE_APOS_BACKUP` após essa confrontação. Até lá, prevalece `PRESERVAR`
ou `INDETERMINADO`.
