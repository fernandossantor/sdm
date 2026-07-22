from engine.score_engine import ScoreEngine
from datetime import date


class InventoryEngine:

    # ==========================================================
    # INDEXADORES
    # ==========================================================

    def indexar_objetivos(

        self,

        dados

    ):

        return {

            (

                item["inventario_id"],

                item["objetivo_id"]

            ): item

            for item in dados

        }

    # ==========================================================

    def indexar_kpis(

        self,

        dados

    ):

        return {

            (

                item["inventario_id"],

                item["kpi_id"]

            ): item

            for item in dados

        }

    # ==========================================================

    def indexar_metricas(

        self,

        dados

    ):

        return {

            item["inventario_id"]: item

            for item in dados

        }

    # ==========================================================

    def indexar_consumo(

        self,

        dados

    ):

        return {

            (

                item["audiencia_id"],

                item["ambiente_id"]

            ): item

            for item in dados

        }

    # ==========================================================

    def indexar_catalogo_kpis(

        self,

        dados

    ):

        return {

            item["nome"]: item["id"]

            for item in dados

        }

    # ==========================================================
    # MÉTRICAS
    # ==========================================================

    def fator_metricas(

        self,

        metricas

    ):

        fator = 1.0

        if not metricas:
            return 0.0

        ctr = metricas.get(

            "ctr"

        )

        try:

            ctr = float(

                ctr

            )

        except Exception:

            ctr = None

        if ctr is not None:

            if ctr >= 2:

                fator *= 1.10

            elif ctr >= 1:

                fator *= 1.05

        view = metricas.get(

            "viewability"

        )

        try:

            view = float(

                view

            )

        except Exception:

            view = None

        if view is not None:

            if view >= 80:

                fator *= 1.10

            elif view >= 70:

                fator *= 1.05

        freq = metricas.get(

            "frequencia_media"

        )

        try:

            freq = float(

                freq

            )

        except Exception:

            freq = None

        if freq is not None:

            if 3 <= freq <= 6:

                fator *= 1.05

        return fator

    # ==========================================================
    # ENGINE
    # ==========================================================

    def calcular(

        self,

        contexto

    ):

        briefing = contexto["briefing"]

        objetivo = contexto["objetivo"]

        inventarios = contexto["inventarios"]

        # Quando a campanha já passou pelo MCP, somente os inventários
        # explicitamente selecionados podem participar do planejamento.
        papeis_campanha = contexto.get("papeis_inventarios", [])
        if papeis_campanha:
            ids_selecionados = {
                item.get("inventario_id") for item in papeis_campanha
                if item.get("selecionado", True)
            }
            inventarios = [
                item for item in inventarios
                if item.get("id") in ids_selecionados
            ]

        audiencias = contexto["audiencias"]

        # ==========================================================
        # COMPATIBILIDADE COM AUDIÊNCIAS V3
        # ==========================================================

        audiencias_processadas = []

        for audiencia in audiencias:

            #
            # Novo modelo (V3)
            #

            if "audiencias_v3" in audiencia:

                audiencias_processadas.append(

                    {

                        "audiencia_id": audiencia["audiencia_id"],

                        "peso": float(

                            audiencia.get(

                                "peso",

                                1

                            )

                        ),

                        "dados": audiencia["audiencias_v3"]

                    }

                )

            #
            # Modelo legado
            #

            else:

                audiencias_processadas.append(

                    audiencia

                )

        audiencias = audiencias_processadas

        idx_obj = self.indexar_objetivos(

            contexto["inventarios_objetivos"]

        )

        idx_kpi = self.indexar_kpis(

            contexto["inventarios_kpis"]

        )

        idx_metricas = self.indexar_metricas(

            contexto["metricas"]

        )

        idx_consumo = self.indexar_consumo(

            contexto["consumo"]

        )

        idx_catalogo_kpis = self.indexar_catalogo_kpis(

            contexto["kpis"]

        )

        afinidades_interesses = contexto.get("interesses_afinidade", [])

        idx_afinidades = {
            (item["interesse_id"], item["ambiente_id"]): float(item["afinidade"])
            for item in afinidades_interesses
        }

        if isinstance(briefing, dict):
            referencia_preco = briefing.get("periodo_inicio")
        else:
            referencia_preco = getattr(briefing, "inicio", None)
        hoje = (
            referencia_preco.isoformat()
            if hasattr(referencia_preco, "isoformat")
            else str(referencia_preco)[:10] if referencia_preco else date.today().isoformat()
        )
        precos_validos = []
        for item in contexto.get("precos", []):
            inicio = item.get("inicio_vigencia")
            fim = item.get("fim_vigencia")
            if inicio and inicio > hoje:
                continue
            if fim and fim < hoje:
                continue
            bruto = float(item.get("valor_bruto", 0))
            desconto = float(item.get("desconto_percentual", 0))
            item_preco = dict(item)
            item_preco["valor_liquido"] = bruto * (1 - desconto / 100)
            precos_validos.append(item_preco)

        precos_validos.sort(
            key=lambda item: (
                item.get("inicio_vigencia") or "0001-01-01",
                item.get("criado_em") or "",
            ),
            reverse=True,
        )
        precos = {}
        for item in precos_validos:
            precos.setdefault(item["inventario_id"], item)

        papeis_mcp = {
            item["inventario_id"]: item
            for item in contexto.get("papeis_inventarios", [])
        }

        #
        # KPIs DO BRIEFING
        #

        lista_kpis = []

        if isinstance(

            briefing,

            dict

        ):

            nome = briefing.get(

                "kpi"

            )

            if nome:

                kpi_id = idx_catalogo_kpis.get(

                    nome

                )

                if kpi_id:

                    lista_kpis.append(

                        (

                            kpi_id,

                            100

                        )

                    )

        else:

            if getattr(

                briefing,

                "kpis",

                None

            ):

                for item in briefing.kpis:

                    kpi_id = idx_catalogo_kpis.get(

                        item["nome"]

                    )

                    if kpi_id:

                        lista_kpis.append(

                            (

                                kpi_id,

                                float(

                                    item.get(

                                        "peso",

                                        100

                                    )

                                )

                            )

                        )

            elif briefing.kpi:

                kpi_id = idx_catalogo_kpis.get(

                    briefing.kpi

                )

                if kpi_id:

                    lista_kpis.append(

                        (

                            kpi_id,

                            100

                        )

                    )

        resultado = []

        # ======================================================
        # CONTINUA NA PARTE 2
        # ======================================================

        for inventario in inventarios:

            preco = precos.get(inventario["id"])

            # --------------------------------------------------
            # SCORE DE PÚBLICOS
            # --------------------------------------------------

            audiencia_score = ScoreEngine.publicos(

                inventario,

                audiencias,

                idx_consumo

            )

            interesse_score = ScoreEngine.interesses(
                inventario,
                audiencias,
                idx_afinidades,
            )

            if interesse_score is not None:
                audiencia_score = round(
                    audiencia_score * 0.75 + interesse_score * 0.25,
                    2,
                )

            # --------------------------------------------------
            # OBJETIVO
            # --------------------------------------------------

            rel_obj = idx_obj.get(

                (

                    inventario["id"],

                    objetivo["id"]

                )

            )

            objetivo_score = ScoreEngine.objetivo(

                rel_obj

            )

            # --------------------------------------------------
            # KPIs
            # --------------------------------------------------

            kpi_score = ScoreEngine.kpis(

                inventario["id"],

                idx_kpi,

                lista_kpis

            )

            # --------------------------------------------------
            # MÉTRICAS
            # --------------------------------------------------

            metricas = idx_metricas.get(

                inventario["id"]

            )

            fator = self.fator_metricas(

                metricas

            )

            metricas_score = ScoreEngine.metricas(

                fator

            )

            # --------------------------------------------------
            # RESTRIÇÕES
            # --------------------------------------------------

            bonus, penalidade = ScoreEngine.restricoes(

                briefing,

                inventario

            )

            # --------------------------------------------------
            # SCORE FINAL
            # --------------------------------------------------

            score = ScoreEngine.score_final(

                objetivo_score,

                kpi_score,

                audiencia_score,

                metricas_score,

                bonus,

                penalidade,

                briefing

            )

            classificacao_mcp = papeis_mcp.get(inventario["id"])
            if classificacao_mcp:
                score_mcp = float(classificacao_mcp.get("score", 0))
                score = round(score * 0.8 + score_mcp * 0.2, 2)
                papel = classificacao_mcp.get("papel", "APOIO").upper()
            else:
                score_mcp = None
                papel = ScoreEngine.papel(

                    score

                )

            resultado.append(

                {

                    "inventario": inventario["nome"],

                    "inventario_id": inventario["id"],

                    "plataforma": inventario["plataformas_v3"]["nome"],

                    "plataforma_id": inventario["plataforma_id"],

                    "ambiente": inventario["ambientes_v3"]["nome"],

                    "ambiente_id": inventario["ambiente_id"],

                    "formato_id": inventario["formato_id"],

                    "score": score,

                    "papel": papel,

                    "score_mcp": score_mcp,

                    "objetivo": round(

                        objetivo_score,

                        1

                    ),

                    "kpi": round(

                        kpi_score,

                        1

                    ),

                    "audiencia": round(

                        audiencia_score,

                        1

                    ),

                    "metricas": round(

                        metricas_score,

                        1

                    ),

                    "preco_unitario": (
                        round(preco["valor_liquido"], 4) if preco else None
                    ),

                    "unidade_compra": preco.get("unidade") if preco else None,

                }

            )

        # ======================================================
        # CONTINUA NA PARTE 3
        # ======================================================

        # --------------------------------------------------
        # ORDENAÇÃO
        # --------------------------------------------------

        resultado.sort(

            key=lambda item: (

                item["score"],

                item["objetivo"],

                item["kpi"],

                item["audiencia"]

            ),

            reverse=True

        )

        return resultado
