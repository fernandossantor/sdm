"""Administração de contas com autorização JWT e auditoria própria."""

import secrets
import string

from infrastructure.database.admin_client import get_admin_client
from infrastructure.database.data_client import (
    create_authenticated_client,
    create_auth_client,
)


class AccountAdminService:
    def __init__(self, actor_id, user_db, admin_db=None):
        self.actor_id = str(actor_id)
        self.user_db = user_db
        self.admin_db = admin_db or get_admin_client()
        self._autorizar()

    @classmethod
    def from_access_token(cls, access_token):
        if not str(access_token or "").strip():
            raise PermissionError("Sessão administrativa obrigatória.")
        auth = create_auth_client()
        usuario = auth.auth.get_user(access_token).user
        if not usuario:
            raise PermissionError("Sessão administrativa inválida.")
        return cls(
            actor_id=usuario.id,
            user_db=create_authenticated_client(access_token),
        )

    def _autorizar(self):
        perfil = (
            self.user_db.table("perfis_usuarios")
            .select("id,papel_global,ativo")
            .eq("id", self.actor_id)
            .single()
            .execute()
            .data
        )
        if (
            not perfil
            or not perfil.get("ativo")
            or perfil.get("papel_global") != "ADMINISTRADOR"
        ):
            raise PermissionError("Ação restrita a administrador ativo.")

    @staticmethod
    def _senha_temporaria():
        alfabeto = string.ascii_letters + string.digits + "!@#%*-_"
        return "".join(secrets.choice(alfabeto) for _ in range(24))

    def _auditar(self, acao, alvo_id, detalhes=None):
        self.admin_db.table("logs_auditoria").insert(
            {
                "ator_id": self.actor_id,
                "acao": acao,
                "alvo_tipo": "USUARIO",
                "alvo_id": str(alvo_id),
                "detalhes": detalhes or {},
            }
        ).execute()

    def listar(self):
        usuarios = self.admin_db.auth.admin.list_users(page=1, per_page=1000)
        perfis = self.admin_db.table("perfis_usuarios").select(
            "id,nome,papel_global,ativo,trocar_senha,criado_em"
        ).execute().data
        perfis_por_id = {item["id"]: item for item in perfis}
        return [
            {
                **perfis_por_id.get(str(usuario.id), {}),
                "id": str(usuario.id),
                "email": usuario.email,
                "confirmado_em": getattr(usuario, "email_confirmed_at", None),
                "ultimo_acesso_em": getattr(usuario, "last_sign_in_at", None),
            }
            for usuario in usuarios
        ]

    def criar(self, email, nome, papel_global="USUARIO"):
        if papel_global not in {"ADMINISTRADOR", "USUARIO"}:
            raise ValueError("Papel global inválido.")
        if not str(email or "").strip() or not str(nome or "").strip():
            raise ValueError("Nome e e-mail são obrigatórios.")

        senha = self._senha_temporaria()
        resposta = self.admin_db.auth.admin.create_user(
            {
                "email": email.strip().lower(),
                "password": senha,
                "email_confirm": True,
                "user_metadata": {"nome": nome.strip()},
            }
        )
        usuario = resposta.user
        try:
            self.admin_db.table("perfis_usuarios").update(
                {
                    "nome": nome.strip(),
                    "papel_global": papel_global,
                    "ativo": True,
                    "trocar_senha": True,
                }
            ).eq("id", str(usuario.id)).execute()
            self._auditar(
                "CONTA_CRIADA",
                usuario.id,
                {"papel_global": papel_global},
            )
        except Exception:
            self.admin_db.auth.admin.delete_user(str(usuario.id))
            raise
        return {"id": str(usuario.id), "senha_temporaria": senha}

    def bloquear(self, usuario_id):
        if str(usuario_id) == self.actor_id:
            raise ValueError("O administrador não pode bloquear a própria conta.")
        self.admin_db.auth.admin.update_user_by_id(
            str(usuario_id),
            {"ban_duration": "876000h"},
        )
        self.admin_db.table("perfis_usuarios").update({"ativo": False}).eq(
            "id", str(usuario_id)
        ).execute()
        self._auditar("CONTA_BLOQUEADA", usuario_id)

    def reativar(self, usuario_id):
        self.admin_db.auth.admin.update_user_by_id(
            str(usuario_id),
            {"ban_duration": "none"},
        )
        self.admin_db.table("perfis_usuarios").update({"ativo": True}).eq(
            "id", str(usuario_id)
        ).execute()
        self._auditar("CONTA_REATIVADA", usuario_id)

    def redefinir_senha(self, usuario_id):
        senha = self._senha_temporaria()
        self.admin_db.auth.admin.update_user_by_id(
            str(usuario_id),
            {"password": senha},
        )
        self.admin_db.table("perfis_usuarios").update(
            {"trocar_senha": True}
        ).eq("id", str(usuario_id)).execute()
        self._auditar("SENHA_TEMPORARIA_REDEFINIDA", usuario_id)
        return senha
