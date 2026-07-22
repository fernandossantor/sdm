from datetime import date, datetime


def numero_ptbr(valor, casas=0):
    if valor is None:
        return "—"
    try:
        texto = f"{float(valor):,.{casas}f}"
    except (TypeError, ValueError):
        return str(valor)
    return texto.replace(",", "#").replace(".", ",").replace("#", ".")


def moeda_ptbr(valor):
    return f"R$ {numero_ptbr(valor, 2)}"


def percentual_ptbr(valor, casas=2):
    return f"{numero_ptbr(valor, casas)}%"


def data_ptbr(valor):
    if valor in (None, ""):
        return "—"
    if isinstance(valor, datetime):
        valor = valor.date()
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    try:
        return date.fromisoformat(str(valor)[:10]).strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return str(valor)


def dataframe_ptbr(
    tabela, moedas=(), percentuais=(), inteiros=(), decimais=(), datas=()
):
    """Formata uma cópia para exibição sem alterar os dados de cálculo."""
    resultado = tabela.copy()
    for coluna in moedas:
        if coluna in resultado:
            resultado[coluna] = resultado[coluna].map(moeda_ptbr)
    for coluna in percentuais:
        if coluna in resultado:
            resultado[coluna] = resultado[coluna].map(percentual_ptbr)
    for coluna in inteiros:
        if coluna in resultado:
            resultado[coluna] = resultado[coluna].map(numero_ptbr)
    for coluna in decimais:
        if coluna in resultado:
            resultado[coluna] = resultado[coluna].map(
                lambda valor: numero_ptbr(valor, 2)
            )
    for coluna in datas:
        if coluna in resultado:
            resultado[coluna] = resultado[coluna].map(data_ptbr)
    return resultado
