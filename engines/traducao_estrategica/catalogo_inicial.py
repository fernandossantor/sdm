"""Núcleo verificável das Bibliotecas 15, 17 e 18 para tradução inicial."""

from domain.bibliotecas import (
    ConhecimentoTecnico, IndicadorPlanejamento, ProblemaTecnico,
    RegraComunicacaoMidia,
)

VERSAO_NUCLEO = "2026.08.02.1"

INDICADORES = (
    IndicadorPlanejamento(codigo="B15-ALCANCE", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="alcance do público-alvo",
        familia="PLANEJAMENTO_E_PRESSAO", unidade="percentual"),
    IndicadorPlanejamento(codigo="B15-COBERTURA", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="cobertura geográfica ou populacional",
        familia="PLANEJAMENTO_E_PRESSAO", unidade="percentual"),
    IndicadorPlanejamento(codigo="B15-FREQUENCIA", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="frequência média",
        familia="PLANEJAMENTO_E_PRESSAO", unidade="contatos médios"),
    IndicadorPlanejamento(codigo="B15-CONTINUIDADE", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="continuidade",
        familia="PLANEJAMENTO_E_PRESSAO", unidade="períodos ativos"),
    IndicadorPlanejamento(codigo="B15-RESPOSTA", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="respostas ou taxa de resposta",
        familia="RESPOSTA", unidade="contagem ou percentual"),
    IndicadorPlanejamento(codigo="B15-CONVERSAO", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="conversões e taxa de conversão",
        familia="RESPOSTA", unidade="contagem ou percentual"),
    IndicadorPlanejamento(codigo="B15-IMPACTO", biblioteca=15,
        versao=VERSAO_NUCLEO, nome="proxy de visibilidade ou atenção",
        familia="ENTREGA", unidade="índice ou contagem"),
)

CONHECIMENTOS = (
    ConhecimentoTecnico(codigo="B17-DERIVAR-COM-MIDIA", biblioteca=17,
        versao=VERSAO_NUCLEO, nome="Derivação Comunicação–Mídia",
        tipo="REGRA_CONDICIONAL",
        pre_condicoes=("objetivo de comunicação declarado",),
        limitacoes=("não seleciona meio", "não define meta ausente")),
)

PROBLEMAS = (
    ProblemaTecnico(codigo="B18-DERIVAR-OBJETIVO-MIDIA", biblioteca=18,
        versao=VERSAO_NUCLEO, nome="Derivar objetivo de mídia",
        pergunta_orientadora=(
            "Quais condições de mídia favorecem o objetivo de comunicação?"
        ), objetivo_decisorio="produzir objetivos rastreáveis para arquitetura",
        conhecimentos_aplicaveis=("B17-DERIVAR-COM-MIDIA",),
        criterios_conclusao=(
            "cada derivação possui origem, regra, indicador e versão",
        )),
)

REGRAS = tuple(
    RegraComunicacaoMidia(
        codigo=f"B15-CM-{origem.upper()}", biblioteca=15,
        versao=VERSAO_NUCLEO, objetivo_comunicacao=origem,
        objetivos_midia=objetivos, indicadores=indicadores,
        conhecimento_aplicado="B17-DERIVAR-COM-MIDIA",
        problema_atendido="B18-DERIVAR-OBJETIVO-MIDIA",
    )
    for origem, objetivos, indicadores in (
        ("notoriedade", ("construir alcance", "produzir impacto"),
         ("B15-ALCANCE", "B15-IMPACTO")),
        ("conhecimento", ("construir alcance", "ampliar cobertura"),
         ("B15-ALCANCE", "B15-COBERTURA")),
        ("lembrança", ("gerar frequência", "sustentar continuidade"),
         ("B15-FREQUENCIA", "B15-CONTINUIDADE")),
        ("consideração", ("gerar frequência", "ampliar cobertura"),
         ("B15-FREQUENCIA", "B15-COBERTURA")),
        ("engajamento", ("gerar tráfego ou resposta",), ("B15-RESPOSTA",)),
        ("experimentação", ("apoiar conversão mensurável",),
         ("B15-CONVERSAO",)),
        ("ação", ("gerar tráfego ou resposta", "apoiar conversão mensurável"),
         ("B15-RESPOSTA", "B15-CONVERSAO")),
    )
)


class CatalogoTraducaoInicial:
    versao = VERSAO_NUCLEO

    def regra_para(self, objetivo_comunicacao: str):
        return next((item for item in REGRAS
                     if item.objetivo_comunicacao == objetivo_comunicacao), None)

    def indicador(self, codigo: str):
        return next((item for item in INDICADORES if item.codigo == codigo), None)

    def objeto(self, codigo: str):
        return next((item for item in self.referencias()
                     if item.codigo == codigo), None)

    def referencias(self):
        return (*INDICADORES, *CONHECIMENTOS, *PROBLEMAS, *REGRAS)
