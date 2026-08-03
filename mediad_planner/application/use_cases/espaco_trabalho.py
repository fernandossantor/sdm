from uuid import UUID

from mediad_planner.application.dto.espaco_trabalho import (
    ContextoAcessoEspacoTrabalho,
    EspacoTrabalhoCampanhaResumo,
    ModuloEspacoTrabalhoResumo,
)
from mediad_planner.application.mappers.briefing import resumir_briefing
from mediad_planner.application.mappers.campanha import resumir_campanha
from mediad_planner.application.ports.repositorio_briefings import (
    RepositorioBriefings,
)
from mediad_planner.application.ports.repositorio_campanhas import (
    RepositorioCampanhas,
)
from mediad_planner.application.use_cases.briefings import AbrirBriefingCampanha
from mediad_planner.application.use_cases.campanhas import IniciarBriefingCampanha
from mediad_planner.domain.common.enums import PapelAcesso


def _modulos(
    tem_briefing: bool,
    etapa_atual: str,
) -> tuple[ModuloEspacoTrabalhoResumo, ...]:
    estado_briefing = (
        "ETAPA_ATUAL"
        if tem_briefing and etapa_atual == "BRIEFING"
        else "DISPONIVEL" if tem_briefing else "BLOQUEADO"
    )
    return (
        ModuloEspacoTrabalhoResumo(
            codigo="VISAO_GERAL",
            rotulo="Visão geral da Campanha",
            descricao=(
                "Acompanhe a identificação, o estado e o progresso metodológico "
                "da Campanha."
            ),
            disponivel=True,
            estado="DISPONIVEL",
            motivo_bloqueio=None,
        ),
        ModuloEspacoTrabalhoResumo(
            codigo="BRIEFING",
            rotulo="Briefing",
            descricao=(
                "Registre e organize o contexto declarado que sustentará o "
                "planejamento."
            ),
            disponivel=tem_briefing,
            estado=estado_briefing,
            motivo_bloqueio=(
                None if tem_briefing else "Inicie o Briefing para continuar."
            ),
        ),
        ModuloEspacoTrabalhoResumo(
            codigo="TRADUCAO_ESTRATEGICA",
            rotulo="Tradução Estratégica",
            descricao=(
                "Interprete o Briefing e produza o problema e os objetivos de mídia."
            ),
            disponivel=False,
            estado="BLOQUEADO",
            motivo_bloqueio="Conclua o Briefing para continuar.",
        ),
        ModuloEspacoTrabalhoResumo(
            codigo="ARQUITETURA_DE_MIDIA",
            rotulo="Arquitetura de Mídia",
            descricao=(
                "Estruture papéis, pontos de contato, meios, canais e relações da "
                "estratégia."
            ),
            disponivel=False,
            estado="BLOQUEADO",
            motivo_bloqueio="Conclua a Tradução Estratégica para continuar.",
        ),
        ModuloEspacoTrabalhoResumo(
            codigo="SIMULACAO",
            rotulo="Simulação",
            descricao="Construa e compare cenários de investimento e desempenho.",
            disponivel=False,
            estado="BLOQUEADO",
            motivo_bloqueio="Conclua a Arquitetura de Mídia para continuar.",
        ),
        ModuloEspacoTrabalhoResumo(
            codigo="PLANO_CONSOLIDADO",
            rotulo="Plano Consolidado",
            descricao="Organize o cenário selecionado como plano final da Campanha.",
            disponivel=False,
            estado="BLOQUEADO",
            motivo_bloqueio=(
                "Selecione o cenário de Simulação que será consolidado."
            ),
        ),
    )


class ObterEspacoTrabalhoCampanha:
    def __init__(
        self,
        repositorio_campanhas: RepositorioCampanhas,
        repositorio_briefings: RepositorioBriefings,
        contexto_acesso: ContextoAcessoEspacoTrabalho,
    ) -> None:
        self._repositorio_campanhas = repositorio_campanhas
        self._repositorio_briefings = repositorio_briefings
        self._contexto = contexto_acesso

    def executar(self, id_campanha: UUID) -> EspacoTrabalhoCampanhaResumo:
        papeis_autorizados = (
            PapelAcesso.PROPRIETARIO,
            PapelAcesso.EDITOR,
            PapelAcesso.LEITOR,
        )
        if self._contexto.papel not in papeis_autorizados:
            raise PermissionError(
                "Papel sem permissão para acessar o espaço de trabalho"
            )
        campanha = self._repositorio_campanhas.obter(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        if campanha is None:
            raise LookupError("Campanha não encontrada no espaço atual")
        briefing = self._repositorio_briefings.obter_por_campanha(
            self._contexto.id_espaco_trabalho,
            id_campanha,
        )
        return EspacoTrabalhoCampanhaResumo(
            campanha=resumir_campanha(campanha),
            briefing=resumir_briefing(briefing) if briefing is not None else None,
            modulos=_modulos(briefing is not None, campanha.etapa_atual.value),
        )


class PrepararBriefingCampanha:
    def __init__(
        self,
        iniciar_briefing: IniciarBriefingCampanha,
        abrir_briefing: AbrirBriefingCampanha,
        obter_espaco_trabalho: ObterEspacoTrabalhoCampanha,
    ) -> None:
        self._iniciar_briefing = iniciar_briefing
        self._abrir_briefing = abrir_briefing
        self._obter_espaco_trabalho = obter_espaco_trabalho

    def executar(self, id_campanha: UUID) -> EspacoTrabalhoCampanhaResumo:
        resumo = self._obter_espaco_trabalho.executar(id_campanha)
        if resumo.campanha.etapa_atual == "ABERTURA":
            self._iniciar_briefing.executar(id_campanha)
        self._abrir_briefing.executar(id_campanha)
        return self._obter_espaco_trabalho.executar(id_campanha)
