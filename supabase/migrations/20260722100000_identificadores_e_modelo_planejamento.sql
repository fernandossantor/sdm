-- Identificadores legíveis, linhagem de cópias e premissas auditáveis do plano.

create table if not exists public.contadores_identificadores (
    tipo char(1) not null,
    competencia char(6) not null,
    ultimo_numero integer not null default 0,
    primary key (tipo, competencia),
    check (ultimo_numero between 0 and 9999)
);

create table if not exists public.identificadores_registros (
    codigo varchar(13) primary key,
    tipo char(1) not null,
    familia varchar(11) not null,
    versao integer not null,
    tabela text not null,
    registro_id uuid not null,
    criado_em timestamptz not null default now(),
    unique (tabela, registro_id),
    unique (familia, versao),
    check (versao between 1 and 99)
);

create or replace function public.gerar_codigo_original(p_tipo char, p_tabela text, p_id uuid)
returns varchar
language plpgsql
security definer
set search_path = public
as $$
declare
    v_competencia char(6) := to_char(current_date, 'YYYYMM');
    v_numero integer;
    v_familia varchar(11);
    v_codigo varchar(13);
begin
    insert into public.contadores_identificadores(tipo, competencia, ultimo_numero)
    values (upper(p_tipo), v_competencia, 1)
    on conflict (tipo, competencia) do update
        set ultimo_numero = public.contadores_identificadores.ultimo_numero + 1
    returning ultimo_numero into v_numero;

    if v_numero > 9999 then
        raise exception 'Limite mensal de identificadores atingido para o tipo %', p_tipo;
    end if;
    v_familia := upper(p_tipo) || v_competencia || lpad(v_numero::text, 4, '0');
    v_codigo := v_familia || '01';
    insert into public.identificadores_registros
        (codigo, tipo, familia, versao, tabela, registro_id)
    values (v_codigo, upper(p_tipo), v_familia, 1, p_tabela, p_id);
    return v_codigo;
end;
$$;

create or replace function public.proximo_codigo_copia(
    p_codigo_origem varchar,
    p_tabela text,
    p_id uuid
)
returns varchar
language plpgsql
security definer
set search_path = public
as $$
declare
    v_familia varchar(11) := left(p_codigo_origem, 11);
    v_tipo char(1) := left(p_codigo_origem, 1);
    v_versao integer;
    v_codigo varchar(13);
begin
    perform pg_advisory_xact_lock(hashtext(v_familia));
    select coalesce(max(versao), 0) + 1 into v_versao
    from public.identificadores_registros where familia = v_familia;
    if v_versao > 99 then
        raise exception 'A família % atingiu o limite de 99 versões', v_familia;
    end if;
    v_codigo := v_familia || lpad(v_versao::text, 2, '0');
    insert into public.identificadores_registros
        (codigo, tipo, familia, versao, tabela, registro_id)
    values (v_codigo, v_tipo, v_familia, v_versao, p_tabela, p_id);
    return v_codigo;
end;
$$;

alter table public.projetos add column if not exists codigo varchar(13) unique;
alter table public.briefings_v3 add column if not exists codigo varchar(13) unique;
alter table public.planejamentos add column if not exists codigo varchar(13) unique;
alter table public.inventarios_v3 add column if not exists codigo varchar(13) unique;
alter table public.universos add column if not exists codigo varchar(13) unique;
alter table public.segmentos add column if not exists codigo varchar(13) unique;
alter table public.biblioteca_publicos add column if not exists codigo varchar(13) unique;
alter table public.projetos add column if not exists criado_em timestamptz not null default now();
alter table public.briefings_v3 add column if not exists criado_em timestamptz not null default now();
alter table public.planejamentos add column if not exists criado_em timestamptz not null default now();
alter table public.inventarios_v3 add column if not exists criado_em timestamptz not null default now();
alter table public.universos add column if not exists criado_em timestamptz not null default now();
alter table public.segmentos add column if not exists criado_em timestamptz not null default now();
alter table public.biblioteca_publicos add column if not exists criado_em timestamptz not null default now();

alter table public.planejamentos
    add column if not exists premissas jsonb not null default '{}'::jsonb,
    add column if not exists estrategia jsonb not null default '{}'::jsonb,
    add column if not exists auditoria_calculo jsonb not null default '{}'::jsonb;
alter table public.inventarios_papeis
    add column if not exists jornada numeric(5,2),
    add column if not exists pesos jsonb not null default '{}'::jsonb;

create table if not exists public.medicoes_inventario (
    id uuid primary key default gen_random_uuid(),
    inventario_id uuid not null references public.inventarios_v3(id) on delete cascade,
    tipo_original varchar(80) not null,
    valor_original numeric(16,4) not null,
    unidade_original varchar(80) not null,
    audiencia_percentual numeric(7,3), alcance_percentual numeric(7,3),
    frequencia numeric(10,3), contatos bigint,
    universo_id uuid references public.universos(id) on delete set null,
    publico_id uuid references public.biblioteca_publicos(id) on delete set null,
    jornada_id uuid references public.jornadas(id) on delete set null,
    praca varchar(150), fonte varchar(200) not null, metodologia text,
    inicio_referencia date, fim_referencia date,
    confianca varchar(20) not null default 'MEDIDO',
    ativo boolean not null default true, criado_em timestamptz not null default now(),
    check (audiencia_percentual is null or audiencia_percentual between 0 and 100),
    check (alcance_percentual is null or alcance_percentual between 0 and 100),
    check (frequencia is null or frequencia > 0),
    check (fim_referencia is null or inicio_referencia is null or fim_referencia >= inicio_referencia)
);
create index if not exists idx_medicoes_inventario
    on public.medicoes_inventario(inventario_id, ativo, fim_referencia desc);
alter table public.medicoes_inventario enable row level security;
revoke all on public.medicoes_inventario from anon, authenticated;
grant all on public.medicoes_inventario to service_role;

-- Preenche o legado de forma determinística por tabela. A função também
-- registra a família, permitindo que futuras cópias continuem a numeração.
do $$
declare r record;
begin
    for r in select id from public.projetos where codigo is null order by criado_em, id loop
        update public.projetos set codigo = public.gerar_codigo_original('P','projetos',r.id) where id=r.id;
    end loop;
    for r in select id from public.briefings_v3 where codigo is null order by criado_em, id loop
        update public.briefings_v3 set codigo = public.gerar_codigo_original('B','briefings_v3',r.id) where id=r.id;
    end loop;
    for r in select id from public.planejamentos where codigo is null order by criado_em, id loop
        update public.planejamentos set codigo = public.gerar_codigo_original('L','planejamentos',r.id) where id=r.id;
    end loop;
    for r in select id from public.inventarios_v3 where codigo is null order by criado_em, id loop
        update public.inventarios_v3 set codigo = public.gerar_codigo_original('I','inventarios_v3',r.id) where id=r.id;
    end loop;
    for r in select id from public.universos where codigo is null order by criado_em, id loop
        update public.universos set codigo = public.gerar_codigo_original('U','universos',r.id) where id=r.id;
    end loop;
    for r in select id from public.segmentos where codigo is null order by criado_em, id loop
        update public.segmentos set codigo = public.gerar_codigo_original('S','segmentos',r.id) where id=r.id;
    end loop;
    for r in select id from public.biblioteca_publicos where codigo is null order by criado_em, id loop
        update public.biblioteca_publicos set codigo = public.gerar_codigo_original('A','biblioteca_publicos',r.id) where id=r.id;
    end loop;
end $$;

create or replace function public.atribuir_codigo_registro()
returns trigger language plpgsql security definer set search_path=public as $$
begin
    if new.codigo is null then
        new.codigo := public.gerar_codigo_original(TG_ARGV[0], TG_TABLE_NAME, new.id);
    end if;
    return new;
end $$;

do $$
declare item text[];
begin
    foreach item slice 1 in array array[
        ['projetos','P'], ['briefings_v3','B'], ['planejamentos','L'],
        ['inventarios_v3','I'], ['universos','U'], ['segmentos','S'],
        ['biblioteca_publicos','A']
    ] loop
        execute format('drop trigger if exists trg_codigo on public.%I', item[1]);
        execute format(
            'create trigger trg_codigo before insert on public.%I for each row execute function public.atribuir_codigo_registro(%L)',
            item[1], item[2]
        );
    end loop;
end $$;

revoke all on public.contadores_identificadores from anon, authenticated;
revoke all on public.identificadores_registros from anon, authenticated;
alter table public.contadores_identificadores enable row level security;
alter table public.identificadores_registros enable row level security;
grant all on public.contadores_identificadores to service_role;
grant all on public.identificadores_registros to service_role;
notify pgrst, 'reload schema';
