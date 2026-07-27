import unittest
from unittest.mock import Mock, patch

from scripts.health_check import main as health_main
from scripts.homologar import executar_comando, homologar


class TestHomologacao(unittest.TestCase):
    def test_comando_falha_quando_processo_retorna_erro(self):
        processo = Mock(returncode=2, stdout="", stderr="falha")
        with patch("scripts.homologar.subprocess.run", return_value=processo):
            resultado = executar_comando("teste", ["comando"])

        self.assertFalse(resultado["sucesso"])
        self.assertEqual(resultado["codigo"], 2)

    def test_gate_so_aprova_quando_todos_passam(self):
        with patch(
            "scripts.homologar.executar_comando",
            side_effect=[
                {"sucesso": True},
                {"sucesso": False},
                {"sucesso": True},
                {"sucesso": True},
                {"sucesso": True},
                {"sucesso": True},
            ],
        ):
            resultado = homologar(conectado=True, ambiente={})

        self.assertFalse(resultado["aprovado"])
        self.assertEqual(resultado["modo"], "CONECTADO")

    def test_health_retorna_quantidade_de_erros(self):
        with (
            patch(
                "scripts.health_check.verificar_tabela",
                side_effect=[(False, "erro")] + [(True, 1)] * 9,
            ),
            patch("builtins.print"),
        ):
            erros = health_main()

        self.assertEqual(erros, 1)


if __name__ == "__main__":
    unittest.main()
