from infrastructure.repositories.public_repository import (
    PublicRepository
)


class PublicService:

    def __init__(self):

        self.repository = PublicRepository()

    # =====================================================
    # LISTAGEM
    # =====================================================

    def listar(self):

        return self.repository.listar()

    # =====================================================
    # BUSCA
    # =====================================================

    def buscar(

        self,

        publico_id

    ):

        publico = self.repository.buscar(

            publico_id

        )

        publico["segmentos"] = self.repository.segmentos(

            publico_id

        )

        publico["interesses"] = self.repository.interesses(

            publico_id

        )

        publico["jornadas"] = self.repository.jornadas(

            publico_id

        )

        return publico

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar(

        self,

        dados

    ):

        erros = []

        if not dados["nome"]:

            erros.append(

                "Nome é obrigatório."

            )

        return erros

    # =====================================================
    # SALVAR
    # =====================================================

    def salvar(

        self,

        dados,

        segmentos=None,

        interesses=None,

        jornada=None

    ):

        segmentos = segmentos or []

        interesses = interesses or []

        erros = self.validar(

            dados

        )

        if erros:

            return False, erros

        resposta = self.repository.salvar(

            dados

        )

        publico = resposta.data[0]

        publico_id = publico["id"]

        registros_segmentos = [

            {

                "publico_id": publico_id,

                "segmento_id": segmento

            }

            for segmento in segmentos

        ]

        registros_interesses = [

            {

                "publico_id": publico_id,

                "interesse_id": interesse

            }

            for interesse in interesses

        ]

        self.repository.salvar_segmentos(

            registros_segmentos

        )

        self.repository.salvar_interesses(

            registros_interesses

        )

        if jornada:

            self.repository.salvar_jornada(

                publico_id,

                jornada

            )

        return True, publico

    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(

        self,

        publico_id,

        dados

    ):

        erros = self.validar(

            dados

        )

        if erros:

            return False, erros

        self.repository.atualizar(

            publico_id,

            dados

        )

        return True, None

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir(

        self,

        publico_id

    ):

        self.repository.excluir(

            publico_id

        )

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        publicos = self.listar()

        return {

            "total": len(

                publicos

            ),

            "ativos": len(

                [

                    p

                    for p in publicos

                    if p["ativo"]

                ]

            )

        }