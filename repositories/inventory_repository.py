from infrastructure.database.admin_client import admin


class InventoryRepository:


    def listar_por_ambiente(

        self,

        ambiente_id

    ):


        r = (

            admin

            .table("inventarios_v3")

            .select("""

                id,

                nome,

                descricao,

                plataforma_id,

                ambiente_id,

                formato_id,

                estrutura_id,

                modelo_comercial_id,

                modalidade_compra_id,

                unidade_compra_id

            """)

            .eq(

                "ambiente_id",

                ambiente_id

            )

            .eq(

                "ativo",

                True

            )

            .execute()

        )


        return r.data


    def obter_metricas(

        self,

        inventario_id

    ):


        r = (

            admin

            .table(

                "inventarios_metricas_v3"

            )

            .select("*")

            .eq(

                "inventario_id",

                inventario_id

            )

            .execute()

        )


        if not r.data:

            return None


        return r.data[0]