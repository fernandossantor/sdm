# Auditoria multiusuário — Fase 4

Data: 27 de julho de 2026.

## Estado encontrado

- todos os repositories herdam `BaseRepository`, que usa o cliente
  administrativo;
- `authenticated` está revogado nas tabelas atuais;
- RLS está habilitada, mas funciona apenas como bloqueio público;
- projetos, briefings, planejamentos e artefatos não possuem proprietário;
- versões de planejamento herdam a identidade apenas pela relação com o plano;
- catálogos e inventários ainda não distinguem escopo global e privado.

## Modelo escolhido

O isolamento será feito por espaço de trabalho:

```text
perfil ──< membro >── espaço ──< projeto ──< briefing ──< planejamento
                                      └────< artefato          └────< versão
```

Papéis no espaço:

- `PROPRIETARIO`: administra membros e dados;
- `EDITOR`: cria e altera dados, sem administrar propriedade;
- `LEITOR`: consulta;
- `ADMINISTRADOR`: papel global e operação excepcional.

## Migração inicial

`20260727030000_fundacao_multiusuario.sql`:

- cria perfis, espaços e membros;
- cria perfil automaticamente após inclusão em `auth.users`;
- adiciona `espaco_id` à cadeia central;
- migra registros existentes para um único `Espaço legado`;
- mantém esse espaço sem membros até atribuição administrativa explícita;
- concede acesso autenticado somente através de políticas RLS;
- mantém `service_role` para a aplicação atual durante a transição.

## Limites deste incremento

- a migration ainda não deve ser aplicada remotamente;
- login e sessão ainda não foram implementados;
- inventários globais/privados e bibliotecas de público serão tratados depois;
- testes locais e revisão das políticas precedem backup e aplicação remota.

## Ponte de cliente autenticado

- repositories resolvem o cliente de dados no contexto da requisição;
- quando há `auth_access_token` na sessão, o PostgREST recebe o JWT do usuário;
- o token não é guardado em cache global e o contexto é limpo a cada rerun;
- repositories aceitam injeção direta para testes e operações controladas;
- o fallback para `service_role` permanece explícito somente durante a
  transição, antes da ativação do login;
- serviços de aplicação não importam mais o cliente administrativo.

A RPC legada `proximo_codigo_copia` usa `SECURITY DEFINER` e não valida o
espaço do registro de origem. A migration revoga sua execução de `public`,
`anon` e `authenticated`, preservando-a apenas para `service_role`. Portanto,
o fluxo autenticado de cópia só será habilitado depois de uma RPC contextual,
com autorização por espaço. Essa restrição evita trocar o bypass do cliente
administrativo por um bypass dentro do banco.

## Login e sessão preparados

- o login aceita somente contas previamente criadas; não há cadastro público;
- cada autenticação usa um cliente Supabase isolado, evitando estado global
  compartilhado entre sessões Streamlit;
- tokens ficam apenas na sessão do servidor e são renovados perto da expiração;
- logout invalida a sessão no provedor e remove os dados locais;
- contas inativas são recusadas;
- `trocar_senha=true` bloqueia a navegação até a definição de uma senha nova;
- a RPC contextual `confirmar_troca_senha()` só altera o perfil de `auth.uid()`;
- a interface inteira permanece atrás de `PLANOS_AUTH_ENABLED`, desabilitada
  por padrão até a migração e os testes remotos controlados.

As escolhas foram confrontadas com a documentação oficial do
[Supabase Auth para Python](https://supabase.com/docs/reference/python/auth-signinwithpassword),
do [uso de JWT com RLS](https://supabase.com/docs/guides/auth/jwts) e com o
[guia de sessões da OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
Elas sustentam o uso do JWT do usuário nas políticas, a renovação por sessão,
o logout visível e a não persistência do token em armazenamento do navegador.

## Validação local

- migration executada duas vezes no PostgreSQL isolado sem erro;
- 2 projetos, 2 briefings, 1 planejamento e 1 artefato legados receberam espaço;
- teste transacional com três identidades confirmou:
  - isolamento de leitura entre dois espaços;
  - escrita permitida ao proprietário somente no próprio espaço;
  - escrita negada ao leitor;
  - autopromoção para administrador negada;
  - mudança de um registro entre espaços negada;
  - vínculo entre entidades de espaços diferentes bloqueado;
- todos os registros e identidades de teste foram revertidos por `rollback`.
- testes unitários confirmaram aplicação do JWT, isolamento do contexto,
  fallback transitório e injeção de cliente nos repositories.
- login, renovação, expiração, senha temporária e limpeza local também foram
  cobertos por testes unitários, ainda sem ativação na implantação.
