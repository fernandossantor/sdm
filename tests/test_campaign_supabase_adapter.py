from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest

from application.dto import CorrigirCampanhaEntrada
from domain.briefing import BriefingInicial, ConteudoBriefing, EstadoBriefing
from domain.campanha import (
    Campanha,
    EtapaCampanha,
    SituacaoCampanha,
    SnapshotVinculosCampanha,
)
from domain.traducao import ContratoEstrategico, EstadoContratoEstrategico
from domain.contracts import Confianca
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

    def order(self, campo, **opcoes):
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


def test_edicao_e_versionamento_do_briefing_usam_rpcs_rastreaveis():
    cliente = ClienteFake()
    repositorio = UnidadeTrabalhoCampanhaSupabase(
        cliente=cliente, espaco_id=uuid4()
    )
    anterior = BriefingInicial(
        id=uuid4(), campanha_id=uuid4(), criado_por=uuid4(),
        criado_em=datetime(2026, 8, 1, 20, tzinfo=timezone.utc),
    )
    conteudo = ConteudoBriefing(
        objetivos_marketing=({"categoria": "Crescimento"},)
    )
    atualizado = anterior.model_copy(update={
        "conteudo": conteudo,
        "estado": EstadoBriefing.EM_PREENCHIMENTO,
        "atualizado_por": anterior.criado_por,
        "atualizado_em": anterior.criado_em,
    })
    repositorio.salvar_edicao(anterior, atualizado, "Complemento")
    nome, parametros = cliente.chamadas_rpc[-1]
    assert nome == "editar_briefing_mediad"
    assert parametros["p_motivo"] == "Complemento"
    assert parametros["p_conteudo"]["objetivos_marketing"][0]["categoria"] == (
        "Crescimento"
    )

    nova = anterior.model_copy(update={
        "id": uuid4(), "versao": 2, "conteudo": conteudo,
        "criado_por": anterior.criado_por, "criado_em": anterior.criado_em,
    })
    repositorio.salvar_nova_versao(anterior, nova, "Mudança relevante")
    nome, parametros = cliente.chamadas_rpc[-1]
    assert nome == "versionar_briefing_mediad"
    assert parametros["p_briefing_origem_id"] == str(anterior.id)
    assert parametros["p_novo_briefing_id"] == str(nova.id)

    em_revisao = atualizado.model_copy(
        update={"estado": EstadoBriefing.EM_REVISAO}
    )
    repositorio.transicionar_estado(
        atualizado, em_revisao, "Conteúdo conferido", ()
    )
    nome, parametros = cliente.chamadas_rpc[-1]
    assert nome == "transicionar_briefing_mediad"
    assert parametros["p_estado_destino"] == "EM_REVISAO"
    assert parametros["p_motivo"] == "Conteúdo conferido"


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


def test_traducao_e_lida_por_briefing_e_salva_por_rpc():
    cliente = ClienteFake()
    espaco_id = uuid4()
    briefing_id = uuid4()
    contrato = ContratoEstrategico(
        id=uuid4(), campanha_id=uuid4(), briefing_id=briefing_id,
        briefing_versao=1, estado=EstadoContratoEstrategico.PROVISORIO,
        objetivos_declarados=(), objetivos_midia_derivados=(), lacunas=(),
        confianca=Confianca.BAIXA, versao_regras="regra-v1",
        criado_por=uuid4(),
        criado_em=datetime(2026, 8, 2, 1, 30, tzinfo=timezone.utc),
    )
    cliente.respostas["traducoes_estrategicas_mediad"] = [
        {"resultado": contrato.model_dump(mode="json")}
    ]
    repositorio = UnidadeTrabalhoCampanhaSupabase(
        cliente=cliente, espaco_id=espaco_id
    )

    assert repositorio.obter_traducao_por_briefing(briefing_id) == contrato
    repositorio.salvar_traducao(contrato)

    nome, parametros = cliente.chamadas_rpc[-1]
    assert nome == "criar_traducao_estrategica_mediad"
    assert parametros["p_briefing_id"] == str(briefing_id)
    assert parametros["p_espaco_id"] == str(espaco_id)
    assert parametros["p_resultado"]["estado"] == "PROVISORIO"

    nova = contrato.model_copy(update={"id": uuid4(), "versao": 2})
    repositorio.salvar_nova_versao_traducao(contrato, nova)
    nome, parametros = cliente.chamadas_rpc[-1]
    assert nome == "versionar_traducao_estrategica_mediad"
    assert parametros["p_traducao_anterior_id"] == str(contrato.id)
    assert parametros["p_resultado"]["versao"] == 2


def test_migracao_da_traducao_exige_briefing_concluido_e_rls():
    migracao = Path(
        "supabase/migrations/20260802013000_traducao_estrategica_inicial.sql"
    ).read_text()
    rollback = Path(
        "supabase/rollbacks/20260802013000_traducao_estrategica_inicial.down.sql"
    ).read_text()

    assert "enable row level security" in migracao
    assert "estado='CONCLUIDO'" in migracao
    assert "pode_editar_espaco" in migracao
    assert "drop table" in rollback
    versionamento = Path(
        "supabase/migrations/20260802023000_versiona_traducao_estrategica.sql"
    ).read_text()
    assert "for update" in versionamento
    assert "set estado='SUPERADO'" in versionamento


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


def test_migracao_do_briefing_preserva_versoes_e_auditoria():
    migracao = Path(
        "supabase/migrations/20260801210000_briefing_estruturado_versionado.sql"
    ).read_text()
    rollback = Path(
        "supabase/rollbacks/"
        "20260801210000_briefing_estruturado_versionado.down.sql"
    ).read_text()

    assert "conteudo jsonb not null" in migracao
    assert "briefings_mediad_revisoes" in migracao
    assert "to_jsonb(v_antes)" in migracao
    assert "estado='SUBSTITUIDO'" in migracao
    assert "versionar_briefing_mediad" in migracao
    assert "drop table if exists public.briefings_mediad_revisoes" in rollback


def test_migracao_de_conclusao_avanca_campanha_atomicamente():
    migracao = Path(
        "supabase/migrations/20260801233000_fluxo_revisao_briefing.sql"
    ).read_text()
    rollback = Path(
        "supabase/rollbacks/20260801233000_fluxo_revisao_briefing.down.sql"
    ).read_text()
    assert "transicionar_briefing_mediad" in migracao
    assert "alertas_reconhecidos" in migracao
    assert "etapa_atual='TRADUCAO_ESTRATEGICA'" in migracao
    assert "to_jsonb(v_antes)" in migracao
    assert "drop function if exists public.transicionar_briefing_mediad" in rollback


def test_migracao_simplifica_para_conclusao_direta():
    migracao = Path(
        "supabase/migrations/20260802001000_conclusao_direta_briefing.sql"
    ).read_text()
    assert (
        "v_antes.estado='EM_PREENCHIMENTO' "
        "and p_estado_destino='CONCLUIDO'"
    ) in migracao
    assert "etapa_atual='TRADUCAO_ESTRATEGICA'" in migracao
