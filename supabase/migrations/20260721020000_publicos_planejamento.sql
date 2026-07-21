-- PMAH: estabiliza a cadeia Universo -> Segmento -> Público e prepara
-- planejamento, afinidades e preços. A migration é aditiva e idempotente.

create extension if not exists pgcrypto;

create table if not exists public.universos (
    id uuid primary key default gen_random_uuid(),
    nome varchar(150) not null,
    populacao bigint not null default 0 check (populacao >= 0),
    publico_alvo bigint not null default 0 check (publico_alvo >= 0),
    ativo boolean not null default true,
    criado_em timestamptz not null default now()
);

alter table public.universos add column if not exists ativo boolean default true;

do $$
begin
    if exists (
        select 1 from information_schema.columns
        where table_schema = 'public' and table_name = 'universos'
          and column_name = 'cenario_id'
    ) then
        alter table public.universos alter column cenario_id drop not null;
    end if;
end $$;

create table if not exists public.segmentos (
    id uuid primary key default gen_random_uuid(),
    universo_id uuid not null references public.universos(id) on delete restrict,
    nome varchar(150) not null,
    sexo varchar(30),
    faixa_etaria varchar(80),
    classe_social varchar(80),
    escolaridade varchar(120),
    populacao bigint not null default 0 check (populacao >= 0),
    ativo boolean not null default true,
    criado_em timestamptz not null default now()
);

alter table public.segmentos add column if not exists ativo boolean default true;
create index if not exists idx_segmentos_universo on public.segmentos(universo_id);

create table if not exists public.interesses (
    id uuid primary key default gen_random_uuid(),
    nome varchar(150) not null,
    ativo boolean not null default true
);

create table if not exists public.jornadas (
    id uuid primary key default gen_random_uuid(),
    etapa varchar(80) not null,
    codigo varchar(30),
    descricao varchar(150),
    ordem smallint,
    ativo boolean not null default true
);

alter table public.jornadas add column if not exists codigo varchar(30);
alter table public.jornadas add column if not exists descricao varchar(150);
alter table public.jornadas add column if not exists ordem smallint;
alter table public.jornadas add column if not exists ativo boolean default true;

do $$
begin
    if exists (
        select 1 from information_schema.columns
        where table_schema = 'public' and table_name = 'jornadas'
          and column_name = 'cenario_id'
    ) then
        alter table public.jornadas alter column cenario_id drop not null;
    end if;
end $$;

-- Instalações legadas usam o enum jornada_tipo em `etapa`. A taxonomia
-- canônica abaixo precisa aceitar as oito etapas em inglês e preservar os
-- valores antigos; varchar atende aos dois casos sem remover registros.
alter table public.jornadas
    alter column etapa type varchar(80) using etapa::text;

-- Etapas canônicas. Registros legados são preservados, mas deixam de aparecer.
update public.jornadas set ativo = false;

insert into public.jornadas (etapa, codigo, descricao, ordem, ativo)
select v.*
from (values
    ('Need', 'NEED', 'necessidade', 1::smallint, true),
    ('Awareness', 'AWARENESS', 'conhecimento', 2::smallint, true),
    ('Preference', 'PREFERENCE', 'preferência', 3::smallint, true),
    ('Search', 'SEARCH', 'procura', 4::smallint, true),
    ('Selection', 'SELECTION', 'seleção', 5::smallint, true),
    ('Purchase', 'PURCHASE', 'compra', 6::smallint, true),
    ('Use', 'USE', 'uso', 7::smallint, true),
    ('Satisfaction', 'SATISFACTION', 'satisfação', 8::smallint, true)
) as v(etapa, codigo, descricao, ordem, ativo)
where not exists (
    select 1 from public.jornadas j where j.etapa = v.etapa
);

update public.jornadas set codigo = 'NEED', descricao = 'necessidade', ordem = 1, ativo = true where etapa = 'Need';
update public.jornadas set codigo = 'AWARENESS', descricao = 'conhecimento', ordem = 2, ativo = true where etapa = 'Awareness';
update public.jornadas set codigo = 'PREFERENCE', descricao = 'preferência', ordem = 3, ativo = true where etapa = 'Preference';
update public.jornadas set codigo = 'SEARCH', descricao = 'procura', ordem = 4, ativo = true where etapa = 'Search';
update public.jornadas set codigo = 'SELECTION', descricao = 'seleção', ordem = 5, ativo = true where etapa = 'Selection';
update public.jornadas set codigo = 'PURCHASE', descricao = 'compra', ordem = 6, ativo = true where etapa = 'Purchase';
update public.jornadas set codigo = 'USE', descricao = 'uso', ordem = 7, ativo = true where etapa = 'Use';
update public.jornadas set codigo = 'SATISFACTION', descricao = 'satisfação', ordem = 8, ativo = true where etapa = 'Satisfaction';

create table if not exists public.biblioteca_publicos (
    id uuid primary key default gen_random_uuid(),
    nome varchar(150) not null,
    descricao text,
    ativo boolean not null default true,
    criado_em timestamptz not null default now()
);

create table if not exists public.biblioteca_publicos_segmentos (
    id uuid primary key default gen_random_uuid(),
    publico_id uuid not null references public.biblioteca_publicos(id) on delete cascade,
    segmento_id uuid not null references public.segmentos(id) on delete restrict,
    unique (publico_id, segmento_id)
);

create table if not exists public.biblioteca_publicos_interesses (
    id uuid primary key default gen_random_uuid(),
    publico_id uuid not null references public.biblioteca_publicos(id) on delete cascade,
    interesse_id uuid not null references public.interesses(id) on delete restrict,
    peso numeric(5,2) not null default 100 check (peso between 0 and 100),
    unique (publico_id, interesse_id)
);

alter table public.biblioteca_publicos_interesses
    add column if not exists peso numeric(5,2) default 100;

create table if not exists public.biblioteca_publicos_jornadas (
    id uuid primary key default gen_random_uuid(),
    publico_id uuid not null references public.biblioteca_publicos(id) on delete cascade,
    jornada_id uuid not null references public.jornadas(id) on delete restrict,
    unique (publico_id)
);

create index if not exists idx_bp_segmentos_publico on public.biblioteca_publicos_segmentos(publico_id);
create index if not exists idx_bp_interesses_publico on public.biblioteca_publicos_interesses(publico_id);
create index if not exists idx_bp_jornadas_publico on public.biblioteca_publicos_jornadas(publico_id);

-- Afinidade declarativa dos interesses por ambiente. Alimenta o motor de papéis.
create table if not exists public.interesses_ambientes_afinidade (
    id uuid primary key default gen_random_uuid(),
    interesse_id uuid not null references public.interesses(id) on delete cascade,
    ambiente_id uuid not null references public.ambientes_v3(id) on delete cascade,
    afinidade numeric(5,2) not null default 50 check (afinidade between 0 and 100),
    unique (interesse_id, ambiente_id)
);

-- Matriz inicial baseada em padrões de consumo e estilo de vida. Os valores
-- podem ser refinados pela interface sem alterar o motor.
insert into public.interesses_ambientes_afinidade (
    interesse_id, ambiente_id, afinidade
)
select
    i.id,
    a.id,
    case
        when lower(i.nome) similar to '%(games|streaming|cinema|música)%'
             and lower(a.nome) similar to '%(vídeo|video|áudio|audio|stream|social)%' then 90
        when lower(i.nome) similar to '%(finanças|investimentos|educação|negócios|economia)%'
             and lower(a.nome) similar to '%(search|busca|notícia|noticia|display|digital)%' then 85
        when lower(i.nome) similar to '%(moda|beleza|fitness|gastronomia|viagens|pets|casa)%'
             and lower(a.nome) similar to '%(social|vídeo|video|influ|conteúdo|conteudo)%' then 85
        when lower(i.nome) similar to '%(automóveis|motociclismo|eventos|turismo)%'
             and lower(a.nome) similar to '%(ooh|exterior|vídeo|video|search|busca)%' then 80
        when lower(i.nome) similar to '%(compras online|tecnologia|marketing|publicidade)%'
             and lower(a.nome) similar to '%(digital|social|search|busca|display)%' then 90
        else 50
    end
from public.interesses i
cross join public.ambientes_v3 a
on conflict (interesse_id, ambiente_id) do nothing;

-- Tabela comercial temporal; não mistura preço com o cadastro do inventário.
create table if not exists public.precos_inventario (
    id uuid primary key default gen_random_uuid(),
    inventario_id uuid not null references public.inventarios_v3(id) on delete cascade,
    unidade varchar(30) not null,
    valor_bruto numeric(14,4) not null check (valor_bruto >= 0),
    desconto_percentual numeric(5,2) not null default 0 check (desconto_percentual between 0 and 100),
    inicio_vigencia date,
    fim_vigencia date,
    praca varchar(120),
    fonte varchar(150),
    observacoes text,
    ativo boolean not null default true,
    criado_em timestamptz not null default now(),
    check (fim_vigencia is null or inicio_vigencia is null or fim_vigencia >= inicio_vigencia)
);

create index if not exists idx_precos_inventario on public.precos_inventario(inventario_id, ativo);

-- Snapshot editável do planejamento. O JSON preserva a configuração usada no cálculo.
create table if not exists public.planejamentos (
    id uuid primary key default gen_random_uuid(),
    nome varchar(180) not null,
    briefing_id uuid references public.briefings_v3(id) on delete set null,
    configuracao jsonb not null default '{}'::jsonb,
    resultado jsonb not null default '{}'::jsonb,
    status varchar(30) not null default 'RASCUNHO',
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now()
);

alter table public.universos enable row level security;
alter table public.segmentos enable row level security;
alter table public.interesses enable row level security;
alter table public.jornadas enable row level security;
alter table public.biblioteca_publicos enable row level security;
alter table public.biblioteca_publicos_segmentos enable row level security;
alter table public.biblioteca_publicos_interesses enable row level security;
alter table public.biblioteca_publicos_jornadas enable row level security;
alter table public.interesses_ambientes_afinidade enable row level security;
alter table public.precos_inventario enable row level security;
alter table public.planejamentos enable row level security;

revoke all on table public.universos, public.segmentos, public.interesses,
    public.jornadas, public.biblioteca_publicos,
    public.biblioteca_publicos_segmentos, public.biblioteca_publicos_interesses,
    public.biblioteca_publicos_jornadas, public.interesses_ambientes_afinidade,
    public.precos_inventario, public.planejamentos from anon, authenticated;

grant all on table public.universos, public.segmentos, public.interesses,
    public.jornadas, public.biblioteca_publicos,
    public.biblioteca_publicos_segmentos, public.biblioteca_publicos_interesses,
    public.biblioteca_publicos_jornadas, public.interesses_ambientes_afinidade,
    public.precos_inventario, public.planejamentos to service_role;
