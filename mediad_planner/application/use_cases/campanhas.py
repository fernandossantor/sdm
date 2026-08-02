from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from mediad_planner.application.dto.campanha import (
    CampanhaResumo,
    ContextoAcessoCampanhas,
    CriarCampanhaEntrada,
)
from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.domain.campanha.codigo import gerar_codigo_campanha
from mediad_planner.domain.campanha.entidades import Campanha
from mediad_planner.domain.campanha.vinculos import (
    AnuncianteCampanha,
    MarcaCampanha,
    ParticipanteCampanha,
    ProdutoServicoCampanha,
)
from mediad_planner.domain.common.enums import PapelAcesso


Relogio = Callable[[], datetime]
GeradorUUID = Callable[[], UUID]


def _validar_permissao_de_autoria(contexto: ContextoAcessoCampanhas) -> None:
    papeis_autorizados = (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR)
    if contexto.papel not in papeis_autorizados:
        raise PermissionError("Papel sem permissão para alterar Campanhas")


def _resumir(campanha: Campanha) -> CampanhaResumo:
    referencia = campanha.marca or campanha.anunciante
    identificacao = (
        f"[{campanha.codigo.valor}] {campanha.nome} — {referencia.nome_snapshot}"
    )
    return CampanhaResumo(
        id_campanha=campanha.id_campanha,
        codigo=campanha.codigo.valor,
        nome=campanha.nome,
        anunciante=campanha.anunciante.nome_snapshot,
        marca=campanha.marca.nome_snapshot if campanha.marca else None,
        produto_servico=(
            campanha.produto_servico.nome_snapshot
            if campanha.produto_servico
            else None
        ),
        planejador_responsavel=campanha.planejador_responsavel.nome_snapshot,
        equipe=tuple(item.nome_snapshot for item in campanha.equipe),
        observacao_inicial=campanha.observacao_inicial,
        situacao=campanha.situacao.value,
        etapa_atual=campanha.etapa_atual.value,
        criado_em=campanha.criado_em,
        atualizado_em=campanha.atualizado_em,
        identificacao_completa=identificacao,
    )


def _nomes_equipe_unicos(nomes: tuple[str, ...]) -> tuple[str, ...]:
    nomes_por_chave: dict[str, str] = {}
    for nome in nomes:
        nome_normalizado = nome.strip()
        if nome_normalizado:
            nomes_por_chave.setdefault(nome_normalizado.casefold(), nome_normalizado)
    return tuple(nomes_por_chave.values())


class CriarCampanha:
    def __init__(
        self,
        repositorio: RepositorioCampanhas,
        contexto_acesso: ContextoAcessoCampanhas,
        relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio
        self._gerador_uuid = gerador_uuid

    def executar(self, entrada: CriarCampanhaEntrada) -> CampanhaResumo:
        _validar_permissao_de_autoria(self._contexto)
        agora = self._relogio()
        sequencial = self._repositorio.reservar_proximo_sequencial_global()
        codigo = gerar_codigo_campanha(agora, sequencial)

        id_anunciante = self._gerador_uuid()
        anunciante = AnuncianteCampanha(id_anunciante, entrada.nome_anunciante)
        marca = None
        if entrada.nome_marca and entrada.nome_marca.strip():
            marca = MarcaCampanha(
                id_marca=self._gerador_uuid(),
                id_anunciante=id_anunciante,
                nome_snapshot=entrada.nome_marca,
            )
        produto_servico = None
        if entrada.nome_produto_servico and entrada.nome_produto_servico.strip():
            produto_servico = ProdutoServicoCampanha(
                id_produto_servico=self._gerador_uuid(),
                id_anunciante=id_anunciante,
                id_marca=marca.id_marca if marca else None,
                nome_snapshot=entrada.nome_produto_servico,
            )
        planejador = ParticipanteCampanha(
            id_usuario=self._gerador_uuid(),
            nome_snapshot=entrada.nome_planejador_responsavel,
        )
        equipe = tuple(
            ParticipanteCampanha(
                id_usuario=self._gerador_uuid(),
                nome_snapshot=nome,
            )
            for nome in _nomes_equipe_unicos(entrada.nomes_equipe)
        )
        campanha = Campanha.criar_rascunho(
            id_campanha=self._gerador_uuid(),
            id_espaco_trabalho=self._contexto.id_espaco_trabalho,
            codigo=codigo,
            nome=entrada.nome,
            anunciante=anunciante,
            marca=marca,
            produto_servico=produto_servico,
            planejador_responsavel=planejador,
            equipe=equipe,
            observacao_inicial=entrada.observacao_inicial,
            criado_por=self._contexto.id_usuario,
            criado_em=agora,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=agora,
        )
        if entrada.iniciar_briefing:
            campanha = campanha.iniciar_briefing(
                atualizado_por=self._contexto.id_usuario,
                atualizado_em=agora,
            )
        self._repositorio.salvar(campanha)
        return _resumir(campanha)


class IniciarBriefingCampanha:
    def __init__(
        self,
        repositorio: RepositorioCampanhas,
        contexto_acesso: ContextoAcessoCampanhas,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID) -> CampanhaResumo:
        _validar_permissao_de_autoria(self._contexto)
        campanha = self._repositorio.obter(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        if campanha is None:
            raise LookupError("Campanha não encontrada no espaço atual")
        campanha_atualizada = campanha.iniciar_briefing(
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(campanha_atualizada)
        return _resumir(campanha_atualizada)


class ListarCampanhas:
    def __init__(
        self,
        repositorio: RepositorioCampanhas,
        contexto_acesso: ContextoAcessoCampanhas,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso

    def executar(self) -> tuple[CampanhaResumo, ...]:
        papeis_autorizados = (
            PapelAcesso.PROPRIETARIO,
            PapelAcesso.EDITOR,
            PapelAcesso.LEITOR,
        )
        if self._contexto.papel not in papeis_autorizados:
            raise PermissionError("Papel sem permissão para listar Campanhas")
        campanhas = self._repositorio.listar(self._contexto.id_espaco_trabalho)
        return tuple(_resumir(campanha) for campanha in campanhas)
