from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from domain.media_metrics import resolver_grp


# ==========================================================
# BRIEFING
# ==========================================================

@dataclass
class Briefing:

    # ------------------------------------------------------
    # IDENTIFICAÇÃO
    # ------------------------------------------------------

    cliente: str

    campanha: str

    objetivo_id: str

    objetivo: str

    kpi: str

    orcamento: float

    # ------------------------------------------------------
    # NOVOS CAMPOS (Sprint 3)
    # ------------------------------------------------------

    marca: str = ""

    produto: str = ""

    objetivos_secundarios: List[str] = field(
        default_factory=list
    )

    #
    # Mantém compatibilidade com o campo "kpi"
    #

    kpis: List[dict] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # PLANEJAMENTO
    # ------------------------------------------------------

    inicio: Optional[date] = None

    fim: Optional[date] = None

    #
    # Flight
    #

    tipo_flight: str = "LINEAR"

    frequencia_objetivo: Optional[str] = None

    frequencia_alvo: Optional[float] = 5

    alcance_objetivo: str = "MEDIO"

    alcance_percentual: Optional[float] = 60

    grp: Optional[float] = None

    praca: Optional[str] = None

    universo: Optional[str] = None

    segmento: Optional[str] = None

    #
    # Compatibilidade
    #

    audiencia_id: Optional[str] = None

    #
    # Novo modelo
    #

    publicos: List[dict] = field(
        default_factory=list
    )

    jornada: Optional[str] = None

    observacoes: str = ""

    # ------------------------------------------------------
    # RESTRIÇÕES
    # ------------------------------------------------------

    inventarios_obrigatorios: List[str] = field(
        default_factory=list
    )

    inventarios_proibidos: List[str] = field(
        default_factory=list
    )

    plataformas_obrigatorias: List[str] = field(
        default_factory=list
    )

    plataformas_proibidas: List[str] = field(
        default_factory=list
    )

    ambientes_obrigatorios: List[str] = field(
        default_factory=list
    )

    ambientes_proibidos: List[str] = field(
        default_factory=list
    )

    tecnologias_obrigatorias: List[str] = field(
        default_factory=list
    )

    tecnologias_proibidas: List[str] = field(
        default_factory=list
    )

    verba_teste: float = 0.0

    registro_id: Optional[str] = None

    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    def validar(self):

        erros = []

        if not self.cliente:

            erros.append(
                "Cliente é obrigatório."
            )

        if not self.campanha:

            erros.append(
                "Campanha é obrigatória."
            )

        if not self.objetivo_id:

            erros.append(
                "Objetivo é obrigatório."
            )

        #
        # Compatibilidade entre KPI único e múltiplos KPIs
        #

        possui_kpi = bool(self.kpi)

        possui_lista = len(self.kpis) > 0

        if not possui_kpi and not possui_lista:

            erros.append(
                "Pelo menos um KPI deve ser informado."
            )

        if self.orcamento <= 0:

            erros.append(
                "Orçamento deve ser maior que zero."
            )

        #
        # Flight
        #

        if self.inicio and self.fim:

            if self.fim < self.inicio:

                erros.append(
                    "Data final anterior à data inicial."
                )

        #
        # Frequência
        #

        flights = ["LINEAR", "ONDA", "CONCENTRADO"]

        if self.tipo_flight not in flights:
            erros.append("Flight inválido.")

        frequencias = [

            None,

            "BAIXA",

            "MEDIA",

            "ALTA"

        ]

        if self.frequencia_objetivo not in frequencias:

            erros.append(
                "Frequência inválida."
            )

        if self.frequencia_alvo is not None:
            if self.frequencia_alvo < 1:
                erros.append("A frequência alvo deve ser maior que zero.")
            elif self.frequencia_objetivo == "BAIXA" and self.frequencia_alvo > 3:
                erros.append("Frequência baixa deve estar entre 1 e 3.")
            elif self.frequencia_objetivo == "MEDIA" and not 4 <= self.frequencia_alvo <= 7:
                erros.append("Frequência média deve estar entre 4 e 7.")
            elif self.frequencia_objetivo == "ALTA" and self.frequencia_alvo < 8:
                erros.append("Frequência alta deve ser 8 ou mais.")

        alcances = {
            "BAIXO": (0, 50),
            "MEDIO": (51, 69),
            "ALTO": (70, 100),
        }
        if self.alcance_objetivo not in alcances:
            erros.append("Faixa de alcance inválida.")
        else:
            minimo, maximo = alcances[self.alcance_objetivo]
            if self.alcance_percentual is None:
                erros.append("Informe o alcance ou permita que ele seja calculado pelo GRP.")
            elif not minimo <= self.alcance_percentual <= maximo:
                erros.append(
                    f"Alcance {self.alcance_objetivo.lower()} deve estar entre "
                    f"{minimo}% e {maximo}%."
                )

        try:
            resolver_grp(
                self.alcance_percentual,
                self.frequencia_alvo,
                self.grp,
            )
        except ValueError as erro:
            erros.append(str(erro))

        return erros

    # ======================================================
    # STATUS
    # ======================================================

    @property
    def valido(self):

        return len(

            self.validar()

        ) == 0

    # ======================================================
    # COMPATIBILIDADE
    # ======================================================

    @property
    def possui_multiplos_kpis(self):

        return len(

            self.kpis

        ) > 0

    @property
    def possui_publicos(self):

        return len(

            self.publicos

        ) > 0
