from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError

from domain.contracts import (
    Alerta,
    ComandoMotor,
    EstadoExecucao,
    NivelExecucao,
    NaturezaValor,
    PlanoReexecucao,
    PoliticaReexecucao,
    ResultadoValidacao,
    SaidaMotor,
    Severidade,
    ValidacaoLocal,
    ValorTipado,
)
from engines.base import Motor
from infrastructure.configuration import SupabaseSettings


def comando_valido(**ajustes):
    dados = {
        "motor_destino": "traducao_estrategica",
        "modo_execucao": "traduzir",
        "id_campanha": uuid4(),
        "id_snapshot_campanha": uuid4(),
        "id_usuario": uuid4(),
        "perfil_de_acesso": "PLANEJADOR",
        "solicitado_em": datetime.now(timezone.utc),
        "origem_do_comando": "teste",
        "objetivo_da_execucao": "validar a fundacao",
    }
    dados.update(ajustes)
    return ComandoMotor(**dados)


def saida(comando, estado=EstadoExecucao.PARCIAL, **ajustes):
    dados = {
        "id_comando": comando.id_comando,
        "motor": comando.motor_destino,
        "modo_execucao": comando.modo_execucao,
        "nivel_execucao": comando.nivel_execucao,
        "estado_execucao": estado,
        "produzido_em": datetime.now(timezone.utc),
        "reexecucao": PlanoReexecucao(
            politica=PoliticaReexecucao.REEXECUTAR_MODO,
            motivo="entrada pendente",
            alvos=("traduzir",),
        ),
    }
    dados.update(ajustes)
    return SaidaMotor(**dados)


def test_criacao_valida_de_comando():
    assert comando_valido().nivel_execucao is NivelExecucao.PADRAO


def test_rejeita_comando_invalido_e_timestamp_sem_fuso():
    with pytest.raises(ValidationError):
        comando_valido(motor_destino="", solicitado_em=datetime.now())


def test_serializacao_e_desserializacao():
    original = comando_valido()
    restaurado = ComandoMotor.model_validate_json(original.model_dump_json())
    assert restaurado == original


def test_timestamp_com_fuso_na_saida():
    assert saida(comando_valido()).produzido_em.utcoffset() is not None


def test_ausencia_nao_vira_zero():
    ausente = ValorTipado(
        valor=None, natureza=NaturezaValor.NAO_DISPONIVEL, origem="briefing"
    )
    zero = ValorTipado(valor=0, natureza=NaturezaValor.INFORMADO, origem="briefing")
    assert ausente.valor is None
    assert zero.valor == 0
    assert ausente != zero


def test_saida_parcial_e_nao_executavel():
    comando = comando_valido()
    assert saida(comando).estado_execucao is EstadoExecucao.PARCIAL
    assert (
        saida(comando, EstadoExecucao.NAO_EXECUTAVEL).estado_execucao
        is EstadoExecucao.NAO_EXECUTAVEL
    )


def test_validacao_com_alerta():
    validacao = ValidacaoLocal(
        codigo="DADO_ESTIMADO",
        objeto_validado="orcamento",
        resultado=ResultadoValidacao.VALIDO_COM_ALERTA,
        severidade=Severidade.ATENCAO,
        mensagem="Valor estimado.",
    )
    alerta = Alerta(
        codigo="DADO_ESTIMADO",
        severidade=Severidade.ATENCAO,
        titulo="Estimativa",
        mensagem="Revisar antes da aprovação.",
        origem="validacao_local",
    )
    resultado = saida(comando_valido(), validacoes=(validacao,), alertas=(alerta,))
    assert resultado.validacoes[0].resultado is ResultadoValidacao.VALIDO_COM_ALERTA


def test_plano_de_reexecucao():
    plano = saida(comando_valido()).reexecucao
    assert plano.politica is PoliticaReexecucao.REEXECUTAR_MODO


def test_interface_base_aceita_motor_falso():
    class MotorFalso:
        def executar(self, comando: ComandoMotor) -> SaidaMotor:
            return saida(comando, EstadoExecucao.CONCLUIDA)

    motor: Motor[ComandoMotor, SaidaMotor] = MotorFalso()
    assert motor.executar(comando_valido()).estado_execucao is EstadoExecucao.CONCLUIDA


def test_dominio_nao_importa_streamlit_ou_supabase():
    raiz = Path(__file__).parents[1] / "domain"
    conteudo = "\n".join(p.read_text() for p in raiz.rglob("*.py"))
    assert "import streamlit" not in conteudo
    assert "from streamlit" not in conteudo
    assert "import supabase" not in conteudo
    assert "from supabase" not in conteudo


def test_configuracao_supabase_nao_expoe_secrets(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://project.example")
    monkeypatch.setenv("SUPABASE_KEY", "anon-secret")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "service-secret")
    config = SupabaseSettings.from_environment(administrative=True)
    representacao = repr(config.safe_status())
    assert "anon-secret" not in representacao
    assert "service-secret" not in representacao
    assert config.safe_status() == {
        "SUPABASE_URL": True,
        "SUPABASE_KEY": True,
        "SUPABASE_SERVICE_KEY": True,
    }
