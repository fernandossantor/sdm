import os
import unittest
from unittest.mock import Mock, patch

from infrastructure.database import data_client
from infrastructure.database.admin_client import admin
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.repositories.briefing_repository import BriefingRepository


class TestDataClient(unittest.TestCase):

    def setUp(self):
        data_client.clear_request_client()
        data_client.get_public_client.cache_clear()

    def tearDown(self):
        data_client.clear_request_client()
        data_client.get_public_client.cache_clear()

    @staticmethod
    def _ambiente():
        return patch.dict(
            os.environ,
            {
                "SUPABASE_URL": "https://project.example",
                "SUPABASE_KEY": "anon-key",
            },
        )

    def test_cliente_autenticado_aplica_jwt_ao_postgrest(self):
        cliente = Mock()

        with (
            self._ambiente(),
            patch.object(data_client, "create_client", return_value=cliente)
            as criar,
        ):
            resultado = data_client.create_authenticated_client("jwt-user")

        self.assertIs(resultado, cliente)
        criar.assert_called_once_with("https://project.example", "anon-key")
        cliente.postgrest.auth.assert_called_once_with("jwt-user")

    def test_token_vazio_e_rejeitado_sem_criar_cliente(self):
        with patch.object(data_client, "create_client") as criar:
            with self.assertRaisesRegex(ValueError, "Token de acesso"):
                data_client.create_authenticated_client("")

        criar.assert_not_called()

    def test_repository_usa_cliente_vinculado_a_requisicao(self):
        cliente = Mock()
        with (
            self._ambiente(),
            patch.object(data_client, "create_client", return_value=cliente),
        ):
            data_client.bind_authenticated_client("jwt-user")
            repository = BaseRepository()

        self.assertIs(repository.db, cliente)
        self.assertTrue(data_client.using_authenticated_client())

    def test_fallback_administrativo_permanece_explicito_na_transicao(self):
        self.assertIs(data_client.get_data_client(), admin)
        self.assertFalse(data_client.using_authenticated_client())

    def test_repository_aceita_injecao_direta(self):
        cliente = Mock()

        self.assertIs(BriefingRepository(cliente).db, cliente)
