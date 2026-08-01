"""Estado de sessão da abertura de Campanha, sem dependência de Streamlit."""

CHAVES_CAMPANHA_ATUAL = (
    "campanha_id",
    "campanha_codigo",
    "campanha_nome",
    "campanha_anunciante",
    "campanha_marca",
    "campanha_produto",
    "campanha_planejador",
    "campanha_etapa",
    "briefing_id",
    "campanha_anunciante_id",
    "campanha_marca_id",
    "campanha_produto_id",
    "campanha_observacao",
    "campanha_em_edicao",
)


def iniciar_nova_campanha(estado) -> None:
    for chave in CHAVES_CAMPANHA_ATUAL:
        estado.pop(chave, None)
    estado["campanha_em_criacao"] = True
