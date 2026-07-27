\set ON_ERROR_STOP on
begin;

insert into auth.users (
    id, aud, role, email, raw_user_meta_data, created_at, updated_at
) values
    ('11000000-0000-0000-0000-000000000001', 'authenticated',
     'authenticated', 'admin-audit@example.test', '{}', now(), now()),
    ('11000000-0000-0000-0000-000000000002', 'authenticated',
     'authenticated', 'user-audit@example.test', '{}', now(), now());

update public.perfis_usuarios
set papel_global = 'ADMINISTRADOR'
where id = '11000000-0000-0000-0000-000000000001';

insert into public.logs_auditoria (
    ator_id, acao, alvo_tipo, alvo_id
) values (
    '11000000-0000-0000-0000-000000000001',
    'TESTE', 'USUARIO',
    '11000000-0000-0000-0000-000000000002'
);

set local role authenticated;
select set_config(
    'request.jwt.claim.sub',
    '11000000-0000-0000-0000-000000000002',
    true
);

do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.logs_auditoria;
    if quantidade <> 0 then
        raise exception 'Usuário comum leu logs administrativos';
    end if;
    begin
        insert into public.logs_auditoria (acao, alvo_tipo)
        values ('INVASAO', 'USUARIO');
        raise exception 'Usuário comum escreveu log administrativo';
    exception
        when insufficient_privilege then null;
    end;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '11000000-0000-0000-0000-000000000001',
    true
);

do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.logs_auditoria;
    if quantidade <> 1 then
        raise exception 'Administrador não leu o log de auditoria';
    end if;
    begin
        insert into public.logs_auditoria (acao, alvo_tipo)
        values ('DIRETO', 'USUARIO');
        raise exception 'Administrador escreveu log sem service_role';
    exception
        when insufficient_privilege then null;
    end;
end;
$$;

rollback;
