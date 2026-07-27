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

- login e sessão estão implementados, mas ainda não ativados na implantação;
- inventários globais/privados e bibliotecas de público serão tratados depois;
- a autenticação continuará desativada até existirem contas e membresias de
  teste controladas.

O backup pré-migration `20260727030000` e seu ensaio de restauração foram
concluídos em 27 de julho de 2026. A cópia durável está privada no Google
Drive, com manifesto SHA-256 e contagens materiais equivalentes à origem.
A migration foi aplicada remotamente de forma controlada após esse gate. O
teste autenticado posterior continua pendente.

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
`anon` e `authenticated`, preservando-a apenas para `service_role`.

A substituta `proximo_codigo_copia_espaco`:

- aceita somente projetos, briefings e planejamentos;
- exige usuário autenticado com permissão de edição;
- confere ID, código e espaço do registro de origem;
- evita SQL dinâmico e tabelas arbitrárias;
- só então chama a reserva atômica legada.

Cópias autenticadas de inventários, universos, segmentos e públicos continuam
bloqueadas até a definição de escopo global ou privado na Fase 5. Isso evita
trocar o bypass do cliente administrativo por um bypass dentro do banco.

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

## Contexto de espaço de trabalho

- após o login, a aplicação consulta somente espaços permitidos pela RLS;
- usuário comum recebe o papel da própria membresia e administrador pode
  selecionar qualquer espaço ativo;
- um espaço único é selecionado automaticamente; múltiplos exigem escolha;
- a escolha é revalidada a cada rerun e valores forjados são recusados;
- inclusões de projetos, briefings, planejamentos e artefatos recebem sempre o
  `espaco_id` do contexto validado, substituindo qualquer valor do payload;
- listagens dessas tabelas recebem filtro adicional pelo espaço ativo, sem
  substituir a proteção RLS do banco;
- troca de espaço limpa projeto, briefing, plano e resultados derivados;
- logout ou expiração limpa todo o estado privado da sessão, prevenindo
  exposição residual quando outra pessoa usa o mesmo navegador.

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
- atualização comum de projeto preservada sem acessar colunas exclusivas das
  tabelas dependentes;
- todos os registros e identidades de teste foram revertidos por `rollback`.
- testes unitários confirmaram aplicação do JWT, isolamento do contexto,
  fallback transitório e injeção de cliente nos repositories.
- login, renovação, expiração, senha temporária e limpeza local também foram
  cobertos por testes unitários, ainda sem ativação na implantação.
- seleção autorizada, troca de contexto, inclusão forçada no espaço e
  filtragem de leituras foram validadas por testes específicos.
- a cópia contextual foi testada para proprietário e negada para leitor.

## Aplicação remota

Em 27 de julho de 2026:

- `20260727030000` foi aplicada e confirmada no histórico remoto;
- regressão funcional e três integrações conectadas foram aprovadas;
- foi criado um espaço legado, ainda sem membros;
- não havia usuários em `auth.users`, portanto não foram criados perfis;
- projetos, briefings, planejamentos e artefatos ficaram com zero registros
  sem `espaco_id`;
- `PLANOS_AUTH_ENABLED` permaneceu desligado.
