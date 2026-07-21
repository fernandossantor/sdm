"""Cliente administrativo do Supabase com inicialização tardia."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client


@lru_cache(maxsize=1)
def get_admin_client():
    """Cria o cliente apenas quando uma operação de banco é solicitada."""

    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not service_key:
        raise RuntimeError(
            "SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar configuradas "
            "para acessar o banco administrativamente."
        )

    return create_client(url, service_key)


class LazyAdminClient:
    """Proxy compatível com o antigo objeto ``admin`` global."""

    def __getattr__(self, atributo):
        return getattr(get_admin_client(), atributo)


admin = LazyAdminClient()
