from datetime import date
from decimal import Decimal, InvalidOperation
from uuid import UUID

from mediad_planner.application.dto.briefing import BriefingResumo, ContextoAcessoBriefings
from mediad_planner.application.dto.periodo_verba import (
    IntervaloDeclaradoEntrada,
    NaturezaLimiteVerbaResumo,
    SalvarPeriodoVerbaEntrada,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.ports.repositorio_briefings import RepositorioBriefings
from mediad_planner.application.use_cases.briefings import Relogio, _obter_briefing, _validar_autoria
from mediad_planner.domain.briefing.periodo_verba import (
    ContextoPeriodoVerba,
    IntervaloDeclarado,
    NaturezaLimiteVerba,
    PeriodoPretendido,
    ROTULOS_NATUREZA_LIMITE,
    VerbaDeclarada,
)


def _data(valor: str | None, campo: str) -> date | None:
    if valor is None or not valor.strip():
        return None
    try:
        return date.fromisoformat(valor.strip())
    except ValueError as erro:
        raise ValueError(f"{campo} deve usar AAAA-MM-DD") from erro


def _valor(valor: str | None, campo: str) -> Decimal | None:
    if valor is None or not valor.strip():
        return None
    if "," in valor:
        raise ValueError(f"{campo} inválido")
    try:
        numero = Decimal(valor.strip())
    except InvalidOperation as erro:
        raise ValueError(f"{campo} inválido") from erro
    if not numero.is_finite() or numero < 0:
        raise ValueError(f"{campo} inválido")
    return numero


def _intervalo(item: IntervaloDeclaradoEntrada) -> IntervaloDeclarado:
    inicial = _data(item.data_inicial, "Data inicial do intervalo")
    final = _data(item.data_final, "Data final do intervalo")
    if inicial is None or final is None:
        raise ValueError("Datas do intervalo são obrigatórias")
    if final < inicial:
        raise ValueError("Data final do intervalo anterior à inicial")
    return IntervaloDeclarado(inicial, final, item.descricao)


class ListarNaturezasLimiteVerba:
    def executar(self) -> tuple[NaturezaLimiteVerbaResumo, ...]:
        return tuple(
            NaturezaLimiteVerbaResumo(item.value, ROTULOS_NATUREZA_LIMITE[item])
            for item in NaturezaLimiteVerba
        )


class DefinirPeriodoVerba:
    def __init__(
        self, repositorio: RepositorioBriefings,
        contexto_acesso: ContextoAcessoBriefings, relogio: Relogio,
    ) -> None:
        self._repositorio = repositorio
        self._contexto = contexto_acesso
        self._relogio = relogio

    def executar(
        self, id_campanha: UUID, entrada: SalvarPeriodoVerbaEntrada,
    ) -> BriefingResumo:
        _validar_autoria(self._contexto)
        briefing = _obter_briefing(self._repositorio, self._contexto, id_campanha)
        try:
            natureza = NaturezaLimiteVerba(entrada.natureza_limite)
        except ValueError as erro:
            raise ValueError("Natureza do limite inválida") from erro
        contexto = ContextoPeriodoVerba(
            periodo=PeriodoPretendido(
                data_inicial=_data(entrada.data_inicial, "Data inicial"),
                data_final=_data(entrada.data_final, "Data final"),
                duracao=entrada.duracao,
                datas_criticas=tuple(
                    _data(item, "Data crítica") for item in entrada.datas_criticas
                ),
                sazonalidades=entrada.sazonalidades,
                eventos_condicionantes=entrada.eventos_condicionantes,
                periodos_obrigatorios=tuple(_intervalo(item) for item in entrada.periodos_obrigatorios),
                periodos_vedados=tuple(_intervalo(item) for item in entrada.periodos_vedados),
                observacao=entrada.observacao_periodo,
            ),
            verba=VerbaDeclarada(
                valor_total=_valor(entrada.valor_total, "Valor total"),
                moeda=entrada.moeda,
                natureza_limite=natureza,
                margem_flexibilidade=entrada.margem_flexibilidade,
                valor_minimo=_valor(entrada.valor_minimo, "Valor mínimo"),
                valor_maximo=_valor(entrada.valor_maximo, "Valor máximo"),
                parcela_comprometida=_valor(
                    entrada.parcela_comprometida, "Parcela comprometida"
                ),
                observacao=entrada.observacao_verba,
            ),
        )
        atualizado = briefing.definir_contexto_periodo_verba(
            contexto, self._contexto.id_usuario, self._relogio()
        )
        self._repositorio.salvar(atualizado)
        return resumir_briefing(atualizado)
