import unittest
from unittest.mock import Mock

from application.services.project_sharing_service import ProjectSharingService


class TestProjectSharingService(unittest.TestCase):
    def test_normaliza_email_e_papel(self):
        db = Mock()
        db.rpc.return_value.execute.return_value.data = "usuario-1"

        resultado = ProjectSharingService(db).compartilhar(
            "projeto-1", " PESSOA@EXAMPLE.COM ", "EDITOR"
        )

        self.assertEqual(resultado, "usuario-1")
        db.rpc.assert_called_once_with(
            "compartilhar_projeto",
            {
                "p_projeto_id": "projeto-1",
                "p_email": "pessoa@example.com",
                "p_papel": "EDITOR",
            },
        )

    def test_rejeita_papel_invalido_antes_do_banco(self):
        db = Mock()
        with self.assertRaisesRegex(ValueError, "inválido"):
            ProjectSharingService(db).compartilhar(
                "projeto-1", "pessoa@example.com", "GESTOR"
            )
        db.rpc.assert_not_called()

    def test_revogacao_usa_ids_contextuais(self):
        db = Mock()
        ProjectSharingService(db).revogar("projeto-1", "usuario-1")
        db.rpc.assert_called_once_with(
            "revogar_compartilhamento_projeto",
            {
                "p_projeto_id": "projeto-1",
                "p_usuario_id": "usuario-1",
            },
        )
