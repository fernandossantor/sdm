import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
)
from mediad_planner.application.ports.catalogo_territorial import (
    CatalogoTerritorialIndisponivel,
)


URL_BASE_IBGE = "https://servicodados.ibge.gov.br/api/v1/localidades"
MENSAGEM_INDISPONIVEL = "Catálogo territorial do IBGE indisponível no momento"
LeitorJSON = Callable[[str, float], object]


def _ler_json_http(url: str, timeout_segundos: float) -> object:
    requisicao = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
            "User-Agent": "MediAd-Planner/1.0 catalogo-territorial",
        },
    )
    with urllib.request.urlopen(requisicao, timeout=timeout_segundos) as resposta:
        conteudo = resposta.read().decode("utf-8")
    return json.loads(conteudo)


def _codigo_numerico(valor: object, tamanho: int) -> str:
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError("Código territorial inválido")
    texto = str(valor)
    if not texto.isdigit() or len(texto) > tamanho:
        raise ValueError("Código territorial inválido")
    return texto.zfill(tamanho)


def _texto_obrigatorio(valor: object) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("Texto territorial inválido")
    return valor.strip()


class CatalogoTerritorialIBGE:
    def __init__(
        self,
        *,
        url_base: str = URL_BASE_IBGE,
        timeout_segundos: float = 5.0,
        duracao_cache_segundos: float = 86400.0,
        leitor_json: LeitorJSON | None = None,
        relogio_monotonico: Callable[[], float] = time.monotonic,
    ) -> None:
        if not isinstance(url_base, str) or not url_base.strip():
            raise ValueError("URL base do catálogo inválida")
        if timeout_segundos <= 0:
            raise ValueError("Timeout do catálogo deve ser positivo")
        if duracao_cache_segundos <= 0:
            raise ValueError("Duração do cache deve ser positiva")
        self._url_base = url_base.rstrip("/")
        self._timeout_segundos = timeout_segundos
        self._duracao_cache_segundos = duracao_cache_segundos
        self._leitor_json = leitor_json or _ler_json_http
        self._relogio_monotonico = relogio_monotonico
        self._cache_estados: tuple[tuple[EstadoCatalogoResumo, ...], float] | None = None
        self._cache_municipios: dict[
            str,
            tuple[tuple[MunicipioCatalogoResumo, ...], float],
        ] = {}

    def listar_estados(self) -> tuple[EstadoCatalogoResumo, ...]:
        agora = self._relogio_monotonico()
        if self._cache_estados is not None and agora < self._cache_estados[1]:
            return self._cache_estados[0]
        url = self._montar_url("estados")
        payload = self._consultar(url)
        try:
            estados = self._parsear_estados(payload)
        except (KeyError, TypeError, ValueError) as erro:
            raise CatalogoTerritorialIndisponivel(MENSAGEM_INDISPONIVEL) from erro
        self._cache_estados = (
            estados,
            agora + self._duracao_cache_segundos,
        )
        return estados

    def listar_municipios(
        self,
        codigo_estado: str,
    ) -> tuple[MunicipioCatalogoResumo, ...]:
        if (
            not isinstance(codigo_estado, str)
            or len(codigo_estado) != 2
            or not codigo_estado.isdigit()
        ):
            raise ValueError("Código de UF inválido")
        agora = self._relogio_monotonico()
        cache = self._cache_municipios.get(codigo_estado)
        if cache is not None and agora < cache[1]:
            return cache[0]
        url = self._montar_url(f"estados/{codigo_estado}/municipios")
        payload = self._consultar(url)
        try:
            municipios = self._parsear_municipios(payload, codigo_estado)
        except (KeyError, TypeError, ValueError) as erro:
            raise CatalogoTerritorialIndisponivel(MENSAGEM_INDISPONIVEL) from erro
        self._cache_municipios[codigo_estado] = (
            municipios,
            agora + self._duracao_cache_segundos,
        )
        return municipios

    def _montar_url(self, caminho: str) -> str:
        consulta = urllib.parse.urlencode({"orderBy": "nome"})
        return f"{self._url_base}/{caminho}?{consulta}"

    def _consultar(self, url: str) -> object:
        try:
            return self._leitor_json(url, self._timeout_segundos)
        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
            UnicodeError,
        ) as erro:
            raise CatalogoTerritorialIndisponivel(MENSAGEM_INDISPONIVEL) from erro

    @staticmethod
    def _parsear_estados(payload: object) -> tuple[EstadoCatalogoResumo, ...]:
        if not isinstance(payload, list):
            raise ValueError("Resposta de Estados inválida")
        estados = []
        for item in payload:
            if not isinstance(item, Mapping):
                raise TypeError("Item de Estado inválido")
            regiao = item["regiao"]
            if not isinstance(regiao, Mapping):
                raise TypeError("Região inválida")
            estados.append(
                EstadoCatalogoResumo(
                    codigo=_codigo_numerico(item["id"], 2),
                    sigla=_texto_obrigatorio(item["sigla"]),
                    nome=_texto_obrigatorio(item["nome"]),
                    codigo_regiao=_codigo_numerico(regiao["id"], 1),
                    sigla_regiao=_texto_obrigatorio(regiao["sigla"]),
                    nome_regiao=_texto_obrigatorio(regiao["nome"]),
                )
            )
        return tuple(estados)

    @staticmethod
    def _parsear_municipios(
        payload: object,
        codigo_estado: str,
    ) -> tuple[MunicipioCatalogoResumo, ...]:
        if not isinstance(payload, list):
            raise ValueError("Resposta de Municípios inválida")
        municipios = []
        for item in payload:
            if not isinstance(item, Mapping):
                raise TypeError("Item de Município inválido")
            municipios.append(
                MunicipioCatalogoResumo(
                    codigo=_codigo_numerico(item["id"], 7),
                    nome=_texto_obrigatorio(item["nome"]),
                    codigo_estado=codigo_estado,
                )
            )
        return tuple(municipios)
