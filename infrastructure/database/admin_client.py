from dotenv import load_dotenv
import os

from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


class SupabaseNotConfiguredError(RuntimeError):
    """Erro emitido quando o Supabase admin é usado sem credenciais."""


class LazySupabaseClient:
    """Inicializa o client admin do Supabase apenas quando ele é usado."""

    def __init__(self, supabase_url=None, supabase_key=None):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self._client = None

    def _get_client(self):
        if not self.supabase_url or not self.supabase_key:
            raise SupabaseNotConfiguredError(
                "Supabase admin não configurado. "
                "Defina SUPABASE_URL e SUPABASE_SERVICE_KEY."
            )

        if self._client is None:
            self._client = create_client(
                self.supabase_url,
                self.supabase_key,
            )

        return self._client

    def __getattr__(self, name):
        return getattr(
            self._get_client(),
            name,
        )


admin = LazySupabaseClient(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY,
)
