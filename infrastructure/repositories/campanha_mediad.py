"""Adaptador Supabase novo para a unidade de trabalho Campanha/Briefing."""

from typing import Any
from uuid import UUID

from domain.briefing import BriefingInicial
from domain.campanha import (
    Campanha,
    EtapaCampanha,
    SituacaoCampanha,
    SnapshotVinculosCampanha,
)


class UnidadeTrabalhoCampanhaSupabase:
    """Persiste a fatia canônica usando RPCs transacionais e cliente injetado."""

    def __init__(self, *, cliente: Any, espaco_id: UUID):
        self.cliente = cliente
        self.espaco_id = espaco_id

    @staticmethod
    def _serializar_campanha(campanha: Campanha) -> dict[str, Any]:
        return {
            "id": str(campanha.id),
            "codigo": campanha.codigo,
            "nome": campanha.nome,
            "anunciante_id": str(campanha.anunciante_id),
            "marca_id": str(campanha.marca_id) if campanha.marca_id else None,
            "produto_servico_id": (
                str(campanha.produto_servico_id)
                if campanha.produto_servico_id
                else None
            ),
            "planejador_responsavel_id": str(campanha.planejador_responsavel_id),
            "equipe_ids": [str(item) for item in campanha.equipe_ids],
            "observacao_inicial": campanha.observacao_inicial,
            "campanha_derivada_de_id": (
                str(campanha.campanha_derivada_de_id)
                if campanha.campanha_derivada_de_id
                else None
            ),
            "snapshot_nome_anunciante": campanha.snapshot.nome_anunciante,
            "snapshot_nome_marca": campanha.snapshot.nome_marca,
            "snapshot_nome_produto_servico": (campanha.snapshot.nome_produto_servico),
            "snapshot_identificacao_planejador": (
                campanha.snapshot.identificacao_planejador
            ),
            "criado_por": str(campanha.criado_por),
            "criado_em": campanha.criado_em.isoformat(),
            "atualizado_em": campanha.atualizado_em.isoformat(),
            "situacao": campanha.situacao.value,
            "etapa_atual": campanha.etapa_atual.value,
        }

    @staticmethod
    def _desserializar_campanha(
        registro: dict[str, Any], equipe_ids: tuple[UUID, ...]
    ) -> Campanha:
        return Campanha(
            id=registro["id"],
            codigo=registro["codigo"],
            nome=registro["nome"],
            anunciante_id=registro["anunciante_id"],
            marca_id=registro.get("marca_id"),
            produto_servico_id=registro.get("produto_servico_id"),
            planejador_responsavel_id=registro["planejador_responsavel_id"],
            equipe_ids=equipe_ids,
            observacao_inicial=registro.get("observacao_inicial"),
            campanha_derivada_de_id=registro.get("campanha_derivada_de_id"),
            snapshot=SnapshotVinculosCampanha(
                nome_anunciante=registro["snapshot_nome_anunciante"],
                nome_marca=registro.get("snapshot_nome_marca"),
                nome_produto_servico=registro.get("snapshot_nome_produto_servico"),
                identificacao_planejador=registro["snapshot_identificacao_planejador"],
            ),
            criado_por=registro["criado_por"],
            criado_em=registro["criado_em"],
            atualizado_em=registro["atualizado_em"],
            situacao=registro["situacao"],
            etapa_atual=registro["etapa_atual"],
        )

    def salvar_abertura(self, campanha: Campanha) -> None:
        if campanha.situacao is not SituacaoCampanha.RASCUNHO:
            raise ValueError("abertura deve persistir campanha em rascunho")
        if campanha.etapa_atual is not EtapaCampanha.ABERTURA:
            raise ValueError("abertura deve persistir etapa de abertura")
        self.cliente.rpc(
            "abrir_campanha_mediad",
            {
                "p_campanha": self._serializar_campanha(campanha),
                "p_espaco_id": str(self.espaco_id),
            },
        ).execute()

    def obter_campanha(self, campanha_id: UUID) -> Campanha | None:
        resposta = (
            self.cliente.table("campanhas_mediad")
            .select("*")
            .eq("id", str(campanha_id))
            .eq("espaco_id", str(self.espaco_id))
            .limit(1)
            .execute()
        )
        if not resposta.data:
            return None
        resposta_equipe = (
            self.cliente.table("campanhas_mediad_equipe")
            .select("usuario_id")
            .eq("campanha_id", str(campanha_id))
            .order("usuario_id")
            .execute()
        )
        equipe_ids = tuple(
            UUID(registro["usuario_id"]) for registro in resposta_equipe.data
        )
        return self._desserializar_campanha(resposta.data[0], equipe_ids)

    def listar_campanhas(self) -> list[dict[str, Any]]:
        """Lista campanhas do espaço para permitir retomada explícita."""
        resposta = (
            self.cliente.table("campanhas_mediad")
            .select("id,codigo,nome,anunciante_id,marca_id,produto_servico_id,planejador_responsavel_id,observacao_inicial,campanha_derivada_de_id,snapshot_nome_anunciante,snapshot_nome_marca,snapshot_nome_produto_servico,snapshot_identificacao_planejador,criado_por,criado_em,atualizado_em,situacao,etapa_atual")
            .eq("espaco_id", str(self.espaco_id))
            .order("atualizado_em", desc=True)
            .execute()
        )
        return list(resposta.data or [])

    def obter_briefing_id(self, campanha_id: UUID) -> str | None:
        resposta = (
            self.cliente.table("briefings_mediad")
            .select("id")
            .eq("campanha_id", str(campanha_id))
            .order("versao", desc=True)
            .limit(1)
            .execute()
        )
        return resposta.data[0]["id"] if resposta.data else None

    def iniciar_briefing(self, campanha: Campanha, briefing: BriefingInicial) -> None:
        if campanha.id != briefing.campanha_id:
            raise ValueError("briefing pertence a outra campanha")
        if campanha.situacao is not SituacaoCampanha.EM_ANDAMENTO:
            raise ValueError("campanha deve estar em andamento")
        if campanha.etapa_atual is not EtapaCampanha.BRIEFING:
            raise ValueError("campanha deve estar na etapa de briefing")
        if campanha.atualizado_em != briefing.criado_em:
            raise ValueError("transição deve compartilhar o mesmo instante")
        self.cliente.rpc(
            "iniciar_briefing_mediad",
            {
                "p_campanha_id": str(campanha.id),
                "p_espaco_id": str(self.espaco_id),
                "p_briefing_id": str(briefing.id),
                "p_usuario_id": str(briefing.criado_por),
                "p_instante": briefing.criado_em.isoformat(),
            },
        ).execute()
