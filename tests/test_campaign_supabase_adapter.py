from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest

from application.dto import CorrigirCampanhaEntrada
from domain.briefing import BriefingInicial
from domain.campanha import (
    Campanha,
    EtapaCampanha,
    SituacaoCampanha,
    SnapshotVinculosCampanha,
)
from infrastructure.repositories.campanha_mediad import (
    UnidadeTrabalhoCampanhaSupabase,
)


@dataclass
class Resposta:
    data: list


class Operacao:
    def __init__(self, resposta):
        self.resposta = resposta

    def execute(self):
        return self.resposta


class Consulta:
    def __init__(self, cliente, tabela):
        self.cliente = cliente
        self.tabela = tabela
        self.filtros = []

    def select(self, campos):
        return self

    def eq(self, campo, valor):
        self.filtros.append((campo, valor))
        return self

    def limit(self, quantidade):
        return self

    def order(self, campo):
        return self

    def execute(self):
        self.cliente.consultas.append((self.tabela, tuple(self.filtros)))
        return Resposta(self.cliente.respostas.get(self.tabela, []))


class ClienteFake:
    def __init__(self):
        self.chamadas_rpc = []
        self.consultas = []
        self.respostas = {}

    def rpc(self, nome, parametros):
        self.chamadas_rpc.append((nome, parametros))
        return Operacao(Resposta([]))

    def table(self, tabela):
        return Consulta(self, tabela)


def campanha_aberta(**ajustes):
    instante = datetime(2026, 7, 30, 18, tzinfo=timezone.utc)
    dados = {
        "id": uuid4(),
        "codigo": "MP-202607-0001",
        "nome": "Lançamento",
        "anunciante_id": uuid4(),
        "marca_id": uuid4(),
        "produto_servico_id": None,
        "planejador_responsavel_id": uuid4(),
        "equipe_ids": (uuid4(), uuid4()),
        "observacao_inicial": "Contexto inicial",
        "snapshot": SnapshotVinculosCampanha(
            nome_anunciante="Anunciante",
            nome_marca="Marca",
            nome_produto_servico=None,
            identificacao_planejador="Planejador",
        ),
        "criado_por": uuid4(),
        "criado_em": instante,
        "atualizado_em": instante,
    }
    dados.update(ajustes)
    return Campanha(**dados)


def registro(campanha):
    serializado = UnidadeTrabalhoCampanhaSupabase._serializar_campanha(campanha)
    return {
        chave.replace("snapshot_", "snapshot_"): valor
        for chave, valor in serializado.items()
        if chave != "equipe_ids"
    }


def test_abertura_usa_uma_rpc_atomica_e_espaco_fora_do_payload():
    cliente = ClienteFake()
    espaco_id = uuid4()
    campanha = campanha_aberta()
    repositorio = UnidadeTrabalhoCampanhaSupabase(cliente=cliente, espaco_id=espaco_id)

    repositorio.salvar_abertura(campanha)

    nome, parametros = cliente.chamadas_rpc[0]
    assert nome == "abrir_campanha_mediad"
    assert parametros["p_espaco_id"] == str(espaco_id)
    assert "espaco_id" not in parametros["p_campanha"]
    assert parametros["p_campanha"]["equipe_ids"] == [
        str(item) for item in campanha.equipe_ids
    ]


def test_obtem_campanha_no_espaco_e_reconstroi_equipe():
    cliente = ClienteFake()
    espaco_id = uuid4()
    campanha = campanha_aberta()
    cliente.respostas["campanhas_mediad"] = [registro(campanha)]
    cliente.respostas["campanhas_mediad_equipe"] = [
        {"usuario_id": str(item)} for item in campanha.equipe_ids
    ]
    repositorio = UnidadeTrabalhoCampanhaSupabase(cliente=cliente, espaco_id=espaco_id)

    obtida = repositorio.obter_campanha(campanha.id)

    assert obtida == campanha
    assert (
        "campanhas_mediad",
        (("id", str(campanha.id)), ("espaco_id", str(espaco_id))),
    ) in cliente.consultas


def test_inicio_do_briefing_e_uma_unica_operacao_transacional():
    cliente = ClienteFake()
    espaco_id = uuid4()
    aberta = campanha_aberta()
    em_briefing = aberta.iniciar_briefing(aberta.atualizado_em)
    briefing = BriefingInicial(
        id=uuid4(),
        campanha_id=aberta.id,
        criado_por=aberta.criado_por,
        criado_em=aberta.atualizado_em,
    )
    repositorio = UnidadeTrabalhoCampanhaSupabase(cliente=cliente, espaco_id=espaco_id)

    repositorio.iniciar_briefing(em_briefing, briefing)

    assert len(cliente.chamadas_rpc) == 1
    nome, parametros = cliente.chamadas_rpc[0]
    assert nome == "iniciar_briefing_mediad"
    assert parametros["p_campanha_id"] == str(aberta.id)
    assert parametros["p_briefing_id"] == str(briefing.id)


def test_rejeita_transicao_incoerente_antes_de_chamar_banco():
    cliente = ClienteFake()
    repositorio = UnidadeTrabalhoCampanhaSupabase(cliente=cliente, espaco_id=uuid4())
    campanha = campanha_aberta(
        situacao=SituacaoCampanha.EM_ANDAMENTO,
        etapa_atual=EtapaCampanha.BRIEFING,
    )
    briefing = BriefingInicial(
        id=uuid4(),
        campanha_id=uuid4(),
        criado_por=campanha.criado_por,
        criado_em=campanha.atualizado_em,
    )

    with pytest.raises(ValueError, match="outra campanha"):
        repositorio.iniciar_briefing(campanha, briefing)
    assert cliente.chamadas_rpc == []


def test_migracao_e_nova_reversivel_e_protegida_por_rls():
    migracao = Path(
        "supabase/migrations/20260730010000_campanhas_briefings_mediad.sql"
    ).read_text()
    rollback = Path(
        "supabase/rollbacks/" "20260730010000_campanhas_briefings_mediad.down.sql"
    ).read_text()

    assert "enable row level security" in migracao
    assert "public.pode_editar_espaco" in migracao
    assert "auth.uid()" in migracao
    assert "security definer" in migracao
    assert "revoke insert, update, delete" in migracao
    assert "public.projetos" not in migracao
    assert "public.briefings_v3" not in migracao
    assert "drop table if exists public.campanhas_mediad" in rollback

def test_correcao_usa_rpc_com_motivo_autor_e_valores_atuais():
    cliente = ClienteFake()
    espaco_id = uuid4()
    campanha = campanha_aberta()
    entrada = CorrigirCampanhaEntrada(
        campanha_id=campanha.id,
        nome="Nome corrigido",
        anunciante_id=campanha.anunciante_id,
        nome_anunciante="Anunciante atual",
        planejador_responsavel_id=campanha.planejador_responsavel_id,
        identificacao_planejador="Fernando Santor",
        alterado_por=campanha.criado_por,
        motivo="Correção solicitada",
    )
    repositorio = UnidadeTrabalhoCampanhaSupabase(
        cliente=cliente, espaco_id=espaco_id
    )

    repositorio.corrigir_campanha(entrada, campanha.atualizado_em)

    nome, parametros = cliente.chamadas_rpc[0]
    assert nome == "atualizar_campanha_mediad"
    assert parametros["p_motivo"] == "Correção solicitada"
    assert parametros["p_alteracoes"]["nome_anunciante_atual"] == "Anunciante atual"
    assert parametros["p_alteracoes"]["identificacao_planejador_atual"] == "Fernando Santor"


def test_migracao_de_correcao_preserva_snapshot_e_registra_revisao():
    migracao = Path(
        "supabase/migrations/20260801190000_edicao_rastreavel_campanha.sql"
    ).read_text()
    rollback = Path(
        "supabase/rollbacks/20260801190000_edicao_rastreavel_campanha.down.sql"
    ).read_text()

    assert "campanhas_mediad_revisoes" in migracao
    assert "to_jsonb(v_antes)" in migracao
    assert "snapshot_nome_anunciante" not in migracao.split(
        "create function public.atualizar_campanha_mediad", 1
    )[1].split("end;", 1)[0]
    assert "drop table if exists public.campanhas_mediad_revisoes" in rollback
