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
    DefinirVinculosObjetivoEntrada,
    EditarPrioridadeObjetivoEntrada,
)
from mediad_planner.application.dto.praca_universo import (
    AdicionarPracaEntrada,
    AdicionarUniversoEntrada,
    DefinicaoTipoPracaResumo,
    DefinicaoUnidadePopulacionalResumo,
)
from mediad_planner.application.dto.criterios_segmentacao import (
    DefinicaoCriterioSegmentacaoResumo,
    DefinirCriteriosSegmentacaoEntrada,
)
from mediad_planner.application.use_cases.criterios_segmentacao import (
    DefinirCriteriosSegmentacao,
    ListarCriteriosSegmentacao,
)
from mediad_planner.application.dto.segmentos import SalvarSegmentoEntrada
from mediad_planner.application.use_cases.segmentos import (
    AdicionarSegmento,
    EditarSegmento,
    RemoverSegmento,
)
from mediad_planner.application.dto.publicos import SalvarPublicoEntrada
from mediad_planner.application.use_cases.publicos import (
    AdicionarPublico,
    EditarPublico,
    RemoverPublico,
)
from mediad_planner.application.dto.jornada import (
    DefinirAplicabilidadeJornadaEntrada,
    CategoriaEtapaJornadaResumo,
    SalvarEtapaJornadaEntrada,
    SalvarJornadaEntrada,
)
from mediad_planner.application.use_cases.jornada import (
    DefinirAplicabilidadeJornada,
    AdicionarEtapaJornada,
    AdicionarJornada,
    EditarEtapaJornada,
    EditarJornada,
    ListarCategoriasEtapaJornada,
    RemoverEtapaJornada,
    RemoverJornada,
)
from mediad_planner.application.dto.periodo_verba import (
    NaturezaLimiteVerbaResumo,
    SalvarPeriodoVerbaEntrada,
)
from mediad_planner.application.use_cases.periodo_verba import (
    DefinirPeriodoVerba,
    ListarNaturezasLimiteVerba,
)
from mediad_planner.application.dto.condicoes_declaradas import (
    DefinirInexistenciaRestricoesEntrada,
    DefinicaoCategoriaResumo,
    SalvarPretensaoEntrada,
    SalvarPrioridadeEntrada,
    SalvarRestricaoEntrada,
)
from mediad_planner.application.use_cases.condicoes_declaradas import GerenciarCondicoesDeclaradas
from mediad_planner.application.use_cases.objetivos_declarados import (
    AdicionarObjetivoComunicacao,
    AdicionarObjetivoMarketing,
    ListarDimensoesCompostoMarketing,
    ListarObjetivosComunicacaoDeclarados,
    ListarObjetivosMarketingDeclarados,
    RemoverObjetivoComunicacao,
    RemoverObjetivoMarketing,
    DefinirVinculosObjetivo,
    EditarPrioridadeObjetivo,
)
from mediad_planner.application.use_cases.briefings import (
    AbrirBriefingCampanha,
    AdicionarRegistroSituacaoMercadologica,
    ListarAspectosSituacaoMercadologica,
    RemoverRegistroSituacaoMercadologica,
)
from mediad_planner.application.use_cases.praca_universo import (
    AdicionarPraca,
    AdicionarUniverso,
    ListarTiposPracaTerritorial,
    ListarUnidadesPopulacionais,
    RemoverPraca,
    RemoverUniverso,
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
        listar_tipos_praca: ListarTiposPracaTerritorial,
        listar_unidades_populacionais: ListarUnidadesPopulacionais,
        adicionar_praca: AdicionarPraca,
        remover_praca: RemoverPraca,
        adicionar_universo: AdicionarUniverso,
        remover_universo: RemoverUniverso,
        listar_criterios_segmentacao: ListarCriteriosSegmentacao,
        definir_criterios_segmentacao: DefinirCriteriosSegmentacao,
        adicionar_segmento: AdicionarSegmento,
        editar_segmento: EditarSegmento,
        remover_segmento: RemoverSegmento,
        adicionar_publico: AdicionarPublico,
        editar_publico: EditarPublico,
        remover_publico: RemoverPublico,
        listar_categorias_etapa: ListarCategoriasEtapaJornada,
        adicionar_jornada: AdicionarJornada,
        editar_jornada: EditarJornada,
        remover_jornada: RemoverJornada,
        adicionar_etapa_jornada: AdicionarEtapaJornada,
        editar_etapa_jornada: EditarEtapaJornada,
        remover_etapa_jornada: RemoverEtapaJornada,
        listar_naturezas_limite_verba: ListarNaturezasLimiteVerba,
        definir_periodo_verba: DefinirPeriodoVerba,
        gerenciar_condicoes: GerenciarCondicoesDeclaradas,
        definir_aplicabilidade_jornada: DefinirAplicabilidadeJornada,
        definir_vinculos_objetivo: DefinirVinculosObjetivo,
        editar_prioridade_objetivo: EditarPrioridadeObjetivo,
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
        self._listar_tipos_praca = listar_tipos_praca
        self._listar_unidades_populacionais = listar_unidades_populacionais
        self._adicionar_praca = adicionar_praca
        self._remover_praca = remover_praca
        self._adicionar_universo = adicionar_universo
        self._remover_universo = remover_universo
        self._listar_criterios_segmentacao = listar_criterios_segmentacao
        self._definir_criterios_segmentacao = definir_criterios_segmentacao
        self._adicionar_segmento = adicionar_segmento
        self._editar_segmento = editar_segmento
        self._remover_segmento = remover_segmento
        self._adicionar_publico = adicionar_publico
        self._editar_publico = editar_publico
        self._remover_publico = remover_publico
        self._listar_categorias_etapa = listar_categorias_etapa
        self._adicionar_jornada = adicionar_jornada
        self._editar_jornada = editar_jornada
        self._remover_jornada = remover_jornada
        self._adicionar_etapa_jornada = adicionar_etapa_jornada
        self._editar_etapa_jornada = editar_etapa_jornada
        self._remover_etapa_jornada = remover_etapa_jornada
        self._listar_naturezas_limite_verba = listar_naturezas_limite_verba
        self._definir_periodo_verba = definir_periodo_verba
        self._gerenciar_condicoes = gerenciar_condicoes
        self._definir_aplicabilidade_jornada = definir_aplicabilidade_jornada
        self._definir_vinculos_objetivo = definir_vinculos_objetivo
        self._editar_prioridade_objetivo = editar_prioridade_objetivo

    def editar_prioridade_objetivo(
        self, id_campanha: UUID, entrada: EditarPrioridadeObjetivoEntrada,
    ) -> BriefingResumo:
        return self._editar_prioridade_objetivo.executar(id_campanha, entrada)

    def definir_vinculos_objetivo(
        self, id_campanha: UUID, entrada: DefinirVinculosObjetivoEntrada,
    ) -> BriefingResumo:
        return self._definir_vinculos_objetivo.executar(id_campanha, entrada)

    def definir_aplicabilidade_jornada(
        self, id_campanha: UUID, entrada: DefinirAplicabilidadeJornadaEntrada,
    ) -> BriefingResumo:
        return self._definir_aplicabilidade_jornada.executar(id_campanha, entrada)

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

    def listar_tipos_praca(self) -> tuple[DefinicaoTipoPracaResumo, ...]:
        return self._listar_tipos_praca.executar()

    def listar_unidades_populacionais(
        self,
    ) -> tuple[DefinicaoUnidadePopulacionalResumo, ...]:
        return self._listar_unidades_populacionais.executar()

    def adicionar_praca(
        self,
        id_campanha: UUID,
        entrada: AdicionarPracaEntrada,
    ) -> BriefingResumo:
        return self._adicionar_praca.executar(id_campanha, entrada)

    def remover_praca(
        self,
        id_campanha: UUID,
        id_praca: UUID,
    ) -> BriefingResumo:
        return self._remover_praca.executar(id_campanha, id_praca)

    def adicionar_universo(
        self,
        id_campanha: UUID,
        entrada: AdicionarUniversoEntrada,
    ) -> BriefingResumo:
        return self._adicionar_universo.executar(id_campanha, entrada)

    def remover_universo(
        self,
        id_campanha: UUID,
        id_universo: UUID,
    ) -> BriefingResumo:
        return self._remover_universo.executar(id_campanha, id_universo)

    def listar_criterios_segmentacao(
        self,
    ) -> tuple[DefinicaoCriterioSegmentacaoResumo, ...]:
        return self._listar_criterios_segmentacao.executar()

    def definir_criterios_segmentacao(
        self,
        id_campanha: UUID,
        entrada: DefinirCriteriosSegmentacaoEntrada,
    ) -> BriefingResumo:
        return self._definir_criterios_segmentacao.executar(id_campanha, entrada)

    def adicionar_segmento(
        self, id_campanha: UUID, entrada: SalvarSegmentoEntrada,
    ) -> BriefingResumo:
        return self._adicionar_segmento.executar(id_campanha, entrada)

    def editar_segmento(
        self, id_campanha: UUID, id_segmento: UUID, entrada: SalvarSegmentoEntrada,
    ) -> BriefingResumo:
        return self._editar_segmento.executar(id_campanha, id_segmento, entrada)

    def remover_segmento(
        self, id_campanha: UUID, id_segmento: UUID,
    ) -> BriefingResumo:
        return self._remover_segmento.executar(id_campanha, id_segmento)

    def adicionar_publico(
        self, id_campanha: UUID, entrada: SalvarPublicoEntrada,
    ) -> BriefingResumo:
        return self._adicionar_publico.executar(id_campanha, entrada)

    def editar_publico(
        self, id_campanha: UUID, id_publico: UUID, entrada: SalvarPublicoEntrada,
    ) -> BriefingResumo:
        return self._editar_publico.executar(id_campanha, id_publico, entrada)

    def remover_publico(
        self, id_campanha: UUID, id_publico: UUID,
    ) -> BriefingResumo:
        return self._remover_publico.executar(id_campanha, id_publico)

    def listar_categorias_etapa_jornada(
        self,
    ) -> tuple[CategoriaEtapaJornadaResumo, ...]:
        return self._listar_categorias_etapa.executar()

    def adicionar_jornada(
        self, id_campanha: UUID, entrada: SalvarJornadaEntrada,
    ) -> BriefingResumo:
        return self._adicionar_jornada.executar(id_campanha, entrada)

    def editar_jornada(
        self, id_campanha: UUID, id_jornada: UUID, entrada: SalvarJornadaEntrada,
    ) -> BriefingResumo:
        return self._editar_jornada.executar(id_campanha, id_jornada, entrada)

    def remover_jornada(
        self, id_campanha: UUID, id_jornada: UUID,
    ) -> BriefingResumo:
        return self._remover_jornada.executar(id_campanha, id_jornada)

    def adicionar_etapa_jornada(
        self, id_campanha: UUID, id_jornada: UUID,
        entrada: SalvarEtapaJornadaEntrada,
    ) -> BriefingResumo:
        return self._adicionar_etapa_jornada.executar(id_campanha, id_jornada, entrada)

    def editar_etapa_jornada(
        self, id_campanha: UUID, id_jornada: UUID, id_etapa: UUID,
        entrada: SalvarEtapaJornadaEntrada,
    ) -> BriefingResumo:
        return self._editar_etapa_jornada.executar(
            id_campanha, id_jornada, id_etapa, entrada
        )

    def remover_etapa_jornada(
        self, id_campanha: UUID, id_jornada: UUID, id_etapa: UUID,
    ) -> BriefingResumo:
        return self._remover_etapa_jornada.executar(id_campanha, id_jornada, id_etapa)

    def listar_naturezas_limite_verba(
        self,
    ) -> tuple[NaturezaLimiteVerbaResumo, ...]:
        return self._listar_naturezas_limite_verba.executar()

    def definir_periodo_verba(
        self, id_campanha: UUID, entrada: SalvarPeriodoVerbaEntrada,
    ) -> BriefingResumo:
        return self._definir_periodo_verba.executar(id_campanha, entrada)

    def listar_categorias_restricao(self) -> tuple[DefinicaoCategoriaResumo, ...]:
        return self._gerenciar_condicoes.listar_restricoes()

    def listar_categorias_pretensao(self) -> tuple[DefinicaoCategoriaResumo, ...]:
        return self._gerenciar_condicoes.listar_pretensoes()

    def salvar_prioridade(self, id_campanha, entrada: SalvarPrioridadeEntrada, identificador=None):
        return self._gerenciar_condicoes.salvar_prioridade(id_campanha, entrada, identificador)

    def remover_prioridade(self, id_campanha, identificador):
        return self._gerenciar_condicoes.remover_prioridade(id_campanha, identificador)

    def salvar_restricao(self, id_campanha, entrada: SalvarRestricaoEntrada, identificador=None):
        return self._gerenciar_condicoes.salvar_restricao(id_campanha, entrada, identificador)

    def remover_restricao(self, id_campanha, identificador):
        return self._gerenciar_condicoes.remover_restricao(id_campanha, identificador)

    def definir_inexistencia_restricoes(
        self, id_campanha: UUID, entrada: DefinirInexistenciaRestricoesEntrada,
    ) -> BriefingResumo:
        return self._gerenciar_condicoes.definir_inexistencia_restricoes(id_campanha, entrada)

    def salvar_pretensao(self, id_campanha, entrada: SalvarPretensaoEntrada, identificador=None):
        return self._gerenciar_condicoes.salvar_pretensao(id_campanha, entrada, identificador)

    def remover_pretensao(self, id_campanha, identificador):
        return self._gerenciar_condicoes.remover_pretensao(id_campanha, identificador)
