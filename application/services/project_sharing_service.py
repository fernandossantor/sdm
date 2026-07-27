"""Compartilhamento de projetos executado somente com o JWT do usuário."""

from infrastructure.database.data_client import create_authenticated_client


class ProjectSharingService:
    def __init__(self, db):
        self.db = db

    @classmethod
    def from_access_token(cls, access_token):
        return cls(create_authenticated_client(access_token))

    def listar(self, projeto_id):
        resposta = self.db.rpc(
            "listar_compartilhamentos_projeto",
            {"p_projeto_id": str(projeto_id)},
        ).execute()
        return resposta.data or []

    def compartilhar(self, projeto_id, email, papel):
        if papel not in {"PROPRIETARIO", "EDITOR", "LEITOR"}:
            raise ValueError("Papel de projeto inválido.")
        if not str(email or "").strip():
            raise ValueError("Informe o e-mail do usuário cadastrado.")
        return self.db.rpc(
            "compartilhar_projeto",
            {
                "p_projeto_id": str(projeto_id),
                "p_email": email.strip().lower(),
                "p_papel": papel,
            },
        ).execute().data

    def revogar(self, projeto_id, usuario_id):
        return self.db.rpc(
            "revogar_compartilhamento_projeto",
            {
                "p_projeto_id": str(projeto_id),
                "p_usuario_id": str(usuario_id),
            },
        ).execute()
