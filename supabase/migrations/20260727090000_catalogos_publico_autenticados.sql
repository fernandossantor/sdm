-- Libera os cadastros de universos, segmentos e públicos para o fluxo
-- autenticado do aplicativo. Essas tabelas são catálogos compartilhados;
-- nenhum dado de sessão ou credencial é armazenado nelas.

do $$
declare
    v_tabela text;
begin
    foreach v_tabela in array array[
        'universos',
        'segmentos',
        'interesses',
        'jornadas',
        'biblioteca_publicos',
        'biblioteca_publicos_segmentos',
        'biblioteca_publicos_interesses',
        'biblioteca_publicos_jornadas'
    ] loop
        execute format('alter table public.%I enable row level security', v_tabela);
        execute format('drop policy if exists catalogo_autenticado_select on public.%I', v_tabela);
        execute format(
            'create policy catalogo_autenticado_select on public.%I '
            'for select to authenticated using (true)',
            v_tabela
        );
        execute format('drop policy if exists catalogo_autenticado_write on public.%I', v_tabela);
        execute format(
            'create policy catalogo_autenticado_write on public.%I '
            'for all to authenticated using (true) with check (true)',
            v_tabela
        );
        execute format(
            'grant select, insert, update, delete on public.%I to authenticated',
            v_tabela
        );
    end loop;
end;
$$;

notify pgrst, 'reload schema';
