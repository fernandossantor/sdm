import unittest
from unittest.mock import patch

from application.services.runtime_config_service import RuntimeConfigService


class TestRuntimeConfigService(unittest.TestCase):
    def test_desenvolvimento_mantem_modo_transitorio(self):
        with patch.dict(
            "os.environ",
            {"PLANOS_ENV": "development", "PLANOS_AUTH_ENABLED": "false"},
            clear=True,
        ):
            resultado = RuntimeConfigService.validar()

        self.assertEqual(resultado["ambiente"], "development")
        self.assertFalse(resultado["autenticacao"])

    def test_producao_falha_com_autenticacao_desligada(self):
        with patch.dict(
            "os.environ",
            {"PLANOS_ENV": "production", "PLANOS_AUTH_ENABLED": "false"},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "exige"):
                RuntimeConfigService.validar()

    def test_producao_exige_chaves_distintas(self):
        with patch.dict(
            "os.environ",
            {
                "PLANOS_ENV": "production",
                "PLANOS_AUTH_ENABLED": "true",
                "SUPABASE_URL": "https://project.example",
                "SUPABASE_KEY": "mesma-chave",
                "SUPABASE_SERVICE_KEY": "mesma-chave",
            },
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "não pode"):
                RuntimeConfigService.validar()

    def test_producao_valida_configuracao_completa(self):
        with patch.dict(
            "os.environ",
            {
                "PLANOS_ENV": "production",
                "PLANOS_AUTH_ENABLED": "true",
                "SUPABASE_URL": "https://project.example",
                "SUPABASE_KEY": "sb_publishable_teste",
                "SUPABASE_SERVICE_KEY": "sb_secret_teste",
            },
            clear=True,
        ):
            resultado = RuntimeConfigService.validar()

        self.assertTrue(resultado["autenticacao"])

    def test_producao_rejeita_chaves_legadas(self):
        with patch.dict(
            "os.environ",
            {
                "PLANOS_ENV": "production",
                "PLANOS_AUTH_ENABLED": "true",
                "SUPABASE_URL": "https://project.example",
                "SUPABASE_KEY": "jwt-anon",
                "SUPABASE_SERVICE_KEY": "jwt-service-role",
            },
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "sb_publishable"):
                RuntimeConfigService.validar()


if __name__ == "__main__":
    unittest.main()
