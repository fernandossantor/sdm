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
- repositories ainda não usam JWT de usuário;
- login e sessão ainda não foram implementados;
- inventários globais/privados e bibliotecas de público serão tratados depois;
- testes locais e revisão das políticas precedem backup e aplicação remota.

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
