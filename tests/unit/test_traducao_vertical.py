from datetime import date
from decimal import Decimal

from presentation.traducao_vertical_presenter import apresentar_contrato, comparar_contratos
from src.application.traducao_vertical import EntradaTraducaoVertical, ExecutarTraducaoVertical


def _entrada(**mudancas):
    dados = dict(id_comando="tela-v1", campanha_id="campanha-canonica", campanha_nome="Lume Casa", marca="Lume Casa", produto_ou_servico="energia solar", situacao_marca_mercado="Notoriedade alta e baixa conclusão.", objetivos_marketing=("aumento de vendas", "crescimento"), objetivos_comunicacao_candidatos=("intenção", "redução de incerteza", "notoriedade"), publico_prioritario="Responsáveis pela decisão de energia residencial", segmento_secundario="Interessados sem pesquisa recente", praca="Campinas (SP)", data_inicial=date(2026, 9, 1), data_final=date(2026, 10, 31), verba=Decimal("300000"), prioridade="muito alta", restricao="A verba não pode ultrapassar BRL 300.000.", tensao_estrategica="Vendas e crescimento disputam a verba.", notoriedade_auxiliada=Decimal("78"), taxa_conclusao_proposta=Decimal("1.1"), pressao_competitiva=35, verba_disponivel_percentual_do_necessario=60, jornada="consideração para intenção")
    dados.update(mudancas)
    return EntradaTraducaoVertical(**dados)


def test_caso_de_uso_chama_motor_sem_streamlit_ou_supabase():
    class MotorFake:
        comando = None
        def executar(self, comando):
            self.comando = comando
            return "resultado"
    motor = MotorFake()
    assert ExecutarTraducaoVertical(motor).executar(_entrada()) == "resultado"
    assert motor.comando.briefing.campanha.identificacao.nome == "Lume Casa"


def test_dado_ausente_nao_vira_zero():
    class MotorFake:
        def executar(self, comando): return comando
    comando = ExecutarTraducaoVertical(MotorFake()).executar(_entrada(notoriedade_auxiliada=None))
    assert all(item.metrica != "notoriedade auxiliada" for item in comando.briefing.indicadores_disponiveis)


def test_presenter_esconde_codigos_internos():
    apresentado = apresentar_contrato(ExecutarTraducaoVertical().executar(_entrada()))
    assert apresentado.comunicacao[0]["Objetivo de comunicação"] == "Intenção de resposta"
    assert "com_intencao" not in repr(apresentado)
    assert apresentado.midia[0]["Objetivo de mídia"]


def test_comparacao_expoe_mudancas_observaveis():
    anterior = apresentar_contrato(ExecutarTraducaoVertical().executar(_entrada()))
    atual = apresentar_contrato(ExecutarTraducaoVertical().executar(_entrada(id_comando="tela-v2", notoriedade_auxiliada=Decimal("15"), taxa_conclusao_proposta=Decimal("8"))))
    comparacao = comparar_contratos(anterior, atual)
    assert {item["Dimensão"] for item in comparacao} == {"Objetivos de comunicação", "Objetivos de mídia", "Confiança", "Estado do contrato", "Alertas"}
    assert any(item["Mudou"] == "Sim" for item in comparacao)
