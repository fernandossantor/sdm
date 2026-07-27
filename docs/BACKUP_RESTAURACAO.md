# Backup e restauração

Último ensaio: 27 de julho de 2026 (UTC).

## Escopo

Antes de qualquer migration estrutural, gerar fora do repositório:

- `schema.sql`: esquema do projeto vinculado;
- `data.sql`: dados de todos os schemas incluídos pela CLI;
- `public-data.sql`: dados da aplicação, limitados ao schema `public`;
- `roles.sql`: papéis exportáveis do banco;
- checksums SHA-256 dos quatro arquivos.

Os dumps contêm dados e não devem ser versionados nem armazenados em área
pública. `/tmp` serve apenas ao ensaio local; a cópia durável deve ficar em
armazenamento privado, criptografado e com retenção definida.

## Geração

Com o projeto correto previamente vinculado:

```bash
SUPABASE_TELEMETRY_DISABLED=1 npx supabase db dump \
  --linked --file "$BACKUP_DIR/schema.sql"
SUPABASE_TELEMETRY_DISABLED=1 npx supabase db dump \
  --linked --data-only --use-copy --file "$BACKUP_DIR/data.sql"
SUPABASE_TELEMETRY_DISABLED=1 npx supabase db dump \
  --linked --data-only --use-copy --schema public \
  --file "$BACKUP_DIR/public-data.sql"
SUPABASE_TELEMETRY_DISABLED=1 npx supabase db dump \
  --linked --role-only --file "$BACKUP_DIR/roles.sql"
sha256sum "$BACKUP_DIR"/*.sql
```

`BACKUP_DIR` deve apontar para um diretório explícito e privado. Não usar o
workspace Git.

## Ensaio de restauração

1. Inicializar um projeto Supabase temporário sem migrations da aplicação.
2. Subir somente o PostgreSQL para evitar dependência dos demais serviços.
3. Se os dados públicos referenciarem `auth.users`, criar primeiro o esquema
   `auth` da mesma versão local do Supabase.
4. Restaurar `schema.sql` com `psql -v ON_ERROR_STOP=1`.
5. Restaurar `data.sql` até concluir os blocos de `auth` e `public`; erros
   posteriores em schemas internos não invalidam esses blocos, mas devem ser
   registrados.
6. Reaplicar as migrations idempotentes que criam objetos entre schemas,
   especialmente gatilhos pertencentes a `auth`.
7. Conferir tabelas, constraints, identidades Auth e contagens de entidades
   materiais.
8. Aplicar a migration seguinte e executar seus testes SQL no banco restaurado.
9. Encerrar o ambiente temporário.

O dump completo inclui tabelas internas de `storage`. A restauração direta
dessas tabelas pode exigir o proprietário administrativo do serviço. Para
validar os dados da aplicação de forma determinística, usar
`public-data.sql`; objetos de Storage devem seguir o procedimento oficial do
serviço e ter validação separada.

O dump de esquema da aplicação não contém necessariamente gatilhos pertencentes
ao schema `auth` que chamam funções de `public`. Por isso, restaurar somente
`public-data.sql` deixou de ser um ensaio suficiente depois da adoção de
usuários reais. A restauração deve incluir as identidades de `auth` e reaplicar
a migration multiusuário idempotente para recompor esses objetos entre schemas.

## Resultado do ensaio de 26 de julho de 2026

- esquema restaurado sem erro em PostgreSQL 17 do Supabase local;
- 83 tabelas públicas e 93 chaves estrangeiras presentes;
- dados públicos restaurados antes do início dos blocos de Storage;
- contagens verificadas: 2 projetos, 2 briefings, 1 planejamento e
  16 inventários;
- referências circulares entre `projetos` e `briefings_v3` não impediram a
  carga no conjunto atual;
- carga do dump completo parou em `storage.buckets_vectors` por propriedade
  interna do serviço, sem afetar a validação do schema `public`;
- migrations locais atuais não recriam o banco desde o zero, pois partem de
  um esquema-base que ainda não está versionado.

## Cópia durável de 27 de julho de 2026

O conjunto anterior à migration `20260727000000` foi copiado para a pasta
privada [PlanOS Backups / 2026-07-27 pre-migration
20260727000000](https://drive.google.com/drive/folders/1d8ZtFBRiYJ6bnQ0V4fSJ6y_sDoxRuVx9)
no Google Drive conectado.

Foram verificados quatro arquivos com os mesmos tamanhos dos originais:

- `schema.sql`: 95.301 bytes;
- `data.sql`: 404.289 bytes;
- `public-data.sql`: 395.446 bytes;
- `roles.sql`: 358 bytes.

Todos foram confirmados como não compartilhados (`not_shared`).

Antes da migration `20260727010000`, um segundo conjunto foi copiado para a
pasta privada [PlanOS Backups / pre-migration
20260727010000](https://drive.google.com/drive/folders/1CClQzjIfWGuPqW8JfdrPzaezLc6lWc1A).

Os quatro arquivos também foram confirmados como não compartilhados:

- `schema.sql`: 106.489 bytes;
- `data.sql`: 408.703 bytes;
- `public-data.sql`: 399.860 bytes;
- `roles.sql`: 358 bytes.

Antes da migration `20260727020000`, um terceiro conjunto foi copiado para a
pasta privada [PlanOS Backups / pre-migration
20260727020000](https://drive.google.com/drive/folders/1So_nysbnRq8Y0ygwJiI9iv6ruQ7zSlaw).

Os quatro arquivos foram confirmados com `shared=false`, somente com a
permissão do proprietário, e com os mesmos tamanhos dos dumps locais:

- `schema.sql`: 112.551 bytes;
- `data.sql`: 411.023 bytes;
- `public-data.sql`: 402.180 bytes;
- `roles.sql`: 358 bytes.

Antes da migration `20260727030000`, um quarto conjunto foi gerado e copiado
para a pasta privada [PlanOS Backups / pre-migration
20260727030000](https://drive.google.com/drive/folders/14s1xBYS9CmOHhdt2OcfO_eW8G6zC6q_c).

Os cinco arquivos foram confirmados com `shared=false` e
`source_visibility_status=not_shared`, com os mesmos tamanhos locais:

- `schema.sql`: 114.992 bytes;
- `data.sql`: 411.761 bytes;
- `public-data.sql`: 402.918 bytes;
- `roles.sql`: 358 bytes;
- `SHA256SUMS`: 310 bytes.

O ensaio foi repetido em banco PostgreSQL isolado. Um banco vazio exigiu os
pré-requisitos de plataforma `extensions`, `vault` e a publicação
`supabase_realtime`, normalmente criados pelo bootstrap do Supabase. Depois
deles:

- o esquema foi restaurado com `ON_ERROR_STOP`;
- os dados públicos foram restaurados integralmente;
- 89 tabelas públicas e 106 chaves estrangeiras foram verificadas;
- origem e restauração coincidiram em projetos (2), briefings (2),
  planejamentos (1), inventários (16), versões (1) e métricas (8);
- o banco temporário foi removido e o ambiente local desligado.

Antes da migration `20260727040000`, um quinto conjunto foi copiado para a
pasta privada [PlanOS Backups / pre-migration
20260727040000](https://drive.google.com/drive/folders/10a82X6KMHsQJjcB7FfxuwKqBvSWW5V0F).

Os cinco arquivos foram confirmados com `shared=false` e
`source_visibility_status=not_shared`, com os mesmos tamanhos locais:

- `schema.sql`: 133.139 bytes;
- `data.sql`: 417.276 bytes;
- `public-data.sql`: 406.832 bytes;
- `roles.sql`: 358 bytes;
- `SHA256SUMS`: 310 bytes.

O ensaio desta cópia incluiu o schema e as duas identidades reais do Supabase
Auth. Depois de restaurar os blocos de `auth` e `public`, a migration
multiusuário idempotente foi reaplicada para recriar o gatilho entre schemas.
Foram confirmadas 92 tabelas públicas, 114 chaves estrangeiras, 2 identidades,
2 perfis, 2 espaços, 2 membresias, 2 projetos, 2 briefings, 1 planejamento,
16 inventários, 2 versões e 8 métricas. Por fim, a migration
`20260727040000` e o teste SQL de auditoria administrativa passaram no banco
restaurado.

## Pendências operacionais

- definir retenção e responsáveis;
- versionar o esquema-base anterior à migration `20260721000000`;
- criar ensaio separado para metadados e objetos do Storage;
- automatizar comparação de contagens entre origem e restauração.
