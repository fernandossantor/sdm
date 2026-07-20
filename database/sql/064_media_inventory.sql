create extension if not exists pgcrypto;

create table if not exists media_inventory (

    id uuid primary key default gen_random_uuid(),

    vehicle_id uuid
        references media_vehicles(id),

    channel_id uuid
        references media_channels(id),

    format_id uuid
        references media_formats(id),

    buying_model_id uuid
        references media_buying_models(id),

    inventory_name text,

    placement text,

    description text,

    supports_video boolean default false,

    supports_image boolean default true,

    supports_audio boolean default false,

    active boolean default true,

    created_at timestamptz default now(),

    updated_at timestamptz default now()

);