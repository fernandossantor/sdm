# Banco de Dados

Banco oficial:

Supabase PostgreSQL

---

## Convenções

- UUID como chave primária.
- snake_case.
- plural para tabelas.
- foreign keys explícitas.

---

## Estrutura principal

cenarios

↓

universos

↓

segmentos

↓

segmento_interesse

↓

publicos

↓

inventarios

↓

consumo_midia

---

## Filosofia

O banco representa conhecimento.

As regras pertencem aos motores.

---

## Segurança

- RLS deve permanecer habilitado em todas as tabelas expostas pela API.
- `anon` e `authenticated` não possuem acesso enquanto o SDM não tiver login.
- `SUPABASE_SERVICE_KEY` é exclusiva do backend e de scripts administrativos.
- A interface nunca deve importar `admin_client` nem receber a chave de serviço.
- Toda mudança de permissão deve ser registrada em `database/sql/`.

### Aplicação e auditoria de RLS

A migration executável pelo Supabase CLI fica em `supabase/migrations/` e deve
espelhar a versão de referência mantida em `database/sql/`.

As migrations de segurança atuais são:

- `040_seguranca_rls.sql`: bloqueio público e acesso administrativo das tabelas
  principais;
- `041_universos_rls.sql`: RLS explícita para o cadastro de universos.

```bash
npx supabase db push --dry-run
npx supabase db push
python -m scripts.auditar_seguranca
```

O `db push` exige uma sessão autenticada (`supabase login`) ou a variável
`SUPABASE_ACCESS_TOKEN`. A auditoria exige as três variáveis descritas em
`.env.example` e termina com erro se a chave pública ler qualquer tabela ou se
a chave de serviço não conseguir lê-la. A auditoria inclui `universos`.
