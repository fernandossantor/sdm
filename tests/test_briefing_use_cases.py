from datetime import datetime, timezone
from uuid import uuid4

import pytest

from application.dto import (
    CriarVersaoBriefingEntrada, EditarBriefingEntrada,
    TransicionarBriefingEntrada,
)
from application.use_cases import (
    ConcluirBriefing, CriarNovaVersaoBriefing, EditarBriefing,
    EnviarBriefingRevisao,
)
from domain.briefing import (
    BriefingInicial, ConteudoBriefing, EstadoBriefing, avaliar_briefing,
)


class Dependencias:
    def __init__(self):
        self.instante = datetime(2026, 8, 1, 20, tzinfo=timezone.utc)
        self.autorizado = True
        self.registros = {}
        self.edicao = None
        self.versionamento = None
        self.transicao = None

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

    def transicionar_estado(
        self, anterior, atualizado, motivo, alertas_reconhecidos
    ):
        self.transicao = (anterior, atualizado, motivo, alertas_reconhecidos)
        self.registros[atualizado.id] = atualizado


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


def test_primeiro_preenchimento_registra_motivo_automatico():
    deps = Dependencias()
    anterior = briefing()
    deps.registros[anterior.id] = anterior
    atualizado = EditarBriefing(
        relogio=deps, autorizador=deps, repositorio=deps
    ).executar(EditarBriefingEntrada(
        briefing_id=anterior.id, usuario_id=anterior.criado_por,
        conteudo=conteudo(), motivo="",
    ))
    assert atualizado.id == anterior.id
    assert atualizado.versao == 1
    assert atualizado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert atualizado.atualizado_por == anterior.criado_por
    assert deps.edicao[0].conteudo != deps.edicao[1].conteudo
    assert deps.edicao[2] == "Preenchimento inicial"


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
    deps.registros[item.id] = item.model_copy(
        update={
            "estado": EstadoBriefing.EM_PREENCHIMENTO,
            "conteudo": conteudo(),
        }
    )
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


def test_avaliacao_expoe_pendencias_sem_alterar_conteudo():
    vazio = ConteudoBriefing()
    avaliacao = avaliar_briefing(vazio)
    assert avaliacao.apto_para_revisao is False
    assert avaliacao.percentual_completude == 0
    assert "Selecione ao menos um objetivo de marketing." in avaliacao.pendencias
    assert vazio == ConteudoBriefing()


def test_avaliacao_aprova_conteudo_minimo_e_preserva_alerta_de_verba():
    completo = ConteudoBriefing(
        situacao_mercadologica={"descricao": "Mercado em crescimento"},
        objetivos_marketing=({"categoria": "Crescimento"},),
        objetivos_comunicacao=({"categoria": "conhecimento"},),
        relacoes_objetivos=({"descricao": "Conhecimento apoia crescimento"},),
        pracas=({"nome": "Brasil"},),
        universos=({"nome": "Adultos"},),
        criterios_segmentacao=("demográfica",),
        segmentos=({"nome": "Adultos compradores"},),
        publicos=({"nome": "Compradores prioritários"},),
        jornada_aplicavel=False,
        periodo={"inicio": "2026-09-01", "fim": "2026-10-31"},
        verba={"natureza": "ainda não definido", "valor_total": 0},
        prioridades=({"descricao": "Público prioritário"},),
        sem_restricoes_declaradas=True,
        pretensoes=({"categoria": "ampliar presença"},),
    )
    avaliacao = avaliar_briefing(completo)
    assert avaliacao.apto_para_revisao is True
    assert avaliacao.percentual_completude == 100
    assert avaliacao.alertas == ("A verba ainda não está definida.",)


def test_avaliacao_rejeita_periodo_invertido_ou_texto_que_nao_e_data():
    base = conteudo()
    invertido = base.model_copy(update={
        "periodo": {"inicio": "2026-10-31", "fim": "2026-09-01"}
    })
    invalido = base.model_copy(update={
        "periodo": {"inicio": "amanhã", "fim": "depois"}
    })

    for item in (invertido, invalido):
        avaliacao = avaliar_briefing(item)
        assert any("datas válidas" in texto for texto in avaliacao.pendencias)


def test_conclusao_direta_exige_suficiencia_e_reconhecimento():
    deps = Dependencias()
    incompleto = briefing(EstadoBriefing.EM_PREENCHIMENTO)
    deps.registros[incompleto.id] = incompleto
    concluir = ConcluirBriefing(
        relogio=deps, autorizador=deps, repositorio=deps
    )
    entrada = TransicionarBriefingEntrada(
        briefing_id=incompleto.id, usuario_id=incompleto.criado_por,
        motivo="Conteúdo conferido",
    )
    with pytest.raises(ValueError, match="pendências"):
        concluir.executar(entrada)

    conteudo_completo = ConteudoBriefing(
        situacao_mercadologica={"descricao": "Mercado em crescimento"},
        objetivos_marketing=({"categoria": "Crescimento"},),
        objetivos_comunicacao=({"categoria": "conhecimento"},),
        relacoes_objetivos=({"descricao": "Relação explícita"},),
        pracas=({"nome": "Brasil"},), universos=({"nome": "Adultos"},),
        segmentos=({"nome": "Compradores"},),
        publicos=({"nome": "Prioritário"},), jornada_aplicavel=False,
        periodo={"inicio": "2026-09-01", "fim": "2026-10-31"},
        verba={"natureza": "ainda não definido", "valor_total": 0},
        prioridades=({"descricao": "Público"},),
        sem_restricoes_declaradas=True,
        pretensoes=({"categoria": "ampliar presença"},),
    )
    deps.registros[incompleto.id] = incompleto.model_copy(
        update={"conteudo": conteudo_completo}
    )
    with pytest.raises(ValueError, match="alertas"):
        concluir.executar(TransicionarBriefingEntrada(
            briefing_id=incompleto.id, usuario_id=incompleto.criado_por,
            motivo="Aprovação final",
        ))
    concluido = concluir.executar(TransicionarBriefingEntrada(
        briefing_id=incompleto.id, usuario_id=incompleto.criado_por,
        motivo="Aprovação final",
        alertas_reconhecidos=("A verba ainda não está definida.",),
    ))
    assert concluido.estado is EstadoBriefing.CONCLUIDO
    assert deps.transicao[2] == "Aprovação final"
