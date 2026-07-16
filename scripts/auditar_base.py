from infrastructure.database.admin_client import admin


def carregar(nome):

    return (

        admin

        .table(nome)

        .select("*")

        .execute()

        .data

    )


def ids(dados, campo):

    return {

        item[campo]

        for item in dados

    }


def main():

    print()

    print("=" * 80)

    print("SDM - AUDITORIA DA BASE")

    print("=" * 80)

    print()

    inventarios = carregar(

        "inventarios_v3"

    )

    objetivos = carregar(

        "objetivos_campanha_v3"

    )

    kpis = carregar(

        "kpis_v3"

    )

    inv_obj = carregar(

        "inventarios_objetivos_v3"

    )

    inv_kpi = carregar(

        "inventarios_kpis_v3"

    )

    metricas = carregar(

        "inventarios_metricas_v3"

    )

    consumo = carregar(

        "consumo_midia_v3"

    )

    ambientes = ids(

        inventarios,

        "ambiente_id"

    )

    inventario_ids = ids(

        inventarios,

        "id"

    )

    objetivo_ids = ids(

        objetivos,

        "id"

    )

    kpi_ids = ids(

        kpis,

        "id"

    )

    obj_inv = {

        r["inventario_id"]

        for r in inv_obj

    }

    kpi_inv = {

        r["inventario_id"]

        for r in inv_kpi

    }

    metrica_inv = {

        r["inventario_id"]

        for r in metricas

    }

    consumo_amb = {

        r["ambiente_id"]

        for r in consumo

    }

    print("INVENTÁRIOS")

    print("-" * 80)

    for inv in inventarios:

        problemas = []

        if inv["id"] not in obj_inv:

            problemas.append(

                "Sem objetivo"

            )

        if inv["id"] not in kpi_inv:

            problemas.append(

                "Sem KPI"

            )

        if inv["id"] not in metrica_inv:

            problemas.append(

                "Sem métricas"

            )

        if problemas:

            print(

                f'{inv["nome"]}: '

                + ", ".join(problemas)

            )

    print()

    print("OBJETIVOS SEM RELAÇÃO")

    print("-" * 80)

    usados = {

        r["objetivo_id"]

        for r in inv_obj

    }

    for obj in objetivos:

        if obj["id"] not in usados:

            print(

                obj["nome"]

            )

    print()

    print("KPIs SEM RELAÇÃO")

    print("-" * 80)

    usados = {

        r["kpi_id"]

        for r in inv_kpi

    }

    for kpi in kpis:

        if kpi["id"] not in usados:

            print(

                kpi["nome"]

            )

    print()

    print("AMBIENTES SEM CONSUMO")

    print("-" * 80)

    for ambiente in sorted(

        ambientes

    ):

        if ambiente not in consumo_amb:

            print(

                ambiente

            )

    print()

    print("REGISTROS ÓRFÃOS")

    print("-" * 80)

    for r in inv_obj:

        if (

            r["inventario_id"]

            not in inventario_ids

        ):

            print(

                "inventarios_objetivos -> inventário inexistente:",

                r["inventario_id"]

            )

        if (

            r["objetivo_id"]

            not in objetivo_ids

        ):

            print(

                "inventarios_objetivos -> objetivo inexistente:",

                r["objetivo_id"]

            )

    for r in inv_kpi:

        if (

            r["inventario_id"]

            not in inventario_ids

        ):

            print(

                "inventarios_kpis -> inventário inexistente:",

                r["inventario_id"]

            )

        if (

            r["kpi_id"]

            not in kpi_ids

        ):

            print(

                "inventarios_kpis -> KPI inexistente:",

                r["kpi_id"]

            )

    print()

    print("=" * 80)

    print("AUDITORIA FINALIZADA")

    print("=" * 80)


if __name__ == "__main__":

    main()