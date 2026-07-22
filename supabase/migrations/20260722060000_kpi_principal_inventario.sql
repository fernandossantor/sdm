alter table public.inventarios_v3
    add column if not exists kpi_principal_id uuid
    references public.kpis_v3(id) on delete set null;

create index if not exists idx_inventarios_kpi_principal
    on public.inventarios_v3(kpi_principal_id);

notify pgrst, 'reload schema';
