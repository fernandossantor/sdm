"""Elegibilidade e diagnóstico de restrições duras do planejamento."""

from dataclasses import dataclass
from math import ceil

from domain.custos import CustoCompra, calcular_custo_compra


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


@dataclass(frozen=True)
class ResultadoRestricoesCompra:
    quantidade: int
    custo: CustoCompra
    limites_ativos: tuple[str, ...]


def resolver_restricoes_compra(
    quantidade_calculada,
    modo,
    premissa,
    preco_unitario,
) -> ResultadoRestricoesCompra:
    """Aplica pisos e tetos à compra inteira, incluindo fees no orçamento."""

    quantidade = int(ceil(float(quantidade_calculada or 0)))
    if quantidade < 0:
        raise ValueError("A quantidade não pode ser negativa.")

    minimo = float(premissa.get("quantidade_minima") or 0)
    maximo = premissa.get("quantidade_maxima")
    maximo = float(maximo) if maximo is not None else None
    verba_minima = float(premissa.get("verba_minima") or 0)
    verba_maxima = premissa.get("verba_maxima")
    verba_maxima = float(verba_maxima) if verba_maxima is not None else None
    limites_ativos = []

    if maximo is not None and minimo > maximo:
        raise ValueError(
            f"Restrições inviáveis: piso de quantidade {minimo:g} "
            f"excede o teto {maximo:g}."
        )
    if verba_maxima is not None and verba_minima > verba_maxima:
        raise ValueError(
            f"Restrições inviáveis: piso de verba {verba_minima:.2f} "
            f"excede o teto {verba_maxima:.2f}."
        )

    if quantidade < minimo:
        if str(modo).upper() != "METAS":
            raise ValueError(
                f"A quantidade {quantidade:g} está abaixo do piso {minimo:g}."
            )
        quantidade = int(ceil(minimo))
        limites_ativos.append("QUANTIDADE_MINIMA")

    if maximo is not None and quantidade > maximo:
        raise ValueError(
            f"A quantidade necessária {quantidade:g} excede o teto "
            f"{maximo:g}; a meta é inviável com este limite."
        )

    custo = calcular_custo_compra(quantidade, preco_unitario, premissa)
    if verba_minima > 0 and custo.custo_total < verba_minima:
        if str(modo).upper() != "METAS":
            raise ValueError(
                f"O custo total {custo.custo_total:.2f} está abaixo do piso "
                f"{verba_minima:.2f}."
            )
        custo_zero = calcular_custo_compra(0, preco_unitario, premissa)
        custo_um = calcular_custo_compra(1, preco_unitario, premissa)
        custo_variavel = custo_um.custo_total - custo_zero.custo_total
        if custo_variavel <= 0:
            raise ValueError(
                "Restrições inviáveis: o piso de verba exige compra, "
                "mas o custo variável é zero."
            )
        quantidade_piso = ceil(
            (verba_minima - custo_zero.custo_total) / custo_variavel
        )
        quantidade = max(quantidade, quantidade_piso)
        limites_ativos.append("VERBA_MINIMA")
        if maximo is not None and quantidade > maximo:
            raise ValueError(
                "Restrições inviáveis: a quantidade necessária para o piso "
                f"de verba ({quantidade:g}) excede o teto {maximo:g}."
            )
        custo = calcular_custo_compra(quantidade, preco_unitario, premissa)

    if verba_maxima is not None and custo.custo_total > verba_maxima:
        raise ValueError(
            f"O custo total {custo.custo_total:.2f} excede o teto "
            f"{verba_maxima:.2f}."
        )

    return ResultadoRestricoesCompra(
        quantidade=quantidade,
        custo=custo,
        limites_ativos=tuple(limites_ativos),
    )
