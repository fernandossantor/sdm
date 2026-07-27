-- Fundação metodológica: catálogo, unidades, conversões e proveniência.
-- Migration aditiva; não altera nem recalcula registros legados.

create table if not exists public.unidades_metricas (
    id uuid primary key default gen_random_uuid(),
    codigo varchar(60) not null unique,
    nome varchar(120) not null,
    dimensao varchar(60) not null,
    simbolo varchar(20),
    casas_decimais smallint not null default 2,
    permite_fracao boolean not null default true,
    regra_arredondamento varchar(20) not null default 'MEIO_PARA_CIMA',
    ativo boolean not null default true,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now(),
    check (casas_decimais between 0 and 8),
    check (regra_arredondamento in (
        'MEIO_PARA_CIMA', 'PARA_CIMA', 'PARA_BAIXO', 'NAO_APLICAVEL'
    ))
);

create table if not exists public.metricas_catalogo (
    id uuid primary key default gen_random_uuid(),
    codigo varchar(80) not null unique,
    nome varchar(160) not null,
    descricao text,
    categoria varchar(60) not null,
    unidade_nativa_id uuid not null
        references public.unidades_metricas(id) on delete restrict,
    exige_denominador boolean not null default false,
    permite_agregacao boolean not null default false,
    regra_agregacao varchar(30) not null default 'NAO_AGREGAVEL',
    ativo boolean not null default true,
    criado_em timestamptz not null default now(),
    atualizado_em timestamptz not null default now(),
    check (regra_agregacao in (
        'SOMA', 'MEDIA_PONDERADA', 'MAXIMO', 'MINIMO', 'NAO_AGREGAVEL'
    ))
);

create table if not exists public.formulas_metricas (
    id uuid primary key default gen_random_uuid(),
    codigo varchar(100) not null,
    versao varchar(40) not null,
    nome varchar(160) not null,
    expressao text not null,
    descricao text,
    entradas jsonb not null default '[]'::jsonb,
    saida_metrica_id uuid references public.metricas_catalogo(id)
        on delete restrict,
    ativo boolean not null default true,
    vigente_desde timestamptz not null default now(),
    vigente_ate timestamptz,
    criado_em timestamptz not null default now(),
    unique (codigo, versao),
    check (jsonb_typeof(entradas) = 'array'),
    check (vigente_ate is null or vigente_ate >= vigente_desde)
);

create table if not exists public.conversoes_metricas (
    id uuid primary key default gen_random_uuid(),
    metrica_origem_id uuid not null
        references public.metricas_catalogo(id) on delete cascade,
    unidade_origem_id uuid not null
        references public.unidades_metricas(id) on delete restrict,
    metrica_destino_id uuid not null
        references public.metricas_catalogo(id) on delete cascade,
    unidade_destino_id uuid not null
        references public.unidades_metricas(id) on delete restrict,
    formula_id uuid not null
        references public.formulas_metricas(id) on delete restrict,
    confianca varchar(20) not null default 'NAO_AVALIADA',
    requer_aprovacao boolean not null default true,
    ativo boolean not null default true,
    criado_em timestamptz not null default now(),
    unique (
        metrica_origem_id, unidade_origem_id,
        metrica_destino_id, unidade_destino_id, formula_id
    ),
    check (confianca in ('ALTA', 'MEDIA', 'BAIXA', 'NAO_AVALIADA')),
    check (
        metrica_origem_id <> metrica_destino_id
        or unidade_origem_id <> unidade_destino_id
    )
);

create table if not exists public.valores_metricas (
    id uuid primary key default gen_random_uuid(),
    metrica_id uuid not null
        references public.metricas_catalogo(id) on delete restrict,
    unidade_id uuid not null
        references public.unidades_metricas(id) on delete restrict,
    valor numeric(24,8) not null,
    natureza varchar(20) not null,
    origem varchar(20) not null,
    confianca varchar(20) not null default 'NAO_AVALIADA',
    fonte text,
    metodologia text,
    inicio_referencia date,
    fim_referencia date,
    universo_id uuid references public.universos(id) on delete set null,
    publico_id uuid references public.biblioteca_publicos(id) on delete set null,
    praca varchar(160),
    granularidade varchar(40),
    formula_id uuid references public.formulas_metricas(id) on delete restrict,
    versao_metodo varchar(80),
    entradas jsonb not null default '[]'::jsonb,
    entidade_tipo varchar(80),
    entidade_id uuid,
    criado_em timestamptz not null default now(),
    check (natureza in ('FATO', 'PREMISSA', 'DECISAO', 'RESULTADO')),
    check (origem in (
        'MEDIDO', 'CONTRATADO', 'INFORMADO', 'CALCULADO', 'ESTIMADO'
    )),
    check (confianca in ('ALTA', 'MEDIA', 'BAIXA', 'NAO_AVALIADA')),
    check (fim_referencia is null or inicio_referencia is null
        or fim_referencia >= inicio_referencia),
    check (origem <> 'MEDIDO' or fonte is not null),
    check (
        natureza <> 'RESULTADO'
        or (
            formula_id is not null
            and versao_metodo is not null
            and jsonb_array_length(entradas) > 0
        )
    ),
    check (jsonb_typeof(entradas) = 'array'),
    check (
        (entidade_tipo is null and entidade_id is null)
        or (entidade_tipo is not null and entidade_id is not null)
    )
);

create index if not exists idx_valores_metricas_contexto
    on public.valores_metricas (
        metrica_id, universo_id, publico_id, praca,
        inicio_referencia, fim_referencia
    );
create index if not exists idx_valores_metricas_entidade
    on public.valores_metricas (entidade_tipo, entidade_id);

insert into public.unidades_metricas
    (codigo, nome, dimensao, simbolo, casas_decimais, permite_fracao)
values
    ('PERCENTUAL', 'Percentual', 'PROPORCAO', '%', 4, true),
    ('PESSOA', 'Pessoa', 'AUDIENCIA', null, 0, false),
    ('IMPRESSAO', 'Impressão', 'ENTREGA', null, 0, false),
    ('IMPACTO', 'Impacto', 'ENTREGA', null, 0, false),
    ('CONTATO_ESTIMADO', 'Contato estimado', 'ENTREGA_ESTIMADA', null, 0, false),
    ('PONTO_GRP', 'Ponto de GRP', 'PRESSAO', 'GRP', 3, true),
    ('FREQUENCIA_MEDIA', 'Frequência média', 'FREQUENCIA', null, 3, true),
    ('REAL_BRL', 'Real brasileiro', 'MOEDA', 'R$', 2, true)
on conflict (codigo) do nothing;

insert into public.metricas_catalogo
    (codigo, nome, categoria, unidade_nativa_id,
     exige_denominador, permite_agregacao, regra_agregacao)
select dados.codigo, dados.nome, dados.categoria, unidades.id,
       dados.exige_denominador, dados.permite_agregacao, dados.regra_agregacao
from (
    values
        ('ALCANCE_PERCENTUAL', 'Alcance percentual', 'AUDIENCIA',
         'PERCENTUAL', true, false, 'NAO_AGREGAVEL'),
        ('AUDIENCIA_PERCENTUAL', 'Audiência percentual', 'AUDIENCIA',
         'PERCENTUAL', true, false, 'NAO_AGREGAVEL'),
        ('IMPRESSOES', 'Impressões', 'ENTREGA',
         'IMPRESSAO', false, true, 'SOMA'),
        ('IMPACTOS', 'Impactos', 'ENTREGA',
         'IMPACTO', false, true, 'SOMA'),
        ('CONTATOS_ESTIMADOS', 'Contatos estimados', 'ENTREGA_ESTIMADA',
         'CONTATO_ESTIMADO', true, true, 'SOMA'),
        ('GRP', 'Gross Rating Points', 'PRESSAO',
         'PONTO_GRP', true, true, 'SOMA'),
        ('FREQUENCIA_MEDIA', 'Frequência média', 'FREQUENCIA',
         'FREQUENCIA_MEDIA', true, false, 'MEDIA_PONDERADA'),
        ('INVESTIMENTO', 'Investimento', 'CUSTO',
         'REAL_BRL', false, true, 'SOMA')
) as dados (
    codigo, nome, categoria, unidade_codigo,
    exige_denominador, permite_agregacao, regra_agregacao
)
join public.unidades_metricas unidades
    on unidades.codigo = dados.unidade_codigo
on conflict (codigo) do nothing;

do $$
declare tabela text;
begin
    foreach tabela in array array[
        'unidades_metricas', 'metricas_catalogo', 'formulas_metricas',
        'conversoes_metricas', 'valores_metricas'
    ] loop
        execute format('alter table public.%I enable row level security', tabela);
        execute format(
            'revoke all on table public.%I from anon, authenticated', tabela
        );
        execute format('grant all on table public.%I to service_role', tabela);
    end loop;
end $$;

notify pgrst, 'reload schema';
