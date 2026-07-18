create extension if not exists pgcrypto;

create table if not exists media_vehicles (

    id uuid primary key default gen_random_uuid(),

    name text not null,

    company text,

    website text,

    country text,

    description text,

    active boolean default true,

    created_at timestamptz default now(),

    updated_at timestamptz default now()

);

create unique index idx_vehicle_name
on media_vehicles(lower(name));