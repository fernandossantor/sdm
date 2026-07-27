-- Condições comerciais auditáveis por preço e vigência.

alter table public.precos_inventario
    add column if not exists moeda char(3) not null default 'BRL',
    add column if not exists modelo_negociacao varchar(30) not null default 'DIRETO',
    add column if not exists fee_tecnologia_percentual numeric(7,4) not null default 0,
    add column if not exists fee_tecnologia_fixo numeric(14,4) not null default 0,
    add column if not exists fee_dados_percentual numeric(7,4) not null default 0,
    add column if not exists fee_dados_fixo numeric(14,4) not null default 0,
    add column if not exists fee_verificacao_percentual numeric(7,4) not null default 0,
    add column if not exists fee_verificacao_fixo numeric(14,4) not null default 0,
    add column if not exists fee_operacao_percentual numeric(7,4) not null default 0,
    add column if not exists fee_operacao_fixo numeric(14,4) not null default 0,
    add column if not exists quantidade_minima numeric(14,4) not null default 0,
    add column if not exists investimento_minimo numeric(14,4) not null default 0,
    add column if not exists disponibilidade numeric(14,4),
    add column if not exists capacidade numeric(14,4);

alter table public.precos_inventario
    drop constraint if exists precos_inventario_moeda_check,
    add constraint precos_inventario_moeda_check
        check (moeda = upper(moeda) and moeda ~ '^[A-Z]{3}$'),
    drop constraint if exists precos_inventario_modelo_negociacao_check,
    add constraint precos_inventario_modelo_negociacao_check
        check (modelo_negociacao in (
            'OPEN_AUCTION', 'PMP', 'PREFERRED_DEAL',
            'GARANTIDO', 'DIRETO'
        )),
    drop constraint if exists precos_inventario_fees_check,
    add constraint precos_inventario_fees_check check (
        fee_tecnologia_percentual >= 0
        and fee_tecnologia_fixo >= 0
        and fee_dados_percentual >= 0
        and fee_dados_fixo >= 0
        and fee_verificacao_percentual >= 0
        and fee_verificacao_fixo >= 0
        and fee_operacao_percentual >= 0
        and fee_operacao_fixo >= 0
    ),
    drop constraint if exists precos_inventario_limites_check,
    add constraint precos_inventario_limites_check check (
        quantidade_minima >= 0
        and investimento_minimo >= 0
        and (disponibilidade is null or disponibilidade >= 0)
        and (capacidade is null or capacidade >= 0)
        and (
            disponibilidade is null
            or capacidade is null
            or disponibilidade <= capacidade
        )
    );

comment on column public.precos_inventario.modelo_negociacao is
    'OPEN_AUCTION, PMP, PREFERRED_DEAL, GARANTIDO ou DIRETO.';
comment on column public.precos_inventario.disponibilidade is
    'Quantidade atualmente disponível na unidade comercial informada.';
comment on column public.precos_inventario.capacidade is
    'Capacidade máxima na unidade comercial informada.';

notify pgrst, 'reload schema';
