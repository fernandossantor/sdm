from mediad_planner.application.dto.campanha import CampanhaResumo
from mediad_planner.domain.campanha.entidades import Campanha


def resumir_campanha(campanha: Campanha) -> CampanhaResumo:
    referencia = campanha.marca or campanha.anunciante
    identificacao = (
        f"[{campanha.codigo.valor}] {campanha.nome} — {referencia.nome_snapshot}"
    )
    return CampanhaResumo(
        id_campanha=campanha.id_campanha,
        codigo=campanha.codigo.valor,
        nome=campanha.nome,
        anunciante=campanha.anunciante.nome_snapshot,
        marca=campanha.marca.nome_snapshot if campanha.marca else None,
        produto_servico=(
            campanha.produto_servico.nome_snapshot
            if campanha.produto_servico
            else None
        ),
        planejador_responsavel=campanha.planejador_responsavel.nome_snapshot,
        equipe=tuple(item.nome_snapshot for item in campanha.equipe),
        observacao_inicial=campanha.observacao_inicial,
        situacao=campanha.situacao.value,
        etapa_atual=campanha.etapa_atual.value,
        criado_em=campanha.criado_em,
        atualizado_em=campanha.atualizado_em,
        identificacao_completa=identificacao,
    )
