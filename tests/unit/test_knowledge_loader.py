import copy
import json
from pathlib import Path

import pytest

from src.knowledge.loader import ARQUIVOS, ErroConhecimento, carregar_conhecimento


RAIZ_CONHECIMENTO = Path("src/knowledge")


def _documentos_validos():
    return {
        nome: json.loads((RAIZ_CONHECIMENTO / arquivo).read_text(encoding="utf-8"))
        for nome, arquivo in ARQUIVOS.items()
    }


def _gravar(tmp_path, documentos):
    for nome, arquivo in ARQUIVOS.items():
        (tmp_path / arquivo).write_text(
            json.dumps(documentos[nome], ensure_ascii=False),
            encoding="utf-8",
        )


def test_carrega_base_minima_valida():
    base = carregar_conhecimento()

    assert len(base["objetivos"]) == 9
    assert len(base["relacoes_marketing_comunicacao"]) == 5
    assert len(base["relacoes_comunicacao_midia"]) == 4
    assert len(base["indicadores"]) == 8
    assert all(registro["versao"] == "1.0" for registros in base.values() for registro in registros)


def test_rejeita_codigo_duplicado(tmp_path):
    documentos = _documentos_validos()
    duplicado = copy.deepcopy(documentos["objetivos"]["registros"][0])
    documentos["objetivos"]["registros"].append(duplicado)
    _gravar(tmp_path, documentos)

    with pytest.raises(ErroConhecimento, match="código duplicado"):
        carregar_conhecimento(tmp_path)


def test_rejeita_referencia_inexistente(tmp_path):
    documentos = _documentos_validos()
    documentos["relacoes_marketing_comunicacao"]["registros"][0]["origem"] = "mkt_inexistente"
    _gravar(tmp_path, documentos)

    with pytest.raises(ErroConhecimento, match="referência inexistente mkt_inexistente"):
        carregar_conhecimento(tmp_path)


def test_rejeita_versao_ausente(tmp_path):
    documentos = _documentos_validos()
    del documentos["indicadores"]["registros"][0]["versao"]
    _gravar(tmp_path, documentos)

    with pytest.raises(ErroConhecimento, match="campo obrigatório versao"):
        carregar_conhecimento(tmp_path)


def test_rejeita_relacao_invalida(tmp_path):
    documentos = _documentos_validos()
    documentos["relacoes_comunicacao_midia"]["registros"][0]["destino"] = "com_notoriedade"
    _gravar(tmp_path, documentos)

    with pytest.raises(ErroConhecimento, match="relação inválida"):
        carregar_conhecimento(tmp_path)
