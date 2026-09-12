from dataclasses import asdict, replace
from datetime import timedelta
from uuid import UUID

import pytest

from mediad_planner.application.dto.briefing import ContextoAcessoBriefings
from mediad_planner.application.dto.objetivos_declarados import DefinirVinculosObjetivoEntrada
from mediad_planner.application.use_cases.objetivos_declarados import DefinirVinculosObjetivo
from mediad_planner.domain.briefing.enums import EstadoBriefing
from mediad_planner.domain.briefing.objetivos_declarados import ObjetivosDeclarados
from mediad_planner.domain.common.enums import PapelAcesso
from mediad_planner.infrastructure.repositories.briefings_em_memoria import RepositorioBriefingsEmMemoria
from test_aplicabilidade_jornada import _dominio
from test_briefing_dominio import AGORA
from test_casos_uso_objetivos_declarados import entrada_marketing, entrada_comunicacao
from test_objetivos_declarados_dominio import marketing, comunicacao
from test_publicos import _preparar, _entrada


AUTOR = UUID(int=80)
PUBLICO = UUID(int=72)
PRACA = UUID(int=101)


def _dominio_objetivos():
    return replace(_dominio(), objetivos_declarados=ObjetivosDeclarados(
        (marketing(),), (comunicacao(relacionados=(UUID(int=1),)),),
    ))


def _ambiente_vinculos():
    ambiente, campanha, segmentos, pracas = _preparar()
    for i in range(2):
        ambiente.briefings.adicionar_publico(campanha, _entrada(
            (segmentos[i],), (pracas[i],), nome="Público com mesmo nome",
        ))
    resumo = ambiente.briefings.adicionar_objetivo_marketing(campanha, entrada_marketing())
    ambiente.briefings.adicionar_objetivo_comunicacao(campanha,
        entrada_comunicacao((resumo.objetivos_marketing[0].id_objetivo,)))
    return ambiente, campanha


def _objetivo(briefing, id_objetivo):
    return next(item for item in briefing.objetivos_declarados.marketing + briefing.objetivos_declarados.comunicacao
                if item.id_objetivo == id_objetivo)


@pytest.mark.parametrize("id_objetivo", (UUID(int=1), UUID(int=10)))
@pytest.mark.parametrize("publicos,pracas", (((), ()), ((PUBLICO,), ()), ((), (PRACA,)), ((PUBLICO,), (PRACA,))))
def test_define_e_retira_vinculos_preservando_demais_declaracoes(id_objetivo, publicos, pracas):
    original = _dominio_objetivos()
    antes = asdict(original)
    atualizado = original.definir_vinculos_objetivo(id_objetivo, publicos, pracas, AUTOR, AGORA)
    esperado = replace(_objetivo(original, id_objetivo), ids_publicos_relacionados=publicos,
                       ids_pracas_relacionadas=pracas)
    assert _objetivo(atualizado, id_objetivo) == esperado
    outro_id = UUID(int=10) if id_objetivo == UUID(int=1) else UUID(int=1)
    assert _objetivo(atualizado, outro_id) == _objetivo(original, outro_id)
    assert atualizado.estado is EstadoBriefing.EM_PREENCHIMENTO
    assert atualizado.atualizado_por == AUTOR
    assert atualizado.atualizado_em == AGORA
    assert atualizado.numero_versao == original.numero_versao
    assert atualizado.contexto_herdado == original.contexto_herdado
    assert atualizado.estrutura_territorial_populacional == original.estrutura_territorial_populacional
    retirado = atualizado.definir_vinculos_objetivo(id_objetivo, (), (), AUTOR, AGORA + timedelta(seconds=1))
    assert retirado.objetivos_declarados == original.objetivos_declarados
    assert asdict(original) == antes


@pytest.mark.parametrize("id_objetivo", (UUID(int=1), UUID(int=10)))
@pytest.mark.parametrize("campo,valor,erro", (
    ("ids_publicos_relacionados", ("72",), TypeError),
    ("ids_pracas_relacionadas", (101,), TypeError),
    ("ids_publicos_relacionados", (PUBLICO, PUBLICO), ValueError),
    ("ids_pracas_relacionadas", (PRACA, PRACA), ValueError),
))
def test_entidade_rejeita_identidades_invalidas_e_duplicadas(id_objetivo, campo, valor, erro):
    with pytest.raises(erro, match=campo):
        replace(_objetivo(_dominio_objetivos(), id_objetivo), **{campo: valor})


@pytest.mark.parametrize("id_objetivo", (UUID(int=1), UUID(int=10)))
def test_lista_de_entrada_nao_permite_mutar_vinculos_salvos(id_objetivo):
    publicos, pracas = [PUBLICO], [PRACA]
    entrada = DefinirVinculosObjetivoEntrada(id_objetivo, publicos, pracas)
    original = _dominio_objetivos()
    atualizado = original.definir_vinculos_objetivo(id_objetivo, publicos, pracas, AUTOR, AGORA)
    publicos.clear()
    pracas.clear()
    assert entrada.ids_publicos_relacionados == (PUBLICO,)
    assert entrada.ids_pracas_relacionadas == (PRACA,)
    assert _objetivo(atualizado, id_objetivo).ids_publicos_relacionados == (PUBLICO,)
    assert _objetivo(atualizado, id_objetivo).ids_pracas_relacionadas == (PRACA,)


@pytest.mark.parametrize("estado", (EstadoBriefing.EM_REVISAO, EstadoBriefing.CONCLUIDO, EstadoBriefing.SUBSTITUIDO))
def test_vinculos_respeitam_estados_nao_editaveis(estado):
    original = replace(_dominio_objetivos(), estado=estado)
    with pytest.raises(ValueError, match="não permite alteração"):
        original.definir_vinculos_objetivo(UUID(int=1), (PUBLICO,), (PRACA,), AUTOR, AGORA)


@pytest.mark.parametrize("autor,instante,erro,mensagem", (
    ("autor", AGORA, TypeError, "UUID"),
    (AUTOR, AGORA.replace(tzinfo=None), ValueError, "fuso"),
    (AUTOR, AGORA - timedelta(seconds=1), ValueError, "regredir"),
))
def test_vinculos_validam_autoria_e_data(autor, instante, erro, mensagem):
    with pytest.raises(erro, match=mensagem):
        _dominio_objetivos().definir_vinculos_objetivo(UUID(int=1), (), (), autor, instante)


@pytest.mark.parametrize("campo", ("ids_publicos_relacionados", "ids_pracas_relacionadas"))
@pytest.mark.parametrize("grupo", ("marketing", "comunicacao"))
def test_agregado_rejeita_referencia_inexistente_mesmo_sem_caso_de_uso(campo, grupo):
    original = _dominio_objetivos()
    item = getattr(original.objetivos_declarados, grupo)[0]
    objetivos = replace(original.objetivos_declarados, **{grupo: (replace(item, **{campo: (UUID(int=999),)}),)})
    with pytest.raises(ValueError, match="não existe no Briefing"):
        replace(original, objetivos_declarados=objetivos)


@pytest.mark.parametrize("papel", tuple(PapelAcesso))
def test_caso_de_uso_respeita_permissoes(papel):
    original = _dominio_objetivos()
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    chamadas = []
    def relogio():
        chamadas.append(True)
        return AGORA
    caso = DefinirVinculosObjetivo(repositorio,
        ContextoAcessoBriefings(AUTOR, original.id_espaco_trabalho, papel), relogio)
    entrada = DefinirVinculosObjetivoEntrada(UUID(int=1), (PUBLICO,), (PRACA,))
    if papel in (PapelAcesso.PROPRIETARIO, PapelAcesso.EDITOR):
        resumo = caso.executar(original.id_campanha, entrada)
        assert resumo.objetivos_marketing[0].ids_publicos_relacionados == (PUBLICO,)
        assert resumo.objetivos_marketing[0].ids_pracas_relacionadas == (PRACA,)
    else:
        with pytest.raises(PermissionError):
            caso.executar(original.id_campanha, entrada)
        assert chamadas == []
        assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize("alvo", ("espaco", "campanha", "objetivo", "publico", "praca", "id_invalido"))
def test_rejeicoes_preservam_dados_e_isolamento(alvo):
    original = _dominio_objetivos()
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    caso = DefinirVinculosObjetivo(repositorio, ContextoAcessoBriefings(
        AUTOR, UUID(int=999) if alvo == "espaco" else original.id_espaco_trabalho, PapelAcesso.EDITOR,
    ), lambda: AGORA)
    entrada = DefinirVinculosObjetivoEntrada(
        "1" if alvo == "id_invalido" else UUID(int=999) if alvo == "objetivo" else UUID(int=1),
        (UUID(int=999),) if alvo == "publico" else (PUBLICO,),
        (UUID(int=999),) if alvo == "praca" else (PRACA,),
    )
    erro = TypeError if alvo == "id_invalido" else ValueError if alvo in ("publico", "praca") else LookupError
    with pytest.raises(erro):
        caso.executar(UUID(int=999) if alvo == "campanha" else original.id_campanha, entrada)
    assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original


@pytest.mark.parametrize("grupo", ("objetivos_marketing", "objetivos_comunicacao"))
def test_aplicacao_salva_substitui_reabre_e_retira_multiplos_vinculos(grupo):
    ambiente, campanha = _ambiente_vinculos()
    resumo = ambiente.briefings.abrir_briefing(campanha)
    objetivo = getattr(resumo, grupo)[0]
    publicos = tuple(item.id_publico for item in resumo.publicos)
    pracas = tuple(item.id_praca for item in resumo.pracas)
    for ids_publicos, ids_pracas in ((publicos, pracas), (publicos[1:], pracas[:1]), ((), ())):
        salvo = ambiente.briefings.definir_vinculos_objetivo(campanha,
            DefinirVinculosObjetivoEntrada(objetivo.id_objetivo, ids_publicos, ids_pracas))
        assert ambiente.briefings.abrir_briefing(campanha) == salvo
        assert getattr(salvo, grupo)[0] == replace(objetivo,
            ids_publicos_relacionados=ids_publicos, ids_pracas_relacionadas=ids_pracas)


@pytest.mark.parametrize("grupo", ("objetivos_marketing", "objetivos_comunicacao"))
def test_remocao_de_publico_vinculado_exige_retirada_explicita(grupo):
    ambiente, campanha = _ambiente_vinculos()
    resumo = ambiente.briefings.abrir_briefing(campanha)
    objetivo = getattr(resumo, grupo)[0]
    publico = resumo.publicos[0]
    vinculado = ambiente.briefings.definir_vinculos_objetivo(campanha,
        DefinirVinculosObjetivoEntrada(objetivo.id_objetivo, (publico.id_publico,), ()))
    with pytest.raises(ValueError, match="Retire o vínculo"):
        ambiente.briefings.remover_publico(campanha, publico.id_publico)
    assert ambiente.briefings.abrir_briefing(campanha) == vinculado
    ambiente.briefings.definir_vinculos_objetivo(campanha,
        DefinirVinculosObjetivoEntrada(objetivo.id_objetivo, (), ()))
    removido = ambiente.briefings.remover_publico(campanha, publico.id_publico)
    assert publico.id_publico not in {item.id_publico for item in removido.publicos}


@pytest.mark.parametrize("id_objetivo", (UUID(int=1), UUID(int=10)))
def test_praca_vinculada_e_protegida_ate_retirar_vinculo(id_objetivo):
    original = _dominio_objetivos()
    estrutura = original.estrutura_territorial_populacional
    livre = replace(estrutura.pracas[0], id_praca=UUID(int=999), nome="Praça livre")
    original = replace(original, estrutura_territorial_populacional=replace(
        estrutura, pracas=estrutura.pracas + (livre,)))
    vinculado = original.definir_vinculos_objetivo(id_objetivo, (), (livre.id_praca,), AUTOR, AGORA)
    with pytest.raises(ValueError, match="Retire o vínculo"):
        vinculado.remover_praca(livre.id_praca, AUTOR, AGORA)
    retirado = vinculado.definir_vinculos_objetivo(id_objetivo, (), (), AUTOR, AGORA)
    assert retirado.remover_praca(livre.id_praca, AUTOR, AGORA).estrutura_territorial_populacional == estrutura


@pytest.mark.parametrize("alvo", ("objetivo", "publico", "praca"))
def test_entidade_existente_em_outra_campanha_nao_pode_ser_vinculada(alvo):
    original = _dominio_objetivos()
    estrutura = original.estrutura_territorial_populacional
    estrangeiro = replace(original, id_briefing=UUID(int=801), id_campanha=UUID(int=802),
        objetivos_declarados=ObjetivosDeclarados((marketing(numero=803),), ()),
        estrutura_territorial_populacional=replace(estrutura,
            publicos=(replace(estrutura.publicos[0], id_publico=UUID(int=804)),),
            pracas=estrutura.pracas + (replace(estrutura.pracas[0], id_praca=UUID(int=805), nome="Outra praça"),)))
    repositorio = RepositorioBriefingsEmMemoria()
    repositorio.salvar(original)
    repositorio.salvar(estrangeiro)
    caso = DefinirVinculosObjetivo(repositorio, ContextoAcessoBriefings(
        AUTOR, original.id_espaco_trabalho, PapelAcesso.EDITOR), lambda: AGORA)
    entrada = DefinirVinculosObjetivoEntrada(
        UUID(int=803) if alvo == "objetivo" else UUID(int=1),
        (UUID(int=804),) if alvo == "publico" else (),
        (UUID(int=805),) if alvo == "praca" else (),
    )
    with pytest.raises(LookupError if alvo == "objetivo" else ValueError):
        caso.executar(original.id_campanha, entrada)
    assert repositorio.obter_por_campanha(original.id_espaco_trabalho, original.id_campanha) == original
    assert repositorio.obter_por_campanha(estrangeiro.id_espaco_trabalho, estrangeiro.id_campanha) == estrangeiro


@pytest.mark.parametrize("grupo", ("objetivos_marketing", "objetivos_comunicacao"))
def test_editar_publico_preserva_vinculo_e_remover_objetivo_libera_publico(grupo):
    ambiente, campanha = _ambiente_vinculos()
    resumo = ambiente.briefings.abrir_briefing(campanha)
    # Retira a Comunicação para que a remoção do Marketing não esbarre no vínculo já existente entre objetivos.
    if grupo == "objetivos_marketing":
        resumo = ambiente.briefings.remover_objetivo_comunicacao(campanha, resumo.objetivos_comunicacao[0].id_objetivo)
    objetivo = getattr(resumo, grupo)[0]
    publico = resumo.publicos[0]
    vinculado = ambiente.briefings.definir_vinculos_objetivo(campanha,
        DefinirVinculosObjetivoEntrada(objetivo.id_objetivo, (publico.id_publico,), ()))
    editado = ambiente.briefings.editar_publico(campanha, publico.id_publico,
        _entrada(publico.ids_segmentos_origem, publico.ids_pracas, nome="Novo nome", prioridade=3))
    assert getattr(editado, grupo) == getattr(vinculado, grupo)
    remover = ambiente.briefings.remover_objetivo_marketing if grupo == "objetivos_marketing" else ambiente.briefings.remover_objetivo_comunicacao
    removido = remover(campanha, objetivo.id_objetivo)
    assert removido.publicos == editado.publicos
    assert removido.pracas == editado.pracas
    assert not getattr(removido, grupo)
    liberado = ambiente.briefings.remover_publico(campanha, publico.id_publico)
    assert publico.id_publico not in {item.id_publico for item in liberado.publicos}
