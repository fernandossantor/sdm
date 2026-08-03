import ast
from pathlib import Path

from streamlit.testing.v1 import AppTest


RAIZ = Path(__file__).parents[1]
ARQUIVOS = (
    RAIZ / "mediad_planner" / "presentation" / "campanhas.py",
    RAIZ / "mediad_planner" / "presentation" / "streamlit_app.py",
)


def _modulos_importados(caminho: Path) -> tuple[str, ...]:
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    modulos = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            modulos.extend(alias.name for alias in no.names)
        elif isinstance(no, ast.ImportFrom):
            if no.level:
                modulos.append(f"relativo:{no.level}:{no.module or ''}")
            elif no.module:
                modulos.append(no.module)
    return tuple(modulos)


def test_apresentacao_nao_importa_camadas_proibidas() -> None:
    prefixos_proibidos = (
        "mediad_planner.domain",
        "mediad_planner.engines",
        "mediad_planner.infrastructure",
    )
    for caminho in ARQUIVOS:
        for modulo in _modulos_importados(caminho):
            assert not modulo.startswith(prefixos_proibidos)
            assert not modulo.startswith("relativo:")


def test_frontoffice_importa_aplicacao_ou_composicao_autorizada() -> None:
    modulos = _modulos_importados(ARQUIVOS[0])
    assert any(
        modulo.startswith("mediad_planner.application") for modulo in modulos
    )
    modulos_controlador = _modulos_importados(ARQUIVOS[1])
    assert "mediad_planner.composition.ambiente" in modulos_controlador


def test_interface_contem_acoes_e_aviso_temporario() -> None:
    fonte = ARQUIVOS[0].read_text(encoding="utf-8")
    for texto in (
        "Cancelar",
        "Salvar como Rascunho",
        "Criar Campanha e iniciar Briefing",
        "Iniciar Briefing",
        "Persistência temporária em memória.",
        "perdidas quando o servidor é reiniciado.",
    ):
        assert texto in fonte


def test_abertura_usa_rotulos_e_ajudas_administrativas_precisas() -> None:
    fonte = ARQUIVOS[0].read_text(encoding="utf-8")
    for texto in (
        "Nome da Campanha",
        "Marca (opcional)",
        "Produto ou Serviço (opcional)",
        "Planejador Responsável",
        "Equipe da Campanha (opcional)",
        "Observação inicial (opcional)",
        "Use um nome que permita identificar esta iniciativa",
        "Nesta versão temporária, informe o nome do responsável.",
        "Informe um nome por linha.",
        "Dados mercadológicos e estratégicos devem ser informados no Briefing.",
    ):
        assert texto in fonte
    for antigo in (
        'st.text_input("Nome")',
        'st.text_input("Marca opcional")',
        'st.text_input("Produto ou Serviço opcional")',
    ):
        assert antigo not in fonte


def test_interface_nao_contem_motores_formulas_ou_sql() -> None:
    fonte = ARQUIVOS[0].read_text(encoding="utf-8").casefold()
    termos_proibidos = (
        "select *",
        "insert into",
        "update campanhas",
        "delete from",
        "motor_especialista",
        "executar_motor",
        "cpm",
        "grp",
    )
    for termo in termos_proibidos:
        assert termo not in fonte


def _e_chamada_expander(no: ast.AST) -> bool:
    return (
        isinstance(no, ast.Call)
        and isinstance(no.func, ast.Attribute)
        and no.func.attr == "expander"
        and isinstance(no.func.value, ast.Name)
        and no.func.value.id == "st"
    )


class _DetectorExpanderAninhado(ast.NodeVisitor):
    def __init__(self) -> None:
        self.profundidade = 0
        self.aninhado = False
        self.rotulos: list[str] = []

    def visit_With(self, no: ast.With) -> None:
        contem_expander = any(
            _e_chamada_expander(item.context_expr) for item in no.items
        )
        if contem_expander:
            if self.profundidade:
                self.aninhado = True
            self.profundidade += 1
            for item in no.items:
                chamada = item.context_expr
                if _e_chamada_expander(chamada) and chamada.args:
                    argumento = chamada.args[0]
                    if isinstance(argumento, ast.Constant):
                        self.rotulos.append(argumento.value)
            for instrucao in no.body:
                self.visit(instrucao)
            self.profundidade -= 1
            return
        self.generic_visit(no)


def test_streamlit_app_nao_possui_expander_aninhado() -> None:
    fonte = ARQUIVOS[1].read_text(encoding="utf-8")
    detector = _DetectorExpanderAninhado()
    detector.visit(ast.parse(fonte))
    assert detector.aninhado is False
    assert "Estado da fundação" in detector.rotulos
    assert "Detalhes técnicos" in fonte


def test_app_renderiza_sem_excecoes() -> None:
    app = AppTest.from_file(str(RAIZ / "app.py"))
    app.run(timeout=3)
    assert not app.exception
