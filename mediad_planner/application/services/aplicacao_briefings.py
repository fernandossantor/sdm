from uuid import UUID

from mediad_planner.application.dto.briefing import (
    AdicionarRegistroSituacaoEntrada,
    AspectoSituacaoResumo,
    BriefingResumo,
)
from mediad_planner.application.dto.objetivos_declarados import (
    AdicionarObjetivoComunicacaoEntrada,
    AdicionarObjetivoMarketingEntrada,
    DefinicaoObjetivoResumo,
    DimensaoCompostoMarketingResumo,
)
from mediad_planner.application.use_cases.objetivos_declarados import (
    AdicionarObjetivoComunicacao,
    AdicionarObjetivoMarketing,
    ListarDimensoesCompostoMarketing,
    ListarObjetivosComunicacaoDeclarados,
    ListarObjetivosMarketingDeclarados,
    RemoverObjetivoComunicacao,
    RemoverObjetivoMarketing,
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
        listar_marketing: ListarObjetivosMarketingDeclarados,
        listar_comunicacao: ListarObjetivosComunicacaoDeclarados,
        listar_dimensoes_composto: ListarDimensoesCompostoMarketing,
        adicionar_marketing: AdicionarObjetivoMarketing,
        adicionar_comunicacao: AdicionarObjetivoComunicacao,
        remover_marketing: RemoverObjetivoMarketing,
        remover_comunicacao: RemoverObjetivoComunicacao,
    ) -> None:
        self._abrir = abrir
        self._listar_aspectos = listar_aspectos
        self._adicionar = adicionar
        self._remover = remover
        self._listar_marketing = listar_marketing
        self._listar_comunicacao = listar_comunicacao
        self._listar_dimensoes_composto = listar_dimensoes_composto
        self._adicionar_marketing = adicionar_marketing
        self._adicionar_comunicacao = adicionar_comunicacao
        self._remover_marketing = remover_marketing
        self._remover_comunicacao = remover_comunicacao

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

    def listar_objetivos_marketing(self) -> tuple[DefinicaoObjetivoResumo, ...]:
        return self._listar_marketing.executar()

    def listar_objetivos_comunicacao(self) -> tuple[DefinicaoObjetivoResumo, ...]:
        return self._listar_comunicacao.executar()

    def listar_dimensoes_composto_marketing(
        self,
    ) -> tuple[DimensaoCompostoMarketingResumo, ...]:
        return self._listar_dimensoes_composto.executar()

    def adicionar_objetivo_marketing(
        self,
        id_campanha: UUID,
        entrada: AdicionarObjetivoMarketingEntrada,
    ) -> BriefingResumo:
        return self._adicionar_marketing.executar(id_campanha, entrada)

    def remover_objetivo_marketing(
        self,
        id_campanha: UUID,
        id_objetivo: UUID,
    ) -> BriefingResumo:
        return self._remover_marketing.executar(id_campanha, id_objetivo)

    def adicionar_objetivo_comunicacao(
        self,
        id_campanha: UUID,
        entrada: AdicionarObjetivoComunicacaoEntrada,
    ) -> BriefingResumo:
        return self._adicionar_comunicacao.executar(id_campanha, entrada)

    def remover_objetivo_comunicacao(
        self,
        id_campanha: UUID,
        id_objetivo: UUID,
    ) -> BriefingResumo:
        return self._remover_comunicacao.executar(id_campanha, id_objetivo)
