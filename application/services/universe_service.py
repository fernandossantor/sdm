from infrastructure.repositories.universe_repository import (
    UniverseRepository
)


class UniverseService:

    def __init__(self):

        self.repository = UniverseRepository()

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):

        return self.repository.listar()

    # =====================================================
    # BUSCAR
    # =====================================================

    def buscar(

        self,

        universo_id

    ):

        return self.repository.buscar(

            universo_id

        )

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar(

        self,

        dados

    ):

        erros = []

        if not dados.get(

            "nome"

        ):

            erros.append(

                "Nome é obrigatório."

            )

        populacao = dados.get(

            "populacao",

            0

        )

        try:

            populacao = int(

                populacao

            )

        except Exception:

            populacao = -1

        if populacao < 0:

            erros.append(

                "População inválida."

            )

        publico = dados.get(

            "publico_alvo",

            0

        )

        try:

            publico = int(

                publico

            )

        except Exception:

            publico = -1

        if publico < 0:

            erros.append(

                "Público-alvo inválido."

            )

        if (

            populacao > 0

            and

            publico > populacao

        ):

            erros.append(

                "O público-alvo não pode ser maior que a população."

            )

        return erros

    # =====================================================
    # SALVAR
    # =====================================================

    def salvar(

        self,

        dados

    ):

        erros = self.validar(

            dados

        )

        if erros:

            return False, erros

        try:
            self.repository.salvar(dados)
        except Exception as erro:
            return False, [f"Não foi possível salvar o Universo: {erro}"]

        return True, None

    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(

        self,

        universo_id,

        dados

    ):

        erros = self.validar(

            dados

        )

        if erros:

            return False, erros

        try:
            self.repository.atualizar(universo_id, dados)
        except Exception as erro:
            return False, [f"Não foi possível atualizar o Universo: {erro}"]

        return True, None

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir(

        self,

        universo_id

    ):

        self.repository.excluir(

            universo_id

        )

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        return self.repository.resumo()
