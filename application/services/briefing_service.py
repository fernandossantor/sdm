from domain.models.briefing import Briefing
from infrastructure.repositories.briefing_repository import BriefingRepository
from application.services.project_service import ProjectService
from infrastructure.database.database_schema import OBJETIVOS


class BriefingService:

    def __init__(self):
        self.repository = BriefingRepository()
        self.projetos = ProjectService()

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

        tipo_flight="LINEAR",

        frequencia_objetivo=None,

        frequencia_alvo=None,

        alcance_objetivo="MEDIO",

        alcance_percentual=60,

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

            frequencia_alvo=frequencia_alvo,

            alcance_objetivo=alcance_objetivo,

            alcance_percentual=alcance_percentual,

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
        for chave in (
            "mcp_papeis",
            "plano",
            "diagnostico",
            "forecast",
            "dashboard",
            "exportacao",
        ):
            session_state.pop(chave, None)

        projeto_id = session_state.get("projeto_id")
        if not projeto_id:
            return None

        dados = self._para_registro(briefing, projeto_id)
        briefing_id = session_state.get("briefing_id")
        if briefing_id:
            self.repository.atualizar(briefing_id, dados)
        else:
            resposta = self.repository.salvar(dados)
            briefing_id = resposta.data[0]["id"]
            session_state["briefing_id"] = briefing_id
        session_state["briefing_ref"] = briefing.campanha
        self.projetos.registrar(
            session_state, "briefing", True, briefing_id=briefing_id
        )
        return briefing_id

    def listar(self, projeto_id=None):
        try:
            return [
                item for item in self.repository.listar(projeto_id)
                if item.get("ativo", True)
            ]
        except Exception:
            return []

    def carregar(self, registro, session_state):
        briefing = self._do_registro(registro)
        session_state["briefing"] = briefing
        session_state["briefing_id"] = registro["id"]
        session_state["briefing_ref"] = briefing.campanha
        return briefing

    def restaurar(self, registro):
        return self._do_registro(registro)

    def excluir(self, briefing_id, session_state=None):
        resposta = self.repository.excluir(briefing_id)
        if session_state is not None and session_state.get("briefing_id") == briefing_id:
            for chave in ("briefing", "briefing_id", "briefing_ref"):
                session_state.pop(chave, None)
        return resposta

    @staticmethod
    def _para_registro(briefing, projeto_id=None):
        return {
            "projeto_id": projeto_id,
            "anunciante": briefing.cliente,
            "nome": briefing.campanha,
            "marca": briefing.marca,
            "produto": briefing.produto,
            "objetivo_id": briefing.objetivo_id,
            "kpi": briefing.kpi,
            "kpis": briefing.kpis,
            "orcamento": briefing.orcamento,
            "periodo_inicio": briefing.inicio.isoformat() if briefing.inicio else None,
            "periodo_fim": briefing.fim.isoformat() if briefing.fim else None,
            "tipo_flight": briefing.tipo_flight,
            "frequencia_objetivo": briefing.frequencia_objetivo,
            "frequencia_alvo": briefing.frequencia_alvo,
            "alcance_objetivo": briefing.alcance_objetivo,
            "alcance_percentual": briefing.alcance_percentual,
            "publicos": briefing.publicos,
            "observacoes": briefing.observacoes,
            "ativo": True,
        }

    def _do_registro(self, registro):
        from datetime import date

        objetivo = self.repository.by_id(OBJETIVOS, registro["objetivo_id"])
        briefing = self.criar(
            cliente=registro.get("anunciante", ""),
            campanha=registro.get("nome", ""),
            marca=registro.get("marca") or "",
            produto=registro.get("produto") or "",
            objetivo_id=registro.get("objetivo_id"),
            objetivo=objetivo.get("nome", ""),
            kpi=registro.get("kpi", ""),
            kpis=registro.get("kpis") or [],
            orcamento=float(registro.get("orcamento") or 0),
            inicio=date.fromisoformat(registro["periodo_inicio"][:10]) if registro.get("periodo_inicio") else None,
            fim=date.fromisoformat(registro["periodo_fim"][:10]) if registro.get("periodo_fim") else None,
            tipo_flight=registro.get("tipo_flight") or "LINEAR",
            frequencia_objetivo=registro.get("frequencia_objetivo") or "MEDIA",
            frequencia_alvo=int(registro.get("frequencia_alvo") or 5),
            alcance_objetivo=registro.get("alcance_objetivo") or "MEDIO",
            alcance_percentual=int(registro.get("alcance_percentual") or 60),
            publicos=registro.get("publicos") or [],
            observacoes=registro.get("observacoes") or "",
        )
        briefing.registro_id = registro["id"]
        return briefing

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

            ,"frequencia_alvo": briefing.frequencia_alvo

            ,"alcance": briefing.alcance_objetivo

            ,"alcance_percentual": briefing.alcance_percentual

        }
