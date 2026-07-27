from uuid import uuid4

from infrastructure.database.data_client import (
    get_data_client,
    using_authenticated_client,
)
from infrastructure.database.workspace_context import require_workspace


class IdentifierService:
    """Reserva códigos de cópia de forma atômica no banco."""

    @staticmethod
    def preparar_copia(origem, tabela):
        codigo = origem.get("codigo")
        if not codigo:
            raise ValueError("O registro legado ainda não possui código identificador.")
        novo_id = str(uuid4())
        cliente = get_data_client()
        if using_authenticated_client():
            if tabela == "inventarios_v3":
                resposta = cliente.rpc(
                    "proximo_codigo_copia_inventario",
                    {
                        "p_codigo_origem": codigo,
                        "p_id": novo_id,
                        "p_origem_id": origem.get("id"),
                        "p_espaco_id": require_workspace(),
                    },
                ).execute()
            elif tabela in {"projetos", "briefings_v3", "planejamentos"}:
                resposta = cliente.rpc(
                    "proximo_codigo_copia_espaco",
                    {
                        "p_codigo_origem": codigo,
                        "p_tabela": tabela,
                        "p_id": novo_id,
                        "p_origem_id": origem.get("id"),
                        "p_espaco_id": require_workspace(),
                    },
                ).execute()
            else:
                raise PermissionError(
                    "A cópia autenticada desta entidade depende da definição "
                    "de escopo global ou privado."
                )
        else:
            resposta = cliente.rpc(
                "proximo_codigo_copia",
                {"p_codigo_origem": codigo, "p_tabela": tabela, "p_id": novo_id},
            ).execute()
        novo_codigo = resposta.data
        return novo_id, novo_codigo

    @staticmethod
    def rotulo(registro, campo="nome"):
        codigo = registro.get("codigo") or str(registro.get("id", ""))[:8]
        return f"{codigo} · {registro.get(campo, 'Sem nome')}"
