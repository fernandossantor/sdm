from datetime import datetime, timezone
from uuid import uuid4

from domain.briefing import BriefingInicial, ConteudoBriefing, EstadoBriefing
from domain.contracts import (
    ComandoMotor, EstadoExecucao, NivelExecucao, PoliticaReexecucao,
)
from domain.traducao import ContratoEstrategico
from application.use_cases import ReprocessarTraducaoEstrategica
from engines.traducao_estrategica import (
    MOTOR_TRADUCAO_ESTRATEGICA, CatalogoTraducaoInicial,
    ModoTraducaoEstrategica, MotorTraducaoEstrategica,
)


class RelogioFixo:
    instante = datetime(2026, 8, 2, 3, tzinfo=timezone.utc)

    def agora(self):
        return self.instante


def test_motor_real_consulta_bibliotecas_e_declara_dependencias():
    briefing = BriefingInicial(
        id=uuid4(), campanha_id=uuid4(), criado_por=uuid4(),
        criado_em=RelogioFixo.instante, estado=EstadoBriefing.CONCLUIDO,
        conteudo=ConteudoBriefing(
            objetivos_marketing=({"categoria": "Crescimento"},),
            objetivos_comunicacao=({"categoria": "conhecimento"},),
            fontes=({"descricao": "Pesquisa 2026"},),
            publicos=({"nome": "Compradores"},), jornada_aplicavel=False,
        ),
    )
    comando = ComandoMotor(
        motor_destino=MOTOR_TRADUCAO_ESTRATEGICA,
        modo_execucao=ModoTraducaoEstrategica.TRADUZIR_BRIEFING,
        nivel_execucao=NivelExecucao.PREVIA,
        id_campanha=briefing.campanha_id,
        id_snapshot_campanha=briefing.campanha_id,
        id_usuario=briefing.criado_por,
        perfil_de_acesso="PLANEJADOR", solicitado_em=RelogioFixo.instante,
        origem_do_comando="teste",
        objetivo_da_execucao="Traduzir briefing",
        parametros_locais={"briefing": briefing},
    )

    saida = MotorTraducaoEstrategica(
        relogio=RelogioFixo(), catalogo=CatalogoTraducaoInicial()
    ).executar(comando)

    assert saida.estado_execucao is EstadoExecucao.CONCLUIDA
    assert saida.resultado_principal.objetivos_midia_derivados
    assert {item.tipo for item in saida.rastreabilidade.conhecimentos_aplicados} == {
        "BIBLIOTECA_14", "BIBLIOTECA_15", "BIBLIOTECA_16",
        "BIBLIOTECA_17", "BIBLIOTECA_18",
    }
    assert saida.dependencias[0].recalcula_quando
    assert saida.reexecucao.politica is PoliticaReexecucao.RECALCULAR_PARCIALMENTE
    assert "sem selecionar inventário" in (
        saida.explicacao["conclusao_pratica"].lower()
    )

    persistido = saida.resultado_principal.model_copy(update={
        "execucao_motor": saida.model_copy(update={"resultado_principal": None})
    })
    restaurado = ContratoEstrategico.model_validate(
        persistido.model_dump(mode="json")
    )
    assert restaurado.execucao_motor.id_execucao == saida.id_execucao
    assert restaurado.execucao_motor.resultado_principal is None


def test_reprocessamento_cria_versao_com_as_cinco_bibliotecas():
    briefing = BriefingInicial(
        id=uuid4(), campanha_id=uuid4(), criado_por=uuid4(),
        criado_em=RelogioFixo.instante, estado=EstadoBriefing.CONCLUIDO,
        conteudo=ConteudoBriefing(
            objetivos_marketing=({"categoria": "Crescimento"},),
            objetivos_comunicacao=({"categoria": "conhecimento"},),
            publicos=({"nome": "Compradores"},), jornada_aplicavel=False,
        ),
    )
    antigo = ContratoEstrategico(
        id=uuid4(), campanha_id=briefing.campanha_id,
        briefing_id=briefing.id, briefing_versao=1, versao=1,
        estado="PARCIAL", objetivos_declarados=(),
        objetivos_midia_derivados=(), lacunas=(), confianca="BAIXA",
        versao_regras="traducao-inicial", criado_por=briefing.criado_por,
        criado_em=RelogioFixo.instante,
    )

    class Dependencias:
        salvo = None
        def obter_briefing(self, briefing_id): return briefing
        def obter_traducao_por_briefing(self, briefing_id): return antigo
        def pode_editar(self, usuario_id, campanha_id): return True
        def salvar_nova_versao_traducao(self, anterior, nova):
            self.salvo = (anterior, nova)

    deps = Dependencias()
    nova = ReprocessarTraducaoEstrategica(
        relogio=RelogioFixo(), autorizador=deps, repositorio=deps,
        motor=MotorTraducaoEstrategica(
            relogio=RelogioFixo(), catalogo=CatalogoTraducaoInicial()
        ),
    ).executar(briefing_id=briefing.id, usuario_id=briefing.criado_por)

    assert nova.versao == 2
    assert {item.biblioteca for item in nova.referencias_bibliotecas} == {
        14, 15, 16, 17, 18
    }
    assert deps.salvo == (antigo, nova)
