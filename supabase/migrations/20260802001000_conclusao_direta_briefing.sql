-- Simplifica o piloto: conclusão direta, mantendo revisão formal para etapa futura.

create or replace function public.transicionar_briefing_mediad(
    p_briefing_id uuid, p_espaco_id uuid, p_estado_destino text,
    p_motivo text, p_alertas_reconhecidos jsonb,
    p_usuario_id uuid, p_instante timestamptz
) returns uuid language plpgsql security definer set search_path = public as $$
declare v_antes public.briefings_mediad%rowtype;
begin
    if auth.uid() is null or auth.uid() <> p_usuario_id then
        raise exception 'Autoria não corresponde ao usuário autenticado';
    end if;
    if not public.pode_editar_espaco(p_espaco_id) then
        raise exception 'Usuário sem permissão para transicionar briefing';
    end if;
    if btrim(coalesce(p_motivo, '')) = '' then
        raise exception 'Motivo da transição é obrigatório';
    end if;
    select * into v_antes from public.briefings_mediad
    where id=p_briefing_id and espaco_id=p_espaco_id for update;
    if not found then raise exception 'Briefing não encontrado'; end if;
    if not (
        (v_antes.estado='EM_PREENCHIMENTO' and p_estado_destino='CONCLUIDO')
        or (v_antes.estado='EM_REVISAO' and p_estado_destino='CONCLUIDO')
    ) then raise exception 'Transição de estado inválida'; end if;

    update public.briefings_mediad set
        estado=p_estado_destino,
        alertas_reconhecidos=coalesce(p_alertas_reconhecidos, '[]'::jsonb),
        atualizado_por=p_usuario_id, atualizado_em=p_instante,
        motivo_ultima_alteracao=btrim(p_motivo)
    where id=p_briefing_id;

    insert into public.briefings_mediad_revisoes (
        briefing_id, espaco_id, versao, motivo, alterado_por, alterado_em,
        valores_anteriores, valores_novos
    ) values (
        p_briefing_id, p_espaco_id, v_antes.versao, btrim(p_motivo),
        p_usuario_id, p_instante, to_jsonb(v_antes),
        (select to_jsonb(b) from public.briefings_mediad b where b.id=p_briefing_id)
    );

    update public.campanhas_mediad set
        etapa_atual='TRADUCAO_ESTRATEGICA', atualizado_em=p_instante
    where id=v_antes.campanha_id and espaco_id=p_espaco_id
      and etapa_atual='BRIEFING' and situacao='EM_ANDAMENTO';
    if not found then
        raise exception 'Campanha não está apta à Tradução Estratégica';
    end if;
    return p_briefing_id;
end; $$;
