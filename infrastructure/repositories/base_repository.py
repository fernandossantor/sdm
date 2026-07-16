from infrastructure.database.admin_client import admin


class BaseRepository:

    def __init__(self):

        self.db = admin

    # =====================================================
    # SELECT
    # =====================================================

    def all(

        self,

        tabela,

        campos="*"

    ):

        return (

            self.db

            .table(tabela)

            .select(campos)

            .execute()

            .data

        )

    # =====================================================
    # SELECT + ORDER
    # =====================================================

    def ordered(

        self,

        tabela,

        campo,

        campos="*"

    ):

        return (

            self.db

            .table(tabela)

            .select(campos)

            .order(campo)

            .execute()

            .data

        )

    # =====================================================
    # BY ID
    # =====================================================

    def by_id(

        self,

        tabela,

        registro_id,

        campos="*"

    ):

        return (

            self.db

            .table(tabela)

            .select(campos)

            .eq("id", registro_id)

            .single()

            .execute()

            .data

        )

    # =====================================================
    # BY FIELD
    # =====================================================

    def by_field(

        self,

        tabela,

        campo,

        valor,

        campos="*",

        single=False

    ):

        consulta = (

            self.db

            .table(tabela)

            .select(campos)

            .eq(campo, valor)

        )

        if single:

            return (

                consulta

                .single()

                .execute()

                .data

            )

        return (

            consulta

            .execute()

            .data

        )

    # =====================================================
    # INSERT
    # =====================================================

    def insert(

        self,

        tabela,

        registros

    ):

        return (

            self.db

            .table(tabela)

            .insert(registros)

            .execute()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(

        self,

        tabela,

        campo,

        valor,

        dados

    ):

        return (

            self.db

            .table(tabela)

            .update(dados)

            .eq(campo, valor)

            .execute()

        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(

        self,

        tabela,

        campo,

        valor

    ):

        return (

            self.db

            .table(tabela)

            .delete()

            .eq(campo, valor)

            .execute()

        )