create extension if not exists pgcrypto;

create table if not exists audiences (

    id uuid primary key default gen_random_uuid(),

    campaign_id uuid not null references campaigns(id) on delete cascade,

    target_name text,

    gender text,

    age_min integer,

    age_max integer,

    social_class text,

    income text,

    education text,

    occupation text,

    city text,

    state text,

    region text,

    interests text,

    habits text,

    pain_points text,

    media_consumption text,

    devices text,

    observations text,

    created_at timestamptz default now(),

    updated_at timestamptz default now(),

    unique(campaign_id)

);

create index idx_audience_campaign
on audiences(campaign_id);