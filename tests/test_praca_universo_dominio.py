from dataclasses import FrozenInstanceError
from decimal import Decimal
from uuid import UUID

import pytest

from mediad_planner.domain.briefing.praca_universo import (
    EstruturaTerritorialPopulacional,
    PracaDeclarada,
    TipoPracaTerritorial,
    UniversoDeclarado,
    listar_tipos_praca_territorial,
    listar_unidades_populacionais,
)


ID_PRACA_1 = UUID(int=101)
ID_PRACA_2 = UUID(int=102)
ID_UNIVERSO = UUID(int=201)


def _praca(id_praca: UUID = ID_PRACA_1, **alteracoes: object) -> PracaDeclarada:
    dados = dict(
        id_praca=id_praca,
        tipo=TipoPracaTerritorial.MUNICIPIO,
        nome="  Município de teste  ",
        codigo_oficial=" 04318000 ",
        abrangencia="  Todo o município ",
        valor_populacao_referencia=Decimal("60000"),
        codigo_unidade_populacional="pessoas",
        unidade_populacional=" Pessoas ",
        fonte="  IBGE ",
        data_referencia=" 2025 ",
        observacao="  Estimativa ",
    )
    dados.update(alteracoes)
    return PracaDeclarada(**dados)


def _universo(**alteracoes: object) -> UniversoDeclarado:
    dados = dict(
        id_universo=ID_UNIVERSO,
        nome=" Adultos ",
        definicao=" Pessoas com 18 anos ou mais ",
        ids_pracas=(ID_PRACA_1,),
        valor_populacional=Decimal("45000"),
        codigo_unidade="pessoas",
        unidade=" Pessoas ",
        fonte=None,
        data_referencia=None,
        criterios_inclusao=" Residentes ",
        criterios_exclusao=" Menores de 18 anos ",
        observacao=" ",
    )
    dados.update(alteracoes)
    return UniversoDeclarado(**dados)


def test_catalogos_possuem_codigos_unicos_e_estaveis() -> None:
    tipos = tuple(item.codigo.value for item in listar_tipos_praca_territorial())
    unidades = tuple(item.codigo for item in listar_unidades_populacionais())
    assert len(tipos) == len(set(tipos))
    assert tipos == tuple(item.value for item in TipoPracaTerritorial)
    assert unidades == (
        "pessoas",
        "domicilios",
        "familias",
        "empresas",
        "estabelecimentos",
        "pontos_de_venda",
    )


def test_praca_normaliza_textos_e_preserva_codigo_oficial() -> None:
    praca = _praca()
    assert praca.nome == "Município de teste"
    assert praca.codigo_oficial == "04318000"
    assert praca.fonte == "IBGE"
    assert praca.observacao == "Estimativa"


@pytest.mark.parametrize("nome", ("", "   "))
def test_praca_exige_nome(nome: str) -> None:
    with pytest.raises(ValueError, match="nome é obrigatório"):
        _praca(nome=nome)


def test_praca_exige_uuid_e_tipo_valido() -> None:
    with pytest.raises(TypeError, match="id_praca"):
        _praca(id_praca="invalido")
    with pytest.raises(TypeError, match="tipo inválido"):
        _praca(tipo="MUNICIPIO")


@pytest.mark.parametrize("valor", (Decimal("0"), Decimal("-1")))
def test_populacao_da_praca_deve_ser_positiva(valor: Decimal) -> None:
    with pytest.raises(ValueError, match="positivo"):
        _praca(valor_populacao_referencia=valor)


def test_populacao_da_praca_exige_unidade_e_unidade_exige_valor() -> None:
    with pytest.raises(ValueError, match="obrigatória"):
        _praca(
            codigo_unidade_populacional=None,
            unidade_populacional=None,
        )
    with pytest.raises(ValueError, match="exige valor"):
        _praca(valor_populacao_referencia=None)
    sem_populacao = _praca(
        valor_populacao_referencia=None,
        codigo_unidade_populacional=None,
        unidade_populacional=None,
    )
    assert sem_populacao.valor_populacao_referencia is None


@pytest.mark.parametrize("campo", ("nome", "definicao", "unidade"))
def test_universo_exige_textos_obrigatorios(campo: str) -> None:
    with pytest.raises(ValueError, match="obrigatório|obrigatória"):
        _universo(**{campo: " "})


def test_universo_exige_praca_sem_repeticao_e_preserva_ordem() -> None:
    with pytest.raises(ValueError, match="ao menos uma Praça"):
        _universo(ids_pracas=())
    with pytest.raises(ValueError, match="duplicatas"):
        _universo(ids_pracas=(ID_PRACA_1, ID_PRACA_1))
    universo = _universo(ids_pracas=(ID_PRACA_2, ID_PRACA_1))
    assert universo.ids_pracas == (ID_PRACA_2, ID_PRACA_1)


@pytest.mark.parametrize("valor", (Decimal("0"), Decimal("-0.1")))
def test_populacao_do_universo_deve_ser_positiva(valor: Decimal) -> None:
    with pytest.raises(ValueError, match="positivo"):
        _universo(valor_populacional=valor)


def test_estrutura_valida_relacoes_e_e_imutavel() -> None:
    praca = _praca()
    universo = _universo()
    estrutura = EstruturaTerritorialPopulacional((praca,), (universo,))
    assert estrutura.pracas == (praca,)
    with pytest.raises(FrozenInstanceError):
        estrutura.pracas = ()
    with pytest.raises(ValueError, match="Praça relacionada não existe"):
        EstruturaTerritorialPopulacional((), (universo,))


def test_operacoes_preservam_ordem_e_protegem_vinculo() -> None:
    primeira = _praca()
    segunda = _praca(ID_PRACA_2, nome="Centro", codigo_oficial=None)
    estrutura = EstruturaTerritorialPopulacional((), ())
    estrutura = estrutura.adicionar_praca(primeira).adicionar_praca(segunda)
    estrutura = estrutura.adicionar_universo(_universo())
    assert estrutura.pracas == (primeira, segunda)
    with pytest.raises(ValueError, match="Praça vinculada a Universo"):
        estrutura.remover_praca(ID_PRACA_1)
    sem_universo = estrutura.remover_universo(ID_UNIVERSO)
    assert sem_universo.pracas == (primeira, segunda)
    assert sem_universo.remover_praca(ID_PRACA_1).pracas == (segunda,)


def test_remocoes_inexistentes_possuem_mensagens_controladas() -> None:
    estrutura = EstruturaTerritorialPopulacional((_praca(),), ())
    with pytest.raises(LookupError, match="Praça não encontrada"):
        estrutura.remover_praca(UUID(int=999))
    with pytest.raises(LookupError, match="Universo não encontrado"):
        estrutura.remover_universo(UUID(int=999))


def test_tipos_de_regioes_geograficas_sao_explicitos_e_regiao_permanece() -> None:
    codigos = {item.value for item in TipoPracaTerritorial}
    assert "REGIAO" in codigos
    assert "REGIAO_GEOGRAFICA_INTERMEDIARIA" in codigos
    assert "REGIAO_GEOGRAFICA_IMEDIATA" in codigos
    definicoes = {
        item.codigo: item for item in listar_tipos_praca_territorial()
    }
    assert definicoes[
        TipoPracaTerritorial.REGIAO_GEOGRAFICA_INTERMEDIARIA
    ].rotulo == "Região Geográfica Intermediária"
    assert definicoes[
        TipoPracaTerritorial.REGIAO_GEOGRAFICA_IMEDIATA
    ].rotulo == "Região Geográfica Imediata"


def test_pracas_regionais_preservam_codigos_textuais() -> None:
    from uuid import uuid4

    comuns = {
        "codigo_unidade_populacional": None,
        "unidade_populacional": None,
        "valor_populacao_referencia": None,
        "abrangencia": None,
        "fonte": None,
        "data_referencia": None,
        "observacao": None,
    }
    intermediaria = PracaDeclarada(
        id_praca=uuid4(),
        tipo=TipoPracaTerritorial.REGIAO_GEOGRAFICA_INTERMEDIARIA,
        nome="Uruguaiana",
        codigo_oficial="4304",
        **comuns,
    )
    imediata = PracaDeclarada(
        id_praca=uuid4(),
        tipo=TipoPracaTerritorial.REGIAO_GEOGRAFICA_IMEDIATA,
        nome="São Borja",
        codigo_oficial="430017",
        **comuns,
    )
    assert intermediaria.codigo_oficial == "4304"
    assert imediata.codigo_oficial == "430017"
