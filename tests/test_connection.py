import os
import unittest
import sys
from pathlib import Path

from postgrest.exceptions import APIError

sys.path.append(str(Path(__file__).resolve().parent.parent))


@unittest.skipUnless(
    os.getenv("SDM_RUN_INTEGRATION") == "1",
    "Teste de integração desabilitado.",
)
class TestConnection(unittest.TestCase):

    def test_acesso_publico_permanece_bloqueado(self):

        from infrastructure.database.supabase_client import supabase

        with self.assertRaises(APIError) as contexto:
            supabase.table("canais_v3").select("id").limit(1).execute()

        self.assertEqual(contexto.exception.code, "42501")

    def test_service_role_acessa_supabase(self):

        from infrastructure.database.admin_client import admin

        response = admin.table("canais_v3").select("id").limit(1).execute()
        self.assertIsInstance(response.data, list)

    def test_schema_integrado_do_planejamento(self):

        from infrastructure.database.admin_client import admin

        universos = (
            admin.table("universos")
            .select("id,publico_alvo,ativo")
            .limit(1)
            .execute()
        )
        papeis = (
            admin.table("inventarios_papeis")
            .select("inventario_id,score,papel")
            .limit(1)
            .execute()
        )

        self.assertIsInstance(universos.data, list)
        self.assertIsInstance(papeis.data, list)


if __name__ == "__main__":
    unittest.main()
