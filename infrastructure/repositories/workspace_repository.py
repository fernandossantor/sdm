from infrastructure.database.data_client import get_data_client


class WorkspaceRepository:
    def __init__(self, db=None):
        self.db = db or get_data_client()

    def listar(self):
        return (
            self.db.table("espacos_trabalho")
            .select("id,nome,slug,ativo,legado,proprietario_id")
            .eq("ativo", True)
            .order("nome")
            .execute()
            .data
        )

    def papeis_do_usuario(self, usuario_id):
        return (
            self.db.table("membros_espacos")
            .select("espaco_id,papel")
            .eq("usuario_id", usuario_id)
            .execute()
            .data
        )
