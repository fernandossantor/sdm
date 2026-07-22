from domain.models.plano_estrategico import (
    PlanoEstrategico,
    PlanoItem
)

from application.services.context_service import (
    ContextService
)

from application.services.recomendacao_service import (
    RecomendacaoService
)

from engine.inventory_engine import InventoryEngine
from engine.allocation_engine import AllocationEngine
from infrastructure.repositories.planning_repository import PlanningRepository
from copy import deepcopy
from datetime import date, timedelta

from domain.media_metrics import resolver_grp


class PlanejamentoService:

    def __init__(self):

        self.context_service = ContextService()

        self.inventory_engine = InventoryEngine()

        self.allocation_engine = AllocationEngine()

        self.recomendacao_service = RecomendacaoService()

        self.repository = PlanningRepository()

    # ======================================================
    # GERAÇÃO
    # ======================================================

    def gerar(

        self,

        briefing=None,

        nome_briefing=None,

        configuracao=None,

    ):

        # Compatibilidade com chamadores legados que enviam o nome do
        # briefing como primeiro argumento posicional.
        if isinstance(briefing, str) and nome_briefing is None:
            nome_briefing = briefing
            briefing = None

        if briefing is None:

            contexto = self.context_service.carregar(

                nome_briefing

            )

            # =====================================================
            # NORMALIZAÇÃO DO CONTEXTO V3
            # =====================================================

            if "audiencias" not in contexto:

                contexto["audiencias"] = []

            for audiencia in contexto["audiencias"]:

                #
                # Compatibilidade V3
                #

                if "peso" not in audiencia:

                    audiencia["peso"] = 1

            briefing_bd = dict(contexto["briefing"])

            if configuracao:
                briefing_bd["kpi"] = configuracao.get("kpi", briefing_bd.get("kpi"))

            contexto["briefing"] = briefing_bd

            objetivo = contexto["objetivo"]

            verba = float((configuracao or {}).get("orcamento", briefing_bd["orcamento"]))

            cliente = briefing_bd["anunciante"]

            campanha = briefing_bd["nome"]

        else:

            briefing_calculo = deepcopy(briefing)

            if configuracao:
                briefing_calculo.kpi = configuracao.get("kpi", briefing_calculo.kpi)
                briefing_calculo.kpis = configuracao.get("kpis", briefing_calculo.kpis)
                briefing_calculo.tipo_flight = configuracao.get(
                    "tipo_flight", briefing_calculo.tipo_flight
                )
                briefing_calculo.frequencia_objetivo = configuracao.get(
                    "frequencia_objetivo", briefing_calculo.frequencia_objetivo
                )
                briefing_calculo.frequencia_alvo = configuracao.get(
                    "frequencia_alvo", briefing_calculo.frequencia_alvo
                )
                briefing_calculo.alcance_objetivo = configuracao.get(
                    "alcance_objetivo", briefing_calculo.alcance_objetivo
                )
                briefing_calculo.alcance_percentual = configuracao.get(
                    "alcance_percentual", briefing_calculo.alcance_percentual
                )
                briefing_calculo.grp = configuracao.get(
                    "grp", briefing_calculo.grp
                )

            contexto = self.context_service.carregar_por_objeto(

                briefing_calculo

            )

            objetivo = contexto["objetivo"]

            verba = float((configuracao or {}).get("orcamento", briefing.orcamento))

            cliente = briefing.cliente

            campanha = briefing.campanha

        ranking = self.inventory_engine.calcular(

            contexto

        )

        ids_configurados = set(
            (configuracao or {}).get("inventarios_selecionados", [])
        )
        if ids_configurados:
            ranking = [
                item for item in ranking
                if item.get("inventario_id") in ids_configurados
            ]

        if not ranking:
            raise ValueError(
                "Nenhum inventário foi aplicado à campanha no MCP Papéis."
            )

        plano = self._montar_plano(

            cliente=cliente,

            campanha=campanha,

            objetivo=objetivo["nome"],

            verba=verba,

            ranking=ranking,

            observacao="Plano estratégico gerado automaticamente pelo PlanOS."

        )

        fonte = configuracao or {}
        if briefing is not None:
            plano.tipo_flight = fonte.get("tipo_flight", briefing.tipo_flight)
            plano.frequencia_objetivo = fonte.get(
                "frequencia_objetivo", briefing.frequencia_objetivo or "MEDIA"
            )
            plano.frequencia_alvo = float(
                fonte.get("frequencia_alvo", briefing.frequencia_alvo or 5)
            )
            plano.alcance_objetivo = fonte.get(
                "alcance_objetivo", briefing.alcance_objetivo or "MEDIO"
            )
            plano.alcance_percentual = float(
                fonte.get("alcance_percentual", briefing.alcance_percentual or 60)
            )
            plano.grp = float(
                fonte.get(
                    "grp",
                    briefing.grp
                    or plano.alcance_percentual * plano.frequencia_alvo,
                )
            )
            plano.publico_referencia = self._publico_referencia(briefing.publicos)
            plano.alcance_meta = round(
                plano.publico_referencia * plano.alcance_percentual / 100
            )
            plano.kpis = fonte.get("kpis", briefing.kpis)
            inicio_cronograma, fim_cronograma = briefing.inicio, briefing.fim
        else:
            plano.tipo_flight = fonte.get("tipo_flight", briefing_bd.get("tipo_flight", "LINEAR"))
            plano.frequencia_objetivo = fonte.get("frequencia_objetivo", "MEDIA")
            plano.frequencia_alvo = float(fonte.get("frequencia_alvo", 5))
            plano.alcance_objetivo = fonte.get(
                "alcance_objetivo", briefing_bd.get("alcance_objetivo", "MEDIO")
            )
            plano.alcance_percentual = float(
                fonte.get("alcance_percentual", briefing_bd.get("alcance_percentual", 60))
            )
            plano.grp = float(
                fonte.get(
                    "grp",
                    briefing_bd.get("grp")
                    or plano.alcance_percentual * plano.frequencia_alvo,
                )
            )
            plano.publico_referencia = int(
                fonte.get("publico_referencia", briefing_bd.get("publico_referencia", 0))
            )
            plano.alcance_meta = round(
                plano.publico_referencia * plano.alcance_percentual / 100
            )
            plano.kpis = fonte.get("kpis", [{"nome": fonte.get("kpi", briefing_bd.get("kpi")), "peso": 100}])
            inicio_cronograma = self._data(briefing_bd.get("periodo_inicio"))
            fim_cronograma = self._data(briefing_bd.get("periodo_fim"))

        resolver_grp(plano.alcance_percentual, plano.frequencia_alvo, plano.grp)
        self._calcular_entrega(plano)
        plano.cronograma = self._cronograma(
            inicio_cronograma,
            fim_cronograma,
            plano.tipo_flight,
            plano.itens,
        )

        return plano

    @staticmethod
    def _calcular_entrega(plano):

        for item in plano.itens:
            if item.preco_unitario <= 0:
                continue
            item.quantidade_estimada = round(item.verba / item.preco_unitario, 2)
            unidade = (item.unidade_compra or "").casefold()
            if "mil impress" in unidade:
                item.impressoes_estimadas = round(item.quantidade_estimada * 1000)
                item.alcance_estimado = round(
                    item.impressoes_estimadas / max(plano.frequencia_alvo, 1)
                )
            elif unidade in {"impressão", "impressao"}:
                item.impressoes_estimadas = round(item.quantidade_estimada)
                item.alcance_estimado = round(
                    item.impressoes_estimadas / max(plano.frequencia_alvo, 1)
                )
            elif "mil contato" in unidade:
                item.alcance_estimado = round(
                    item.quantidade_estimada * 1000
                    / max(plano.frequencia_alvo, 1)
                )

        if plano.publico_referencia > 0:
            nao_alcancado = 1.0
            for item in plano.itens:
                if item.alcance_estimado is None:
                    continue
                alcance_item = min(
                    item.alcance_estimado / plano.publico_referencia,
                    1.0,
                )
                nao_alcancado *= 1 - alcance_item
            plano.alcance_projetado = round(
                plano.publico_referencia * (1 - nao_alcancado)
            )
        else:
            plano.alcance_projetado = round(
                sum(item.alcance_estimado or 0 for item in plano.itens)
            )

    @staticmethod
    def _data(valor):
        if not valor:
            return None
        if isinstance(valor, date):
            return valor
        return date.fromisoformat(str(valor)[:10])

    @staticmethod
    def _publico_referencia(publicos):

        return round(
            sum(
                int(publico.get("populacao_estimada") or 0)
                * float(publico.get("peso", 100)) / 100
                for publico in (publicos or [])
                if isinstance(publico, dict)
            )
        )

    @staticmethod
    def _cronograma(inicio, fim, tipo_flight, itens=None):

        if not inicio or not fim or fim < inicio:
            return []

        dias = (fim - inicio).days + 1
        semanas = max(1, (dias + 6) // 7)

        if tipo_flight == "ONDA":
            pesos = [1.5 if indice % 2 == 0 else 0.5 for indice in range(semanas)]
        elif tipo_flight == "CONCENTRADO":
            ativas = max(1, (semanas + 2) // 3)
            pesos = [1.0 if indice < ativas else 0.0 for indice in range(semanas)]
        else:
            pesos = [1.0] * semanas

        total = sum(pesos)
        percentuais = [peso / total for peso in pesos]
        colunas = []
        for indice in range(semanas):
            semana_inicio = inicio + timedelta(days=indice * 7)
            semana_fim = min(semana_inicio + timedelta(days=6), fim)
            colunas.append(
                f"S{indice + 1} · {semana_inicio:%d/%m}–{semana_fim:%d/%m}"
            )

        if not itens:
            return [
                {
                    "Semana": coluna,
                    "Participação (%)": round(percentual * 100, 2),
                }
                for coluna, percentual in zip(colunas, percentuais)
            ]

        cronograma = []
        for item in itens:
            total_item = float(item.quantidade_estimada or 0)
            distribuicao = [round(total_item * percentual, 2) for percentual in percentuais]
            if distribuicao:
                distribuicao[-1] = round(
                    distribuicao[-1] + total_item - sum(distribuicao), 2
                )
            linha = {
                "Inventário": item.inventario,
                "Unidade": item.unidade_compra or "Sem unidade",
                "Total": total_item,
            }
            linha.update(dict(zip(colunas, distribuicao)))
            cronograma.append(linha)
        return cronograma

    def listar(self):

        try:
            return self.repository.listar()
        except Exception:
            return []

    def salvar(self, nome, plano, configuracao, briefing_id=None):

        itens = [
            {
                "inventario": item.inventario,
                "plataforma": item.plataforma,
                "ambiente": item.ambiente,
                "papel": item.papel,
                "score": item.score,
                "score_mcp": item.score_mcp,
                "objetivo_score": item.objetivo_score,
                "kpi_score": item.kpi_score,
                "audiencia_score": item.audiencia_score,
                "metricas_score": item.metricas_score,
                "verba": item.verba,
                "percentual": item.percentual,
                "justificativas": item.justificativas,
                "inventario_id": item.inventario_id,
                "preco_unitario": item.preco_unitario,
                "unidade_compra": item.unidade_compra,
                "quantidade_estimada": item.quantidade_estimada,
                "impressoes_estimadas": item.impressoes_estimadas,
                "alcance_estimado": item.alcance_estimado,
            }
            for item in plano.itens
        ]

        return self.repository.salvar(
            {
                "nome": nome,
                "briefing_id": briefing_id,
                "configuracao": configuracao,
                "resultado": {
                    "cliente": plano.cliente,
                    "campanha": plano.campanha,
                    "objetivo": plano.objetivo,
                    "orcamento": plano.orcamento,
                    "itens": itens,
                "observacoes": plano.observacoes,
                    "tipo_flight": plano.tipo_flight,
                    "frequencia_objetivo": plano.frequencia_objetivo,
                    "frequencia_alvo": plano.frequencia_alvo,
                    "alcance_objetivo": plano.alcance_objetivo,
                    "alcance_percentual": plano.alcance_percentual,
                    "grp": plano.grp,
                    "publico_referencia": plano.publico_referencia,
                    "alcance_meta": plano.alcance_meta,
                    "alcance_projetado": plano.alcance_projetado,
                    "kpis": plano.kpis,
                    "cronograma": plano.cronograma,
                },
                "status": "SALVO",
            }
        )

    def excluir(self, planejamento_id):

        return self.repository.excluir(planejamento_id)

    def atualizar_cronograma(self, planejamento_id, cronograma):
        registro = self.repository.obter(planejamento_id)
        resultado = dict(registro.get("resultado") or {})
        resultado["cronograma"] = cronograma
        return self.repository.atualizar(
            planejamento_id,
            {"resultado": resultado},
        )

    @staticmethod
    def restaurar(registro):

        dados = registro["resultado"]
        plano = PlanoEstrategico(
            cliente=dados["cliente"],
            campanha=dados["campanha"],
            objetivo=dados["objetivo"],
            orcamento=float(dados["orcamento"]),
            tipo_flight=dados.get("tipo_flight", "LINEAR"),
            frequencia_objetivo=dados.get("frequencia_objetivo", "MEDIA"),
            frequencia_alvo=float(dados.get("frequencia_alvo", 5)),
            alcance_objetivo=dados.get("alcance_objetivo", "MEDIO"),
            alcance_percentual=float(dados.get("alcance_percentual", 60)),
            grp=float(
                dados.get("grp")
                or float(dados.get("alcance_percentual", 60))
                * float(dados.get("frequencia_alvo", 5))
            ),
            publico_referencia=int(dados.get("publico_referencia", 0)),
            alcance_meta=int(dados.get("alcance_meta", 0)),
            alcance_projetado=int(dados.get("alcance_projetado", 0)),
            kpis=dados.get("kpis", []),
            cronograma=dados.get("cronograma", []),
            observacoes=dados.get("observacoes", []),
        )

        for item in dados.get("itens", []):
            plano.adicionar_item(PlanoItem(**item))

        return plano

    # ======================================================
    # RECÁLCULO
    # ======================================================

    def recalcular(

        self,

        nome_briefing,

        inventarios

    ):

        contexto = self.context_service.carregar(

            nome_briefing

        )

        briefing = contexto["briefing"]

        objetivo = contexto["objetivo"]

        ranking = self.inventory_engine.calcular(

            contexto

        )

        ranking = [

            item

            for item in ranking

            if item["inventario"] in inventarios

        ]

        return self._montar_plano(

            cliente=briefing["anunciante"],

            campanha=briefing["nome"],

            objetivo=objetivo["nome"],

            verba=briefing["orcamento"],

            ranking=ranking,

            observacao="Plano recalculado pelo Planejamento Assistido."

        )

    # ======================================================
    # MONTAGEM
    # ======================================================

    def _montar_plano(

        self,

        cliente,

        campanha,

        objetivo,

        verba,

        ranking,

        observacao

    ):

        plano_tatico = self.allocation_engine.distribuir(

            ranking,

            verba

        )

        indice = {

            item["inventario"]: item

            for item in ranking

        }

        plano = PlanoEstrategico(

            cliente=cliente,

            campanha=campanha,

            objetivo=objetivo,

            orcamento=verba

        )

        for item in plano_tatico.itens:

            origem = indice[item.inventario]

            plano.adicionar_item(

                PlanoItem(

                    inventario=item.inventario,

                    plataforma=item.plataforma,

                    ambiente=item.ambiente,

                    papel=item.papel,

                    score=item.score,

                    score_mcp=(
                        float(origem["score_mcp"])
                        if origem.get("score_mcp") is not None
                        else None
                    ),

                    objetivo_score=float(origem.get("objetivo") or 0),

                    kpi_score=float(origem.get("kpi") or 0),

                    audiencia_score=float(origem.get("audiencia") or 0),

                    metricas_score=float(origem.get("metricas") or 0),

                    verba=item.verba,

                    percentual=item.percentual,

                    justificativas=self.recomendacao_service.inventario(

                        origem

                    ),

                    inventario_id=origem.get("inventario_id", ""),

                    preco_unitario=float(origem.get("preco_unitario") or 0),

                    unidade_compra=origem.get("unidade_compra") or "",

                )

            )

        plano.observacoes = [

            observacao,

            "Distribuição proporcional ao score estratégico.",

            "Recomendações geradas automaticamente pelo PlanOS."

        ]

        return plano
