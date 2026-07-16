from copy import deepcopy


class BudgetOptimizer:

    # =====================================================
    # OTIMIZAÇÃO
    # =====================================================

    def otimizar(

        self,

        ranking,

        verba_total,

        minimo_ambiente=None,

        maximo_ambiente=None,

        minimo_plataforma=None,

        maximo_plataforma=None,

        obrigatorios=None,

        excluidos=None,

        percentual_teste=0

    ):

        ranking = deepcopy(ranking)

        obrigatorios = obrigatorios or []

        excluidos = excluidos or []

        minimo_ambiente = minimo_ambiente or {}

        maximo_ambiente = maximo_ambiente or {}

        minimo_plataforma = minimo_plataforma or {}

        maximo_plataforma = maximo_plataforma or {}

        #
        # Remove excluídos
        #

        ranking = [

            item

            for item in ranking

            if item["inventario"] not in excluidos

        ]

        #
        # Score ponderado
        #

        total_score = sum(

            item["score"]

            for item in ranking

        )

        if total_score == 0:

            return []

        #
        # Distribuição inicial
        #

        resultado = []

        verba_disponivel = verba_total * (

            1 - percentual_teste

        )

        for item in ranking:

            percentual = (

                item["score"]

                / total_score

            )

            verba = percentual * verba_disponivel

            resultado.append(

                {

                    **item,

                    "percentual": percentual,

                    "verba": verba

                }

            )

        #
        # Inventários obrigatórios
        #

        for item in resultado:

            if item["inventario"] in obrigatorios:

                item["obrigatorio"] = True

            else:

                item["obrigatorio"] = False

        #
        # Consolidação por ambiente
        #

        ambiente = {}

        for item in resultado:

            nome = item["ambiente"]

            ambiente[nome] = ambiente.get(

                nome,

                0

            ) + item["verba"]

        #
        # Consolidação por plataforma
        #

        plataforma = {}

        for item in resultado:

            nome = item["plataforma"]

            plataforma[nome] = plataforma.get(

                nome,

                0

            ) + item["verba"]

        #
        # Aplicação de limites mínimos
        #

        for nome, minimo in minimo_ambiente.items():

            atual = ambiente.get(

                nome,

                0

            )

            if atual < minimo:

                diferenca = minimo - atual

                candidatos = [

                    i

                    for i in resultado

                    if i["ambiente"] == nome

                ]

                if candidatos:

                    candidatos[0]["verba"] += diferenca

        for nome, minimo in minimo_plataforma.items():

            atual = plataforma.get(

                nome,

                0

            )

            if atual < minimo:

                diferenca = minimo - atual

                candidatos = [

                    i

                    for i in resultado

                    if i["plataforma"] == nome

                ]

                if candidatos:

                    candidatos[0]["verba"] += diferenca

        #
        # Aplicação de limites máximos
        #

        for nome, maximo in maximo_ambiente.items():

            atual = ambiente.get(

                nome,

                0

            )

            if atual > maximo:

                excesso = atual - maximo

                candidatos = [

                    i

                    for i in resultado

                    if i["ambiente"] == nome

                ]

                if candidatos:

                    candidatos[0]["verba"] -= excesso

        for nome, maximo in maximo_plataforma.items():

            atual = plataforma.get(

                nome,

                0

            )

            if atual > maximo:

                excesso = atual - maximo

                candidatos = [

                    i

                    for i in resultado

                    if i["plataforma"] == nome

                ]

                if candidatos:

                    candidatos[0]["verba"] -= excesso

        #
        # Recalcula percentuais
        #

        total = sum(

            item["verba"]

            for item in resultado

        )

        if total > 0:

            for item in resultado:

                item["percentual"] = round(

                    item["verba"]

                    / total

                    * 100,

                    2

                )

                item["verba"] = round(

                    item["verba"],

                    2

                )

        #
        # Reserva para testes
        #

        reserva = round(

            verba_total * percentual_teste,

            2

        )

        return {

            "itens": resultado,

            "verba_total": verba_total,

            "verba_distribuida": round(

                total,

                2

            ),

            "reserva_testes": reserva

        }