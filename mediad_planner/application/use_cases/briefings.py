from collections.abc import Callable
from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from mediad_planner.application.dto.briefing import (
    AdicionarRegistroSituacaoEntrada,
    AspectoSituacaoResumo,
    BriefingResumo,
    ContextoAcessoBriefings,
    RegistroSituacaoResumo,
)
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.domain.briefing.contexto import ContextoHerdadoBriefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.situacao_mercadologica import (
    EscopoSituacaoMercadologica,
    NaturezaRegistroSituacao,
    RegistroSituacaoMercadologica,
    listar_aspectos_iniciais,
)
from mediad_planner.domain.campanha.enums import EtapaCampanha, SituacaoCampanha
from mediad_planner.domain.common.enums import PapelAcesso


Relogio = Callable[[], datetime]
GeradorUUID = Callable[[], UUID]


def _resumir(briefing: Briefing) -> BriefingResumo:
    contexto = briefing.contexto_herdado
    registros = tuple(
        RegistroSituacaoResumo(
            id_registro=registro.id_registro,
            escopo=registro.escopo.value,
            codigo_aspecto=registro.codigo_aspecto,
            aspecto=registro.aspecto,
            entidade_referencia=registro.entidade_referencia,
            natureza=registro.natureza.value,
            valor_quantitativo=(
                format(registro.valor_quantitativo, "f")
                if registro.valor_quantitativo is not None
                else None
            ),
            unidade=registro.unidade,
            valor_qualitativo=registro.valor_qualitativo,
            fonte=registro.fonte,
            periodo_referencia=registro.periodo_referencia,
            observacao=registro.observacao,
        )
        for registro in briefing.situacao_mercadologica.registros
    )
    return BriefingResumo(
        id_briefing=briefing.id_briefing,
        id_campanha=briefing.id_campanha,
        numero_versao=briefing.numero_versao,
        estado=briefing.estado.value,
        codigo_campanha=contexto.codigo_campanha.valor,
        nome_campanha=contexto.nome_campanha,
        anunciante=contexto.anunciante.nome_snapshot,
        marca=contexto.marca.nome_snapshot if contexto.marca else None,
        produto_servico=(
            contexto.produto_servico.nome_snapshot
            if contexto.produto_servico
            else None
        ),
        planejador_responsavel=contexto.planejador_responsavel.nome_snapshot,
        equipe=tuple(item.nome_snapshot for item in contexto.equipe),
        criado_em=briefing.criado_em,
        atualizado_em=briefing.atualizado_em,
        registros_situacao=registros,
    )


def _validar_autoria(contexto: ContextoAcessoBriefings) -> None:
    if contexto.papel not in (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR):
        raise PermissionError("Papel sem permissão para alterar Briefings")


def _obter_briefing(
    repositorio: RepositorioBriefings,
    contexto: ContextoAcessoBriefings,
    id_campanha: UUID,
) -> Briefing:
    briefing = repositorio.obter_por_campanha(
        contexto.id_espaco_trabalho,
        id_campanha,
    )
    if briefing is None:
        raise LookupError("Briefing não encontrado no espaço atual")
    return briefing


class AbrirBriefingCampanha:
    def __init__(
        self,
        repositorio_campanhas: RepositorioCampanhas,
        repositorio_briefings: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        self._repositorio_campanhas = repositorio_campanhas
        self._repositorio_briefings = repositorio_briefings
        self._contexto = contexto_acesso
        self._relogio = relogio
        self._gerador_uuid = gerador_uuid

    def executar(self, id_campanha: UUID) -> BriefingResumo:
        papeis_consulta = (
            PapelAcesso.PROPRIETARIO,
            PapelAcesso.EDITOR,
            PapelAcesso.LEITOR,
        )
        if self._contexto.papel not in papeis_consulta:
            raise PermissionError("Papel sem permissão para abrir Briefings")
        campanha = self._repositorio_campanhas.obter(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        if campanha is None:
            raise LookupError("Campanha não encontrada no espaço atual")
        if (
            campanha.situacao is not SituacaoCampanha.EM_ANDAMENTO
            or campanha.etapa_atual is not EtapaCampanha.BRIEFING
        ):
            raise ValueError("Campanha não está na etapa de Briefing")
        existente = self._repositorio_briefings.obter_por_campanha(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        if existente is not None:
            return _resumir(existente)
        if self._contexto.papel is PapelAcesso.LEITOR:
            raise PermissionError("Leitor não pode criar a versão inicial do Briefing")

        contexto_herdado = ContextoHerdadoBriefing(
            codigo_campanha=campanha.codigo,
            nome_campanha=campanha.nome,
            anunciante=campanha.anunciante,
            marca=campanha.marca,
            produto_servico=campanha.produto_servico,
            planejador_responsavel=campanha.planejador_responsavel,
            equipe=campanha.equipe,
        )
        agora = self._relogio()
        briefing = Briefing.criar_versao_inicial(
            id_briefing=self._gerador_uuid(),
            id_campanha=campanha.id_campanha,
            id_espaco_trabalho=campanha.id_espaco_trabalho,
            contexto_herdado=contexto_herdado,
            criado_por=self._contexto.id_usuario,
            criado_em=agora,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=agora,
        )
        self._repositorio_briefings.salvar(briefing)
        return _resumir(briefing)


class ListarAspectosSituacaoMercadologica:
    def executar(self, escopo: str) -> tuple[AspectoSituacaoResumo, ...]:
        try:
            escopo_convertido = EscopoSituacaoMercadologica(escopo)
        except ValueError as erro:
            raise ValueError("Escopo inválido") from erro
        return tuple(
            AspectoSituacaoResumo(
                codigo=aspecto.codigo,
                rotulo=aspecto.rotulo,
                descricao=aspecto.descricao,
                unidades_sugeridas=aspecto.unidades_sugeridas,
            )
            for aspecto in listar_aspectos_iniciais(escopo_convertido)
        )


class AdicionarRegistroSituacaoMercadologica:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
        gerador_uuid: GeradorUUID,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio
        self._gerador_uuid = gerador_uuid

    def executar(
        self,
        id_campanha: UUID,
        entrada: AdicionarRegistroSituacaoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(
            self._repositorio,
            self._contexto,
            id_campanha,
        )
        try:
            escopo = EscopoSituacaoMercadologica(entrada.escopo)
        except ValueError as erro:
            raise ValueError("Escopo inválido") from erro
        try:
            natureza = NaturezaRegistroSituacao(entrada.natureza)
        except ValueError as erro:
            raise ValueError("Natureza inválida") from erro
        codigo_aspecto = entrada.codigo_aspecto
        aspecto = entrada.aspecto.strip()
        if codigo_aspecto is not None:
            definicao = next(
                (
                    item
                    for item in listar_aspectos_iniciais(escopo)
                    if item.codigo == codigo_aspecto
                ),
                None,
            )
            if definicao is None:
                raise ValueError("Aspecto não pertence ao escopo informado")
            codigo_aspecto = definicao.codigo
            aspecto = definicao.rotulo
        elif not aspecto or aspecto == "Outro aspecto":
            raise ValueError("Informe o nome do aspecto observado")
        valor = None
        if entrada.valor_quantitativo is not None:
            if "," in entrada.valor_quantitativo:
                raise ValueError("Valor quantitativo inválido")
            try:
                valor = Decimal(entrada.valor_quantitativo)
            except InvalidOperation as erro:
                raise ValueError("Valor quantitativo inválido") from erro
        registro = RegistroSituacaoMercadologica(
            id_registro=self._gerador_uuid(),
            escopo=escopo,
            codigo_aspecto=codigo_aspecto,
            aspecto=aspecto,
            entidade_referencia=entrada.entidade_referencia,
            natureza=natureza,
            valor_quantitativo=valor,
            unidade=entrada.unidade,
            valor_qualitativo=entrada.valor_qualitativo,
            fonte=entrada.fonte,
            periodo_referencia=entrada.periodo_referencia,
            observacao=entrada.observacao,
        )
        atualizado = briefing.adicionar_registro_situacao(
            registro=registro,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return _resumir(atualizado)


class RemoverRegistroSituacaoMercadologica:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_registro: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(
            self._repositorio,
            self._contexto,
            id_campanha,
        )
        atualizado = briefing.remover_registro_situacao(
            id_registro=id_registro,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return _resumir(atualizado)
