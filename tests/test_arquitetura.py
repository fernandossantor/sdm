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

    def test_fluxo_comum_nao_importa_cliente_administrativo(self):
        violacoes = []
        diretorios = (
            RAIZ / "application" / "services",
            RAIZ / "infrastructure" / "repositories",
        )

        for diretorio in diretorios:
            for arquivo in sorted(diretorio.glob("*.py")):
                arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
                for no in ast.walk(arvore):
                    if (
                        isinstance(no, ast.ImportFrom)
                        and no.module == "infrastructure.database.admin_client"
                    ):
                        violacoes.append(f"{arquivo.relative_to(RAIZ)}:{no.lineno}")

        self.assertEqual(violacoes, [])

    def test_migration_multiusuario_preserva_controles_criticos(self):
        migration = (
            RAIZ
            / "supabase"
            / "migrations"
            / "20260727030000_fundacao_multiusuario.sql"
        ).read_text(encoding="utf-8")

        for controle in (
            "create table if not exists public.membros_espacos",
            "create or replace function public.eh_membro_espaco",
            "create or replace function public.pode_editar_espaco",
            "create or replace function public.eh_proprietario_espaco",
            "O espaço de um registro não pode ser alterado",
            "grant update (nome, atualizado_em)",
            "revoke execute on function public.proximo_codigo_copia",
            "create or replace function public.confirmar_troca_senha",
        ):
            self.assertIn(controle, migration)
        self.assertNotIn(
            "grant select, update on public.perfis_usuarios",
            migration,
        )


if __name__ == "__main__":
    unittest.main()
