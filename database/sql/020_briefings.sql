create extension if not exists pgcrypto;

create table if not exists briefings (

    id uuid primary key default gen_random_uuid(),

    campaign_id uuid not null references campaigns(id) on delete cascade,

    company text,

    market text,

    product text,

    category text,

    positioning text,

    differential text,

    objectives text,

    communication_problem text,

    target_audience text,

    competitors text,

    budget numeric,

    start_date date,

    end_date date,

    observations text,

    created_at timestamptz default now(),

    updated_at timestamptz default now(),

    unique(campaign_id)

);

create index idx_briefings_campaign
on briefings(campaign_id);