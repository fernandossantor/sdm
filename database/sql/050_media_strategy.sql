create extension if not exists pgcrypto;

create table if not exists media_strategies (

    id uuid primary key default gen_random_uuid(),

    campaign_id uuid not null
        references campaigns(id)
        on delete cascade,

    strategy_type text,

    purchase_model text,

    campaign_type text,

    coverage_scope text,

    communication_phase text,

    priority text,

    budget_distribution text,

    channel_mix text,

    observations text,

    created_at timestamptz default now(),

    updated_at timestamptz default now(),

    unique(campaign_id)

);

create index idx_media_strategy_campaign
on media_strategies(campaign_id);