from uuid import UUID

from mediad_planner.application.dto.briefing import (
    AdicionarRegistroSituacaoEntrada,
    AspectoSituacaoResumo,
    BriefingResumo,
)
from mediad_planner.application.use_cases.briefings import (
    AbrirBriefingCampanha,
    AdicionarRegistroSituacaoMercadologica,
    ListarAspectosSituacaoMercadologica,
    RemoverRegistroSituacaoMercadologica,
)


class AplicacaoBriefings:
    def __init__(
        self,
        abrir: AbrirBriefingCampanha,
        listar_aspectos: ListarAspectosSituacaoMercadologica,
        adicionar: AdicionarRegistroSituacaoMercadologica,
        remover: RemoverRegistroSituacaoMercadologica,
    ) -> None:
        self._abrir = abrir
        self._listar_aspectos = listar_aspectos
        self._adicionar = adicionar
        self._remover = remover

    def abrir_briefing(self, id_campanha: UUID) -> BriefingResumo:
        return self._abrir.executar(id_campanha)

    def listar_aspectos_situacao(
        self,
        escopo: str,
    ) -> tuple[AspectoSituacaoResumo, ...]:
        return self._listar_aspectos.executar(escopo)

    def adicionar_registro_situacao(
        self,
        id_campanha: UUID,
        entrada: AdicionarRegistroSituacaoEntrada,
    ) -> BriefingResumo:
        return self._adicionar.executar(id_campanha, entrada)

    def remover_registro_situacao(
        self,
        id_campanha: UUID,
        id_registro: UUID,
    ) -> BriefingResumo:
        return self._remover.executar(id_campanha, id_registro)
