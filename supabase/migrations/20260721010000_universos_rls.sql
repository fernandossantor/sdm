-- Protege o cadastro de universos exposto pela API.
alter table if exists public.universos enable row level security;

revoke all on table public.universos from anon, authenticated;
grant all on table public.universos to service_role;
