create extension if not exists pgcrypto;

create table if not exists campaigns (

    id uuid primary key default gen_random_uuid(),

    code text not null unique,

    name text not null,

    client text,

    brand text,

    product text,

    objective text,

    start_date date,

    end_date date,

    notes text,

    status text not null default 'draft',

    created_at timestamptz not null default now(),

    updated_at timestamptz not null default now()

);

create index if not exists idx_campaign_status
on campaigns(status);

create index if not exists idx_campaign_created
on campaigns(created_at desc);