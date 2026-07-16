from infrastructure.database.admin_client import admin

resultado = (
    admin
    .table("plataformas_v3")
    .select("*")
    .limit(5)
    .execute()
)

print(resultado.data)