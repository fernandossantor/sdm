create table if not exists public.formatos_ambientes (
    formato_id uuid not null references public.formatos_v3(id) on delete cascade,
    ambiente_id uuid not null references public.ambientes_v3(id) on delete cascade,
    criado_em timestamptz not null default now(),
    primary key (formato_id, ambiente_id)
);

create table if not exists public.modalidades_unidades_compra (
    modalidade_id uuid not null references public.modalidades_compra_v3(id) on delete cascade,
    unidade_id uuid not null references public.unidades_compra_v3(id) on delete cascade,
    criado_em timestamptz not null default now(),
    primary key (modalidade_id, unidade_id)
);

alter table public.formatos_ambientes enable row level security;
alter table public.modalidades_unidades_compra enable row level security;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select distinct formato_id, ambiente_id
from public.inventarios_v3
where formato_id is not null and ambiente_id is not null
on conflict do nothing;

-- Formatos audiovisuais e de áudio.
insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in (
    'cinema', 'ctv', 'iptv', 'ott', 'streaming vídeo', 'tv aberta',
    'tv fechada', 'vídeo'
)
and lower(f.nome) in (
    '5 segundos', '10 segundos', '15 segundos', '30 segundos', '45 segundos',
    '60 segundos', 'bumper', 'ctv avod', 'ctv fast', 'ctv svod', 'ctv tvod',
    'in-stream', 'live', 'skippable', 'testemunhal', 'vídeo 15', 'vídeo 30',
    'vídeo 60', 'vídeo vertical', 'patrocínio de sessão'
)
on conflict do nothing;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in (
    'am', 'áudio', 'fm', 'podcast', 'rádio web', 'streaming áudio'
)
and lower(f.nome) in (
    'spot 15', 'spot 30', 'spot 45', 'spot 60', 'testemunhal',
    'patrocínio de sessão', 'live'
)
on conflict do nothing;

-- Formatos digitais, sociais, de busca e retail media.
insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) = 'social'
and lower(f.nome) in (
    'carrossel', 'coleção', 'feed', 'live', 'reels', 'stories',
    'vídeo 15', 'vídeo 30', 'vídeo 60', 'vídeo vertical', 'native'
)
on conflict do nothing;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in ('display', 'sites', 'portais', 'blogs', 'mensageria')
and lower(f.nome) in (
    'banner', 'display', 'native', 'newsletter', 'push', 'responsivo',
    'rich media', 'vídeo 15', 'vídeo 30', 'vídeo 60', 'vídeo vertical'
)
on conflict do nothing;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) = 'search'
and lower(f.nome) in ('texto', 'responsivo', 'retail search')
on conflict do nothing;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in ('retail', 'retail media direto', 'gaming')
and lower(f.nome) in (
    'retail display', 'retail search', 'retail vídeo', 'banner', 'display',
    'native', 'vídeo 15', 'vídeo 30', 'vídeo 60'
)
on conflict do nothing;

-- Formatos impressos, OOH, PDV e ações especiais.
insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in ('jornal', 'revista')
and lower(f.nome) in (
    'dupla página', 'encarte', 'meia página', 'página inteira',
    'publieditorial', 'rodapé'
)
on conflict do nothing;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in (
    'aeroporto', 'ambient media', 'balão', 'blimp', 'busdoor', 'dooh',
    'envelopamento', 'faixa de rua', 'metrô', 'mub', 'outdoor', 'painéis',
    'shopping', 'taxidoor'
)
and lower(f.nome) in (
    'backlight', 'banner', 'display', 'faixa', 'frontlight', 'led',
    'vídeo 15', 'vídeo 30', 'vídeo 60'
)
on conflict do nothing;

insert into public.formatos_ambientes (formato_id, ambiente_id)
select f.id, a.id
from public.formatos_v3 f
cross join public.ambientes_v3 a
where lower(a.nome) in (
    'ações especiais', 'checkout', 'gôndola', 'guerrilha', 'quiosque',
    'sampling', 'stand'
)
and lower(f.nome) in (
    'degustação', 'display', 'ilha', 'sampling', 'wobbler', 'faixa',
    'banner', 'vídeo 15', 'vídeo 30'
)
on conflict do nothing;

insert into public.unidades_compra_v3 (nome, descricao, ativo)
select dados.nome, dados.descricao, true
from (values
    ('Mil impressões', 'Bloco de mil impressões publicitárias.'),
    ('Mil contatos', 'Bloco de mil oportunidades de contato com a mensagem.'),
    ('Ponto de audiência', 'Um ponto percentual de audiência no universo pesquisado.'),
    ('Pessoa alcançada', 'Pessoa única alcançada pela campanha.'),
    ('Exemplar', 'Exemplar de publicação impresso ou distribuído.'),
    ('Página', 'Espaço publicitário correspondente a uma página.'),
    ('Programa', 'Programa ou faixa de programação contratada.'),
    ('Ponto', 'Ponto físico de exibição ou instalação.')
) as dados(nome, descricao)
where not exists (
    select 1 from public.unidades_compra_v3 u
    where lower(u.nome) = lower(dados.nome)
);

insert into public.modalidades_compra_v3 (nome, descricao, ativo)
select dados.nome, dados.descricao, true
from (values
    ('CPP', 'Custo por ponto de audiência.'),
    ('Custo por mil contatos', 'Compra baseada em mil oportunidades de contato.'),
    ('Avulsa', 'Compra individual de inserção ou espaço.'),
    ('Patrocínio', 'Compra de propriedade ou cota de patrocínio.'),
    ('Cota', 'Compra de participação definida em projeto ou programação.')
) as dados(nome, descricao)
where not exists (
    select 1 from public.modalidades_compra_v3 m
    where lower(m.nome) = lower(dados.nome)
);

insert into public.modalidades_unidades_compra (modalidade_id, unidade_id)
select m.id, u.id
from public.modalidades_compra_v3 m
join public.unidades_compra_v3 u on (
    (upper(m.nome) = 'CPM' and lower(u.nome) = 'mil impressões') or
    (upper(m.nome) = 'CPC' and lower(u.nome) = 'clique') or
    (upper(m.nome) = 'CPA' and lower(u.nome) = 'ação') or
    (upper(m.nome) = 'CPV' and lower(u.nome) in ('view', 'visualização')) or
    (upper(m.nome) = 'CPP' and lower(u.nome) = 'ponto de audiência') or
    (lower(m.nome) = 'custo por mil contatos' and lower(u.nome) = 'mil contatos') or
    (lower(m.nome) = 'diária' and lower(u.nome) = 'dia') or
    (lower(m.nome) = 'semanal' and lower(u.nome) = 'semana') or
    (lower(m.nome) = 'quinzenal' and lower(u.nome) = 'semana') or
    (lower(m.nome) = 'mensal' and lower(u.nome) = 'mês') or
    (lower(m.nome) = 'circuito' and lower(u.nome) in ('face', 'ponto')) or
    (lower(m.nome) = 'avulsa' and lower(u.nome) in ('inserção', 'página', 'programa')) or
    (lower(m.nome) in ('patrocínio', 'cota') and lower(u.nome) in ('programa', 'sessão', 'mês')) or
    (lower(m.nome) = 'exclusividade' and lower(u.nome) in ('dia', 'semana', 'mês', 'sessão')) or
    (lower(m.nome) = 'projeto especial' and lower(u.nome) in ('ação', 'loja', 'sessão')) or
    (lower(m.nome) = 'pacote' and lower(u.nome) in ('inserção', 'dia', 'semana', 'mês')) or
    (lower(m.nome) in ('negociação', 'tabela') and lower(u.nome) in (
        'ação', 'clique', 'dia', 'exemplar', 'face', 'impressão', 'inserção',
        'lead', 'loja', 'mês', 'mil contatos', 'mil impressões', 'página',
        'pessoa alcançada', 'ponto', 'ponto de audiência', 'programa',
        'semana', 'sessão', 'view'
    ))
)
on conflict do nothing;

insert into public.modelos_comerciais_v3 (nome, descricao, ativo)
select dados.nome, dados.descricao, true
from (values
    ('Mídia avulsa', 'Espaço ou inserção comercial comprada individualmente.'),
    ('Patrocínio', 'Associação da marca a conteúdo, programa, evento ou propriedade.'),
    ('Cota', 'Participação comercial definida dentro de um projeto ou propriedade.'),
    ('Pacote comercial', 'Conjunto negociado de espaços, inserções ou entregas.'),
    ('Permuta', 'Contratação com contrapartida total ou parcial em bens ou serviços.'),
    ('Bonificação', 'Entrega adicional concedida como benefício comercial.')
) as dados(nome, descricao)
where not exists (
    select 1 from public.modelos_comerciais_v3 m
    where lower(m.nome) = lower(dados.nome)
);

insert into public.kpis_v3 (nome, descricao, ativo)
select dados.nome, dados.descricao, true
from (values
    ('Audiência', 'Pessoas ou domicílios expostos ao conteúdo ou veículo, em número absoluto ou percentual.'),
    ('OTS', 'Oportunidades de ver, ouvir ou ler a mensagem publicitária.'),
    ('GRP', 'Soma dos pontos de audiência ou produto entre cobertura percentual e frequência média.'),
    ('TRP', 'Pontos de audiência acumulados especificamente no público-alvo.'),
    ('Cobertura', 'Percentual do universo alcançado ao menos uma vez.'),
    ('Frequência média', 'Número médio de exposições entre as pessoas alcançadas.'),
    ('Impactos', 'Total de contatos ou exposições, incluindo repetições.'),
    ('Afinidade', 'Índice de concentração do público-alvo na audiência do veículo.'),
    ('Circulação', 'Quantidade de exemplares distribuídos de uma publicação.'),
    ('Tiragem', 'Quantidade total de exemplares impressos.'),
    ('Leitura', 'Quantidade ou percentual de leitores de uma publicação.'),
    ('Share de audiência', 'Participação do veículo na audiência total do meio no período.'),
    ('Tempo médio de exposição', 'Tempo médio de contato do público com o conteúdo ou anúncio.'),
    ('Recall de campanha', 'Percentual do público que se recorda da campanha.'),
    ('Brand lift', 'Variação atribuída à campanha em indicadores de marca.')
) as dados(nome, descricao)
where not exists (
    select 1 from public.kpis_v3 k
    where lower(k.nome) = lower(dados.nome)
);

notify pgrst, 'reload schema';
