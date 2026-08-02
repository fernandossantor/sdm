from pathlib import Path

from src.application.executar_traducao import (
    executar_caso_canonico,
    main,
    serializar_resultado,
)


SNAPSHOT = Path("tests/snapshots/traducao_canonica.json")


def test_saida_canonica_corresponde_ao_snapshot():
    atual = serializar_resultado(executar_caso_canonico())

    assert atual == SNAPSHOT.read_text(encoding="utf-8")


def test_cli_salva_e_imprime_o_mesmo_json(tmp_path, capsys):
    saida = tmp_path / "traducao.json"

    codigo = main(["--caso", "canonico", "--saida", str(saida)])

    impresso = capsys.readouterr().out
    assert codigo == 0
    assert saida.read_text(encoding="utf-8") == impresso
    assert impresso == SNAPSHOT.read_text(encoding="utf-8")
    assert "SUPABASE" not in impresso
    assert "<" not in impresso
