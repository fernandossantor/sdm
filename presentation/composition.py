"""Composição da nova aplicação; Streamlit não instancia infraestrutura."""

from uuid import UUID

from application.services.auth_service import (
    AuthService,
    autenticacao_habilitada,
)  # noqa: F401
from application.services.campanha_runtime import (
    AutorizadorCampanhaPorEspaco,
    GeradorCodigoTemporal,
    RelogioSistema,
    ValidadorVinculosIniciais,
)
from application.use_cases import AbrirCampanha, IniciarBriefing
from infrastructure.database.data_client import (
    bind_authenticated_client,  # noqa: F401
    create_authenticated_client,
)
from infrastructure.repositories.campanha_mediad import (
    UnidadeTrabalhoCampanhaSupabase,
)

__all__ = (
    "AuthService",
    "autenticacao_habilitada",
    "bind_authenticated_client",
    "casos_de_uso_campanha",
)


def casos_de_uso_campanha(estado):
    usuario_id = UUID(estado["auth_user_id"])
    unidade = UnidadeTrabalhoCampanhaSupabase(
        cliente=create_authenticated_client(estado["auth_access_token"]),
        espaco_id=UUID(estado["espaco_id"]),
    )
    relogio = RelogioSistema()
    autorizador = AutorizadorCampanhaPorEspaco(
        usuario_id=usuario_id,
        papel_espaco=estado["espaco_papel"],
    )
    return (
        AbrirCampanha(
            relogio=relogio,
            autorizador=autorizador,
            validador_vinculos=ValidadorVinculosIniciais(),
            gerador_codigo=GeradorCodigoTemporal(),
            unidade_trabalho=unidade,
        ),
        IniciarBriefing(
            relogio=relogio,
            autorizador=autorizador,
            unidade_trabalho=unidade,
        ),
    )
