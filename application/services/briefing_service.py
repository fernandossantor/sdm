from domain.models.briefing import Briefing


class BriefingService:

    # =====================================================
    # CONSTRUÇÃO
    # =====================================================

    def criar(

        self,

        cliente,

        campanha,

        objetivo_id,

        objetivo,

        kpi,

        orcamento,

        inicio=None,

        fim=None,

        praca=None,

        universo=None,

        segmento=None,

        audiencia_id=None,

        jornada=None,

        observacoes="",

        inventarios_obrigatorios=None,

        inventarios_proibidos=None,

        plataformas_obrigatorias=None,

        ambientes_obrigatorios=None,

        tecnologias_obrigatorias=None,

        verba_teste=0,

        #
        # Sprint 3
        #

        marca="",

        produto="",

        objetivos_secundarios=None,

        kpis=None,

        publicos=None,

        tipo_flight="CONTINUO",

        frequencia_objetivo=None,

        plataformas_proibidas=None,

        ambientes_proibidos=None,

        tecnologias_proibidas=None

    ):

        #
        # Compatibilidade
        #

        inventarios_obrigatorios = inventarios_obrigatorios or []

        inventarios_proibidos = inventarios_proibidos or []

        plataformas_obrigatorias = plataformas_obrigatorias or []

        plataformas_proibidas = plataformas_proibidas or []

        ambientes_obrigatorios = ambientes_obrigatorios or []

        ambientes_proibidos = ambientes_proibidos or []

        tecnologias_obrigatorias = tecnologias_obrigatorias or []

        tecnologias_proibidas = tecnologias_proibidas or []

        objetivos_secundarios = objetivos_secundarios or []

        kpis = kpis or []

        publicos = publicos or []

        #
        # Compatibilidade entre KPI único e lista
        #

        if not kpis and kpi:

            kpis = [

                {

                    "id": None,

                    "nome": kpi,

                    "peso": 100

                }

            ]

        #
        # Compatibilidade entre audiência única e públicos
        #

        if not publicos and audiencia_id:

            publicos = [

                {

                    "audiencia_id": audiencia_id,

                    "peso": 100

                }

            ]

        briefing = Briefing(

            cliente=cliente,

            campanha=campanha,

            objetivo_id=objetivo_id,

            objetivo=objetivo,

            kpi=kpi,

            orcamento=orcamento,

            marca=marca,

            produto=produto,

            objetivos_secundarios=objetivos_secundarios,

            kpis=kpis,

            inicio=inicio,

            fim=fim,

            tipo_flight=tipo_flight,

            frequencia_objetivo=frequencia_objetivo,

            praca=praca,

            universo=universo,

            segmento=segmento,

            audiencia_id=audiencia_id,

            publicos=publicos,

            jornada=jornada,

            observacoes=observacoes,

            inventarios_obrigatorios=inventarios_obrigatorios,

            inventarios_proibidos=inventarios_proibidos,

            plataformas_obrigatorias=plataformas_obrigatorias,

            plataformas_proibidas=plataformas_proibidas,

            ambientes_obrigatorios=ambientes_obrigatorios,

            ambientes_proibidos=ambientes_proibidos,

            tecnologias_obrigatorias=tecnologias_obrigatorias,

            tecnologias_proibidas=tecnologias_proibidas,

            verba_teste=verba_teste

        )

        return briefing

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validar(

        self,

        briefing

    ):

        return briefing.validar()

    # =====================================================
    # SESSION
    # =====================================================

    def salvar(

        self,

        session_state,

        briefing

    ):

        session_state["briefing"] = briefing

    # =====================================================
    # RECUPERAR
    # =====================================================

    def recuperar(

        self,

        session_state

    ):

        return session_state.get(

            "briefing"

        )

    # =====================================================
    # EXISTE
    # =====================================================

    def existe(

        self,

        session_state

    ):

        return "briefing" in session_state

    # =====================================================
    # LIMPAR
    # =====================================================

    def limpar(

        self,

        session_state

    ):

        if "briefing" in session_state:

            del session_state["briefing"]

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(

        self,

        briefing

    ):

        return {

            "cliente": briefing.cliente,

            "campanha": briefing.campanha,

            "objetivo": briefing.objetivo,

            "orcamento": briefing.orcamento,

            "kpis": len(briefing.kpis),

            "publicos": len(briefing.publicos),

            "flight": briefing.tipo_flight,

            "frequencia": briefing.frequencia_objetivo

        }