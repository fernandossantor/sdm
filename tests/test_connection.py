import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from infrastructure.database.supabase_client import supabase

response = supabase.table("canais").select("*").execute()

print(response.data)