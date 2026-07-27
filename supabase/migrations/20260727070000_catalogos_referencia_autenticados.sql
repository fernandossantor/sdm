-- Catálogos necessários ao inventário: leitura autenticada e escrita admin.

do $$
declare
    v_tabela text;
begin
    foreach v_tabela in array array[
        'tecnologias_v3',
        'canais_v3',
        'ambientes_v3',
        'estruturas_v3',
        'formatos_v3',
        'formatos_ambientes',
        'perfis_editoriais',
        'modelos_comerciais_v3',
        'modalidades_compra_v3',
        'unidades_compra_v3',
        'modalidades_unidades_compra',
        'plataformas_v3',
        'kpis_v3',
        'objetivos_campanha_v3'
    ] loop
        execute format('alter table public.%I enable row level security', v_tabela);
        execute format('drop policy if exists catalogo_select on public.%I', v_tabela);
        execute format(
            'create policy catalogo_select on public.%I '
            'for select to authenticated using (true)',
            v_tabela
        );
        execute format('drop policy if exists catalogo_admin_write on public.%I', v_tabela);
        execute format(
            'create policy catalogo_admin_write on public.%I '
            'for all to authenticated '
            'using (public.eh_admin()) with check (public.eh_admin())',
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
