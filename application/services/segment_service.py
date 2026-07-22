from infrastructure.repositories.segment_repository import (
    SegmentRepository
)


class SegmentService:

    def __init__(self):

        self.repository = SegmentRepository()

    # =====================================================
    # LISTAR
    # =====================================================

    def listar(self):

        return self.repository.listar()

    # =====================================================
    # POR UNIVERSO
    # =====================================================

    def listar_por_universo(

        self,

        universo_id

    ):

        return self.repository.listar_por_universo(

            universo_id

        )

    # =====================================================
    # BUSCAR
    # =====================================================

    def buscar(

        self,

        segmento_id

    ):

        return self.repository.buscar(

            segmento_id

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

            "universo_id"

        ):

            erros.append(

                "Universo é obrigatório."

            )

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

        if not dados.get("classes_sociais"):
            erros.append("Selecione ao menos uma classe social.")

        if not dados.get("faixas_etarias"):
            erros.append("Selecione ao menos uma faixa etária.")

        if not dados.get("escolaridades"):
            erros.append("Selecione ao menos uma escolaridade.")

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
            return False, [f"Não foi possível salvar o Segmento: {erro}"]

        return True, None

    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(

        self,

        segmento_id,

        dados

    ):

        erros = self.validar(

            dados

        )

        if erros:

            return False, erros

        try:
            self.repository.atualizar(segmento_id, dados)
        except Exception as erro:
            return False, [f"Não foi possível atualizar o Segmento: {erro}"]

        return True, None

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir(

        self,

        segmento_id

    ):

        try:
            self.repository.excluir(segmento_id)
            return True, "Segmento excluído."
        except Exception:
            self.repository.atualizar(segmento_id, {"ativo": False})
            return True, (
                "O Segmento está vinculado a Públicos e foi arquivado para "
                "preservar o histórico."
            )

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        segmentos = self.listar()

        return {

            "total": len(

                segmentos

            )

        }
