"""Comparação descritiva entre versões imutáveis de um planejamento."""


class VersionComparisonService:
    METRICAS = (
        ("Orçamento", "orcamento"),
        ("Investimento", "investimento"),
        ("Alcance líquido (%)", "alcance_liquido_percentual"),
        ("Frequência combinada", "frequencia_combinada"),
        ("GRP total", "grp_total"),
        ("Impressões", "impressoes"),
        ("Cliques", "cliques"),
        ("Conversões", "conversoes"),
        ("ROI", "roi"),
    )

    @staticmethod
    def _valor(plano, chave):
        if chave == "orcamento":
            return plano.orcamento
        return (plano.resultados_consolidados or {}).get(chave)

    @staticmethod
    def _delta(anterior, atual):
        if anterior is None or atual is None:
            return None
        return round(float(atual) - float(anterior), 4)

    def comparar(self, plano_anterior, plano_atual, metadados=None):
        metricas = []
        for rotulo, chave in self.METRICAS:
            anterior = self._valor(plano_anterior, chave)
            atual = self._valor(plano_atual, chave)
            metricas.append({
                "metrica": rotulo,
                "anterior": anterior,
                "atual": atual,
                "variacao_absoluta": self._delta(anterior, atual),
            })

        def indexar(plano):
            return {
                item.inventario_id or item.inventario: item
                for item in plano.itens
            }

        itens_anteriores = indexar(plano_anterior)
        itens_atuais = indexar(plano_atual)
        itens = []
        for chave in sorted(set(itens_anteriores) | set(itens_atuais)):
            anterior = itens_anteriores.get(chave)
            atual = itens_atuais.get(chave)
            if anterior and atual:
                situacao = "MANTIDO"
            elif atual:
                situacao = "ADICIONADO"
            else:
                situacao = "REMOVIDO"
            verba_anterior = anterior.verba if anterior else None
            verba_atual = atual.verba if atual else None
            quantidade_anterior = (
                anterior.quantidade_estimada if anterior else None
            )
            quantidade_atual = atual.quantidade_estimada if atual else None
            itens.append({
                "inventario": (
                    atual.inventario if atual else anterior.inventario
                ),
                "situacao": situacao,
                "verba_anterior": verba_anterior,
                "verba_atual": verba_atual,
                "variacao_verba": self._delta(
                    verba_anterior, verba_atual
                ),
                "quantidade_anterior": quantidade_anterior,
                "quantidade_atual": quantidade_atual,
                "variacao_quantidade": self._delta(
                    quantidade_anterior, quantidade_atual
                ),
            })
        return {
            "metadados": metadados or {},
            "metricas": metricas,
            "itens": itens,
            "natureza": (
                "Comparação descritiva entre snapshots; não constitui "
                "inferência causal."
            ),
        }
