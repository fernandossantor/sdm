import unittest
from unittest.mock import Mock, patch

from application.services.identifier_service import IdentifierService
from infrastructure.database import data_client
from infrastructure.database.workspace_context import bind_workspace, clear_workspace


class TestIdentifierService(unittest.TestCase):
    def setUp(self):
        data_client.clear_request_client()
        clear_workspace()

    def tearDown(self):
        data_client.clear_request_client()
        clear_workspace()

    def test_copia_autenticada_usa_rpc_contextual(self):
        cliente = Mock()
        cliente.rpc.return_value.execute.return_value.data = "P202607000102"
        data_client._cliente_requisicao.set(cliente)
        bind_workspace("20000000-0000-0000-0000-000000000001")

        with patch(
            "application.services.identifier_service.uuid4",
            return_value="30000000-0000-0000-0000-000000000001",
        ):
            novo_id, codigo = IdentifierService.preparar_copia(
                {
                    "id": "10000000-0000-0000-0000-000000000001",
                    "codigo": "P202607000101",
                },
                "projetos",
            )

        self.assertEqual(novo_id, "30000000-0000-0000-0000-000000000001")
        self.assertEqual(codigo, "P202607000102")
        cliente.rpc.assert_called_once_with(
            "proximo_codigo_copia_espaco",
            {
                "p_codigo_origem": "P202607000101",
                "p_tabela": "projetos",
                "p_id": "30000000-0000-0000-0000-000000000001",
                "p_origem_id": "10000000-0000-0000-0000-000000000001",
                "p_espaco_id": "20000000-0000-0000-0000-000000000001",
            },
        )

    def test_copia_autenticada_global_permanece_bloqueada(self):
        data_client._cliente_requisicao.set(Mock())
        bind_workspace("espaco-a")

        with self.assertRaisesRegex(PermissionError, "escopo global ou privado"):
            IdentifierService.preparar_copia(
                {"id": "inventario-a", "codigo": "I202607000101"},
                "inventarios_v3",
            )
