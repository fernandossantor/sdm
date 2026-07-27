\set ON_ERROR_STOP on
begin;

insert into auth.users (
    id, aud, role, email, raw_user_meta_data, created_at, updated_at
) values
    ('13000000-0000-0000-0000-000000000001', 'authenticated',
     'authenticated', 'admin-inventory@example.test', '{}', now(), now()),
    ('13000000-0000-0000-0000-000000000002', 'authenticated',
     'authenticated', 'owner-inventory@example.test', '{}', now(), now()),
    ('13000000-0000-0000-0000-000000000003', 'authenticated',
     'authenticated', 'other-inventory@example.test', '{}', now(), now());

update public.perfis_usuarios set papel_global = 'ADMINISTRADOR'
where id = '13000000-0000-0000-0000-000000000001';

insert into public.espacos_trabalho (
    id, nome, slug, proprietario_id
) values
    ('23000000-0000-0000-0000-000000000001', 'Inventory A',
     'inventory-a-test', '13000000-0000-0000-0000-000000000002'),
    ('23000000-0000-0000-0000-000000000002', 'Inventory B',
     'inventory-b-test', '13000000-0000-0000-0000-000000000003');
insert into public.membros_espacos (espaco_id, usuario_id, papel) values
    ('23000000-0000-0000-0000-000000000001',
     '13000000-0000-0000-0000-000000000002', 'PROPRIETARIO'),
    ('23000000-0000-0000-0000-000000000002',
     '13000000-0000-0000-0000-000000000003', 'PROPRIETARIO');

insert into public.inventarios_v3 (
    id, nome, codigo, ambiente_id, escopo, espaco_id
)
select
    '33000000-0000-0000-0000-000000000001', 'Inventário global',
    'INV-TEST-0001', id, 'GLOBAL', null
from public.ambientes_v3 limit 1;

insert into public.inventarios_v3 (
    id, nome, codigo, ambiente_id, escopo, espaco_id
)
select
    '33000000-0000-0000-0000-000000000002', 'Inventário privado A',
    'INV-TEST-0002', id, 'PRIVADO',
    '23000000-0000-0000-0000-000000000001'
from public.ambientes_v3 limit 1;

set local role authenticated;
select set_config(
    'request.jwt.claim.sub',
    '13000000-0000-0000-0000-000000000002',
    true
);
do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.inventarios_v3
    where id in (
        '33000000-0000-0000-0000-000000000001',
        '33000000-0000-0000-0000-000000000002'
    );
    if quantidade <> 2 then
        raise exception 'Proprietário leu % inventários; esperado 2', quantidade;
    end if;
    update public.inventarios_v3 set nome = 'Global indevido'
    where id = '33000000-0000-0000-0000-000000000001';
    if found then
        raise exception 'Usuário comum alterou inventário global';
    end if;
    update public.inventarios_v3 set nome = 'Privado atualizado'
    where id = '33000000-0000-0000-0000-000000000002';
    if not found then
        raise exception 'Proprietário não alterou inventário privado';
    end if;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '13000000-0000-0000-0000-000000000003',
    true
);
do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.inventarios_v3
    where id in (
        '33000000-0000-0000-0000-000000000001',
        '33000000-0000-0000-0000-000000000002'
    );
    if quantidade <> 1 then
        raise exception 'Outro espaço leu % inventários; esperado somente global', quantidade;
    end if;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '13000000-0000-0000-0000-000000000001',
    true
);
update public.inventarios_v3 set nome = 'Global administrado'
where id = '33000000-0000-0000-0000-000000000001';

do $$
declare
    arquivado timestamptz;
begin
    update public.inventarios_v3 set ativo = false
    where id = '33000000-0000-0000-0000-000000000001';
    select arquivado_em into arquivado from public.inventarios_v3
    where id = '33000000-0000-0000-0000-000000000001';
    if arquivado is null then
        raise exception 'Arquivamento não registrou data';
    end if;
end;
$$;

rollback;
