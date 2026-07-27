\set ON_ERROR_STOP on
begin;

insert into auth.users (
    id, aud, role, email, raw_user_meta_data, created_at, updated_at
) values
    ('14000000-0000-0000-0000-000000000001', 'authenticated',
     'authenticated', 'admin-catalog@example.test', '{}', now(), now()),
    ('14000000-0000-0000-0000-000000000002', 'authenticated',
     'authenticated', 'user-catalog@example.test', '{}', now(), now());
update public.perfis_usuarios set papel_global = 'ADMINISTRADOR'
where id = '14000000-0000-0000-0000-000000000001';

set local role authenticated;
select set_config(
    'request.jwt.claim.sub',
    '14000000-0000-0000-0000-000000000002',
    true
);
do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.ambientes_v3;
    if quantidade = 0 then
        raise exception 'Usuário autenticado não leu ambientes';
    end if;
    begin
        insert into public.tecnologias_v3 (nome)
        values ('Tecnologia indevida');
        raise exception 'Usuário comum alterou catálogo';
    exception
        when insufficient_privilege then null;
    end;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '14000000-0000-0000-0000-000000000001',
    true
);
insert into public.tecnologias_v3 (nome)
values ('Tecnologia administrativa de teste');

rollback;
