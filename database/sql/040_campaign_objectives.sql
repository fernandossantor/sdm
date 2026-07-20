create extension if not exists pgcrypto;

create table if not exists campaign_objectives (

    id uuid primary key default gen_random_uuid(),

    campaign_id uuid not null
        references campaigns(id)
        on delete cascade,

    business_objective text,

    communication_objective text,

    media_objective text,

    primary_kpi text,

    secondary_kpis text,

    conversion_goal text,

    desired_reach numeric,

    desired_frequency numeric,

    desired_impressions bigint,

    desired_clicks bigint,

    desired_ctr numeric,

    desired_cpm numeric,

    desired_cpc numeric,

    desired_cpa numeric,

    desired_roas numeric,

    observations text,

    created_at timestamptz default now(),

    updated_at timestamptz default now(),

    unique(campaign_id)

);

create index idx_campaign_objectives_campaign

on campaign_objectives(campaign_id);