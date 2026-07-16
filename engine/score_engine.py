class ScoreEngine:

    # ==========================================================
    # OBJETIVO
    # ==========================================================

    @staticmethod
    def objetivo(

        rel_obj

    ):

        if not rel_obj:

            return 0

        score = rel_obj["score_base"]

        peso = float(

            rel_obj.get(

                "peso_manual",

                1

            )

        )

        return (

            score

            / 5

        ) * 100 * peso


    # ==========================================================
    # KPIs
    # ==========================================================

    @staticmethod
    def kpis(

        inventario_id,

        idx_kpi,

        lista_kpis

    ):

        if not lista_kpis:

            return 0

        soma = 0

        pesos = 0

        for kpi_id, peso in lista_kpis:

            rel = idx_kpi.get(

                (

                    inventario_id,

                    kpi_id

                )

            )

            if rel:

                soma += (

                    rel["score_base"]

                    * peso

                )

                pesos += peso

        if pesos == 0:

            return 0

        score = soma / pesos

        return (

            score

            / 5

        ) * 100


    # ==========================================================
    # PÚBLICOS
    # ==========================================================

    @staticmethod
    def publicos(

        inventario,

        audiencias,

        idx_consumo

    ):

        soma = 0

        pesos = 0

        for audiencia in audiencias:

            consumo = idx_consumo.get(

                (

                    audiencia["audiencia_id"],

                    inventario["ambiente_id"]

                )

            )

            if not consumo:

                continue

            peso = float(

                audiencia.get(

                    "peso",

                    100

                )

            )

            soma += (

                float(

                    consumo["score"]

                )

                * peso

            )

            pesos += peso

        if pesos == 0:

            return 20

        score = soma / pesos

        return (

            score

            / 5

        ) * 100

# ==========================================================
# CONTINUA NA PARTE 2
# ==========================================================

    # ==========================================================
    # MÉTRICAS
    # ==========================================================

    @staticmethod
    def metricas(

        fator

    ):

        return min(

            fator * 100,

            110

        )

    # ==========================================================
    # RESTRIÇÕES
    # ==========================================================

    @staticmethod
    def restricoes(

        briefing,

        inventario

    ):

        bonus = 0

        penalidade = 0

        #
        # Compatibilidade
        #

        if isinstance(

            briefing,

            dict

        ):

            return bonus, penalidade

        inventarios_obrigatorios = getattr(

            briefing,

            "inventarios_obrigatorios",

            []

        )

        inventarios_proibidos = getattr(

            briefing,

            "inventarios_proibidos",

            []

        )

        plataformas_obrigatorias = getattr(

            briefing,

            "plataformas_obrigatorias",

            []

        )

        plataformas_proibidas = getattr(

            briefing,

            "plataformas_proibidas",

            []

        )

        ambientes_obrigatorios = getattr(

            briefing,

            "ambientes_obrigatorios",

            []

        )

        ambientes_proibidos = getattr(

            briefing,

            "ambientes_proibidos",

            []

        )

        if inventario["id"] in inventarios_obrigatorios:

            bonus += 20

        if inventario["id"] in inventarios_proibidos:

            penalidade += 100

        if plataformas_obrigatorias:

            if inventario["plataforma_id"] in plataformas_obrigatorias:

                bonus += 10

        if inventario["plataforma_id"] in plataformas_proibidas:

            penalidade += 50

        if ambientes_obrigatorios:

            if inventario["ambiente_id"] in ambientes_obrigatorios:

                bonus += 10

        if inventario["ambiente_id"] in ambientes_proibidos:

            penalidade += 50

        return (

            bonus,

            penalidade

        )

    # ==========================================================
    # PERFIS
    # ==========================================================

    @staticmethod
    def pesos(

        briefing=None

    ):

        #
        # Preparado para futuras estratégias
        #

        return {

            "objetivo": 0.40,

            "kpi": 0.30,

            "audiencia": 0.20,

            "metricas": 0.10

        }

    # ==========================================================
    # SCORE FINAL
    # ==========================================================

    @staticmethod
    def score_final(

        objetivo,

        kpi,

        audiencia,

        metricas,

        bonus,

        penalidade,

        briefing=None

    ):

        pesos = ScoreEngine.pesos(

            briefing

        )

        score = (

            objetivo * pesos["objetivo"]

            +

            kpi * pesos["kpi"]

            +

            audiencia * pesos["audiencia"]

            +

            metricas * pesos["metricas"]

            +

            bonus

            -

            penalidade

        )

        return round(

            min(

                score,

                100

            ),

            2

        )

    # ==========================================================
    # PAPEL
    # ==========================================================

    @staticmethod
    def papel(

        score

    ):

        if score >= 85:

            return "PRINCIPAL"

        elif score >= 70:

            return "COMPLEMENTAR"

        elif score >= 50:

            return "APOIO"

        return "OPCIONAL"


# ==========================================================
# FIM DO ARQUIVO
# ==========================================================