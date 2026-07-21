import ast
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent


class TestArquitetura(unittest.TestCase):

    def test_engines_legados_foram_removidos(self):

        raiz = Path(__file__).resolve().parent.parent
        legados = (
            "briefing_engine.py",
            "decision_engine.py",
            "mcp_engine.py",
            "models.py",
            "planner_engine.py",
            "scenarios.py",
        )

        for nome in legados:
            self.assertFalse((raiz / "engine" / nome).exists(), nome)

    def test_paginas_nao_importam_camadas_internas(self):

        prefixos_proibidos = ("engine", "infrastructure", "repositories")
        violacoes = []

        for arquivo in sorted((RAIZ / "pages").glob("*.py")):
            arvore = ast.parse(arquivo.read_text(encoding="utf-8"))

            for no in ast.walk(arvore):
                if isinstance(no, ast.ImportFrom) and no.module:
                    if no.module.startswith(prefixos_proibidos):
                        violacoes.append(f"{arquivo.name}:{no.lineno} {no.module}")
                elif isinstance(no, ast.Import):
                    for nome in no.names:
                        if nome.name.startswith(prefixos_proibidos):
                            violacoes.append(
                                f"{arquivo.name}:{no.lineno} {nome.name}"
                            )

        self.assertEqual(violacoes, [])

    def test_namespace_antigo_de_repositorios_foi_removido(self):

        self.assertFalse((RAIZ / "repositories").exists())


if __name__ == "__main__":
    unittest.main()
