"""Casos de uso da abertura da Campanha e transição para o Briefing."""

from datetime import datetime
from typing import Protocol
from uuid import UUID, uuid4

from application.dto.campanha import (
    AberturaCampanhaSaida,
    AbrirCampanhaEntrada,
    CorrigirCampanhaEntrada,
    InicioBriefingSaida,
    IniciarBriefingEntrada,
)
from domain.briefing import BriefingInicial
from domain.campanha import (
    Campanha,
    SituacaoCampanha,
    SnapshotVinculosCampanha,
)


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class AutorizadorCampanha(Protocol):
    def pode_criar(self, usuario_id: UUID) -> bool: ...

    def pode_editar(self, usuario_id: UUID, campanha_id: UUID) -> bool: ...


class ValidadorVinculosCampanha(Protocol):
    def validar(
        self,
        anunciante_id: UUID,
        marca_id: UUID | None,
        produto_servico_id: UUID | None,
    ) -> None: ...


class GeradorCodigoCampanha(Protocol):
    def proximo(self, criado_em: datetime) -> str: ...


class UnidadeTrabalhoCampanha(Protocol):
    def salvar_abertura(self, campanha: Campanha) -> None: ...

    def obter_campanha(self, campanha_id: UUID) -> Campanha | None: ...

    def corrigir_campanha(
        self, entrada: CorrigirCampanhaEntrada, atualizado_em: datetime
    ) -> None: ...

    def iniciar_briefing(
        self, campanha: Campanha, briefing: BriefingInicial
    ) -> None: ...


class AbrirCampanha:
    def __init__(
        self,
        *,
        relogio: Relogio,
        autorizador: AutorizadorCampanha,
        validador_vinculos: ValidadorVinculosCampanha,
        gerador_codigo: GeradorCodigoCampanha,
        unidade_trabalho: UnidadeTrabalhoCampanha,
    ):
        self.relogio = relogio
        self.autorizador = autorizador
        self.validador_vinculos = validador_vinculos
        self.gerador_codigo = gerador_codigo
        self.unidade_trabalho = unidade_trabalho

    def executar(self, entrada: AbrirCampanhaEntrada) -> AberturaCampanhaSaida:
        if not self.autorizador.pode_criar(entrada.criado_por):
            raise PermissionError("usuário não autorizado a criar campanha")
        self.validador_vinculos.validar(
            entrada.anunciante_id,
            entrada.marca_id,
            entrada.produto_servico_id,
        )
        agora = self.relogio.agora()
        campanha = Campanha(
            id=uuid4(),
            codigo=self.gerador_codigo.proximo(agora),
            nome=entrada.nome,
            anunciante_id=entrada.anunciante_id,
            marca_id=entrada.marca_id,
            produto_servico_id=entrada.produto_servico_id,
            planejador_responsavel_id=entrada.planejador_responsavel_id,
            equipe_ids=entrada.equipe_ids,
            observacao_inicial=entrada.observacao_inicial,
            campanha_derivada_de_id=entrada.campanha_derivada_de_id,
            snapshot=SnapshotVinculosCampanha(
                nome_anunciante=entrada.nome_anunciante,
                nome_marca=entrada.nome_marca,
                nome_produto_servico=entrada.nome_produto_servico,
                identificacao_planejador=entrada.identificacao_planejador,
            ),
            criado_por=entrada.criado_por,
            criado_em=agora,
            atualizado_em=agora,
        )
        self.unidade_trabalho.salvar_abertura(campanha)
        return AberturaCampanhaSaida(campanha=campanha)


class IniciarBriefing:
    def __init__(
        self,
        *,
        relogio: Relogio,
        autorizador: AutorizadorCampanha,
        unidade_trabalho: UnidadeTrabalhoCampanha,
    ):
        self.relogio = relogio
        self.autorizador = autorizador
        self.unidade_trabalho = unidade_trabalho

    def executar(self, entrada: IniciarBriefingEntrada) -> InicioBriefingSaida:
        if not self.autorizador.pode_editar(entrada.usuario_id, entrada.campanha_id):
            raise PermissionError("usuário não autorizado a editar campanha")
        campanha = self.unidade_trabalho.obter_campanha(entrada.campanha_id)
        if campanha is None:
            raise LookupError("campanha não encontrada")
        agora = self.relogio.agora()
        campanha_atualizada = campanha.iniciar_briefing(agora)
        briefing = BriefingInicial(
            id=uuid4(),
            campanha_id=campanha.id,
            criado_por=entrada.usuario_id,
            criado_em=agora,
        )
        self.unidade_trabalho.iniciar_briefing(campanha_atualizada, briefing)
        return InicioBriefingSaida(
            campanha=campanha_atualizada,
            briefing=briefing,
        )


class CorrigirCampanha:
    def __init__(
        self,
        *,
        relogio: Relogio,
        autorizador: AutorizadorCampanha,
        validador_vinculos: ValidadorVinculosCampanha,
        unidade_trabalho: UnidadeTrabalhoCampanha,
    ):
        self.relogio = relogio
        self.autorizador = autorizador
        self.validador_vinculos = validador_vinculos
        self.unidade_trabalho = unidade_trabalho

    def executar(self, entrada: CorrigirCampanhaEntrada) -> None:
        if not self.autorizador.pode_editar(
            entrada.alterado_por, entrada.campanha_id
        ):
            raise PermissionError("usuário não autorizado a editar campanha")
        campanha = self.unidade_trabalho.obter_campanha(entrada.campanha_id)
        if campanha is None:
            raise LookupError("campanha não encontrada")
        if campanha.situacao in {
            SituacaoCampanha.CONCLUIDA,
            SituacaoCampanha.CANCELADA,
            SituacaoCampanha.ARQUIVADA,
        }:
            raise ValueError("campanha não pode ser corrigida neste estado")
        if not entrada.nome.strip() or not entrada.nome_anunciante.strip():
            raise ValueError("nome da campanha e anunciante são obrigatórios")
        if not entrada.identificacao_planejador.strip():
            raise ValueError("planejador responsável é obrigatório")
        if not entrada.motivo.strip():
            raise ValueError("motivo da correção é obrigatório")
        self.validador_vinculos.validar(
            entrada.anunciante_id,
            entrada.marca_id,
            entrada.produto_servico_id,
        )
        self.unidade_trabalho.corrigir_campanha(
            entrada, self.relogio.agora()
        )
