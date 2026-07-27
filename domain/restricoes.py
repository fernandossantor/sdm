"""Elegibilidade e diagnóstico de restrições duras do planejamento."""

from dataclasses import dataclass


def _campo(origem, nome, padrao=None):
    if isinstance(origem, dict):
        return origem.get(nome, padrao)
    return getattr(origem, nome, padrao)


def _lista(origem, nome):
    return set(_campo(origem, nome, []) or [])


@dataclass(frozen=True)
class AvaliacaoElegibilidade:
    inventario_id: str
    elegivel: bool
    obrigatorio: bool
    motivos: tuple[str, ...] = ()


@dataclass(frozen=True)
class DiagnosticoViabilidade:
    viavel: bool
    elegiveis: tuple[str, ...]
    excluidos: tuple[AvaliacaoElegibilidade, ...]
    obrigatorios: tuple[str, ...]
    obrigatorios_ausentes: tuple[str, ...]

    @property
    def mensagem(self):
        partes = []
        if self.obrigatorios_ausentes:
            partes.append(
                "inventários obrigatórios ausentes: "
                + ", ".join(self.obrigatorios_ausentes)
            )
        if not self.elegiveis:
            partes.append("nenhum inventário elegível")
        return "; ".join(partes)


def avaliar_elegibilidade(briefing, inventario) -> AvaliacaoElegibilidade:
    inventario_id = str(
        _campo(inventario, "id")
        or _campo(inventario, "inventario_id")
        or _campo(inventario, "inventario", "")
    )
    plataforma_id = _campo(inventario, "plataforma_id")
    ambiente_id = _campo(inventario, "ambiente_id")
    tecnologia_id = _campo(inventario, "tecnologia_id")
    motivos = []

    obrigatorios = _lista(briefing, "inventarios_obrigatorios")
    obrigatorio = inventario_id in obrigatorios

    if inventario_id in _lista(briefing, "inventarios_proibidos"):
        motivos.append("inventário proibido")
    if plataforma_id in _lista(briefing, "plataformas_proibidas"):
        motivos.append("plataforma proibida")
    if ambiente_id in _lista(briefing, "ambientes_proibidos"):
        motivos.append("ambiente proibido")
    if tecnologia_id in _lista(briefing, "tecnologias_proibidas"):
        motivos.append("tecnologia proibida")

    for campo, valor, rotulo in (
        ("plataformas_obrigatorias", plataforma_id, "plataforma"),
        ("ambientes_obrigatorios", ambiente_id, "ambiente"),
        ("tecnologias_obrigatorias", tecnologia_id, "tecnologia"),
    ):
        permitidos = _lista(briefing, campo)
        if permitidos and valor not in permitidos:
            motivos.append(f"{rotulo} fora da seleção obrigatória")

    return AvaliacaoElegibilidade(
        inventario_id=inventario_id,
        elegivel=not motivos,
        obrigatorio=obrigatorio,
        motivos=tuple(motivos),
    )


def diagnosticar_viabilidade(briefing, inventarios) -> DiagnosticoViabilidade:
    avaliacoes = [
        avaliar_elegibilidade(briefing, inventario)
        for inventario in inventarios
    ]
    elegiveis = tuple(
        avaliacao.inventario_id
        for avaliacao in avaliacoes
        if avaliacao.elegivel
    )
    obrigatorios = _lista(briefing, "inventarios_obrigatorios")
    obrigatorios_ausentes = tuple(sorted(obrigatorios - set(elegiveis)))
    excluidos = tuple(
        avaliacao for avaliacao in avaliacoes if not avaliacao.elegivel
    )
    return DiagnosticoViabilidade(
        viavel=bool(elegiveis) and not obrigatorios_ausentes,
        elegiveis=elegiveis,
        excluidos=excluidos,
        obrigatorios=tuple(sorted(obrigatorios)),
        obrigatorios_ausentes=obrigatorios_ausentes,
    )
