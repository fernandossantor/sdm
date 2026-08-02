from __future__ import annotations

import argparse
import json
from datetime import date
from decimal import Decimal
from pathlib import Path
from runpy import run_path
from typing import Any, Sequence

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
from src.domain.objetivos import (
    ObjetivoComunicacaoCandidato,
    ObjetivoMarketing,
    Prioridade,
)
from src.engines.traducao_estrategica.engine import (
    ComandoTraducao,
    ModoTraducao,
    MotorTraducaoEstrategica,
    ResultadoExecucaoTraducao,
)
from src.engines.traducao_estrategica.mensurabilidade import ObjetivoDeclarado


RAIZ_REPOSITORIO = Path(__file__).parents[2]
CAMINHO_FIXTURE_CANONICA = RAIZ_REPOSITORIO / "tests/fixtures/campanha_canonica.py"
SAIDA_PADRAO = RAIZ_REPOSITORIO / "artifacts/traducao_canonica.json"


def _ausente() -> ValorComOrigem[Any]:
    return ValorComOrigem(None, NaturezaValor.NAO_DISPONIVEL)


def _carregar_dados_canonicos() -> dict[str, Any]:
    namespace = run_path(str(CAMINHO_FIXTURE_CANONICA))
    return namespace["CAMPANHA_CANONICA"]


def _criar_briefing(dados: dict[str, Any]) -> Briefing:
    identificacao = dados["identificacao"]
    publico = dados["publico_prioritario"]
    segmento = dados["segmento_secundario"]
    praca = dados["praca"]
    periodo = dados["periodo"]
    verba = dados["verba"]
    restricao = dados["restricao"]
    tensao = dados["tensao_estrategica"]
    return Briefing(
        campanha=Campanha(IdentificacaoCampanha(**identificacao)),
        situacao_marca_mercado=dados["situacao_marca_mercado"]["resumo"],
        objetivos_marketing=tuple(
            ObjetivoMarketing(
                categoria=item["categoria"],
                ordem_declarada=item["ordem_declarada"],
                prioridade=Prioridade(item["prioridade"]),
            )
            for item in dados["objetivos_marketing"]
        ),
        objetivos_comunicacao_candidatos=tuple(
            ObjetivoComunicacaoCandidato(item)
            for item in dados["objetivos_comunicacao_candidatos"]
        ),
        publico_prioritario=Publico(
            nome=publico["nome"],
            descricao=publico["descricao"],
            praca=publico["praca"],
            prioridade=Prioridade(publico["prioridade"]),
            tamanho_estimado=_ausente(),
        ),
        segmento_secundario=Segmento(
            nome=segmento["nome"],
            descricao=segmento["descricao"],
            praca=segmento["praca"],
            prioridade=Prioridade(segmento["prioridade"]),
            tamanho_estimado=_ausente(),
        ),
        praca=Praca(
            nome=praca["nome"],
            tipo_territorial=praca["tipo_territorial"],
            universo_populacional=_ausente(),
        ),
        periodo=Periodo(
            date.fromisoformat(periodo["data_inicial"]),
            date.fromisoformat(periodo["data_final"]),
        ),
        verba=Verba(
            valor_total=ValorComOrigem(
                Decimal(str(verba["valor_total"])), NaturezaValor.INFORMADO
            ),
            moeda=verba["moeda"],
            natureza_do_limite=NaturezaLimiteVerba(verba["natureza_do_limite"]),
            margem_de_flexibilidade=_ausente(),
        ),
        prioridade=Prioridade(dados["prioridade"]["nivel"]),
        restricao=Restricao(
            categoria=restricao["categoria"],
            descricao=restricao["descricao"],
            entidade_afetada=restricao["entidade_afetada"],
            intensidade=Prioridade(restricao["intensidade"]),
            prioridade=Prioridade(restricao["prioridade"]),
            origem=restricao["origem"],
            justificativa=restricao["justificativa"],
        ),
        tensao_estrategica=TensaoEstrategica(
            descricao=tensao["descricao"],
            elementos=tuple(tensao["elementos"]),
        ),
        indicadores_disponiveis=tuple(
            IndicadorDisponivel(
                metrica=item["metrica"],
                valor=ValorComOrigem(
                    Decimal(str(item["valor"])), NaturezaValor.INFORMADO
                ),
                unidade_de_mensuracao=item["unidade_de_mensuracao"],
                publico_ou_target=item["publico_ou_target"],
                territorio=item["territorio"],
                periodo_de_referencia=item["periodo_de_referencia"],
                fonte=item["fonte"],
                metodologia=item["metodologia"],
                nivel_de_confianca=item["nivel_de_confianca"],
            )
            for item in dados["indicadores_disponiveis"]
        ),
        dados_ausentes=tuple(DadoPendente(nome) for nome in dados["dados_ausentes"]),
    )


def _criar_objetivos_mensuraveis(briefing: Briefing) -> tuple[ObjetivoDeclarado, ...]:
    return tuple(
        ObjetivoDeclarado(
            codigo=(
                "mkt_aumento_vendas"
                if objetivo.categoria == "aumento de vendas"
                else "mkt_crescimento"
            ),
            texto_original=objetivo.categoria,
            objeto_da_mudanca="vendas",
            publico=briefing.publico_prioritario.nome,
            praca=briefing.praca.nome,
            direcao="aumentar",
            indicador="vendas",
            unidade_ou_escala="quantidade",
            linha_de_base=None,
            meta_ou_intensidade=None,
            horizonte_temporal=(
                f"{briefing.periodo.data_inicial.isoformat()}/"
                f"{briefing.periodo.data_final.isoformat()}"
            ),
            fonte=None,
            confianca="INDETERMINADA",
            forma_mensuracao="METRICA_DIRETA",
        )
        for objetivo in briefing.objetivos_marketing
    )


def executar_caso_canonico() -> ResultadoExecucaoTraducao:
    briefing = _criar_briefing(_carregar_dados_canonicos())
    comando = ComandoTraducao(
        id_comando="cli-caso-canonico",
        modo=ModoTraducao.TRADUZIR_BRIEFING,
        briefing=briefing,
        objetivos_mensuraveis=_criar_objetivos_mensuraveis(briefing),
        jornada="NÃO_INFORMADA",
        pressao_competitiva=50,
        verba_disponivel_percentual_do_necessario=60,
        observacao_nao_decisoria=None,
    )
    return MotorTraducaoEstrategica().executar(comando)


def apresentar_resultado(resultado: ResultadoExecucaoTraducao) -> dict[str, Any]:
    contrato = resultado.resultado_principal
    comunicacao = [
        {
            "codigo": item.codigo,
            "condicao": item.condicao,
            "forca_contextual": item.forca_contextual,
            "ordem": item.ordem,
            "prioridade": item.prioridade,
        }
        for item in contrato.objetivos_comunicacao
    ]
    midia = [
        {
            "adequacao_contextual": item.adequacao_contextual,
            "codigo": item.codigo,
            "condicao": item.condicao,
            "indicadores_possiveis": list(item.indicadores_possiveis),
            "intensidade": item.intensidade,
            "nome": item.nome,
            "ordem": item.ordem,
            "peso": item.peso,
            "prioridade": item.prioridade,
        }
        for item in contrato.objetivos_midia
    ]
    return {
        "alertas": list(resultado.alertas),
        "confianca": resultado.confianca,
        "explicacao_resumida": list(resultado.explicacao),
        "objetivos_comunicacao": comunicacao,
        "objetivos_midia": midia,
        "pesos": [
            {"objetivo_midia": item["codigo"], "peso": item["peso"]}
            for item in midia
        ],
        "rastreabilidade": list(resultado.rastreabilidade),
        "restricoes": list(resultado.restricoes),
        "resultado_principal": {
            "campanha": contrato.identidade.id_campanha,
            "estado": contrato.identidade.estado.value,
            "versao": contrato.identidade.versao,
        },
    }


def serializar_resultado(resultado: ResultadoExecucaoTraducao) -> str:
    return json.dumps(
        apresentar_resultado(resultado),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Executa a Tradução Estratégica mínima.")
    parser.add_argument("--caso", choices=("canonico",), required=True)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    argumentos = parser.parse_args(argv)

    resultado = executar_caso_canonico()
    documento = serializar_resultado(resultado)
    argumentos.saida.parent.mkdir(parents=True, exist_ok=True)
    argumentos.saida.write_text(documento, encoding="utf-8")
    print(documento, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
