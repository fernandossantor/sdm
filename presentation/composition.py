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
from application.use_cases import AbrirCampanha, CorrigirCampanha, IniciarBriefing
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
    "caso_de_uso_correcao_campanha",
    "campanhas_do_espaco",
    "briefing_da_campanha",
)


def _unidade_campanha(estado):
    return UnidadeTrabalhoCampanhaSupabase(
        cliente=create_authenticated_client(estado["auth_access_token"]),
        espaco_id=UUID(estado["espaco_id"]),
    )


def campanhas_do_espaco(estado):
    return _unidade_campanha(estado).listar_campanhas()


def briefing_da_campanha(estado, campanha_id):
    return _unidade_campanha(estado).obter_briefing_id(UUID(campanha_id))


def casos_de_uso_campanha(estado):
    unidade = _unidade_campanha(estado)
    usuario_id = UUID(estado["auth_user_id"])
    relogio = RelogioSistema()
    autorizador = AutorizadorCampanhaPorEspaco(
        usuario_id=usuario_id, papel_espaco=estado["espaco_papel"]
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

def caso_de_uso_correcao_campanha(estado):
    unidade = _unidade_campanha(estado)
    usuario_id = UUID(estado["auth_user_id"])
    return CorrigirCampanha(
        relogio=RelogioSistema(),
        autorizador=AutorizadorCampanhaPorEspaco(
            usuario_id=usuario_id, papel_espaco=estado["espaco_papel"]
        ),
        validador_vinculos=ValidadorVinculosIniciais(),
        unidade_trabalho=unidade,
    )
