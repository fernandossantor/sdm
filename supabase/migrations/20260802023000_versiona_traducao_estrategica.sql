-- Revisão humana versionada sem apagar a derivação automática original.

create function public.versionar_traducao_estrategica_mediad(
    p_traducao_anterior_id uuid, p_nova_traducao_id uuid, p_espaco_id uuid,
    p_resultado jsonb, p_usuario_id uuid, p_instante timestamptz
) returns uuid language plpgsql security definer set search_path=public as $$
declare v_anterior public.traducoes_estrategicas_mediad%rowtype;
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para revisar tradução';
    end if;
    select * into v_anterior from public.traducoes_estrategicas_mediad
    where id=p_traducao_anterior_id and espaco_id=p_espaco_id
    for update;
    if not found then raise exception 'Tradução anterior não encontrada'; end if;
    if (p_resultado->>'versao')::integer <> v_anterior.versao + 1 then
        raise exception 'Versão da tradução inválida';
    end if;
    if p_resultado->>'briefing_id' <> v_anterior.briefing_id::text then
        raise exception 'Briefing da tradução não pode ser alterado';
    end if;

    update public.traducoes_estrategicas_mediad
    set estado='SUPERADO' where id=v_anterior.id;
    insert into public.traducoes_estrategicas_mediad (
        id, campanha_id, briefing_id, espaco_id, versao, estado,
        resultado, criado_por, criado_em
    ) values (
        p_nova_traducao_id, v_anterior.campanha_id, v_anterior.briefing_id,
        p_espaco_id, (p_resultado->>'versao')::integer,
        p_resultado->>'estado', p_resultado, p_usuario_id, p_instante
    );
    return p_nova_traducao_id;
end; $$;
revoke all on function public.versionar_traducao_estrategica_mediad(
    uuid, uuid, uuid, jsonb, uuid, timestamptz
) from public;
grant execute on function public.versionar_traducao_estrategica_mediad(
    uuid, uuid, uuid, jsonb, uuid, timestamptz
) to authenticated;
