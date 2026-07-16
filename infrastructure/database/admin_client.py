from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")

service_key = os.getenv("SUPABASE_SERVICE_KEY")


admin = create_client(
    url,
    service_key
)