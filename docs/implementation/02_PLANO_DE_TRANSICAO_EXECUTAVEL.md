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
- legado e `app.py` mantidos sem alteração.

## Próxima etapa segura

1. começar navegação nova paralela, mantendo as páginas legadas acessíveis;
2. integrar a abertura de Campanha/Briefing à nova navegação por adaptadores;
3. implementar a primeira regra estratégica somente após contrato e fonte
   normativa serem explicitamente selecionados;
4. persistir comandos e execuções apenas após modelagem e migração revisadas.

## Legado reutilizável

- autenticação, espaços, compartilhamento, auditoria e RLS;
- clientes tardios e repositórios como adaptadores;
- bibliotecas de inventário, público, métricas e custos;
- componentes visuais neutros;
- scripts e testes de segurança/backup após classificação;
- procedimentos matemáticos que forem validados e versionados.

## Candidatos à remoção futura

- `projeto.zip`;
- motores históricos redundantes;
- páginas substituídas com equivalência comprovada;
- nomes, rotas e artefatos SDM/PlanOS/MCP;
- espelhos SQL redundantes;
- tabelas `_v3` que forem migradas e tiverem backup verificado.

Nenhum desses itens está autorizado para remoção nesta etapa.

## Migrações necessárias, ainda não implementadas

- snapshots de campanha;
- comandos, execuções e resultados dos motores;
- validações, alertas, explicações e rastreabilidade;
- dependências, invalidação, reexecução e intervenções humanas;
- bibliotecas 17 e 18 versionadas, após modelagem física;
- mapeamento explícito entre objetos legados e novos contratos.

## Ações destrutivas que exigem confirmação

- apagar ou renomear arquivos e páginas existentes;
- substituir irreversivelmente `app.py`;
- remover dependências;
- executar migração de dados;
- alterar RLS, autenticação, funções ou triggers;
- renomear ou excluir objetos persistidos;
- executar `DROP`, `TRUNCATE` ou exclusões em massa;
- remover dados considerados de teste;
- publicar a tag ou commits no remoto.

## Critério de avanço

Cada fatia deve manter domínio independente de Streamlit/Supabase, possuir contrato
versionado, teste automatizado, migração reversível quando aplicável e comparação
contra o comportamento legado relevante.
