"""Núcleo verificável das Bibliotecas 15, 17 e 18 para tradução inicial."""

from domain.bibliotecas import (
    ConhecimentoTecnico, IndicadorPlanejamento, ObjetoBiblioteca,
    ObjetivoMidiaBiblioteca, ProblemaTecnico, RegraComunicacaoMidia,
)
from .configuracao_pontuacao import CONFIGURACAO_PONTUACAO

VERSAO_NUCLEO = "2026.08.02.4"

RELACOES_MARKETING_COMUNICACAO = {
    "crescimento": {"notoriedade", "preferência", "consideração", "relacionamento"},
    "participação de mercado": {"diferenciação percebida", "preferência", "consideração", "lembrança"},
    "penetração": {"conhecimento", "experimentação", "consideração"},
    "fidelização": {"relacionamento", "fidelização", "recomendação"},
    "diferenciação": {"diferenciação percebida", "preferência", "imagem"},
    "posicionamento": {"imagem", "compreensão", "diferenciação percebida"},
    "branding": {"notoriedade", "conhecimento", "lembrança", "imagem"},
    "segmentação": {"consideração", "engajamento", "ação"},
    "desenvolvimento de produto": {"conhecimento", "compreensão", "experimentação"},
    "diversificação": {"notoriedade", "conhecimento", "consideração"},
}

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

OBJETIVOS_MIDIA = tuple(
    ObjetivoMidiaBiblioteca(
        codigo=codigo, biblioteca=15, versao=VERSAO_NUCLEO,
        nome=nome, indicador_codigo=indicador,
    )
    for codigo, nome, indicador in (
        ("B15-OM-CONSTRUIR-ALCANCE", "construir alcance", "B15-ALCANCE"),
        ("B15-OM-AMPLIAR-COBERTURA", "ampliar cobertura", "B15-COBERTURA"),
        ("B15-OM-ACELERAR-ALCANCE", "acelerar construção de alcance", "B15-ALCANCE"),
        ("B15-OM-GERAR-FREQUENCIA", "gerar frequência", "B15-FREQUENCIA"),
        ("B15-OM-SUSTENTAR-CONTINUIDADE", "sustentar continuidade", "B15-CONTINUIDADE"),
        ("B15-OM-PRODUZIR-IMPACTO", "produzir impacto", "B15-IMPACTO"),
        ("B15-OM-ALCANCAR-PRIORITARIOS", "alcançar públicos prioritários", "B15-ALCANCE"),
        ("B15-OM-AUMENTAR-AFINIDADE", "aumentar afinidade", "B15-ALCANCE"),
        ("B15-OM-GERAR-TRAFEGO", "gerar tráfego", "B15-RESPOSTA"),
        ("B15-OM-FAVORECER-RESPOSTA", "favorecer resposta", "B15-RESPOSTA"),
        ("B15-OM-FAVORECER-CONVERSAO", "favorecer conversão", "B15-CONVERSAO"),
        ("B15-OM-AMPLIAR-PRESENCA-TERRITORIAL", "ampliar presença territorial", "B15-COBERTURA"),
        ("B15-OM-ACOMPANHAR-JORNADA", "acompanhar etapas da jornada", "B15-CONTINUIDADE"),
    )
)

CONTEXTO = (
    ObjetoBiblioteca(codigo="B14-RESOLVER-PUBLICO-SEGMENTO", biblioteca=14,
        versao=VERSAO_NUCLEO),
    ObjetoBiblioteca(codigo="B16-RESOLVER-JORNADA-ETAPA", biblioteca=16,
        versao=VERSAO_NUCLEO),
)

CONHECIMENTOS = (
    ConhecimentoTecnico(codigo="B17-DERIVAR-COM-MIDIA", biblioteca=17,
        versao=VERSAO_NUCLEO, nome="Derivação Comunicação–Mídia",
        tipo="REGRA_CONDICIONAL",
        pre_condicoes=("objetivo de comunicação declarado",),
        limitacoes=("não seleciona meio", "não define meta ausente")),
    ConhecimentoTecnico(codigo="B17-COMPOSICAO-CONTEXTUAL-TRADUCAO",
        biblioteca=17, versao=CONFIGURACAO_PONTUACAO["versao"],
        nome="Composição contextual inicial da tradução",
        tipo="PROCEDIMENTO_DE_DECISAO",
        pre_condicoes=("relação estratégica candidata",),
        limitacoes=("não representa fórmula científica", "não define intensidade quantitativa sem dados")),
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
        ("notoriedade", ("construir alcance", "ampliar cobertura", "acelerar construção de alcance", "produzir impacto"),
         ("B15-ALCANCE", "B15-COBERTURA", "B15-ALCANCE", "B15-IMPACTO")),
        ("conhecimento", ("construir alcance", "gerar frequência", "sustentar continuidade"),
         ("B15-ALCANCE", "B15-FREQUENCIA", "B15-CONTINUIDADE")),
        ("lembrança", ("gerar frequência", "sustentar continuidade"),
         ("B15-FREQUENCIA", "B15-CONTINUIDADE")),
        ("compreensão", ("gerar frequência",), ("B15-FREQUENCIA",)),
        ("diferenciação percebida", ("produzir impacto", "aumentar afinidade"),
         ("B15-IMPACTO", "B15-ALCANCE")),
        ("consideração", ("alcançar públicos prioritários", "acompanhar etapas da jornada", "aumentar afinidade"),
         ("B15-ALCANCE", "B15-CONTINUIDADE", "B15-ALCANCE")),
        ("engajamento", ("favorecer resposta", "aumentar afinidade", "sustentar continuidade"),
         ("B15-RESPOSTA", "B15-ALCANCE", "B15-CONTINUIDADE")),
        ("experimentação", ("favorecer resposta", "ampliar presença territorial"),
         ("B15-RESPOSTA", "B15-COBERTURA")),
        ("relacionamento", ("sustentar continuidade", "gerar frequência"),
         ("B15-CONTINUIDADE", "B15-FREQUENCIA")),
        ("recomendação", ("favorecer resposta",), ("B15-RESPOSTA",)),
        ("ação", ("favorecer resposta", "gerar tráfego", "favorecer conversão"),
         ("B15-RESPOSTA", "B15-RESPOSTA", "B15-CONVERSAO")),
        ("fidelização", ("gerar frequência", "sustentar continuidade", "aumentar afinidade"),
         ("B15-FREQUENCIA", "B15-CONTINUIDADE", "B15-ALCANCE")),
    )
)


class CatalogoTraducaoInicial:
    versao = VERSAO_NUCLEO
    configuracao_pontuacao = CONFIGURACAO_PONTUACAO

    def regra_para(self, objetivo_comunicacao: str):
        return next((item for item in REGRAS
                     if item.objetivo_comunicacao == objetivo_comunicacao), None)

    def comunicacao_para_marketing(self, objetivo_marketing: str):
        return RELACOES_MARKETING_COMUNICACAO.get(
            objetivo_marketing.casefold(), set()
        )

    def indicador(self, codigo: str):
        return next((item for item in INDICADORES if item.codigo == codigo), None)

    def objeto(self, codigo: str):
        return next((item for item in self.referencias()
                     if item.codigo == codigo), None)

    def referencias(self):
        return (
            *CONTEXTO, *INDICADORES, *OBJETIVOS_MIDIA,
            *CONHECIMENTOS, *PROBLEMAS, *REGRAS,
        )

    def referencias_contexto(self, briefing):
        referencias = []
        if briefing.conteudo.publicos or briefing.conteudo.segmentos:
            referencias.append(CONTEXTO[0])
        if (briefing.conteudo.jornadas
                or briefing.conteudo.jornada_aplicavel is False):
            referencias.append(CONTEXTO[1])
        return tuple(referencias)

    def objetivos_midia(self):
        return OBJETIVOS_MIDIA

    def objetivo_midia(self, nome: str):
        return next((item for item in OBJETIVOS_MIDIA if item.nome == nome), None)
