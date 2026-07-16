-- ==========================================================
-- BIBLIOTECA DE PÚBLICOS
-- SDM 2.0
-- ==========================================================

create table if not exists biblioteca_publicos (

    id uuid primary key default gen_random_uuid(),

    nome varchar(150) not null,

    descricao text,

    ativo boolean default true,

    criado_em timestamptz default now()

);

-- ==========================================================

create table if not exists biblioteca_publicos_segmentos (

    id uuid primary key default gen_random_uuid(),

    publico_id uuid not null
        references biblioteca_publicos(id)
        on delete cascade,

    segmento_id uuid not null
        references segmentos(id)

);

-- ==========================================================

create table if not exists biblioteca_publicos_interesses (

    id uuid primary key default gen_random_uuid(),

    publico_id uuid not null
        references biblioteca_publicos(id)
        on delete cascade,

    interesse_id uuid not null
        references interesses(id)

);

-- ==========================================================

create table if not exists biblioteca_publicos_jornadas (

    id uuid primary key default gen_random_uuid(),

    publico_id uuid not null
        references biblioteca_publicos(id)
        on delete cascade,

    jornada_id uuid not null
        references jornadas(id)

);

-- ==========================================================

create index if not exists idx_bp_nome

on biblioteca_publicos(nome);

create index if not exists idx_bp_segmentos

on biblioteca_publicos_segmentos(segmento_id);

create index if not exists idx_bp_interesses

on biblioteca_publicos_interesses(interesse_id);

create index if not exists idx_bp_jornadas

on biblioteca_publicos_jornadas(jornada_id);