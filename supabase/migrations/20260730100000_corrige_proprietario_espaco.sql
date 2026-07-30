-- O proprietário do espaço deve ser membro efetivo mesmo quando a linha
-- correspondente em membros_espacos ainda não foi criada.

create or replace function public.eh_membro_espaco(p_espaco_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1
        from public.espacos_trabalho e
        where e.id = p_espaco_id
          and e.proprietario_id = auth.uid()
    ) or exists (
        select 1
        from public.membros_espacos m
        join public.perfis_usuarios p on p.id = m.usuario_id
        where m.espaco_id = p_espaco_id
          and m.usuario_id = auth.uid()
          and p.ativo
    );
$$;

create or replace function public.pode_editar_espaco(p_espaco_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
    select public.eh_admin() or exists (
        select 1
        from public.espacos_trabalho e
        where e.id = p_espaco_id
          and e.proprietario_id = auth.uid()
    ) or exists (
        select 1
        from public.membros_espacos m
        join public.perfis_usuarios p on p.id = m.usuario_id
        where m.espaco_id = p_espaco_id
          and m.usuario_id = auth.uid()
          and m.papel in ('PROPRIETARIO', 'EDITOR')
          and p.ativo
    );
$$;
