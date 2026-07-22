def classificar_frequencia(valor):
    valor = float(valor)
    if valor <= 3:
        return "BAIXA"
    if valor <= 7:
        return "MEDIA"
    return "ALTA"


def classificar_alcance(valor):
    valor = float(valor)
    if valor <= 50:
        return "BAIXO"
    if valor <= 69:
        return "MEDIO"
    return "ALTO"


def resolver_grp(alcance_percentual=None, frequencia_media=None, grp=None):
    valores = (alcance_percentual, frequencia_media, grp)
    if sum(valor is not None for valor in valores) < 2:
        raise ValueError(
            "Informe dois valores entre alcance, frequência média e GRP."
        )

    alcance = float(alcance_percentual) if alcance_percentual is not None else None
    frequencia = float(frequencia_media) if frequencia_media is not None else None
    grp_valor = float(grp) if grp is not None else None

    if alcance is not None and not 0 < alcance <= 100:
        raise ValueError("O alcance deve estar entre 0% e 100%.")
    if frequencia is not None and frequencia <= 0:
        raise ValueError("A frequência média deve ser maior que zero.")
    if grp_valor is not None and grp_valor <= 0:
        raise ValueError("O GRP deve ser maior que zero.")

    if grp_valor is None:
        grp_valor = alcance * frequencia
    elif frequencia is None:
        frequencia = grp_valor / alcance
    elif alcance is None:
        alcance = grp_valor / frequencia
    elif abs(grp_valor - alcance * frequencia) > 0.1:
        raise ValueError(
            "Os valores são inconsistentes: GRP deve ser igual ao alcance (%) "
            "multiplicado pela frequência média."
        )

    if alcance > 100:
        raise ValueError(
            "O GRP e a frequência informados resultam em alcance superior a 100%."
        )
    return round(alcance, 2), round(frequencia, 2), round(grp_valor, 2)
