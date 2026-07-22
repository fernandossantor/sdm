def numero_ptbr(valor, casas=0):
    try:
        texto = f"{float(valor):,.{casas}f}"
    except (TypeError, ValueError):
        return str(valor)
    return texto.replace(",", "#").replace(".", ",").replace("#", ".")


def moeda_ptbr(valor):
    return f"R$ {numero_ptbr(valor, 2)}"


def percentual_ptbr(valor, casas=2):
    return f"{numero_ptbr(valor, casas)}%"


def dataframe_ptbr(tabela, moedas=(), percentuais=(), inteiros=(), decimais=()):
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
    return resultado
