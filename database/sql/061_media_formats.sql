create extension if not exists pgcrypto;

create table if not exists media_formats (

    id uuid primary key default gen_random_uuid(),

    channel_id uuid
        references media_channels(id),

    name text not null,

    description text,

    active boolean default true,

    created_at timestamptz default now(),

    updated_at timestamptz default now()

);

create index idx_media_format_channel
on media_formats(channel_id);