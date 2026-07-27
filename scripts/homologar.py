"""Executa os gates reproduzíveis de homologação do MediAd Planner."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time


GATES_OFFLINE = (
    ("testes_offline", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
)
GATES_CONECTADOS = (
    ("regressao", [sys.executable, "-m", "scripts.regression_test"]),
    ("saude", [sys.executable, "-m", "scripts.health_check"]),
    ("seguranca", [sys.executable, "-m", "scripts.auditar_seguranca"]),
    (
        "integracao",
        [sys.executable, "-m", "unittest", "tests.test_connection", "-v"],
    ),
    (
        "migrations",
        ["npx", "supabase", "migration", "list", "--linked"],
    ),
)


def executar_comando(nome, comando, ambiente=None, timeout=300):
    inicio = time.monotonic()
    try:
        processo = subprocess.run(
            comando,
            cwd=Path(__file__).resolve().parent.parent,
            env=ambiente,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "gate": nome,
            "sucesso": processo.returncode == 0,
            "codigo": processo.returncode,
            "duracao_segundos": round(time.monotonic() - inicio, 2),
            "saida_final": "\n".join(
                (processo.stdout + processo.stderr).splitlines()[-12:]
            ),
        }
    except (OSError, subprocess.TimeoutExpired) as erro:
        return {
            "gate": nome,
            "sucesso": False,
            "codigo": None,
            "duracao_segundos": round(time.monotonic() - inicio, 2),
            "saida_final": f"{type(erro).__name__}: {erro}",
        }


def homologar(conectado=False, ambiente=None):
    ambiente = dict(ambiente or os.environ)
    ambiente.setdefault("SUPABASE_TELEMETRY_DISABLED", "1")
    gates = list(GATES_OFFLINE)
    if conectado:
        gates.extend(GATES_CONECTADOS)
    resultados = [
        executar_comando(
            nome,
            comando,
            (
                {**ambiente, "SDM_RUN_INTEGRATION": "1"}
                if conectado and nome == "integracao"
                else ambiente
            ),
        )
        for nome, comando in gates
    ]
    return {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "modo": "CONECTADO" if conectado else "OFFLINE",
        "aprovado": all(item["sucesso"] for item in resultados),
        "resultados": resultados,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--connected", action="store_true")
    parser.add_argument("--saida", type=Path)
    argumentos = parser.parse_args()
    resultado = homologar(argumentos.connected, os.environ.copy())
    conteudo = json.dumps(resultado, ensure_ascii=False, indent=2)
    print(conteudo)
    if argumentos.saida:
        argumentos.saida.write_text(conteudo + "\n", encoding="utf-8")
    raise SystemExit(0 if resultado["aprovado"] else 1)


if __name__ == "__main__":
    main()
