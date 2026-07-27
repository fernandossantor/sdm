\set ON_ERROR_STOP on
begin;

insert into auth.users (
    id, aud, role, email, raw_user_meta_data, created_at, updated_at
) values
    ('12000000-0000-0000-0000-000000000001', 'authenticated',
     'authenticated', 'owner-share@example.test', '{"nome":"Owner"}',
     now(), now()),
    ('12000000-0000-0000-0000-000000000002', 'authenticated',
     'authenticated', 'guest-share@example.test', '{"nome":"Guest"}',
     now(), now()),
    ('12000000-0000-0000-0000-000000000003', 'authenticated',
     'authenticated', 'outsider-share@example.test', '{"nome":"Outsider"}',
     now(), now());

insert into public.espacos_trabalho (
    id, nome, slug, proprietario_id
) values
    ('22000000-0000-0000-0000-000000000001', 'Share A',
     'share-a-test', '12000000-0000-0000-0000-000000000001'),
    ('22000000-0000-0000-0000-000000000002', 'Share B',
     'share-b-test', '12000000-0000-0000-0000-000000000002');

insert into public.membros_espacos (espaco_id, usuario_id, papel) values
    ('22000000-0000-0000-0000-000000000001',
     '12000000-0000-0000-0000-000000000001', 'PROPRIETARIO'),
    ('22000000-0000-0000-0000-000000000002',
     '12000000-0000-0000-0000-000000000002', 'PROPRIETARIO');

insert into public.projetos (
    id, nome, espaco_id, proprietario_id
) values (
    '32000000-0000-0000-0000-000000000001', 'Projeto compartilhável',
    '22000000-0000-0000-0000-000000000001',
    '12000000-0000-0000-0000-000000000001'
);
insert into public.briefings_v3 (
    id, nome, anunciante, orcamento, espaco_id, projeto_id
) values (
    '42000000-0000-0000-0000-000000000001', 'Briefing compartilhável',
    'Teste', 100, '22000000-0000-0000-0000-000000000001',
    '32000000-0000-0000-0000-000000000001'
);

set local role authenticated;
select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000001',
    true
);
select public.compartilhar_projeto(
    '32000000-0000-0000-0000-000000000001',
    'guest-share@example.test',
    'LEITOR'
);

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000002',
    true
);
do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade
    from public.projetos
    where id = '32000000-0000-0000-0000-000000000001';
    if quantidade <> 1 then
        raise exception 'Leitor não acessou o projeto compartilhado';
    end if;
    select count(*) into quantidade
    from public.briefings_v3
    where id = '42000000-0000-0000-0000-000000000001';
    if quantidade <> 1 then
        raise exception 'Leitor não acessou o briefing compartilhado';
    end if;
    update public.projetos set nome = 'Alteração indevida'
    where id = '32000000-0000-0000-0000-000000000001';
    if found then
        raise exception 'Leitor alterou o projeto';
    end if;
    begin
        perform public.compartilhar_projeto(
            '32000000-0000-0000-0000-000000000001',
            'outsider-share@example.test',
            'LEITOR'
        );
        raise exception 'Leitor gerenciou participantes';
    exception
        when raise_exception then
            if sqlerrm not like '%Sem permissão%' then
                raise;
            end if;
    end;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000001',
    true
);
select public.compartilhar_projeto(
    '32000000-0000-0000-0000-000000000001',
    'guest-share@example.test',
    'EDITOR'
);

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000002',
    true
);
update public.projetos set nome = 'Alteração legítima do editor'
where id = '32000000-0000-0000-0000-000000000001';

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000001',
    true
);
select public.revogar_compartilhamento_projeto(
    '32000000-0000-0000-0000-000000000001',
    '12000000-0000-0000-0000-000000000002'
);

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000002',
    true
);
do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade
    from public.projetos
    where id = '32000000-0000-0000-0000-000000000001';
    if quantidade <> 0 then
        raise exception 'A revogação não removeu o acesso';
    end if;
end;
$$;

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000001',
    true
);
select public.compartilhar_projeto(
    '32000000-0000-0000-0000-000000000001',
    'guest-share@example.test',
    'PROPRIETARIO'
);

select set_config(
    'request.jwt.claim.sub',
    '12000000-0000-0000-0000-000000000002',
    true
);
select public.compartilhar_projeto(
    '32000000-0000-0000-0000-000000000001',
    'outsider-share@example.test',
    'LEITOR'
);

reset role;
do $$
declare
    quantidade integer;
begin
    select count(*) into quantidade
    from public.logs_auditoria
    where alvo_id = '32000000-0000-0000-0000-000000000001'
      and acao in (
          'PROJETO_COMPARTILHADO',
          'PROJETO_COMPARTILHAMENTO_REVOGADO',
          'PROJETO_TRANSFERIDO'
      );
    if quantidade <> 5 then
        raise exception 'Auditoria registrou % ações; esperado 5', quantidade;
    end if;
end;
$$;

rollback;
