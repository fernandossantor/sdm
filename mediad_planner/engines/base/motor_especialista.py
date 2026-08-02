from typing import Protocol, TypeVar, runtime_checkable

from mediad_planner.domain.contracts.motores import ComandoMotor, SaidaMotor


TResultado = TypeVar("TResultado", covariant=True)


@runtime_checkable
class MotorEspecialista(Protocol[TResultado]):
    def executar(self, comando: ComandoMotor) -> SaidaMotor[TResultado]:
        ...
