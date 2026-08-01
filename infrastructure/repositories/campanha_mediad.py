"""Adaptador Supabase novo para a unidade de trabalho Campanha/Briefing."""

from datetime import datetime
from typing import Any
from uuid import UUID

from application.dto import CorrigirCampanhaEntrada

from domain.briefing import BriefingInicial, ConteudoBriefing
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

    def corrigir_campanha(
        self, entrada: CorrigirCampanhaEntrada, atualizado_em: datetime
    ) -> None:
        alteracoes = {
            "nome": entrada.nome.strip(),
            "anunciante_id": str(entrada.anunciante_id),
            "marca_id": str(entrada.marca_id) if entrada.marca_id else None,
            "produto_servico_id": (
                str(entrada.produto_servico_id)
                if entrada.produto_servico_id
                else None
            ),
            "planejador_responsavel_id": str(
                entrada.planejador_responsavel_id
            ),
            "observacao_inicial": entrada.observacao_inicial,
            "nome_anunciante_atual": entrada.nome_anunciante.strip(),
            "nome_marca_atual": entrada.nome_marca,
            "nome_produto_servico_atual": entrada.nome_produto_servico,
            "identificacao_planejador_atual": (
                entrada.identificacao_planejador.strip()
            ),
        }
        self.cliente.rpc(
            "atualizar_campanha_mediad",
            {
                "p_campanha_id": str(entrada.campanha_id),
                "p_espaco_id": str(self.espaco_id),
                "p_alteracoes": alteracoes,
                "p_motivo": entrada.motivo.strip(),
                "p_usuario_id": str(entrada.alterado_por),
                "p_instante": atualizado_em.isoformat(),
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
            .select("id,codigo,nome,anunciante_id,marca_id,produto_servico_id,planejador_responsavel_id,observacao_inicial,campanha_derivada_de_id,snapshot_nome_anunciante,snapshot_nome_marca,snapshot_nome_produto_servico,snapshot_identificacao_planejador,nome_anunciante_atual,nome_marca_atual,nome_produto_servico_atual,identificacao_planejador_atual,criado_por,criado_em,atualizado_em,situacao,etapa_atual")
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

    def obter_briefing(self, briefing_id: UUID) -> BriefingInicial | None:
        resposta = (
            self.cliente.table("briefings_mediad")
            .select("*")
            .eq("id", str(briefing_id))
            .eq("espaco_id", str(self.espaco_id))
            .limit(1)
            .execute()
        )
        if not resposta.data:
            return None
        registro = resposta.data[0]
        return BriefingInicial(
            id=registro["id"],
            campanha_id=registro["campanha_id"],
            versao=registro["versao"],
            estado=registro["estado"],
            criado_por=registro["criado_por"],
            criado_em=registro["criado_em"],
            conteudo=ConteudoBriefing.model_validate(registro.get("conteudo") or {}),
            atualizado_por=registro.get("atualizado_por"),
            atualizado_em=registro.get("atualizado_em"),
            motivo_ultima_alteracao=registro.get("motivo_ultima_alteracao"),
        )

    def listar_versoes_briefing(self, campanha_id: UUID) -> list[dict[str, Any]]:
        resposta = (
            self.cliente.table("briefings_mediad")
            .select("id,versao,estado,criado_por,criado_em,atualizado_por,atualizado_em,motivo_ultima_alteracao")
            .eq("campanha_id", str(campanha_id))
            .eq("espaco_id", str(self.espaco_id))
            .order("versao", desc=True)
            .execute()
        )
        return list(resposta.data or [])

    def salvar_edicao(self, anterior, atualizado, motivo) -> None:
        self.cliente.rpc("editar_briefing_mediad", {
            "p_briefing_id": str(anterior.id),
            "p_espaco_id": str(self.espaco_id),
            "p_conteudo": atualizado.conteudo.model_dump(mode="json"),
            "p_motivo": motivo,
            "p_usuario_id": str(atualizado.atualizado_por),
            "p_instante": atualizado.atualizado_em.isoformat(),
        }).execute()

    def salvar_nova_versao(self, anterior, nova, motivo) -> None:
        self.cliente.rpc("versionar_briefing_mediad", {
            "p_briefing_origem_id": str(anterior.id),
            "p_novo_briefing_id": str(nova.id),
            "p_espaco_id": str(self.espaco_id),
            "p_conteudo": nova.conteudo.model_dump(mode="json"),
            "p_motivo": motivo,
            "p_usuario_id": str(nova.criado_por),
            "p_instante": nova.criado_em.isoformat(),
        }).execute()

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
