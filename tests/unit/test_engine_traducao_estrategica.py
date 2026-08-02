from dataclasses import replace
from datetime import date
from decimal import Decimal

from src.domain.briefing import (
    Briefing,
    DadoPendente,
    IndicadorDisponivel,
    Publico,
    Restricao,
    Segmento,
    TensaoEstrategica,
)
from src.domain.campanha import (
    Campanha,
    IdentificacaoCampanha,
    NaturezaLimiteVerba,
    Periodo,
    Praca,
    Verba,
)
from src.domain.common import NaturezaValor, ValorComOrigem
from src.domain.contrato_estrategico import EstadoContratoEstrategico
from src.domain.objetivos import (
    ObjetivoComunicacaoCandidato,
    ObjetivoMarketing,
    Prioridade,
)
from src.engines.traducao_estrategica.engine import (
    ComandoTraducao,
    ModoTraducao,
    MotorTraducaoEstrategica,
)
from src.engines.traducao_estrategica.mensurabilidade import ObjetivoDeclarado


def _ausente():
    return ValorComOrigem(None, NaturezaValor.NAO_DISPONIVEL)


def _indicador(nome, valor):
    return IndicadorDisponivel(
        nome,
        ValorComOrigem(Decimal(str(valor)), NaturezaValor.INFORMADO),
        "percentual",
        "Responsáveis pela decisão de energia residencial",
        "Campinas (SP)",
        "2026-06",
        "fonte fictícia declarada",
        "método fictício declarado",
        "MEDIA",
    )


def _briefing():
    return Briefing(
        campanha=Campanha(
            IdentificacaoCampanha(
                "campanha-canonica-lume-2026",
                "Lume Casa — Primavera 2026",
                "Lume Casa",
                "assinatura de energia solar residencial",
            )
        ),
        situacao_marca_mercado=(
            "Notoriedade alta, baixa conclusão e receio sobre economia e retorno."
        ),
        objetivos_marketing=(
            ObjetivoMarketing("aumento de vendas", 1, Prioridade.MUITO_ALTA),
            ObjetivoMarketing("crescimento", 2, Prioridade.ALTA),
        ),
        objetivos_comunicacao_candidatos=(
            ObjetivoComunicacaoCandidato("intenção"),
            ObjetivoComunicacaoCandidato("redução de incerteza"),
            ObjetivoComunicacaoCandidato("notoriedade"),
        ),
        publico_prioritario=Publico(
            "Responsáveis pela decisão de energia residencial",
            "Pessoas de 30 a 55 anos que pesquisaram redução da conta.",
            "Campinas (SP)",
            Prioridade.MUITO_ALTA,
            _ausente(),
        ),
        segmento_secundario=Segmento(
            "Interessados sem pesquisa recente",
            "Interessados em sustentabilidade sem pesquisa recente.",
            "Campinas (SP)",
            Prioridade.MEDIA,
            _ausente(),
        ),
        praca=Praca("Campinas (SP)", "município", _ausente()),
        periodo=Periodo(date(2026, 9, 1), date(2026, 10, 31)),
        verba=Verba(
            ValorComOrigem(Decimal("300000"), NaturezaValor.INFORMADO),
            "BRL",
            NaturezaLimiteVerba.RIGIDO,
            _ausente(),
        ),
        prioridade=Prioridade.MUITO_ALTA,
        restricao=Restricao(
            "orçamentária",
            "A verba total não pode ultrapassar BRL 300.000.",
            "campanha",
            Prioridade.MUITO_ALTA,
            Prioridade.MUITO_ALTA,
            "anunciante",
            "Teto financeiro aprovado.",
        ),
        tensao_estrategica=TensaoEstrategica(
            "Aumento de vendas e crescimento disputam a verba rígida.",
            ("aumento de vendas", "crescimento", "verba rígida"),
        ),
        indicadores_disponiveis=(
            _indicador("notoriedade auxiliada", 78),
            _indicador("taxa de conclusão do pedido de proposta", 1.1),
        ),
        dados_ausentes=(
            DadoPendente("meta_de_vendas"),
            DadoPendente("linha_de_base_de_vendas"),
        ),
    )


def _objetivos_mensuraveis(*, linha_de_base=None):
    comuns = {
        "objeto_da_mudanca": "vendas",
        "publico": "Responsáveis pela decisão de energia residencial",
        "praca": "Campinas (SP)",
        "direcao": "aumentar",
        "indicador": "vendas",
        "unidade_ou_escala": "quantidade",
        "linha_de_base": linha_de_base,
        "meta_ou_intensidade": 150,
        "horizonte_temporal": "2026-09-01/2026-10-31",
        "fonte": "sistema comercial declarado",
        "confianca": "ALTA",
        "forma_mensuracao": "METRICA_DIRETA",
    }
    return (
        ObjetivoDeclarado(
            codigo="mkt_aumento_vendas",
            texto_original="Aumentar vendas.",
            **comuns,
        ),
        ObjetivoDeclarado(
            codigo="mkt_crescimento",
            texto_original="Crescer.",
            **comuns,
        ),
    )


def _comando(**alteracoes):
    dados = {
        "id_comando": "cmd-canonico-1",
        "modo": ModoTraducao.TRADUZIR_BRIEFING,
        "briefing": _briefing(),
        "objetivos_mensuraveis": _objetivos_mensuraveis(),
        "jornada": "consideração para intenção",
        "pressao_competitiva": 35,
        "verba_disponivel_percentual_do_necessario": 60,
        "observacao_nao_decisoria": None,
    }
    dados.update(alteracoes)
    return ComandoTraducao(**dados)


def test_executa_caso_canonico_completo():
    resultado = MotorTraducaoEstrategica().executar(_comando())
    contrato = resultado.resultado_principal

    assert resultado.motor == "TRADUCAO_ESTRATEGICA"
    assert resultado.modo_execucao == "TRADUZIR_BRIEFING"
    assert contrato.identidade.estado is EstadoContratoEstrategico.PROVISORIO
    assert tuple(item.codigo for item in contrato.objetivos_comunicacao) == (
        "com_intencao",
        "com_reducao_incerteza",
        "com_notoriedade",
    )
    assert contrato.objetivos_midia
    assert contrato.tensoes == (
        "Aumento de vendas e crescimento disputam a verba rígida.",
    )
    assert any(item.startswith("relacao:") for item in resultado.rastreabilidade)
    assert "briefing" in resultado.dependencias


def test_aumentar_prioridade_altera_contribuicao_do_objetivo():
    motor = MotorTraducaoEstrategica()
    briefing_baixo = replace(
        _briefing(),
        objetivos_marketing=(
            ObjetivoMarketing("aumento de vendas", 1, Prioridade.BAIXA),
            ObjetivoMarketing("crescimento", 2, Prioridade.ALTA),
        ),
    )
    briefing_alto = replace(
        briefing_baixo,
        objetivos_marketing=(
            ObjetivoMarketing("aumento de vendas", 1, Prioridade.MUITO_ALTA),
            briefing_baixo.objetivos_marketing[1],
        ),
    )
    baixo = motor.executar(_comando(briefing=briefing_baixo))
    alto = motor.executar(_comando(briefing=briefing_alto))

    def contribuicao(resultado):
        intencao = next(
            item
            for item in resultado.resultado_principal.objetivos_comunicacao
            if item.codigo == "com_intencao"
        )
        return dict(intencao.contribuicoes_por_objetivo_marketing)[
            "mkt_aumento_vendas"
        ]

    assert contribuicao(alto) > contribuicao(baixo)


def test_remover_linha_de_base_reduz_confianca():
    motor = MotorTraducaoEstrategica()
    completo = motor.executar(
        _comando(objetivos_mensuraveis=_objetivos_mensuraveis(linha_de_base=0))
    )
    pendente = motor.executar(
        _comando(objetivos_mensuraveis=_objetivos_mensuraveis(linha_de_base=None))
    )

    assert pendente.confianca < completo.confianca


def test_mudar_notoriedade_altera_ordem_da_comunicacao():
    motor = MotorTraducaoEstrategica()
    alta = motor.executar(_comando())
    briefing_baixa = replace(
        _briefing(),
        indicadores_disponiveis=(
            _indicador("notoriedade auxiliada", 30),
            _indicador("taxa de conclusão do pedido de proposta", 1.1),
        ),
    )
    baixa = motor.executar(_comando(briefing=briefing_baixa))

    ordem_alta = tuple(
        item.codigo for item in alta.resultado_principal.objetivos_comunicacao
    )
    ordem_baixa = tuple(
        item.codigo for item in baixa.resultado_principal.objetivos_comunicacao
    )
    assert ordem_baixa != ordem_alta
    assert ordem_baixa[0] == "com_notoriedade"


def test_reduzir_verba_produz_ressalva_sem_declarar_viabilidade():
    resultado = MotorTraducaoEstrategica().executar(
        _comando(verba_disponivel_percentual_do_necessario=15)
    )

    assert resultado.estado_execucao == "CONCLUIDA_COM_RESSALVAS"
    assert "verba muito restrita; viabilidade não determinada" in resultado.alertas
    assert any(
        item.condicao == "COMPENSAVEL"
        for item in resultado.resultado_principal.objetivos_midia
    )


def test_observacao_nao_decisoria_nao_altera_pontuacao():
    motor = MotorTraducaoEstrategica()
    sem_observacao = motor.executar(_comando(observacao_nao_decisoria=None))
    com_observacao = motor.executar(
        _comando(observacao_nao_decisoria="Texto editorial sem efeito decisório.")
    )

    def pontuacoes(resultado):
        contrato = resultado.resultado_principal
        return (
            tuple(item.forca_contextual for item in contrato.objetivos_comunicacao),
            tuple(item.adequacao_contextual for item in contrato.objetivos_midia),
        )

    assert pontuacoes(com_observacao) == pontuacoes(sem_observacao)
