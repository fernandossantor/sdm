from infrastructure.repositories.universe_repository import (
    UniverseRepository
)
from application.services.identifier_service import IdentifierService


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

        if not dados.get("cidade", "").strip():
            erros.append("Cidade é obrigatória.")

        if not dados.get("estado"):
            erros.append("Estado é obrigatório.")

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

        try:
            self.repository.excluir(universo_id)
            return True, "Universo excluído."
        except Exception:
            self.repository.atualizar(universo_id, {"ativo": False})
            return True, (
                "O Universo possui dependências e foi arquivado para preservar "
                "Segmentos e Públicos existentes."
            )

    def duplicar(self, universo):
        novo_id, codigo = IdentifierService.preparar_copia(universo, "universos")
        dados = {k: v for k, v in universo.items() if k not in {"id", "codigo", "criado_em", "atualizado_em"}}
        dados.update({"id": novo_id, "codigo": codigo, "nome": f"{universo['nome']} — cópia"})
        return self.repository.salvar(dados).data[0]

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        return self.repository.resumo()
