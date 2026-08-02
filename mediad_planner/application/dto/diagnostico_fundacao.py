from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiagnosticoFundacao:
    backend_operacional: bool
    versao_contrato: str
    motores_previstos: tuple[str, ...]
    camadas_verificadas: tuple[str, ...]
    mensagem: str
    erros: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "motores_previstos", tuple(self.motores_previstos))
        object.__setattr__(self, "camadas_verificadas", tuple(self.camadas_verificadas))
        object.__setattr__(self, "erros", tuple(self.erros))
