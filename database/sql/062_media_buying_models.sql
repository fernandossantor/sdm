create extension if not exists pgcrypto;

create table if not exists media_buying_models (

    id uuid primary key default gen_random_uuid(),

    name text not null,

    billing_metric text,

    description text,

    active boolean default true,

    created_at timestamptz default now(),

    updated_at timestamptz default now()

);

create unique index idx_buying_name
on media_buying_models(lower(name));