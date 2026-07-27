from domain.models.forecast import ForecastItem


class ForecastEngine:

    @staticmethod
    def _numero(origem, campo):
        valor = origem.get(campo) if origem else None
        return float(valor) if valor is not None else None

    def calcular(self, plano, metricas):
        idx_id = {
            metrica["inventario_id"]: metrica
            for metrica in metricas
            if metrica.get("inventario_id")
        }
        idx_nome = {
            metrica["inventario"]: metrica
            for metrica in metricas
            if metrica.get("inventario")
        }
        resultado = []

        for item in plano.itens:
            metrica = (
                idx_id.get(getattr(item, "inventario_id", ""))
                or idx_nome.get(item.inventario)
                or {}
            )
            verba = float(item.verba)
            lacunas = []

            impressoes_item = getattr(item, "impressoes_estimadas", None)
            cpm = self._numero(metrica, "cpm")
            if impressoes_item is not None:
                impressoes = float(impressoes_item)
                if cpm is None and impressoes > 0:
                    cpm = verba * 1000 / impressoes
            elif cpm is not None and cpm > 0:
                impressoes = verba / cpm * 1000
            else:
                impressoes = None
                lacunas.append("CPM ou impressões do plano")

            alcance_item = getattr(item, "alcance_estimado", None)
            frequencia_plano = getattr(item, "frequencia", None)
            if frequencia_plano is None:
                frequencia_plano = getattr(plano, "frequencia_alvo", None)
            frequencia = (
                float(frequencia_plano)
                if frequencia_plano is not None
                else self._numero(metrica, "frequencia_media")
            )
            if alcance_item is not None:
                alcance = float(alcance_item)
            elif impressoes is not None and frequencia is not None and frequencia > 0:
                alcance = impressoes / frequencia
            else:
                alcance = None
                lacunas.append("alcance do plano ou frequência explícita")

            cliques_item = getattr(item, "cliques_estimados", None)
            ctr = self._numero(metrica, "ctr")
            if cliques_item is not None:
                cliques = float(cliques_item)
                if ctr is None and impressoes:
                    ctr = cliques / impressoes * 100
            elif impressoes is not None and ctr is not None:
                cliques = impressoes * ctr / 100
            else:
                cliques = None
                lacunas.append("CTR explícito")

            conversoes_item = getattr(item, "conversoes_estimadas", None)
            taxa = self._numero(metrica, "taxa_conversao")
            if conversoes_item is not None:
                conversoes = float(conversoes_item)
            elif cliques is not None and taxa is not None:
                conversoes = cliques * taxa
            else:
                conversoes = None
                lacunas.append("taxa de conversão explícita")

            resultado.append(
                ForecastItem(
                    inventario=item.inventario,
                    verba=round(verba, 2),
                    impressoes=round(impressoes) if impressoes is not None else None,
                    alcance=round(alcance) if alcance is not None else None,
                    cliques=round(cliques) if cliques is not None else None,
                    conversoes=(
                        round(conversoes) if conversoes is not None else None
                    ),
                    ctr=ctr,
                    cpm=round(cpm, 2) if cpm is not None else None,
                    cpc=(
                        round(verba / cliques, 2)
                        if cliques is not None and cliques > 0
                        else None
                    ),
                    cpa=(
                        round(verba / conversoes, 2)
                        if conversoes is not None and conversoes > 0
                        else None
                    ),
                    lacunas=lacunas,
                )
            )

        return resultado
