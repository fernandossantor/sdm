-- Versionamento imutável e snapshots auditáveis de planejamentos.

alter table public.planejamentos
    add column if not exists arquivado_em timestamptz,
    add column if not exists motivo_arquivamento text;

create table if not exists public.versoes_planejamento (
    id uuid primary key default gen_random_uuid(),
    planejamento_id uuid not null
        references public.planejamentos(id) on delete restrict,
    numero integer not null,
    evento varchar(20) not null,
    status varchar(40) not null,
    snapshot_entradas jsonb not null,
    snapshot_resultados jsonb not null,
    versoes_engines jsonb not null default '{}'::jsonb,
    versoes_formulas jsonb not null default '{}'::jsonb,
    hash_conteudo char(32) not null,
    criado_em timestamptz not null default now(),
    unique (planejamento_id, numero),
    check (numero > 0),
    check (evento in ('CRIACAO', 'RECALCULO', 'EDICAO', 'ARQUIVAMENTO')),
    check (jsonb_typeof(snapshot_entradas) = 'object'),
    check (jsonb_typeof(snapshot_resultados) = 'object'),
    check (jsonb_typeof(versoes_engines) = 'object'),
    check (jsonb_typeof(versoes_formulas) = 'object')
);

create index if not exists idx_versoes_planejamento_historico
    on public.versoes_planejamento (planejamento_id, numero desc);

create or replace function public.registrar_versao_planejamento()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
    v_numero integer;
    v_evento varchar(20);
    v_entradas jsonb;
    v_resultados jsonb;
    v_engines jsonb;
    v_formulas jsonb;
    v_conteudo text;
begin
    perform pg_advisory_xact_lock(hashtext(new.id::text));

    select coalesce(max(numero), 0) + 1
      into v_numero
      from public.versoes_planejamento
     where planejamento_id = new.id;

    if tg_op = 'INSERT' then
        v_evento := 'CRIACAO';
    elsif new.arquivado_em is not null
          and old.arquivado_em is distinct from new.arquivado_em then
        v_evento := 'ARQUIVAMENTO';
    elsif old.resultado is distinct from new.resultado
          or old.configuracao is distinct from new.configuracao
          or old.premissas is distinct from new.premissas
          or old.estrategia is distinct from new.estrategia then
        v_evento := 'RECALCULO';
    else
        v_evento := 'EDICAO';
    end if;

    v_entradas := jsonb_build_object(
        'nome', new.nome,
        'briefing_id', new.briefing_id,
        'configuracao', coalesce(new.configuracao, '{}'::jsonb),
        'premissas', coalesce(new.premissas, '{}'::jsonb),
        'estrategia', coalesce(new.estrategia, '{}'::jsonb)
    );
    v_resultados := jsonb_build_object(
        'resultado', coalesce(new.resultado, '{}'::jsonb),
        'auditoria_calculo', coalesce(new.auditoria_calculo, '{}'::jsonb),
        'status', new.status,
        'arquivado_em', new.arquivado_em,
        'motivo_arquivamento', new.motivo_arquivamento
    );
    v_engines := coalesce(
        new.auditoria_calculo -> 'versoes_engines',
        '{}'::jsonb
    );
    v_formulas := coalesce(
        new.auditoria_calculo -> 'versoes_formulas',
        '{}'::jsonb
    );
    v_conteudo := jsonb_build_object(
        'entradas', v_entradas,
        'resultados', v_resultados,
        'engines', v_engines,
        'formulas', v_formulas
    )::text;

    insert into public.versoes_planejamento (
        planejamento_id, numero, evento, status,
        snapshot_entradas, snapshot_resultados,
        versoes_engines, versoes_formulas, hash_conteudo
    ) values (
        new.id, v_numero, v_evento, new.status,
        v_entradas, v_resultados,
        v_engines, v_formulas, md5(v_conteudo)
    );

    return new;
end;
$$;

create or replace function public.bloquear_mutacao_versao_planejamento()
returns trigger
language plpgsql
as $$
begin
    raise exception 'Versões de planejamento são imutáveis';
end;
$$;

-- Registra o estado dos planejamentos existentes antes de ativar o trigger.
insert into public.versoes_planejamento (
    planejamento_id, numero, evento, status,
    snapshot_entradas, snapshot_resultados,
    versoes_engines, versoes_formulas, hash_conteudo, criado_em
)
select
    p.id,
    1,
    'CRIACAO',
    p.status,
    jsonb_build_object(
        'nome', p.nome,
        'briefing_id', p.briefing_id,
        'configuracao', coalesce(p.configuracao, '{}'::jsonb),
        'premissas', coalesce(p.premissas, '{}'::jsonb),
        'estrategia', coalesce(p.estrategia, '{}'::jsonb)
    ),
    jsonb_build_object(
        'resultado', coalesce(p.resultado, '{}'::jsonb),
        'auditoria_calculo', coalesce(p.auditoria_calculo, '{}'::jsonb),
        'status', p.status,
        'arquivado_em', p.arquivado_em,
        'motivo_arquivamento', p.motivo_arquivamento
    ),
    coalesce(p.auditoria_calculo -> 'versoes_engines', '{}'::jsonb),
    coalesce(p.auditoria_calculo -> 'versoes_formulas', '{}'::jsonb),
    md5(jsonb_build_object(
        'entradas', jsonb_build_object(
            'nome', p.nome,
            'briefing_id', p.briefing_id,
            'configuracao', coalesce(p.configuracao, '{}'::jsonb),
            'premissas', coalesce(p.premissas, '{}'::jsonb),
            'estrategia', coalesce(p.estrategia, '{}'::jsonb)
        ),
        'resultados', jsonb_build_object(
            'resultado', coalesce(p.resultado, '{}'::jsonb),
            'auditoria_calculo', coalesce(p.auditoria_calculo, '{}'::jsonb),
            'status', p.status,
            'arquivado_em', p.arquivado_em,
            'motivo_arquivamento', p.motivo_arquivamento
        ),
        'engines', coalesce(
            p.auditoria_calculo -> 'versoes_engines', '{}'::jsonb
        ),
        'formulas', coalesce(
            p.auditoria_calculo -> 'versoes_formulas', '{}'::jsonb
        )
    )::text),
    coalesce(p.criado_em, now())
from public.planejamentos p
where not exists (
    select 1
    from public.versoes_planejamento v
    where v.planejamento_id = p.id
);

drop trigger if exists trg_registrar_versao
    on public.planejamentos;
create trigger trg_registrar_versao
after insert or update on public.planejamentos
for each row execute function public.registrar_versao_planejamento();

drop trigger if exists trg_versao_planejamento_imutavel
    on public.versoes_planejamento;
create trigger trg_versao_planejamento_imutavel
before update or delete on public.versoes_planejamento
for each row execute function public.bloquear_mutacao_versao_planejamento();

alter table public.versoes_planejamento enable row level security;
revoke all on public.versoes_planejamento from anon, authenticated;
grant select, insert on public.versoes_planejamento to service_role;

notify pgrst, 'reload schema';
