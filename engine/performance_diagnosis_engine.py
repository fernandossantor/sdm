"""Comparação auditável entre planejado, forecast e realizado."""


class PerformanceDiagnosisEngine:
    METRICAS = {
        "investimento": ("verba", "verba"),
        "impressoes": ("impressoes_estimadas", "impressoes"),
        "cliques": ("cliques_estimados", "cliques"),
        "conversoes": ("conversoes_estimadas", "conversoes"),
    }

    @staticmethod
    def _desvio(realizado, referencia):
        if realizado is None or referencia is None:
            return None
        if float(referencia) == 0:
            return 0.0 if float(realizado) == 0 else None
        return round((float(realizado) - float(referencia)) / float(referencia) * 100, 2)

    @staticmethod
    def _comparabilidade(plano, realizado):
        if not getattr(plano, "inicio", None) or not getattr(plano, "fim", None):
            return "INDETERMINADO", "Período do planejamento ausente."
        if plano.inicio != realizado.inicio or plano.fim != realizado.fim:
            return (
                "NAO_COMPARAVEL",
                "Período realizado difere do período integral do planejamento.",
            )
        if not str(realizado.fonte or "").strip():
            return "INDETERMINADO", "Fonte do realizado ausente."
        for campo in ("universo", "publico_alvo", "praca"):
            planejados = {
                str((getattr(item, "premissas", None) or {}).get(campo))
                for item in plano.itens
                if (getattr(item, "premissas", None) or {}).get(campo)
            }
            observado = getattr(realizado, campo, None)
            rotulo = campo.replace("_", " ")
            if len(planejados) > 1:
                return (
                    "INDETERMINADO",
                    f"Planejamento possui múltiplos contextos de {rotulo}.",
                )
            if planejados and not observado:
                return "INDETERMINADO", f"Contexto realizado sem {rotulo}."
            if observado and planejados and str(observado) not in planejados:
                return (
                    "NAO_COMPARAVEL",
                    f"{rotulo.title()} realizado difere do planejamento.",
                )
        return "COMPARAVEL", None

    def comparar(self, plano, forecast, realizado):
        situacao, motivo = self._comparabilidade(plano, realizado)
        forecast_por_nome = {
            item.inventario: item for item in forecast.itens
        }
        realizado_por_id = {
            item.inventario_id: item
            for item in realizado.itens
            if item.inventario_id
        }
        realizado_por_nome = {
            item.inventario: item for item in realizado.itens
        }
        linhas = []
        for item_plano in plano.itens:
            item_forecast = forecast_por_nome.get(item_plano.inventario)
            item_realizado = (
                realizado_por_id.get(item_plano.inventario_id)
                or realizado_por_nome.get(item_plano.inventario)
            )
            for metrica, (campo_plano, campo_forecast) in self.METRICAS.items():
                planejado = getattr(item_plano, campo_plano, None)
                projetado = (
                    getattr(item_forecast, campo_forecast, None)
                    if item_forecast else None
                )
                observado = (
                    getattr(item_realizado, metrica, None)
                    if item_realizado else None
                )
                linhas.append({
                    "inventario": item_plano.inventario,
                    "inventario_id": item_plano.inventario_id,
                    "metrica": metrica,
                    "planejado": planejado,
                    "forecast": projetado,
                    "realizado": observado,
                    "desvio_planejado_percentual": (
                        self._desvio(observado, planejado)
                        if situacao == "COMPARAVEL" else None
                    ),
                    "desvio_forecast_percentual": (
                        self._desvio(observado, projetado)
                        if situacao == "COMPARAVEL" else None
                    ),
                    "situacao_comparabilidade": situacao,
                    "motivo": (
                        motivo
                        or (
                            "Métrica realizada ausente."
                            if observado is None else None
                        )
                    ),
                })
        return {
            "situacao_comparabilidade": situacao,
            "motivo": motivo,
            "fonte_realizado": realizado.fonte,
            "periodo": {
                "inicio": realizado.inicio.isoformat(),
                "fim": realizado.fim.isoformat(),
            },
            "contexto_realizado": {
                "universo": realizado.universo,
                "publico_alvo": realizado.publico_alvo,
                "praca": realizado.praca,
            },
            "linhas": linhas,
        }
