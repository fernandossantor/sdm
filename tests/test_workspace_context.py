import unittest
from unittest.mock import Mock

from application.services.workspace_service import WorkspaceService
from infrastructure.database.workspace_context import (
    bind_workspace,
    clear_workspace,
    get_workspace,
)
from infrastructure.repositories.base_repository import BaseRepository


class TestWorkspaceContext(unittest.TestCase):
    def setUp(self):
        clear_workspace()

    def tearDown(self):
        clear_workspace()

    def test_selecao_rejeita_espaco_fora_da_lista_autorizada(self):
        service = WorkspaceService(Mock())

        with self.assertRaisesRegex(PermissionError, "não autorizado"):
            service.selecionar("espaco-b", [{"id": "espaco-a"}], {})

        self.assertIsNone(get_workspace())

    def test_troca_de_espaco_limpa_contexto_do_projeto(self):
        service = WorkspaceService(Mock())
        estado = {
            "espaco_id": "espaco-a",
            "projeto_id": "projeto-a",
            "plano": {"id": "plano-a"},
        }
        espacos = [
            {"id": "espaco-b", "nome": "B", "papel": "EDITOR"},
        ]

        service.selecionar("espaco-b", espacos, estado)

        self.assertEqual(get_workspace(), "espaco-b")
        self.assertNotIn("projeto_id", estado)
        self.assertNotIn("plano", estado)

    def test_insert_central_forca_espaco_ativo(self):
        cliente = Mock()
        bind_workspace("espaco-a")

        BaseRepository(cliente).insert(
            "projetos",
            {"nome": "Projeto", "espaco_id": "espaco-forjado"},
        )

        cliente.table.return_value.insert.assert_called_once_with(
            {"nome": "Projeto", "espaco_id": "espaco-a"}
        )

    def test_listagem_central_filtra_espaco_ativo(self):
        cliente = Mock()
        bind_workspace("espaco-a")
        consulta = cliente.table.return_value.select.return_value

        BaseRepository(cliente).ordered("projetos", "atualizado_em")

        consulta.eq.assert_called_once_with("espaco_id", "espaco-a")

    def test_tabela_global_nao_recebe_espaco(self):
        cliente = Mock()
        bind_workspace("espaco-a")

        BaseRepository(cliente).insert("canais_v3", {"nome": "TV"})

        cliente.table.return_value.insert.assert_called_once_with({"nome": "TV"})
