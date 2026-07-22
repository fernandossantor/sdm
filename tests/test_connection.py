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
            .select("id,cidade,estado,ativo")
            .limit(1)
            .execute()
        )
        papeis = (
            admin.table("inventarios_papeis")
            .select("campanha_ref,inventario_id,score,papel")
            .limit(1)
            .execute()
        )
        briefings = (
            admin.table("briefings_v3")
            .select("id,alcance_objetivo,alcance_percentual")
            .limit(1)
            .execute()
        )
        segmentos = (
            admin.table("segmentos")
            .select("id,classes_sociais,faixas_etarias,escolaridades")
            .limit(1)
            .execute()
        )

        self.assertIsInstance(universos.data, list)
        self.assertIsInstance(papeis.data, list)
        self.assertIsInstance(briefings.data, list)
        self.assertIsInstance(segmentos.data, list)


if __name__ == "__main__":
    unittest.main()
