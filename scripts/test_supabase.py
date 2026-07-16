from infrastructure.database.supabase_client import supabase


print("\nPLATAFORMAS")
print(
    supabase.table("plataformas_v3")
    .select("*")
    .execute()
    .data
)


print("\nAMBIENTES")
print(
    supabase.table("ambientes_v3")
    .select("*")
    .limit(5)
    .execute()
    .data
)


print("\nFORMATOS")
print(
    supabase.table("formatos_v3")
    .select("*")
    .limit(5)
    .execute()
    .data
)