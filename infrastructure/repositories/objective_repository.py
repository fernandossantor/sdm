from infrastructure.database.database_schema import *

from infrastructure.repositories.base_repository import (
    BaseRepository
)


class ObjectiveRepository(BaseRepository):

    def __init__(self):

        super().__init__()

    # =====================================================
    # OBJETIVO
    # =====================================================

    def buscar(

        self,

        objetivo_id

    ):

        return self.by_id(

            OBJETIVOS,

            objetivo_id

        )

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):

        return self.ordered(

            OBJETIVOS,

            "nome"

        )