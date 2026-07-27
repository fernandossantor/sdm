# Revisão de referências — Fase 5

Revisão: 27 de julho de 2026 (UTC).

## Escopo

Esta revisão orienta administração de contas, compartilhamento de projetos,
inventários globais e privados e auditoria. Ela complementa as referências
metodológicas de mídia já incorporadas às fases 1–3; não altera fórmulas ou
conceitos dos engines.

## Referências oficiais

- Supabase, [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security):
  tabelas expostas devem usar RLS; políticas funcionam como filtros aplicados
  a cada consulta e integram a identidade do Supabase Auth.
- Supabase, [User Management](https://supabase.com/docs/guides/auth/managing-user-data):
  dados de perfil expostos pela API devem ficar em tabela pública própria,
  vinculada à chave primária de `auth.users`, com privilégios mínimos e RLS.
- Supabase, [Securing your API](https://supabase.com/docs/guides/api/securing-your-api):
  grants e políticas RLS devem ser tratados em conjunto na proteção da Data
  API.
- OWASP, [Authorization Cheat
  Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html):
  aplicar menor privilégio, negar por padrão, verificar autorização em toda
  requisição e registrar eventos relevantes de controle de acesso.

## Decisões incorporadas

- ocultar páginas não substitui autorização no banco;
- leitor, editor e proprietário são verificados por projeto em toda operação;
- compartilhamento concede acesso somente ao projeto e à sua cadeia, não ao
  restante do espaço;
- revogação remove imediatamente o acesso contextual;
- usuários comuns não alteram inventários globais;
- inventários privados pertencem a um espaço e herdam suas permissões;
- funções `security definer` têm `search_path` fixo, entrada validada e execução
  concedida somente a `authenticated`;
- contas e operações sensíveis usam auditoria sem registrar senhas;
- `service_role` continua ausente dos serviços comuns de colaboração e
  inventário.

## Limitações mantidas

- cadastro público e convites automáticos continuam fora de escopo;
- SMTP não é requisito da operação acadêmica inicial;
- MFA administrativo permanece gate da homologação/publicação;
- login geral só será ativado em publicação gradual, após a homologação da
  fase 7.
