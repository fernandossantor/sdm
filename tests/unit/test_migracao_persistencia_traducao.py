from pathlib import Path


MIGRACAO = Path(
    "supabase/migrations/20260802190000_persistencia_vertical_traducao_v1.sql"
)


def test_migracao_e_aditiva_e_modela_apenas_o_escopo() -> None:
    sql = MIGRACAO.read_text(encoding="utf-8").lower()

    assert "drop " not in sql
    assert "truncate " not in sql
    assert "delete from" not in sql
    assert "update " not in sql
    for tabela in (
        "traducao_v1_campanhas",
        "traducao_v1_briefing_snapshots",
        "traducao_v1_comandos",
        "traducao_v1_execucoes",
        "traducao_v1_contratos_estrategicos",
        "traducao_v1_rastreabilidade",
    ):
        assert f"create table public.{tabela}" in sql


def test_snapshots_sao_json_versionado() -> None:
    sql = MIGRACAO.read_text(encoding="utf-8").lower()

    assert sql.count("versao_schema text not null") == 4
    assert "conteudo jsonb not null" in sql
    assert "modo = 'traduzir_briefing'" in sql
