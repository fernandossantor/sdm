"""Verifica integridade mínima de um conjunto de backup do MediAd Planner."""

import argparse
import hashlib
import json
from pathlib import Path


ARQUIVOS_OBRIGATORIOS = (
    "schema.sql",
    "data.sql",
    "public-data.sql",
    "roles.sql",
)


def sha256(caminho):
    resumo = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            resumo.update(bloco)
    return resumo.hexdigest()


def carregar_manifesto(caminho):
    manifesto = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        partes = linha.strip().split(maxsplit=1)
        if len(partes) == 2:
            manifesto[partes[1].lstrip("*")] = partes[0]
    return manifesto


def verificar(diretorio):
    raiz = Path(diretorio).resolve()
    manifesto_path = raiz / "SHA256SUMS"
    erros = []
    if not raiz.is_dir():
        return {"valido": False, "diretorio": str(raiz), "erros": [
            "Diretório inexistente."
        ], "arquivos": []}
    if not manifesto_path.is_file():
        erros.append("SHA256SUMS ausente.")
        manifesto = {}
    else:
        manifesto = carregar_manifesto(manifesto_path)

    arquivos = []
    for nome in ARQUIVOS_OBRIGATORIOS:
        caminho = raiz / nome
        if not caminho.is_file():
            erros.append(f"{nome} ausente.")
            continue
        tamanho = caminho.stat().st_size
        calculado = sha256(caminho)
        esperado = manifesto.get(nome)
        if tamanho == 0:
            erros.append(f"{nome} está vazio.")
        if not esperado:
            erros.append(f"{nome} não consta no manifesto.")
        elif calculado != esperado:
            erros.append(f"Checksum divergente: {nome}.")
        arquivos.append({
            "nome": nome,
            "tamanho": tamanho,
            "sha256": calculado,
            "checksum_valido": calculado == esperado,
        })
    return {
        "valido": not erros,
        "diretorio": str(raiz),
        "erros": erros,
        "arquivos": arquivos,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("diretorio")
    argumentos = parser.parse_args()
    resultado = verificar(argumentos.diretorio)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    raise SystemExit(0 if resultado["valido"] else 1)


if __name__ == "__main__":
    main()
