alter table public.briefings_v3
    add column if not exists grp numeric(10,2);

alter table public.briefings_v3
    alter column frequencia_alvo type numeric(10,2)
    using frequencia_alvo::numeric,
    alter column alcance_percentual type numeric(10,2)
    using alcance_percentual::numeric;

update public.briefings_v3
set grp = alcance_percentual * frequencia_alvo
where grp is null
  and alcance_percentual is not null
  and frequencia_alvo is not null;

-- Corrige os preços antigos de inventários comprados por CPM. A unidade
-- comercial é o milheiro, não uma impressão isolada.
update public.precos_inventario p
set unidade = 'Mil impressões'
from public.inventarios_v3 i
join public.modalidades_compra_v3 m
  on m.id = i.modalidade_compra_id
where p.inventario_id = i.id
  and upper(m.nome) = 'CPM'
  and lower(p.unidade) in ('impressão', 'impressao', 'cpm');

notify pgrst, 'reload schema';
