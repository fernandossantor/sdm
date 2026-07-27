import os
import time
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from application.services.auth_service import AuthService, autenticacao_habilitada


def sessao(expira_em=None):
    usuario = SimpleNamespace(id="user-1", email="user@example.com")
    return SimpleNamespace(
        access_token="access",
        refresh_token="refresh",
        expires_at=expira_em or time.time() + 3600,
        user=usuario,
    )


class TestAuthService(unittest.TestCase):
    def test_autenticacao_fica_desabilitada_por_padrao(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(autenticacao_habilitada())

    def test_login_salva_somente_dados_da_sessao(self):
        cliente = Mock()
        cliente.auth.sign_in_with_password.return_value = SimpleNamespace(
            session=sessao(),
            user=SimpleNamespace(id="user-1"),
        )
        consulta = cliente.table.return_value.select.return_value
        consulta.eq.return_value.single.return_value.execute.return_value = (
            SimpleNamespace(data={"ativo": True, "trocar_senha": True})
        )
        estado = {}

        AuthService(lambda: cliente).entrar(
            " user@example.com ", "segredo-forte", estado
        )

        self.assertEqual(estado["auth_access_token"], "access")
        self.assertEqual(estado["auth_user_id"], "user-1")
        self.assertTrue(estado["auth_trocar_senha"])
        self.assertNotIn("senha", estado)
        cliente.auth.sign_in_with_password.assert_called_once_with(
            {"email": "user@example.com", "password": "segredo-forte"}
        )

    def test_sessao_valida_nao_faz_chamada_remota(self):
        fabrica = Mock()
        estado = {
            "auth_access_token": "access",
            "auth_refresh_token": "refresh",
            "auth_expires_at": time.time() + 3600,
        }

        self.assertTrue(AuthService(fabrica).renovar_se_necessario(estado))
        fabrica.assert_not_called()

    def test_sessao_expirada_e_renovada(self):
        cliente = Mock()
        cliente.auth.set_session.return_value = SimpleNamespace(session=sessao())
        estado = {
            "auth_access_token": "old",
            "auth_refresh_token": "refresh",
            "auth_expires_at": time.time() - 1,
        }

        self.assertTrue(
            AuthService(lambda: cliente).renovar_se_necessario(estado)
        )
        self.assertEqual(estado["auth_access_token"], "access")

    def test_falha_na_renovacao_limpa_credenciais(self):
        cliente = Mock()
        cliente.auth.set_session.side_effect = RuntimeError("expirada")
        estado = {
            "auth_access_token": "old",
            "auth_refresh_token": "refresh",
            "auth_expires_at": time.time() - 1,
        }

        self.assertFalse(
            AuthService(lambda: cliente).renovar_se_necessario(estado)
        )
        self.assertNotIn("auth_access_token", estado)

    def test_senha_nova_exige_oito_caracteres(self):
        with self.assertRaisesRegex(ValueError, "8 caracteres"):
            AuthService(Mock()).alterar_senha("curta", {})

    def test_alteracao_confirma_fim_da_senha_temporaria(self):
        cliente = Mock()
        estado = {
            "auth_access_token": "access",
            "auth_refresh_token": "refresh",
            "auth_trocar_senha": True,
        }

        AuthService(lambda: cliente).alterar_senha("nova-senha", estado)

        cliente.auth.update_user.assert_called_once_with(
            {"password": "nova-senha"}
        )
        cliente.rpc.assert_called_once_with("confirmar_troca_senha")
        self.assertFalse(estado["auth_trocar_senha"])
