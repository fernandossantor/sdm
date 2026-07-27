import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from application.admin.account_admin_service import AccountAdminService


def consulta_perfil(user_db, papel="ADMINISTRADOR", ativo=True):
    (
        user_db.table.return_value.select.return_value.eq.return_value
        .single.return_value.execute.return_value
    ) = SimpleNamespace(
        data={"id": "ator-1", "papel_global": papel, "ativo": ativo}
    )


class TestAccountAdminService(unittest.TestCase):
    def test_rejeita_usuario_comum_antes_de_acessar_service_role(self):
        user_db = Mock()
        consulta_perfil(user_db, papel="USUARIO")

        with self.assertRaisesRegex(PermissionError, "administrador ativo"):
            AccountAdminService("ator-1", user_db, Mock())

    def test_cria_conta_com_senha_temporaria_e_auditoria(self):
        user_db = Mock()
        admin_db = Mock()
        consulta_perfil(user_db)
        admin_db.auth.admin.create_user.return_value = SimpleNamespace(
            user=SimpleNamespace(id="usuario-1")
        )

        with patch.object(
            AccountAdminService,
            "_senha_temporaria",
            return_value="senha-segura-temporaria",
        ):
            resultado = AccountAdminService(
                "ator-1", user_db, admin_db
            ).criar(" NOVO@EXAMPLE.COM ", " Novo Usuário ")

        self.assertEqual(resultado["id"], "usuario-1")
        self.assertEqual(
            resultado["senha_temporaria"], "senha-segura-temporaria"
        )
        admin_db.auth.admin.create_user.assert_called_once_with(
            {
                "email": "novo@example.com",
                "password": "senha-segura-temporaria",
                "email_confirm": True,
                "user_metadata": {"nome": "Novo Usuário"},
            }
        )
        chamadas = admin_db.table.call_args_list
        self.assertIn("logs_auditoria", [item.args[0] for item in chamadas])

    def test_nao_permite_autobloqueio(self):
        user_db = Mock()
        consulta_perfil(user_db)
        service = AccountAdminService("ator-1", user_db, Mock())

        with self.assertRaisesRegex(ValueError, "própria conta"):
            service.bloquear("ator-1")

    def test_redefinicao_nao_registra_senha_na_auditoria(self):
        user_db = Mock()
        admin_db = Mock()
        consulta_perfil(user_db)
        service = AccountAdminService("ator-1", user_db, admin_db)

        with patch.object(
            service,
            "_senha_temporaria",
            return_value="outra-senha-segura",
        ):
            self.assertEqual(
                service.redefinir_senha("usuario-2"),
                "outra-senha-segura",
            )

        insercao = (
            admin_db.table.return_value.insert.call_args.args[0]
        )
        self.assertEqual(insercao["detalhes"], {})
        self.assertNotIn("senha_temporaria", insercao)
