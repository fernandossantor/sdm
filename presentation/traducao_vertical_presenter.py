"""Presenter puro do contrato estratégico."""

from dataclasses import dataclass

from src.engines.traducao_estrategica.engine import ResultadoExecucaoTraducao


NOMES_COMUNICACAO = {"com_intencao": "Intenção de resposta", "com_reducao_incerteza": "Redução de incerteza", "com_notoriedade": "Notoriedade"}
NOMES_INTERNOS = {**NOMES_COMUNICACAO, "mkt_aumento_vendas": "Aumento de vendas", "mkt_crescimento": "Crescimento", "mid_favorecer_resposta": "Favorecer resposta", "mid_gerar_trafego": "Gerar tráfego", "mid_alcancar_publico_prioritario": "Alcançar públicos prioritários", "mid_construir_alcance": "Construir alcance"}

def _humanizar(texto: str) -> str:
    for codigo, nome in NOMES_INTERNOS.items():
        texto = texto.replace(codigo, nome)
    return texto


@dataclass(frozen=True, slots=True)
class ContratoApresentado:
    campanha: str
    estado: str
    confianca: str
    comunicacao: tuple[dict[str, object], ...]
    midia: tuple[dict[str, object], ...]
    restricoes: tuple[str, ...]
    tensoes: tuple[str, ...]
    explicacoes: tuple[str, ...]
    alertas: tuple[str, ...]


def apresentar_contrato(resultado: ResultadoExecucaoTraducao) -> ContratoApresentado:
    contrato = resultado.resultado_principal
    return ContratoApresentado(
        campanha=contrato.identidade.id_campanha,
        estado=contrato.identidade.estado.value.title(),
        confianca=f"{resultado.confianca:.1f}%",
        comunicacao=tuple({"Ordem": item.ordem, "Objetivo de comunicação": NOMES_COMUNICACAO[item.codigo], "Prioridade": item.prioridade.title(), "Força contextual": round(item.forca_contextual, 1), "Condição": item.condicao} for item in contrato.objetivos_comunicacao),
        midia=tuple({"Ordem": item.ordem, "Objetivo de mídia": item.nome, "Prioridade": item.prioridade.title(), "Intensidade": item.intensidade.title(), "Peso": round(item.peso, 3), "Condição": item.condicao, "Indicadores possíveis": ", ".join(item.indicadores_possiveis)} for item in contrato.objetivos_midia),
        restricoes=resultado.restricoes,
        tensoes=contrato.tensoes,
        explicacoes=tuple(_humanizar(item) for item in resultado.explicacao),
        alertas=tuple(_humanizar(item) for item in resultado.alertas),
    )


def comparar_contratos(anterior: ContratoApresentado, atual: ContratoApresentado) -> tuple[dict[str, str], ...]:
    def ordem(itens, chave):
        return " → ".join(str(item[chave]) for item in itens)
    linhas = (
        ("Objetivos de comunicação", ordem(anterior.comunicacao, "Objetivo de comunicação"), ordem(atual.comunicacao, "Objetivo de comunicação")),
        ("Objetivos de mídia", ordem(anterior.midia, "Objetivo de mídia"), ordem(atual.midia, "Objetivo de mídia")),
        ("Confiança", anterior.confianca, atual.confianca),
        ("Estado do contrato", anterior.estado, atual.estado),
        ("Alertas", " | ".join(anterior.alertas) or "Sem alertas", " | ".join(atual.alertas) or "Sem alertas"),
    )
    return tuple({"Dimensão": nome, "Versão anterior": antes, "Nova versão": depois, "Mudou": "Sim" if antes != depois else "Não"} for nome, antes, depois in linhas)
