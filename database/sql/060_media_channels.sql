create extension if not exists pgcrypto;

create table if not exists media_channels (

    id uuid primary key default gen_random_uuid(),

    name text not null,

    description text,

    active boolean default true,

    created_at timestamptz default now(),

    updated_at timestamptz default now()

);

create unique index idx_media_channel_name
on media_channels(lower(name));