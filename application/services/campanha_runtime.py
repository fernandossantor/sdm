"""Dependências concretas e pequenas dos casos de uso de Campanha."""

from datetime import datetime, timezone
from uuid import UUID


class RelogioSistema:
    def agora(self) -> datetime:
        return datetime.now(timezone.utc)


class AutorizadorCampanhaPorEspaco:
    """Pré-validação local; o Supabase/RLS permanece a autoridade final."""

    PAPEIS_COM_ESCRITA = {"ADMINISTRADOR", "PROPRIETARIO", "EDITOR"}

    def __init__(self, *, usuario_id: UUID, papel_espaco: str):
        self.usuario_id = usuario_id
        self.papel_espaco = str(papel_espaco or "").upper()

    def pode_criar(self, usuario_id: UUID) -> bool:
        return (
            usuario_id == self.usuario_id
            and self.papel_espaco in self.PAPEIS_COM_ESCRITA
        )

    def pode_editar(self, usuario_id: UUID, campanha_id: UUID) -> bool:
        return self.pode_criar(usuario_id)


class ValidadorVinculosIniciais:
    """Valida presença; catálogos canônicos serão uma fatia posterior."""

    def validar(
        self,
        anunciante_id: UUID,
        marca_id: UUID | None,
        produto_servico_id: UUID | None,
    ) -> None:
        if not anunciante_id:
            raise ValueError("anunciante é obrigatório")


class GeradorCodigoTemporal:
    """Gera código legível sem consultar estado global."""

    def proximo(self, criado_em: datetime) -> str:
        return criado_em.strftime("MP-%Y%m-%d%H%M%S%f")
