-- Evolui os cadastros geográficos/demográficos e torna os papéis do MCP
-- específicos por campanha.

alter table public.universos
    add column if not exists cidade varchar(150);
alter table public.universos
    add column if not exists estado char(2);

alter table public.segmentos
    add column if not exists classes_sociais text[] not null default '{}'::text[];
alter table public.segmentos
    add column if not exists faixas_etarias text[] not null default '{}'::text[];
alter table public.segmentos
    add column if not exists escolaridades text[] not null default '{}'::text[];

update public.segmentos
set classes_sociais = array[classe_social]
where cardinality(classes_sociais) = 0
  and nullif(trim(classe_social), '') is not null;

update public.segmentos
set faixas_etarias = array[faixa_etaria]
where cardinality(faixas_etarias) = 0
  and nullif(trim(faixa_etaria), '') is not null;

update public.segmentos
set escolaridades = array[escolaridade]
where cardinality(escolaridades) = 0
  and nullif(trim(escolaridade), '') is not null;

alter table public.inventarios_papeis
    add column if not exists campanha_ref varchar(250) not null default 'GLOBAL';

alter table public.inventarios_papeis
    drop constraint if exists inventarios_papeis_inventario_id_key;

create unique index if not exists uq_inventarios_papeis_campanha
    on public.inventarios_papeis(campanha_ref, inventario_id);

create index if not exists idx_inventarios_papeis_campanha
    on public.inventarios_papeis(campanha_ref);

notify pgrst, 'reload schema';
