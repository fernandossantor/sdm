\set ON_ERROR_STOP on
begin;

insert into auth.users (
    id, aud, role, email, raw_user_meta_data, created_at, updated_at
) values
    ('10000000-0000-0000-0000-000000000001', 'authenticated', 'authenticated',
     'owner-a@example.test', '{"nome":"Owner A"}', now(), now()),
    ('10000000-0000-0000-0000-000000000002', 'authenticated', 'authenticated',
     'owner-b@example.test', '{"nome":"Owner B"}', now(), now()),
    ('10000000-0000-0000-0000-000000000003', 'authenticated', 'authenticated',
     'reader-a@example.test', '{"nome":"Reader A"}', now(), now());

insert into public.espacos_trabalho (
    id, nome, slug, proprietario_id
) values
    ('20000000-0000-0000-0000-000000000001', 'Espaço A', 'teste-espaco-a',
     '10000000-0000-0000-0000-000000000001'),
    ('20000000-0000-0000-0000-000000000002', 'Espaço B', 'teste-espaco-b',
     '10000000-0000-0000-0000-000000000002');

insert into public.membros_espacos (espaco_id, usuario_id, papel) values
    ('20000000-0000-0000-0000-000000000001',
     '10000000-0000-0000-0000-000000000001', 'PROPRIETARIO'),
    ('20000000-0000-0000-0000-000000000001',
     '10000000-0000-0000-0000-000000000003', 'LEITOR'),
    ('20000000-0000-0000-0000-000000000002',
     '10000000-0000-0000-0000-000000000002', 'PROPRIETARIO');

insert into public.projetos (id, nome, espaco_id) values
    ('30000000-0000-0000-0000-000000000001', 'Projeto A',
     '20000000-0000-0000-0000-000000000001'),
    ('30000000-0000-0000-0000-000000000002', 'Projeto B',
     '20000000-0000-0000-0000-000000000002');

set local role authenticated;
select set_config(
    'request.jwt.claim.sub',
    '10000000-0000-0000-0000-000000000001',
    true
);

do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.projetos;
    if quantidade <> 1 then
        raise exception 'Owner A leu % projetos; esperado 1', quantidade;
    end if;
end;
$$;

insert into public.projetos (nome, espaco_id)
values ('Projeto editável A', '20000000-0000-0000-0000-000000000001');

do $$
begin
    begin
        update public.projetos
        set espaco_id = '20000000-0000-0000-0000-000000000002'
        where id = '30000000-0000-0000-0000-000000000001';
        raise exception 'Projeto foi movido entre espaços';
    exception
        when raise_exception then
            if sqlerrm not like '%não pode ser alterado%' then
                raise;
            end if;
    end;
end;
$$;

do $$
begin
    begin
        insert into public.projetos (nome, espaco_id)
        values ('Invasão B', '20000000-0000-0000-0000-000000000002');
        raise exception 'Owner A conseguiu inserir no Espaço B';
    exception
        when insufficient_privilege then null;
    end;
end;
$$;

do $$
begin
    begin
        insert into public.briefings_v3 (
            nome, anunciante, orcamento, espaco_id, projeto_id
        ) values (
            'Vínculo cruzado', 'Teste', 100,
            '20000000-0000-0000-0000-000000000001',
            '30000000-0000-0000-0000-000000000002'
        );
        raise exception 'Vínculo entre espaços diferentes foi aceito';
    exception
        when raise_exception then
            if sqlerrm not like '%espaços diferentes%' then
                raise;
            end if;
    end;
end;
$$;

do $$
begin
    begin
        update public.perfis_usuarios
        set papel_global = 'ADMINISTRADOR'
        where id = '10000000-0000-0000-0000-000000000001';
        raise exception 'Usuário alterou o próprio papel global';
    exception
        when insufficient_privilege then null;
    end;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '10000000-0000-0000-0000-000000000003',
    true
);

do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade from public.projetos;
    if quantidade <> 2 then
        raise exception 'Leitor A leu % projetos; esperado 2', quantidade;
    end if;
    begin
        insert into public.projetos (nome, espaco_id)
        values ('Escrita do leitor', '20000000-0000-0000-0000-000000000001');
        raise exception 'Leitor conseguiu inserir projeto';
    exception
        when insufficient_privilege then null;
    end;
end;
$$;

rollback;
