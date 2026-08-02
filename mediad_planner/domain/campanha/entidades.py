from dataclasses import dataclass, replace
from datetime import datetime
from uuid import UUID

from mediad_planner.domain.campanha.codigo import CodigoCampanha
from mediad_planner.domain.campanha.enums import EtapaCampanha, SituacaoCampanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    MarcaCampanha,
    ParticipanteCampanha,
    ProdutoServicoCampanha,
)


def _exigir_fuso(valor: datetime, campo: str) -> None:
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ValueError(f"{campo} deve possuir fuso horário")


@dataclass(frozen=True, slots=True)
class Campanha:
    id_campanha: UUID
    id_espaco_trabalho: UUID
    codigo: CodigoCampanha
    nome: str
    anunciante: AnuncianteCampanha
    marca: MarcaCampanha | None
    produto_servico: ProdutoServicoCampanha | None
    planejador_responsavel: ParticipanteCampanha
    equipe: tuple[ParticipanteCampanha, ...]
    observacao_inicial: str | None
    situacao: SituacaoCampanha
    etapa_atual: EtapaCampanha
    id_campanha_origem: UUID | None
    criado_por: UUID
    criado_em: datetime
    atualizado_por: UUID
    atualizado_em: datetime

    def __post_init__(self) -> None:
        nome_normalizado = self.nome.strip()
        if not nome_normalizado:
            raise ValueError("nome não pode ser vazio")
        if self.anunciante is None:
            raise ValueError("anunciante é obrigatório")
        if self.planejador_responsavel is None:
            raise ValueError("planejador_responsavel é obrigatório")
        _exigir_fuso(self.criado_em, "criado_em")
        _exigir_fuso(self.atualizado_em, "atualizado_em")
        if self.atualizado_em < self.criado_em:
            raise ValueError("atualizado_em não pode anteceder criado_em")

        equipe = tuple(self.equipe)
        ids_equipe = {participante.id_usuario for participante in equipe}
        if len(ids_equipe) != len(equipe):
            raise ValueError("equipe contém IDs duplicados")
        if self.marca is not None:
            if self.marca.id_anunciante != self.anunciante.id_anunciante:
                raise ValueError("marca não pertence ao anunciante da Campanha")
        if self.produto_servico is not None:
            produto = self.produto_servico
            if produto.id_anunciante != self.anunciante.id_anunciante:
                raise ValueError("produto ou serviço não pertence ao anunciante")
            if produto.id_marca is not None:
                if self.marca is None or produto.id_marca != self.marca.id_marca:
                    raise ValueError("produto ou serviço pertence a outra marca")

        observacao = self.observacao_inicial
        observacao_normalizada = observacao.strip() if observacao else None
        object.__setattr__(self, "nome", nome_normalizado)
        object.__setattr__(self, "equipe", equipe)
        object.__setattr__(self, "observacao_inicial", observacao_normalizada or None)

    @classmethod
    def criar_rascunho(
        cls,
        *,
        id_campanha: UUID,
        id_espaco_trabalho: UUID,
        codigo: CodigoCampanha,
        nome: str,
        anunciante: AnuncianteCampanha,
        marca: MarcaCampanha | None,
        produto_servico: ProdutoServicoCampanha | None,
        planejador_responsavel: ParticipanteCampanha,
        equipe: tuple[ParticipanteCampanha, ...],
        observacao_inicial: str | None,
        criado_por: UUID,
        criado_em: datetime,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Campanha":
        return cls(
            id_campanha=id_campanha,
            id_espaco_trabalho=id_espaco_trabalho,
            codigo=codigo,
            nome=nome,
            anunciante=anunciante,
            marca=marca,
            produto_servico=produto_servico,
            planejador_responsavel=planejador_responsavel,
            equipe=equipe,
            observacao_inicial=observacao_inicial,
            situacao=SituacaoCampanha.RASCUNHO,
            etapa_atual=EtapaCampanha.ABERTURA,
            id_campanha_origem=None,
            criado_por=criado_por,
            criado_em=criado_em,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )

    def iniciar_briefing(
        self,
        atualizado_por: UUID,
        atualizado_em: datetime,
    ) -> "Campanha":
        if (
            self.situacao is not SituacaoCampanha.RASCUNHO
            or self.etapa_atual is not EtapaCampanha.ABERTURA
        ):
            raise ValueError("Campanha não está apta a iniciar o Briefing")
        _exigir_fuso(atualizado_em, "atualizado_em")
        if atualizado_em < self.criado_em:
            raise ValueError("atualizado_em não pode anteceder criado_em")
        return replace(
            self,
            situacao=SituacaoCampanha.EM_ANDAMENTO,
            etapa_atual=EtapaCampanha.BRIEFING,
            atualizado_por=atualizado_por,
            atualizado_em=atualizado_em,
        )
