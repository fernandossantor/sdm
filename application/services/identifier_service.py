from uuid import uuid4

from infrastructure.database.admin_client import admin


class IdentifierService:
    """Reserva códigos de cópia de forma atômica no banco."""

    @staticmethod
    def preparar_copia(origem, tabela):
        codigo = origem.get("codigo")
        if not codigo:
            raise ValueError("O registro legado ainda não possui código identificador.")
        novo_id = str(uuid4())
        resposta = admin.rpc(
            "proximo_codigo_copia",
            {"p_codigo_origem": codigo, "p_tabela": tabela, "p_id": novo_id},
        ).execute()
        novo_codigo = resposta.data
        return novo_id, novo_codigo

    @staticmethod
    def rotulo(registro, campo="nome"):
        codigo = registro.get("codigo") or str(registro.get("id", ""))[:8]
        return f"{codigo} · {registro.get(campo, 'Sem nome')}"
