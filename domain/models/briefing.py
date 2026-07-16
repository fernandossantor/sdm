from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


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

    tipo_flight: str = "CONTINUO"

    frequencia_objetivo: Optional[str] = None

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

        frequencias = [

            None,

            "LIVRE",

            "1-2",

            "3-5",

            "6+"

        ]

        if self.frequencia_objetivo not in frequencias:

            erros.append(
                "Frequência inválida."
            )

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