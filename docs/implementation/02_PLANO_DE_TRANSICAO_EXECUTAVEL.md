# Plano de transição executável

## Ações executadas

- `main` atualizado por fast-forward até `544fbda`;
- working tree e itens não rastreados registrados;
- tag local `legacy-pre-mediad-planner-v1` criada no commit `544fbda`;
- documentação normativa prioritária analisada;
- legado e migrações inventariados;
- falha preexistente da suíte registrada;
- fundação de contratos, base dos motores, portas e configuração criada;
- primeira fatia de Campanha/Briefing criada com DTOs, casos de uso, snapshots,
  autorização e persistência abstrata;
- inventário remoto somente leitura executado e 24 migrações locais/remotas
  conciliadas;
- dependências declaradas sincronizadas e ferramentas do ambiente verificadas;
- fachada falsa de Tradução Estratégica criada sobre o contrato comum, com saída
  explicitamente parcial, rastreável e sem regras estratégicas antecipadas;
- `app.py` substituído por uma entrada mínima da nova aplicação;
- navegação inicial criada para Visão Geral, Abertura da Campanha e Briefing;
- páginas e serviços da versão anterior mantidos apenas como memória recuperável,
  sem rota ou integração com a nova interface;
- migração local reversível preparada para Campanhas, equipes e Briefings, com
  isolamento por espaço, RLS e transições atômicas; ainda não aplicada;
- adaptador Supabase novo criado por injeção de cliente autenticado e espaço,
  sem dependência de serviços ou repositórios da versão anterior.

## Próxima etapa segura

1. revisar e validar a migração `20260730010000` em ambiente isolado;
2. aplicar a migração no Supabase somente após confirmação explícita;
3. conectar autenticação, espaço ativo e abertura da Campanha aos casos de uso
   canônicos;
4. implementar o Briefing progressivamente, uma seção normativa por fatia;
5. implementar a primeira regra estratégica somente após contrato e fonte
   normativa serem explicitamente selecionados;
6. persistir comandos e execuções apenas após modelagem e migração revisadas.

## Versão anterior preservada como memória

- a tag `legacy-pre-mediad-planner-v1` mantém uma referência recuperável;
- arquivos históricos permanecem no repositório, mas fora da navegação nova;
- o estado entre telas da nova aplicação não é legado e deverá ser preservado;
- nenhuma integração ou compatibilidade com serviços antigos é requisito;
- eventual remoção física deverá ocorrer em commit próprio e verificável.

## Candidatos à remoção futura

- `projeto.zip`;
- motores históricos redundantes;
- páginas substituídas com equivalência comprovada;
- nomes, rotas e artefatos SDM/PlanOS/MCP;
- espelhos SQL redundantes;
- tabelas `_v3` que forem migradas e tiverem backup verificado.

Nenhum desses itens está autorizado para remoção nesta etapa.

## Migrações necessárias, ainda não implementadas

- aplicação remota da migração local de Campanha/Briefing, após validação;
- comandos, execuções e resultados dos motores;
- validações, alertas, explicações e rastreabilidade;
- dependências, invalidação, reexecução e intervenções humanas;
- bibliotecas 17 e 18 versionadas, após modelagem física;
- mapeamento explícito entre objetos legados e novos contratos.

## Ações destrutivas que exigem confirmação

- apagar ou renomear arquivos e páginas existentes;
- excluir fisicamente páginas ou serviços da versão anterior;
- remover dependências;
- executar migração de dados;
- alterar RLS, autenticação, funções ou triggers;
- renomear ou excluir objetos persistidos;
- executar `DROP`, `TRUNCATE` ou exclusões em massa;
- remover dados considerados de teste;
- publicar a tag ou commits no remoto.

## Critério de avanço

Cada fatia deve manter domínio independente de Streamlit/Supabase, possuir contrato
versionado, teste automatizado, migração reversível quando aplicável e aderência
à documentação normativa relevante.
