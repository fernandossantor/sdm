from datetime import datetime, timezone
from uuid import uuid4

import pytest

from application.dto import CriarVersaoBriefingEntrada, EditarBriefingEntrada
from application.use_cases import CriarNovaVersaoBriefing, EditarBriefing
from domain.briefing import BriefingInicial, ConteudoBriefing, EstadoBriefing


class Dependencias:
    def __init__(self):
        self.instante = datetime(2026, 8, 1, 20, tzinfo=timezone.utc)
        self.autorizado = True
        self.registros = {}
        self.edicao = None
        self.versionamento = None

    def agora(self):
        return self.instante

    def pode_editar(self, usuario_id, campanha_id):
        return self.autorizado

    def obter_briefing(self, briefing_id):
        return self.registros.get(briefing_id)

    def salvar_edicao(self, anterior, atualizado, motivo):
        self.edicao = (anterior, atualizado, motivo)
        self.registros[atualizado.id] = atualizado

    def salvar_nova_versao(self, anterior, nova, motivo):
        self.versionamento = (anterior, nova, motivo)
        self.registros[nova.id] = nova


def briefing(estado=EstadoBriefing.RASCUNHO):
    item = BriefingInicial(
        id=uuid4(), campanha_id=uuid4(), criado_por=uuid4(),
        criado_em=datetime(2026, 8, 1, 19, tzinfo=timezone.utc),
        estado=estado,
    )
    return item


def conteudo():
    return ConteudoBriefing(
        situacao_mercadologica={"contexto": "Categoria em crescimento"},
        objetivos_marketing=({"categoria": "Crescimento", "prioridade": "alta"},),
        objetivos_comunicacao=({"categoria": "conhecimento", "prioridade": "alta"},),
        pracas=({"nome": "Brasil"},),
        universos=({"nome": "Adultos", "praca": "Brasil"},),
        segmentos=({"nome": "Compradores", "universo": "Adultos"},),
        publicos=({"nome": "Compradores prioritários", "segmento": "Compradores"},),
        periodo={"inicio": "2026-09-01", "fim": "2026-10-31"},
        verba={"natureza": "flexível", "moeda": "BRL", "valor_total": 100000},
        pretensoes=({"categoria": "ampliar presença"},),
    )


def test_edita_rascunho_com_autoria_motivo_e_valores_anteriores():
    deps = Dependencias()
    anterior = briefing()
    deps.registros[anterior.id] = anterior
    atualizado = EditarBriefing(
        relogio=deps, autorizador=deps, repositorio=deps
    ).executar(EditarBriefingEntrada(
        briefing_id=anterior.id, usuario_id=anterior.criado_por,
        conteudo=conteudo(), motivo="Complemento das informações recebidas",
    ))
    assert atualizado.id == anterior.id
    assert atualizado.versao == 1
    assert atualizado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert atualizado.atualizado_por == anterior.criado_por
    assert deps.edicao[0].conteudo != deps.edicao[1].conteudo
    assert deps.edicao[2] == "Complemento das informações recebidas"


def test_nova_versao_preserva_anterior_e_incrementa_numero():
    deps = Dependencias()
    anterior = briefing(EstadoBriefing.CONCLUIDO).model_copy(
        update={"conteudo": conteudo()}
    )
    deps.registros[anterior.id] = anterior
    novo_conteudo = conteudo().model_copy(
        update={"situacao_mercadologica": {"contexto": "Categoria estabilizada"}}
    )
    nova = CriarNovaVersaoBriefing(
        relogio=deps, autorizador=deps, repositorio=deps
    ).executar(CriarVersaoBriefingEntrada(
        briefing_id_origem=anterior.id, usuario_id=anterior.criado_por,
        conteudo=novo_conteudo, motivo="Mudança relevante no mercado",
    ))
    assert nova.id != anterior.id
    assert nova.versao == 2
    assert nova.criado_por == anterior.criado_por
    assert deps.versionamento[0] == anterior
    assert deps.registros[anterior.id].conteudo.situacao_mercadologica == {
        "contexto": "Categoria em crescimento"
    }


def test_edicao_exige_permissao_motivo_e_estado_editavel():
    deps = Dependencias()
    item = briefing(EstadoBriefing.CONCLUIDO)
    deps.registros[item.id] = item
    caso = EditarBriefing(relogio=deps, autorizador=deps, repositorio=deps)
    with pytest.raises(ValueError, match="nova versão"):
        caso.executar(EditarBriefingEntrada(
            briefing_id=item.id, usuario_id=item.criado_por,
            conteudo=conteudo(), motivo="Alteração",
        ))
    deps.registros[item.id] = item.model_copy(update={"estado": EstadoBriefing.RASCUNHO})
    with pytest.raises(ValueError, match="motivo"):
        caso.executar(EditarBriefingEntrada(
            briefing_id=item.id, usuario_id=item.criado_por,
            conteudo=conteudo(), motivo=" ",
        ))
    deps.autorizado = False
    with pytest.raises(PermissionError):
        caso.executar(EditarBriefingEntrada(
            briefing_id=item.id, usuario_id=item.criado_por,
            conteudo=conteudo(), motivo="Alteração",
        ))
