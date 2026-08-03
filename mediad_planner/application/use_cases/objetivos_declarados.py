from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    ContextoAcessoBriefings,
)
from mediad_planner.application.dto.objetivos_declarados import (
    AdicionarObjetivoComunicacaoEntrada,
    AdicionarObjetivoMarketingEntrada,
    DefinicaoObjetivoResumo,
    DimensaoCompostoMarketingResumo,
)
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.domain.briefing.entidades import Briefing
from mediad_planner.domain.briefing.objetivos_declarados import (
    DimensaoCompostoMarketing,
    ObjetivoComunicacaoDeclarado,
    ObjetivoMarketingDeclarado,
    listar_dimensoes_composto_marketing,
    listar_objetivos_comunicacao_iniciais,
    listar_objetivos_marketing_iniciais,
)
from mediad_planner.domain.common.enums import PapelAcesso


Relogio = Callable[[], datetime]
GeradorUUID = Callable[[], UUID]


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


def _localizar_definicao(codigo: str, marketing: bool):
    catalogo = (
        listar_objetivos_marketing_iniciais()
        if marketing
        else listar_objetivos_comunicacao_iniciais()
    )
    return next((item for item in catalogo if item.codigo == codigo), None)


def _normalizar_objetivo(
    codigo: str | None,
    objetivo: str,
    marketing: bool,
) -> tuple[str | None, str]:
    if codigo is not None:
        definicao = _localizar_definicao(codigo, marketing)
        if definicao is None:
            tipo = "Marketing" if marketing else "Comunicação"
            raise ValueError(f"Objetivo de {tipo} inválido")
        return definicao.codigo, definicao.rotulo
    normalizado = objetivo.strip()
    if not normalizado or normalizado == "Outro objetivo":
        tipo = "Marketing" if marketing else "Comunicação"
        raise ValueError(f"Informe o Objetivo de {tipo}")
    return None, normalizado


def _validar_escala(valor: object, campo: str) -> None:
    if type(valor) is not int or not 1 <= valor <= 5:
        raise ValueError(f"{campo} deve ser inteiro entre 1 e 5")


class ListarObjetivosMarketingDeclarados:
    def executar(self) -> tuple[DefinicaoObjetivoResumo, ...]:
        return tuple(
            DefinicaoObjetivoResumo(item.codigo, item.rotulo, item.descricao)
            for item in listar_objetivos_marketing_iniciais()
        )


class ListarObjetivosComunicacaoDeclarados:
    def executar(self) -> tuple[DefinicaoObjetivoResumo, ...]:
        return tuple(
            DefinicaoObjetivoResumo(item.codigo, item.rotulo, item.descricao)
            for item in listar_objetivos_comunicacao_iniciais()
        )


class ListarDimensoesCompostoMarketing:
    def executar(self) -> tuple[DimensaoCompostoMarketingResumo, ...]:
        return tuple(
            DimensaoCompostoMarketingResumo(
                item.codigo.value,
                item.rotulo,
                item.descricao,
            )
            for item in listar_dimensoes_composto_marketing()
        )


class AdicionarObjetivoMarketing:
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
        entrada: AdicionarObjetivoMarketingEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(
            self._repositorio,
            self._contexto,
            id_campanha,
        )
        codigo, objetivo = _normalizar_objetivo(
            entrada.codigo_objetivo,
            entrada.objetivo,
            True,
        )
        try:
            dimensoes = tuple(
                DimensaoCompostoMarketing(item)
                for item in entrada.dimensoes_composto
            )
        except ValueError as erro:
            raise ValueError(
                "Dimensão do composto de Marketing inválida"
            ) from erro
        if len(dimensoes) != len(set(dimensoes)):
            raise ValueError("dimensoes_composto possui duplicatas")
        _validar_escala(entrada.prioridade_declarada, "prioridade_declarada")
        _validar_escala(entrada.intensidade_declarada, "intensidade_declarada")
        novo = ObjetivoMarketingDeclarado(
            id_objetivo=self._gerador_uuid(),
            codigo_objetivo=codigo,
            objetivo=objetivo,
            dimensoes_composto=dimensoes,
            prioridade_declarada=entrada.prioridade_declarada,
            intensidade_declarada=entrada.intensidade_declarada,
            justificativa=entrada.justificativa,
        )
        atualizado = briefing.adicionar_objetivo_marketing(
            objetivo=novo,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class AdicionarObjetivoComunicacao:
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
        entrada: AdicionarObjetivoComunicacaoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(
            self._repositorio,
            self._contexto,
            id_campanha,
        )
        codigo, objetivo = _normalizar_objetivo(
            entrada.codigo_objetivo,
            entrada.objetivo,
            False,
        )
        relacionados = tuple(entrada.ids_objetivos_marketing_relacionados)
        if len(relacionados) != len(set(relacionados)):
            raise ValueError("IDs relacionados possuem duplicatas")
        ids_marketing = {
            item.id_objetivo for item in briefing.objetivos_declarados.marketing
        }
        if not set(relacionados) <= ids_marketing:
            raise ValueError("Objetivo de Marketing relacionado não existe")
        _validar_escala(entrada.prioridade_declarada, "prioridade_declarada")
        _validar_escala(entrada.intensidade_declarada, "intensidade_declarada")
        novo = ObjetivoComunicacaoDeclarado(
            id_objetivo=self._gerador_uuid(),
            codigo_objetivo=codigo,
            objetivo=objetivo,
            ids_objetivos_marketing_relacionados=relacionados,
            prioridade_declarada=entrada.prioridade_declarada,
            intensidade_declarada=entrada.intensidade_declarada,
            justificativa=entrada.justificativa,
        )
        atualizado = briefing.adicionar_objetivo_comunicacao(
            objetivo=novo,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class RemoverObjetivoMarketing:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_objetivo: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(
            self._repositorio,
            self._contexto,
            id_campanha,
        )
        atualizado = briefing.remover_objetivo_marketing(
            id_objetivo=id_objetivo,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class RemoverObjetivoComunicacao:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_objetivo: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(
            self._repositorio,
            self._contexto,
            id_campanha,
        )
        atualizado = briefing.remover_objetivo_comunicacao(
            id_objetivo=id_objetivo,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)
