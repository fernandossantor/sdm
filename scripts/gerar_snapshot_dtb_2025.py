import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET


ARQUIVO_ODS = "RELATORIO_DTB_BRASIL_2025_MUNICIPIOS.ods"
MAXIMO_REPETICOES = 10000
SIGLAS_UF_POR_CODIGO = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA",
    "16": "AP", "17": "TO", "21": "MA", "22": "PI", "23": "CE",
    "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE",
    "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS", "50": "MS", "51": "MT",
    "52": "GO", "53": "DF",
}
NS_TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
NS_TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
COLUNAS = {
    "codigo_estado": "uf",
    "nome_estado": "nome_uf",
    "codigo_municipio": "codigo_municipio_completo",
    "nome_municipio": "nome_municipio",
    "codigo_intermediaria": "regiao_geografica_intermediaria",
    "nome_intermediaria": "nome_regiao_geografica_intermediaria",
    "codigo_imediata": "regiao_geografica_imediata",
    "nome_imediata": "nome_regiao_geografica_imediata",
}


def _normalizar_cabecalho(valor: str) -> str:
    sem_acentos = "".join(
        caractere
        for caractere in unicodedata.normalize("NFKD", valor.strip().casefold())
        if not unicodedata.combining(caractere)
    )
    return re.sub(r"[^a-z0-9]+", "_", sem_acentos).strip("_")


def _repeticoes(elemento: ET.Element, atributo: str) -> int:
    texto = elemento.get(f"{{{NS_TABLE}}}{atributo}", "1")
    try:
        quantidade = int(texto)
    except ValueError as erro:
        raise ValueError("Repetição inválida no ODS") from erro
    if quantidade < 1 or quantidade > MAXIMO_REPETICOES:
        raise ValueError("Repetição inválida no ODS")
    return quantidade


def _valor_celula(celula: ET.Element) -> str:
    paragrafos = []
    for paragrafo in celula.findall(f".//{{{NS_TEXT}}}p"):
        texto = "".join(paragrafo.itertext()).strip()
        if texto:
            paragrafos.append(texto)
    return " ".join(paragrafos).strip()


def _linhas_logicas(content_xml: bytes) -> tuple[tuple[str, ...], ...]:
    raiz = ET.fromstring(content_xml)
    linhas = []
    for tabela in raiz.findall(f".//{{{NS_TABLE}}}table"):
        for linha in tabela.findall(f"{{{NS_TABLE}}}table-row"):
            valores = []
            for celula in linha.findall(f"{{{NS_TABLE}}}table-cell"):
                valor = _valor_celula(celula)
                repeticoes = _repeticoes(celula, "number-columns-repeated")
                valores.extend((valor,) * repeticoes)
            while valores and not valores[-1]:
                valores.pop()
            if not any(valores):
                continue
            repeticoes_linha = _repeticoes(linha, "number-rows-repeated")
            linhas.extend((tuple(valores),) * repeticoes_linha)
    return tuple(linhas)


def _localizar_colunas(linhas: tuple[tuple[str, ...], ...]) -> tuple[int, dict[str, int]]:
    obrigatorias = {
        COLUNAS["codigo_estado"],
        COLUNAS["nome_estado"],
        COLUNAS["codigo_municipio"],
        COLUNAS["nome_municipio"],
    }
    for indice, linha in enumerate(linhas):
        normalizados = tuple(_normalizar_cabecalho(item) for item in linha)
        if obrigatorias.issubset(normalizados):
            return indice, {nome: normalizados.index(nome) for nome in normalizados}
    raise ValueError("Estrutura de colunas da DTB 2025 não reconhecida")


def _campo(linha: tuple[str, ...], colunas: dict[str, int], nome: str) -> str | None:
    cabecalho = COLUNAS[nome]
    indice = colunas.get(cabecalho)
    if indice is None or indice >= len(linha):
        return None
    return linha[indice].strip() or None


def _validar_mapeamento() -> None:
    codigos = tuple(SIGLAS_UF_POR_CODIGO)
    siglas = tuple(SIGLAS_UF_POR_CODIGO.values())
    valido = (
        len(codigos) == 27
        and all(len(item) == 2 and item.isdigit() for item in codigos)
        and all(len(item) == 2 and item.isalpha() and item.isupper() for item in siglas)
        and len(set(codigos)) == 27
        and len(set(siglas)) == 27
    )
    if not valido:
        raise ValueError("Mapeamento canônico de siglas das UFs inválido")


def _interpretar(content_xml: bytes) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    _validar_mapeamento()
    linhas = _linhas_logicas(content_xml)
    indice_cabecalho, colunas = _localizar_colunas(linhas)
    estados_por_codigo: dict[str, dict[str, object]] = {}
    municipios = []
    codigos_municipios = set()
    for linha in linhas[indice_cabecalho + 1:]:
        codigo_estado = _campo(linha, colunas, "codigo_estado")
        nome_estado = _campo(linha, colunas, "nome_estado")
        codigo_municipio = _campo(linha, colunas, "codigo_municipio")
        nome_municipio = _campo(linha, colunas, "nome_municipio")
        if not all((codigo_estado, nome_estado, codigo_municipio, nome_municipio)):
            raise ValueError("Estrutura de colunas da DTB 2025 não reconhecida")
        if codigo_estado not in SIGLAS_UF_POR_CODIGO:
            raise ValueError("Código de UF da DTB 2025 não possui sigla canônica")
        if len(codigo_estado) != 2 or not codigo_estado.isdigit():
            raise ValueError("Código de UF inválido na DTB 2025")
        if len(codigo_municipio) != 7 or not codigo_municipio.isdigit():
            raise ValueError("Código municipal inválido na DTB 2025")
        if not codigo_municipio.startswith(codigo_estado):
            raise ValueError("Prefixo municipal incompatível com a UF")
        estado = {
            "codigo": codigo_estado,
            "sigla": SIGLAS_UF_POR_CODIGO[codigo_estado],
            "nome": nome_estado,
            "codigo_regiao": None,
            "sigla_regiao": None,
            "nome_regiao": None,
        }
        anterior = estados_por_codigo.setdefault(codigo_estado, estado)
        if anterior != estado:
            raise ValueError("Estado duplicado ou inconsistente na DTB 2025")
        if codigo_municipio in codigos_municipios:
            raise ValueError("Município duplicado na DTB 2025")
        codigos_municipios.add(codigo_municipio)
        municipios.append({
            "codigo": codigo_municipio,
            "nome": nome_municipio,
            "codigo_estado": codigo_estado,
            "codigo_regiao_intermediaria": _campo(
                linha, colunas, "codigo_intermediaria"
            ),
            "nome_regiao_intermediaria": _campo(linha, colunas, "nome_intermediaria"),
            "codigo_regiao_imediata": _campo(linha, colunas, "codigo_imediata"),
            "nome_regiao_imediata": _campo(linha, colunas, "nome_imediata"),
        })
    ausentes = set(SIGLAS_UF_POR_CODIGO) - set(estados_por_codigo)
    if ausentes:
        raise ValueError("Unidade da Federação canônica ausente da DTB 2025")
    estados = list(estados_por_codigo.values())
    estados.sort(key=lambda item: (str(item["nome"]).casefold(), item["codigo"]))
    municipios.sort(
        key=lambda item: (
            item["codigo_estado"],
            str(item["nome"]).casefold(),
            item["codigo"],
        )
    )
    return estados, municipios


def gerar_dados(arquivo_zip: Path) -> dict[str, object]:
    with zipfile.ZipFile(arquivo_zip) as pacote:
        try:
            ods = pacote.read(ARQUIVO_ODS)
        except KeyError as erro:
            raise ValueError(
                "Arquivo municipal da DTB 2025 não encontrado no pacote"
            ) from erro
    sha256 = hashlib.sha256(ods).hexdigest()
    with zipfile.ZipFile(io.BytesIO(ods)) as arquivo_ods:
        content_xml = arquivo_ods.read("content.xml")
    estados, municipios = _interpretar(content_xml)
    if len(estados) != 27 or len(municipios) <= 5500:
        raise ValueError("Conteúdo oficial da DTB 2025 incompleto")
    sao_borja = next(
        (item for item in municipios if item["nome"] == "São Borja"),
        None,
    )
    if sao_borja is None or sao_borja["codigo"] != "4318002":
        raise ValueError("Sentinela São Borja ausente ou inválida")
    return {
        "metadados": {
            "fonte": "IBGE — Divisão Territorial Brasileira",
            "edicao": "DTB 2025",
            "arquivo_origem": ARQUIVO_ODS,
            "sha256_arquivo_origem": sha256,
            "quantidade_estados": len(estados),
            "quantidade_municipios": len(municipios),
        },
        "estados": estados,
        "municipios": municipios,
    }


def escrever_snapshot(arquivo_zip: Path, saida: Path) -> None:
    dados = gerar_dados(arquivo_zip)
    conteudo = json.dumps(dados, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(conteudo, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arquivo-zip", required=True, type=Path)
    parser.add_argument("--saida", required=True, type=Path)
    argumentos = parser.parse_args()
    escrever_snapshot(argumentos.arquivo_zip, argumentos.saida)


if __name__ == "__main__":
    main()
