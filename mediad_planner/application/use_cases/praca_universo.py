from decimal import Decimal, InvalidOperation
from uuid import UUID

from mediad_planner.application.dto.briefing import (
    BriefingResumo,
    ContextoAcessoBriefings,
)
from mediad_planner.application.dto.praca_universo import (
    AdicionarPracaEntrada,
    AdicionarUniversoEntrada,
    DefinicaoTipoPracaResumo,
    DefinicaoUnidadePopulacionalResumo,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.use_cases.briefings import (
    GeradorUUID,
    Relogio,
    _obter_briefing,
    _validar_autoria,
)
from mediad_planner.domain.briefing.praca_universo import (
    PracaDeclarada,
    TipoPracaTerritorial,
    UniversoDeclarado,
    listar_tipos_praca_territorial,
    listar_unidades_populacionais,
)


def _decimal_opcional(valor: str | None) -> Decimal | None:
    if valor is None or not valor.strip():
        return None
    if "," in valor:
        raise ValueError("Valor populacional inválido")
    try:
        convertido = Decimal(valor)
    except InvalidOperation as erro:
        raise ValueError("Valor populacional inválido") from erro
    if not convertido.is_finite() or convertido <= 0:
        raise ValueError("Valor populacional inválido")
    return convertido


def _resolver_unidade(
    codigo: str | None,
    unidade: str | None,
) -> tuple[str | None, str | None]:
    if codigo is not None:
        definicao = next(
            (
                item
                for item in listar_unidades_populacionais()
                if item.codigo == codigo
            ),
            None,
        )
        if definicao is None:
            raise ValueError("Unidade populacional inválida")
        return definicao.codigo, definicao.rotulo
    return None, unidade


class ListarTiposPracaTerritorial:
    def executar(self) -> tuple[DefinicaoTipoPracaResumo, ...]:
        return tuple(
            DefinicaoTipoPracaResumo(
                codigo=item.codigo.value,
                rotulo=item.rotulo,
                descricao=item.descricao,
            )
            for item in listar_tipos_praca_territorial()
        )


class ListarUnidadesPopulacionais:
    def executar(self) -> tuple[DefinicaoUnidadePopulacionalResumo, ...]:
        return tuple(
            DefinicaoUnidadePopulacionalResumo(
                codigo=item.codigo,
                rotulo=item.rotulo,
                descricao=item.descricao,
            )
            for item in listar_unidades_populacionais()
        )


class AdicionarPraca:
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
        entrada: AdicionarPracaEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        try:
            tipo = TipoPracaTerritorial(entrada.tipo)
        except ValueError as erro:
            raise ValueError("Tipo de praça inválido") from erro
        valor = _decimal_opcional(entrada.valor_populacao_referencia)
        codigo_unidade, unidade = _resolver_unidade(
            entrada.codigo_unidade_populacional,
            entrada.unidade_populacional,
        )
        praca = PracaDeclarada(
            id_praca=self._gerador_uuid(),
            tipo=tipo,
            nome=entrada.nome,
            codigo_oficial=entrada.codigo_oficial,
            abrangencia=entrada.abrangencia,
            valor_populacao_referencia=valor,
            codigo_unidade_populacional=codigo_unidade,
            unidade_populacional=unidade,
            fonte=entrada.fonte,
            data_referencia=entrada.data_referencia,
            observacao=entrada.observacao,
        )
        atualizado = briefing.adicionar_praca(
            praca=praca,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class RemoverPraca:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_praca: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.remover_praca(
            id_praca=id_praca,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class AdicionarUniverso:
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
        entrada: AdicionarUniversoEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        if not entrada.ids_pracas:
            raise ValueError("Informe ao menos uma Praça para o Universo")
        valor = _decimal_opcional(entrada.valor_populacional)
        codigo_unidade, unidade = _resolver_unidade(
            entrada.codigo_unidade,
            entrada.unidade,
        )
        universo = UniversoDeclarado(
            id_universo=self._gerador_uuid(),
            nome=entrada.nome,
            definicao=entrada.definicao,
            ids_pracas=entrada.ids_pracas,
            valor_populacional=valor,
            codigo_unidade=codigo_unidade,
            unidade=unidade or "",
            fonte=entrada.fonte,
            data_referencia=entrada.data_referencia,
            criterios_inclusao=entrada.criterios_inclusao,
            criterios_exclusao=entrada.criterios_exclusao,
            observacao=entrada.observacao,
        )
        atualizado = briefing.adicionar_universo(
            universo=universo,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)


class RemoverUniverso:
    def __init__(
        self,
        repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings,
        relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(self, id_campanha: UUID, id_universo: UUID) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        atualizado = briefing.remover_universo(
            id_universo=id_universo,
            atualizado_por=self._contexto.id_usuario,
            atualizado_em=self._relogio(),
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)
