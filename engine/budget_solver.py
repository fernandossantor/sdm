"""Solver linear auditável para alocação contínua de verba."""

from copy import deepcopy

from scipy.optimize import linprog

from domain.restricoes import diagnosticar_viabilidade


class LinearBudgetSolver:
    METODO = "SOLVER_LINEAR_HIGHS"
    VERSAO = "objetivo-linear-v2"
    FUNCOES_OBJETIVO = {
        "ADERENCIA": "MAXIMIZAR_ADERENCIA_PONDERADA_PELA_VERBA",
        "CONVERSOES": "MAXIMIZAR_CONVERSOES_PROJETADAS",
    }

    @staticmethod
    def _identificador(item):
        return str(
            item.get("id")
            or item.get("inventario_id")
            or item.get("inventario")
        )

    @staticmethod
    def _adicionar_limites_grupo(
        matriz, itens, campo, minimo, maximo
    ):
        for nome, valor in (maximo or {}).items():
            linha = [1.0 if item.get(campo) == nome else 0.0 for item in itens]
            matriz.append((linha, float(valor), f"{campo}:{nome}:maximo"))
        for nome, valor in (minimo or {}).items():
            linha = [-1.0 if item.get(campo) == nome else 0.0 for item in itens]
            matriz.append((linha, -float(valor), f"{campo}:{nome}:minimo"))

    @staticmethod
    def _validar_parametros(verba_total, percentual_teste):
        if float(verba_total) <= 0:
            raise ValueError("A verba total deve ser maior que zero.")
        if not 0 <= float(percentual_teste) < 1:
            raise ValueError("A reserva para testes deve estar entre 0% e 100%.")

    @classmethod
    def _coeficientes_objetivo(cls, itens, funcao_objetivo):
        funcao = str(funcao_objetivo or "ADERENCIA").upper()
        if funcao not in cls.FUNCOES_OBJETIVO:
            raise ValueError(f"Função objetivo desconhecida: '{funcao}'.")
        if funcao == "ADERENCIA":
            coeficientes = [
                float(item.get("score") or 0)
                for item in itens
            ]
            origem = "score estratégico do plano"
        else:
            coeficientes = []
            for item in itens:
                conversoes = item.get("conversoes_estimadas")
                investimento = item.get("investimento_referencia")
                if conversoes is None or investimento is None:
                    raise ValueError(
                        "A função CONVERSOES exige conversões estimadas e "
                        "investimento de referência para todos os inventários."
                    )
                investimento = float(investimento)
                if investimento <= 0:
                    raise ValueError(
                        "O investimento de referência deve ser maior que zero "
                        "para a função CONVERSOES."
                    )
                coeficientes.append(float(conversoes) / investimento)
            origem = "conversões estimadas por real no plano de referência"
        if not any(valor > 0 for valor in coeficientes):
            raise ValueError(
                f"Otimização inviável: a função {funcao} não possui "
                "coeficiente positivo."
            )
        return funcao, coeficientes, origem

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
        percentual_teste=0,
        funcao_objetivo="ADERENCIA",
    ):
        self._validar_parametros(verba_total, percentual_teste)
        ranking = deepcopy(ranking)
        obrigatorios = obrigatorios or []
        excluidos = excluidos or []
        diagnostico = diagnosticar_viabilidade(
            {
                "inventarios_obrigatorios": obrigatorios,
                "inventarios_proibidos": excluidos,
            },
            ranking,
        )
        if not diagnostico.viavel:
            raise ValueError(
                "Otimização inviável por restrições duras: "
                + diagnostico.mensagem
                + "."
            )

        elegiveis = set(diagnostico.elegiveis)
        itens = [
            item for item in ranking
            if self._identificador(item) in elegiveis
        ]
        if not itens:
            raise ValueError("Otimização inviável: não há inventários elegíveis.")
        funcao, coeficientes, origem_coeficientes = (
            self._coeficientes_objetivo(itens, funcao_objetivo)
        )

        verba_disponivel = round(
            float(verba_total) * (1 - float(percentual_teste)), 2
        )
        matriz = []
        self._adicionar_limites_grupo(
            matriz, itens, "ambiente",
            minimo_ambiente, maximo_ambiente,
        )
        self._adicionar_limites_grupo(
            matriz, itens, "plataforma",
            minimo_plataforma, maximo_plataforma,
        )
        limites = []
        obrigatorios_set = {str(item) for item in obrigatorios}
        for item in itens:
            minimo = float(item.get("verba_minima") or 0)
            if (
                self._identificador(item) in obrigatorios_set
                or str(item.get("inventario")) in obrigatorios_set
            ):
                minimo = max(minimo, 0.01)
            maximo = item.get("verba_maxima")
            limites.append((
                minimo,
                float(maximo) if maximo is not None else None,
            ))

        solucao = linprog(
            c=[-valor for valor in coeficientes],
            A_ub=[linha for linha, _, _ in matriz] or None,
            b_ub=[limite for _, limite, _ in matriz] or None,
            A_eq=[[1.0] * len(itens)],
            b_eq=[verba_disponivel],
            bounds=limites,
            method="highs",
        )
        if not solucao.success:
            raise ValueError(
                "Otimização inviável ou não resolvida pelo solver: "
                + solucao.message
            )

        alocacoes = [round(float(valor), 2) for valor in solucao.x]
        diferenca = round(verba_disponivel - sum(alocacoes), 2)
        if diferenca:
            indice = max(
                range(len(itens)),
                key=lambda i: coeficientes[i],
            )
            alocacoes[indice] = round(alocacoes[indice] + diferenca, 2)

        resultado = []
        for item, verba, coeficiente in zip(itens, alocacoes, coeficientes):
            resultado.append({
                **item,
                "verba": verba,
                "coeficiente_objetivo": coeficiente,
                "origem_coeficiente_objetivo": origem_coeficientes,
                "percentual": (
                    round(verba / verba_disponivel * 100, 2)
                    if verba_disponivel else 0
                ),
                "obrigatorio": (
                    self._identificador(item) in obrigatorios_set
                    or str(item.get("inventario")) in obrigatorios_set
                ),
            })

        restricoes_ativas = []
        tolerancia = 0.01
        for linha, limite, nome in matriz:
            valor = sum(
                coeficiente * verba
                for coeficiente, verba in zip(linha, alocacoes)
            )
            if abs(valor - limite) <= tolerancia:
                restricoes_ativas.append(nome)

        reserva = round(float(verba_total) - verba_disponivel, 2)
        return {
            "itens": resultado,
            "verba_total": float(verba_total),
            "verba_distribuida": round(sum(alocacoes), 2),
            "reserva_testes": reserva,
            "metodo_alocacao": self.METODO,
            "versao_metodo": self.VERSAO,
            "funcao": self.FUNCOES_OBJETIVO[funcao],
            "funcao_objetivo": funcao,
            "valor_funcao_objetivo": round(-float(solucao.fun), 4),
            "otimo_comprovado": True,
            "condicao_viabilidade": "VIAVEL",
            "saldo_orcamento": round(
                float(verba_total) - sum(alocacoes) - reserva, 2
            ),
            "restricoes_ativas_solver": restricoes_ativas,
            "status_solver": {
                "codigo": int(solucao.status),
                "mensagem": solucao.message,
                "iteracoes": int(solucao.nit),
            },
            "diagnostico_viabilidade": {
                "viavel": diagnostico.viavel,
                "elegiveis": list(diagnostico.elegiveis),
                "obrigatorios": list(diagnostico.obrigatorios),
            },
            "limitacoes": [
                "Alocação contínua; não resolve quantidades discretas de compra.",
                (
                    "Conversões são extrapoladas linearmente a partir do plano "
                    "de referência; não há curva de resposta marginal."
                    if funcao == "CONVERSOES"
                    else "Aderência usa score linear, sem curva de resposta."
                ),
            ],
        }
