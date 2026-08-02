from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.entidades import Campanha
from mediad_planner.domain.campanha.enums import EtapaCampanha, SituacaoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    MarcaCampanha,
    ParticipanteCampanha,
    ProdutoServicoCampanha,
)


AGORA = datetime(2026, 7, 1, 12, tzinfo=timezone.utc)


def uid(valor: int) -> UUID:
    return UUID(int=valor)


def criar_campanha(**mudancas: object) -> Campanha:
    anunciante = AnuncianteCampanha(uid(3), "Anunciante")
    dados = {
        "id_campanha": uid(1),
        "id_espaco_trabalho": uid(2),
        "codigo": CodigoCampanha("MP-202607-0001"),
        "nome": "Campanha",
        "anunciante": anunciante,
        "marca": None,
        "produto_servico": None,
        "planejador_responsavel": ParticipanteCampanha(uid(4), "Planejador"),
        "equipe": [],
        "observacao_inicial": None,
        "criado_por": uid(5),
        "criado_em": AGORA,
        "atualizado_por": uid(5),
        "atualizado_em": AGORA,
    }
    dados.update(mudancas)
    return Campanha.criar_rascunho(**dados)


def test_enums_tem_composicao_exata() -> None:
    assert tuple(item.value for item in SituacaoCampanha) == (
        "RASCUNHO",
        "EM_ANDAMENTO",
        "CONCLUIDA",
        "CANCELADA",
        "ARQUIVADA",
    )
    assert tuple(item.value for item in EtapaCampanha) == (
        "ABERTURA",
        "BRIEFING",
        "TRADUCAO_ESTRATEGICA",
        "ARQUITETURA_DE_MIDIA",
        "SIMULACAO",
        "CONSOLIDACAO_DO_PLANO",
        "VALIDACAO_E_APROVACAO",
        "ACOMPANHAMENTO_E_RESULTADOS",
    )


def test_cria_rascunho_imutavel_com_campos_opcionais() -> None:
    campanha = criar_campanha(equipe=[], observacao_inicial="   ")
    assert campanha.situacao is SituacaoCampanha.RASCUNHO
    assert campanha.etapa_atual is EtapaCampanha.ABERTURA
    assert campanha.id_campanha_origem is None
    assert campanha.marca is None
    assert campanha.produto_servico is None
    assert campanha.observacao_inicial is None
    assert campanha.equipe == ()
    with pytest.raises(FrozenInstanceError):
        campanha.nome = "Outro"


@pytest.mark.parametrize("nome", ("", "  "))
def test_rejeita_nome_obrigatorio_vazio(nome: str) -> None:
    with pytest.raises(ValueError, match="nome"):
        criar_campanha(nome=nome)


def test_vinculos_exigem_snapshots_e_responsavel() -> None:
    with pytest.raises(ValueError, match="nome_snapshot"):
        AnuncianteCampanha(uid(1), " ")
    with pytest.raises(ValueError, match="anunciante"):
        criar_campanha(anunciante=None)
    with pytest.raises(ValueError, match="planejador"):
        criar_campanha(planejador_responsavel=None)


def test_rejeita_ids_duplicados_na_equipe() -> None:
    participante = ParticipanteCampanha(uid(9), "Pessoa")
    with pytest.raises(ValueError, match="duplicados"):
        criar_campanha(equipe=[participante, participante])


def test_rejeita_vinculos_incoerentes() -> None:
    anunciante = AnuncianteCampanha(uid(3), "Anunciante")
    marca_correta = MarcaCampanha(uid(6), anunciante.id_anunciante, "Marca")
    marca_incorreta = MarcaCampanha(uid(7), uid(99), "Outra")
    produto_outro_anunciante = ProdutoServicoCampanha(uid(8), uid(99), None, "Produto")
    produto_outra_marca = ProdutoServicoCampanha(uid(8), uid(3), uid(88), "Produto")
    with pytest.raises(ValueError, match="marca"):
        criar_campanha(anunciante=anunciante, marca=marca_incorreta)
    with pytest.raises(ValueError, match="anunciante"):
        criar_campanha(
            anunciante=anunciante,
            produto_servico=produto_outro_anunciante,
        )
    with pytest.raises(ValueError, match="outra marca"):
        criar_campanha(
            anunciante=anunciante,
            marca=marca_correta,
            produto_servico=produto_outra_marca,
        )


def test_valida_datas_da_campanha() -> None:
    with pytest.raises(ValueError, match="fuso"):
        criar_campanha(criado_em=datetime.now())
    with pytest.raises(ValueError, match="fuso"):
        criar_campanha(atualizado_em=datetime.now())
    with pytest.raises(ValueError, match="anteceder"):
        criar_campanha(atualizado_em=AGORA - timedelta(seconds=1))


def test_inicia_briefing_preservando_identidade_e_rejeita_repeticao() -> None:
    campanha = criar_campanha()
    atualizada = campanha.iniciar_briefing(uid(10), AGORA + timedelta(minutes=1))
    assert atualizada.situacao is SituacaoCampanha.EM_ANDAMENTO
    assert atualizada.etapa_atual is EtapaCampanha.BRIEFING
    assert atualizada.id_campanha == campanha.id_campanha
    assert atualizada.codigo == campanha.codigo
    assert atualizada.anunciante == campanha.anunciante
    assert atualizada.criado_em == campanha.criado_em
    with pytest.raises(ValueError, match="apta"):
        atualizada.iniciar_briefing(uid(10), AGORA + timedelta(minutes=2))
    with pytest.raises(ValueError, match="fuso"):
        campanha.iniciar_briefing(uid(10), datetime.now())
