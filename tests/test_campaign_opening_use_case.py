from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from application.dto import (
    AbrirCampanhaEntrada,
    CorrigirCampanhaEntrada,
    IniciarBriefingEntrada,
)
from application.use_cases import AbrirCampanha, CorrigirCampanha, IniciarBriefing
from domain.briefing import EstadoBriefing
from domain.campanha import EtapaCampanha, SituacaoCampanha


class DependenciasFalsas:
    def __init__(self):
        self.instante = datetime(2026, 7, 30, 12, tzinfo=timezone.utc)
        self.campanhas = {}
        self.briefings = {}
        self.autorizado = True
        self.vinculos_validados = None
        self.correcao = None

    def agora(self):
        return self.instante

    def pode_criar(self, usuario_id):
        return self.autorizado

    def pode_editar(self, usuario_id, campanha_id):
        return self.autorizado

    def validar(self, anunciante_id, marca_id, produto_servico_id):
        self.vinculos_validados = (
            anunciante_id,
            marca_id,
            produto_servico_id,
        )

    def proximo(self, criado_em):
        return "MP-202607-0001"

    def salvar_abertura(self, campanha):
        self.campanhas[campanha.id] = campanha

    def obter_campanha(self, campanha_id):
        return self.campanhas.get(campanha_id)

    def corrigir_campanha(self, entrada, atualizado_em):
        self.correcao = (entrada, atualizado_em)

    def iniciar_briefing(self, campanha, briefing):
        self.campanhas[campanha.id] = campanha
        self.briefings[briefing.id] = briefing


def entrada_valida():
    return AbrirCampanhaEntrada(
        nome="Lançamento",
        anunciante_id=uuid4(),
        nome_anunciante="Anunciante",
        marca_id=uuid4(),
        nome_marca="Marca",
        produto_servico_id=uuid4(),
        nome_produto_servico="Produto",
        planejador_responsavel_id=uuid4(),
        identificacao_planejador="Planejador",
        criado_por=uuid4(),
    )


def abrir(deps, entrada=None):
    return AbrirCampanha(
        relogio=deps,
        autorizador=deps,
        validador_vinculos=deps,
        gerador_codigo=deps,
        unidade_trabalho=deps,
    ).executar(entrada or entrada_valida())


def test_abre_campanha_em_rascunho_com_snapshot_sem_acionar_motor():
    deps = DependenciasFalsas()
    resultado = abrir(deps)
    campanha = resultado.campanha
    assert campanha.situacao is SituacaoCampanha.RASCUNHO
    assert campanha.etapa_atual is EtapaCampanha.ABERTURA
    assert campanha.snapshot.nome_anunciante == "Anunciante"
    assert campanha.codigo == "MP-202607-0001"
    assert resultado.habilita_inicio_briefing is True


def test_valida_vinculos_antes_de_persistir():
    deps = DependenciasFalsas()
    entrada = entrada_valida()
    abrir(deps, entrada)
    assert deps.vinculos_validados == (
        entrada.anunciante_id,
        entrada.marca_id,
        entrada.produto_servico_id,
    )


def test_rejeita_usuario_sem_permissao_e_nome_vazio():
    deps = DependenciasFalsas()
    deps.autorizado = False
    with pytest.raises(PermissionError):
        abrir(deps)
    deps.autorizado = True
    with pytest.raises(ValidationError):
        abrir(deps, replace(entrada_valida(), nome=" "))


def test_rejeita_snapshot_incoerente_com_vinculo_opcional():
    deps = DependenciasFalsas()
    with pytest.raises(ValidationError):
        abrir(deps, replace(entrada_valida(), nome_marca=None))


def test_concluir_abertura_inicia_briefing_v1_atomicamente():
    deps = DependenciasFalsas()
    campanha = abrir(deps).campanha
    resultado = IniciarBriefing(
        relogio=deps,
        autorizador=deps,
        unidade_trabalho=deps,
    ).executar(
        IniciarBriefingEntrada(
            campanha_id=campanha.id,
            usuario_id=campanha.criado_por,
        )
    )
    assert resultado.campanha.situacao is SituacaoCampanha.EM_ANDAMENTO
    assert resultado.campanha.etapa_atual is EtapaCampanha.BRIEFING
    assert resultado.briefing.estado is EstadoBriefing.RASCUNHO
    assert resultado.briefing.versao == 1
    assert deps.briefings[resultado.briefing.id] == resultado.briefing


def test_nao_inicia_briefing_duas_vezes():
    deps = DependenciasFalsas()
    campanha = abrir(deps).campanha
    caso = IniciarBriefing(
        relogio=deps,
        autorizador=deps,
        unidade_trabalho=deps,
    )
    entrada = IniciarBriefingEntrada(
        campanha_id=campanha.id,
        usuario_id=campanha.criado_por,
    )
    caso.executar(entrada)
    with pytest.raises(ValueError):
        caso.executar(entrada)

def test_corrige_campanha_em_elaboracao_com_motivo_e_autoria():
    deps = DependenciasFalsas()
    campanha = abrir(deps).campanha
    entrada = CorrigirCampanhaEntrada(
        campanha_id=campanha.id,
        nome="Lançamento corrigido",
        anunciante_id=campanha.anunciante_id,
        nome_anunciante="Anunciante corrigido",
        planejador_responsavel_id=campanha.planejador_responsavel_id,
        identificacao_planejador="Pessoa Planejadora",
        alterado_por=campanha.criado_por,
        motivo="Correção de digitação",
    )

    CorrigirCampanha(
        relogio=deps,
        autorizador=deps,
        validador_vinculos=deps,
        unidade_trabalho=deps,
    ).executar(entrada)

    assert deps.correcao == (entrada, deps.instante)
    assert deps.campanhas[campanha.id].snapshot.nome_anunciante == "Anunciante"


def test_correcao_exige_motivo():
    deps = DependenciasFalsas()
    campanha = abrir(deps).campanha
    entrada = CorrigirCampanhaEntrada(
        campanha_id=campanha.id,
        nome=campanha.nome,
        anunciante_id=campanha.anunciante_id,
        nome_anunciante=campanha.snapshot.nome_anunciante,
        planejador_responsavel_id=campanha.planejador_responsavel_id,
        identificacao_planejador="Pessoa Planejadora",
        alterado_por=campanha.criado_por,
        motivo=" ",
    )
    with pytest.raises(ValueError, match="motivo"):
        CorrigirCampanha(
            relogio=deps,
            autorizador=deps,
            validador_vinculos=deps,
            unidade_trabalho=deps,
        ).executar(entrada)
