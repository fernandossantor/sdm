from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from types import MappingProxyType
from uuid import uuid4

import pytest

from mediad_planner.domain.common.enums import (
    ClassificacaoEntrada,
    EstadoExecucao,
    MotorDestino,
    NaturezaValor,
    NivelConfianca,
    NivelExecucao,
    OrigemComando,
    PapelAcesso,
    PoliticaReexecucao,
    ResultadoValidacao,
    Severidade,
    TipoDependencia,
)
from mediad_planner.domain.common.value_objects import (
    LimitesExecucao,
    ParametroLocal,
    ReferenciaVersionada,
)
from mediad_planner.domain.contracts.motores import (
    VERSAO_CONTRATO_MOTORES,
    ComandoMotor,
    ConfiancaExecucao,
    DependenciaExecucao,
    ExplicacaoExecucao,
    RastreabilidadeExecucao,
    SaidaMotor,
)


ENUMS_ESPERADOS = {
    MotorDestino: (
        "TRADUCAO_ESTRATEGICA",
        "DECISAO_ARQUITETURA_CENARIOS",
        "SIMULACAO_TECNICA_E_ECONOMICA",
    ),
    NivelExecucao: ("PREVIA", "PADRAO", "DETALHADA"),
    EstadoExecucao: (
        "RECEBIDA",
        "EM_RESOLUCAO_DE_CONTEXTO",
        "AGUARDANDO_DADO_ESSENCIAL",
        "EM_EXECUCAO",
        "CONCLUIDA",
        "CONCLUIDA_COM_RESSALVAS",
        "PARCIAL",
        "NAO_EXECUTAVEL",
        "CANCELADA",
        "FALHA_TECNICA",
    ),
    ResultadoValidacao: (
        "VALIDO",
        "VALIDO_COM_ALERTA",
        "INVALIDO",
        "INDETERMINADO",
    ),
    Severidade: ("INFORMATIVA", "ATENCAO", "RESTRITIVA", "BLOQUEANTE"),
    NaturezaValor: (
        "INFORMADO",
        "HERDADO",
        "CALCULADO",
        "ESTIMADO",
        "INFERIDO",
        "AJUSTADO_PELO_USUARIO",
        "PADRAO_APLICADO",
        "NAO_DISPONIVEL",
        "NAO_APLICAVEL",
        "INVALIDO",
    ),
    NivelConfianca: ("ALTA", "MEDIA", "BAIXA", "INDETERMINADA"),
    PoliticaReexecucao: (
        "NENHUMA",
        "RECALCULAR_PARCIALMENTE",
        "REEXECUTAR_MODO",
        "REEXECUTAR_MOTOR",
        "INVALIDAR_DEPENDENTES",
        "REQUERER_NOVA_DECISAO_HUMANA",
    ),
    TipoDependencia: (
        "ESTRATEGICA",
        "DECISORIA",
        "TECNICA",
        "ECONOMICA",
        "TEMPORAL",
        "TERRITORIAL",
        "MENSURACAO",
        "INVENTARIO",
        "GOVERNANCA",
    ),
    OrigemComando: (
        "INTERFACE",
        "SERVICO_APLICACAO",
        "REEXECUCAO",
        "CALCULO_ISOLADO",
        "OUTRO_MOTOR",
    ),
    PapelAcesso: ("ADMINISTRADOR", "PROPRIETARIO", "EDITOR", "LEITOR"),
    ClassificacaoEntrada: (
        "OBRIGATORIA",
        "CONDICIONAL",
        "OPCIONAL",
        "HERDADA",
        "PADRAO_CONFIGURAVEL",
        "NAO_PERTINENTE",
    ),
}


def criar_comando(**mudancas: object) -> ComandoMotor:
    dados = {
        "id_comando": uuid4(),
        "motor_destino": MotorDestino.TRADUCAO_ESTRATEGICA,
        "modo_execucao": "TESTE",
        "nivel_execucao": NivelExecucao.PREVIA,
        "id_campanha": uuid4(),
        "id_snapshot_campanha": uuid4(),
        "id_usuario": uuid4(),
        "perfil_de_acesso": PapelAcesso.EDITOR,
        "solicitado_em": datetime.now(timezone.utc),
        "origem_do_comando": OrigemComando.INTERFACE,
        "objetivo_da_execucao": "Validar",
        "referencias_de_entrada": [],
        "parametros_locais": [],
        "limites_de_execucao": LimitesExecucao(),
    }
    dados.update(mudancas)
    return ComandoMotor(**dados)


def criar_saida(**mudancas: object) -> SaidaMotor[str]:
    comando = criar_comando()
    dados = {
        "id_execucao": uuid4(),
        "id_comando": comando.id_comando,
        "motor": comando.motor_destino,
        "modo_execucao": comando.modo_execucao,
        "nivel_execucao": comando.nivel_execucao,
        "estado_execucao": EstadoExecucao.CONCLUIDA,
        "resultado_principal": "ok",
        "resultados_secundarios": [],
        "validacoes": [],
        "alertas": [],
        "restricoes": [],
        "confianca": ConfiancaExecucao(*(NivelConfianca.ALTA,) * 4),
        "explicacao": ExplicacaoExecucao("ok", [], [], [], [], [], []),
        "rastreabilidade": RastreabilidadeExecucao([], [], [], [], []),
        "dependencias": [],
        "reexecucao": PoliticaReexecucao.NENHUMA,
        "produzido_em": datetime.now(timezone.utc),
        "versao_do_contrato": VERSAO_CONTRATO_MOTORES,
    }
    dados.update(mudancas)
    return SaidaMotor(**dados)


def test_todos_os_enums_possuem_composicao_exata() -> None:
    for classe_enum, nomes_esperados in ENUMS_ESPERADOS.items():
        membros = tuple(classe_enum)
        assert tuple(membro.name for membro in membros) == nomes_esperados
        assert tuple(membro.value for membro in membros) == nomes_esperados
        assert len(classe_enum.__members__) == len(nomes_esperados)


@pytest.mark.parametrize("campo", ("codigo", "versao"))
@pytest.mark.parametrize("texto_vazio", ("", "   "))
def test_referencia_rejeita_texto_obrigatorio_vazio(
    campo: str, texto_vazio: str
) -> None:
    dados = {"codigo": "codigo", "versao": "1"}
    dados[campo] = texto_vazio
    with pytest.raises(ValueError, match=campo):
        ReferenciaVersionada(**dados)


@pytest.mark.parametrize("texto_vazio", ("", "   "))
def test_parametro_rejeita_nome_vazio(texto_vazio: str) -> None:
    with pytest.raises(ValueError, match="nome"):
        ParametroLocal(texto_vazio, 1)


@pytest.mark.parametrize("campo", ("modo_execucao", "objetivo_da_execucao"))
@pytest.mark.parametrize("texto_vazio", ("", "   "))
def test_comando_rejeita_texto_obrigatorio_vazio(
    campo: str, texto_vazio: str
) -> None:
    with pytest.raises(ValueError, match=campo):
        criar_comando(**{campo: texto_vazio})


@pytest.mark.parametrize("campo", ("modo_execucao", "versao_do_contrato"))
@pytest.mark.parametrize("texto_vazio", ("", "   "))
def test_saida_rejeita_texto_obrigatorio_vazio(
    campo: str, texto_vazio: str
) -> None:
    with pytest.raises(ValueError, match=campo):
        criar_saida(**{campo: texto_vazio})


def test_parametro_congela_lista_sem_reter_referencia_externa() -> None:
    lista_original = ["a"]
    parametro = ParametroLocal("lista", lista_original)
    lista_original.append("b")
    assert parametro.valor == ("a",)


def test_parametro_copia_e_congela_mapeamento_recursivamente() -> None:
    dicionario_original = {"itens": ["a"]}
    parametro = ParametroLocal("mapa", dicionario_original)
    dicionario_original["itens"].append("b")
    dicionario_original["novo"] = True

    assert isinstance(parametro.valor, MappingProxyType)
    assert "novo" not in parametro.valor
    assert parametro.valor["itens"] == ("a",)
    with pytest.raises(TypeError):
        parametro.valor["novo"] = True


def test_limites_rejeitam_valores_invalidos() -> None:
    for valor in (0, -1, 1.2, True):
        with pytest.raises(ValueError):
            LimitesExecucao(maximo_objetos=valor)


def test_comando_valida_fuso_duplicidades_tuplas_e_imutabilidade() -> None:
    referencia = ReferenciaVersionada("a", "1")
    parametro = ParametroLocal("a", 1)
    comando = criar_comando(
        referencias_de_entrada=[referencia],
        parametros_locais=[parametro],
    )

    assert comando.referencias_de_entrada == (referencia,)
    assert comando.parametros_locais == (parametro,)
    with pytest.raises(ValueError, match="fuso horário"):
        criar_comando(solicitado_em=datetime.now())
    with pytest.raises(ValueError, match="duplicidade"):
        criar_comando(referencias_de_entrada=[referencia, referencia])
    with pytest.raises(ValueError, match="duplicados"):
        criar_comando(parametros_locais=[parametro, parametro])
    with pytest.raises(FrozenInstanceError):
        comando.modo_execucao = "x"


def test_todas_as_colecoes_dos_contratos_sao_tuplas() -> None:
    referencia = ReferenciaVersionada("a", "1")
    explicacao = ExplicacaoExecucao("ok", ["a"], ["b"], ["c"], ["d"], [referencia], ["e"])
    dependencia = DependenciaExecucao(TipoDependencia.TECNICA, ["a"], ["b"], ["c"], ["d"], ["e"])
    rastreabilidade = RastreabilidadeExecucao(
        [referencia],
        ["a"],
        [referencia],
        [referencia],
        ["b"],
    )
    saida = criar_saida(
        explicacao=explicacao,
        rastreabilidade=rastreabilidade,
        dependencias=[dependencia],
        resultados_secundarios=[{"preservado": True}],
        validacoes=[],
        alertas=[],
        restricoes=["r"],
    )

    for campo in explicacao.__dataclass_fields__:
        if campo != "conclusao_pratica":
            assert isinstance(getattr(explicacao, campo), tuple)
    for campo in dependencia.__dataclass_fields__:
        if campo != "tipo":
            assert isinstance(getattr(dependencia, campo), tuple)
    for campo in rastreabilidade.__dataclass_fields__:
        assert isinstance(getattr(rastreabilidade, campo), tuple)
    for campo in ("resultados_secundarios", "validacoes", "alertas", "restricoes", "dependencias"):
        assert isinstance(getattr(saida, campo), tuple)
    assert saida.resultados_secundarios[0] == {"preservado": True}


def test_saida_distingue_nao_executavel_de_falha_tecnica() -> None:
    nao_executavel = criar_saida(
        estado_execucao=EstadoExecucao.NAO_EXECUTAVEL,
        resultado_principal=None,
    )
    falha_tecnica = criar_saida(
        estado_execucao=EstadoExecucao.FALHA_TECNICA,
        resultado_principal=None,
    )
    assert nao_executavel.estado_execucao is EstadoExecucao.NAO_EXECUTAVEL
    assert falha_tecnica.estado_execucao is EstadoExecucao.FALHA_TECNICA
    with pytest.raises(ValueError, match="não admite"):
        criar_saida(
            estado_execucao=EstadoExecucao.NAO_EXECUTAVEL,
            resultado_principal="fictício",
        )
    with pytest.raises(ValueError, match="fuso horário"):
        criar_saida(produzido_em=datetime.now())
