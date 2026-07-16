from dataclasses import dataclass, field
from typing import List


# ==========================================================
# DIAGNÓSTICO DO INVENTÁRIO
# ==========================================================

@dataclass
class DiagnosticoInventario:

    inventario: str

    plataforma: str

    ambiente: str

    score: float

    papel: str

    objetivo: float

    kpi: float

    audiencia: float

    metricas: float

    pontos_fortes: List[str] = field(default_factory=list)

    pontos_fracos: List[str] = field(default_factory=list)

    recomendacoes: List[str] = field(default_factory=list)


# ==========================================================
# RELATÓRIO DE DECISÃO
# ==========================================================

@dataclass
class DecisionReport:

    campanha: str

    objetivo: str

    diagnosticos: List[DiagnosticoInventario] = field(default_factory=list)

    observacoes: List[str] = field(default_factory=list)

    def adicionar(self, diagnostico):

        self.diagnosticos.append(diagnostico)

    @property
    def principais(self):

        return [

            d

            for d in self.diagnosticos

            if d.papel == "PRINCIPAL"

        ]

    @property
    def complementares(self):

        return [

            d

            for d in self.diagnosticos

            if d.papel == "COMPLEMENTAR"

        ]

    @property
    def apoio(self):

        return [

            d

            for d in self.diagnosticos

            if d.papel == "APOIO"

        ]

    @property
    def opcionais(self):

        return [

            d

            for d in self.diagnosticos

            if d.papel == "OPCIONAL"

        ]