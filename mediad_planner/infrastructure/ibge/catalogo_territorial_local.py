import json
from pathlib import Path

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
    RegiaoGeograficaImediataCatalogoResumo,
    RegiaoGeograficaIntermediariaCatalogoResumo,
)
from mediad_planner.application.ports.catalogo_territorial import (
    CatalogoTerritorialIndisponivel,
)


MENSAGEM_INDISPONIVEL = "Catálogo territorial do IBGE indisponível no momento"
CAMINHO_PADRAO = Path(__file__).parent / "dados" / "catalogo_dtb_2025.json"


class CatalogoTerritorialLocal:
    def __init__(self, caminho_snapshot: Path | None = None) -> None:
        self._caminho_snapshot = caminho_snapshot or CAMINHO_PADRAO
        self._estados: tuple[EstadoCatalogoResumo, ...] | None = None
        self._municipios_por_estado: dict[
            str,
            tuple[MunicipioCatalogoResumo, ...],
        ] | None = None
        self._intermediarias_por_estado: dict[
            str,
            tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...],
        ] | None = None
        self._imediatas_por_intermediaria: dict[
            str,
            tuple[RegiaoGeograficaImediataCatalogoResumo, ...],
        ] | None = None

    def listar_estados(self) -> tuple[EstadoCatalogoResumo, ...]:
        self._carregar_se_necessario()
        assert self._estados is not None
        return self._estados

    def listar_municipios(
        self,
        codigo_estado: str,
    ) -> tuple[MunicipioCatalogoResumo, ...]:
        self._carregar_se_necessario()
        assert self._municipios_por_estado is not None
        return self._municipios_por_estado.get(codigo_estado, ())

    def listar_regioes_intermediarias(
        self,
        codigo_estado: str,
    ) -> tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...]:
        self._carregar_se_necessario()
        assert self._intermediarias_por_estado is not None
        return self._intermediarias_por_estado.get(codigo_estado, ())

    def listar_regioes_imediatas(
        self,
        codigo_regiao_intermediaria: str,
    ) -> tuple[RegiaoGeograficaImediataCatalogoResumo, ...]:
        self._carregar_se_necessario()
        assert self._imediatas_por_intermediaria is not None
        return self._imediatas_por_intermediaria.get(
            codigo_regiao_intermediaria,
            (),
        )

    def _carregar_se_necessario(self) -> None:
        if self._estados is not None:
            return
        try:
            dados = json.loads(self._caminho_snapshot.read_text(encoding="utf-8"))
            estados, municipios, intermediarias, imediatas = (
                self._validar_e_converter(dados)
            )
        except (
            FileNotFoundError,
            PermissionError,
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ) as erro:
            raise CatalogoTerritorialIndisponivel(MENSAGEM_INDISPONIVEL) from erro
        self._estados = estados
        self._municipios_por_estado = self._agrupar_municipios(municipios)
        self._intermediarias_por_estado = self._agrupar_intermediarias(
            intermediarias
        )
        self._imediatas_por_intermediaria = self._agrupar_imediatas(imediatas)

    @staticmethod
    def _agrupar_municipios(
        municipios: tuple[MunicipioCatalogoResumo, ...],
    ) -> dict[str, tuple[MunicipioCatalogoResumo, ...]]:
        agrupados: dict[str, list[MunicipioCatalogoResumo]] = {}
        for municipio in municipios:
            agrupados.setdefault(municipio.codigo_estado, []).append(municipio)
        return {
            codigo: tuple(
                sorted(itens, key=lambda item: (item.nome.casefold(), item.codigo))
            )
            for codigo, itens in agrupados.items()
        }

    @staticmethod
    def _agrupar_intermediarias(
        regioes: tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...],
    ) -> dict[str, tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...]]:
        agrupadas: dict[
            str,
            list[RegiaoGeograficaIntermediariaCatalogoResumo],
        ] = {}
        for regiao in regioes:
            agrupadas.setdefault(regiao.codigo_estado, []).append(regiao)
        return {
            codigo: tuple(
                sorted(itens, key=lambda item: (item.nome.casefold(), item.codigo))
            )
            for codigo, itens in agrupadas.items()
        }

    @staticmethod
    def _agrupar_imediatas(
        regioes: tuple[RegiaoGeograficaImediataCatalogoResumo, ...],
    ) -> dict[str, tuple[RegiaoGeograficaImediataCatalogoResumo, ...]]:
        agrupadas: dict[str, list[RegiaoGeograficaImediataCatalogoResumo]] = {}
        for regiao in regioes:
            agrupadas.setdefault(
                regiao.codigo_regiao_intermediaria,
                [],
            ).append(regiao)
        return {
            codigo: tuple(
                sorted(itens, key=lambda item: (item.nome.casefold(), item.codigo))
            )
            for codigo, itens in agrupadas.items()
        }

    @staticmethod
    def _validar_e_converter(
        dados: object,
    ) -> tuple[
        tuple[EstadoCatalogoResumo, ...],
        tuple[MunicipioCatalogoResumo, ...],
        tuple[RegiaoGeograficaIntermediariaCatalogoResumo, ...],
        tuple[RegiaoGeograficaImediataCatalogoResumo, ...],
    ]:
        if not isinstance(dados, dict):
            raise TypeError("Raiz do snapshot inválida")
        metadados = dados["metadados"]
        estados_dados = dados["estados"]
        municipios_dados = dados["municipios"]
        if not isinstance(metadados, dict):
            raise TypeError("Metadados inválidos")
        if not isinstance(estados_dados, list) or not isinstance(
            municipios_dados,
            list,
        ):
            raise TypeError("Coleções do snapshot inválidas")
        if metadados["quantidade_estados"] != len(estados_dados):
            raise ValueError("Contagem de Estados incompatível")
        if metadados["quantidade_municipios"] != len(municipios_dados):
            raise ValueError("Contagem de Municípios incompatível")
        estados = tuple(
            EstadoCatalogoResumo(
                codigo=item["codigo"],
                sigla=item["sigla"],
                nome=item["nome"],
                codigo_regiao=item.get("codigo_regiao"),
                sigla_regiao=item.get("sigla_regiao"),
                nome_regiao=item.get("nome_regiao"),
            )
            for item in estados_dados
        )
        codigos_estados = {item.codigo for item in estados}
        if len(codigos_estados) != len(estados):
            raise ValueError("Código de Estado duplicado")
        municipios = []
        intermediarias: dict[
            str,
            RegiaoGeograficaIntermediariaCatalogoResumo,
        ] = {}
        imediatas: dict[str, RegiaoGeograficaImediataCatalogoResumo] = {}
        codigos_municipios = set()
        for item in municipios_dados:
            municipio = MunicipioCatalogoResumo(
                codigo=item["codigo"],
                nome=item["nome"],
                codigo_estado=item["codigo_estado"],
            )
            if municipio.codigo in codigos_municipios:
                raise ValueError("Código de Município duplicado")
            if municipio.codigo_estado not in codigos_estados:
                raise ValueError("Município relacionado a UF inexistente")
            codigos_municipios.add(municipio.codigo)
            municipios.append(municipio)
            intermediaria = RegiaoGeograficaIntermediariaCatalogoResumo(
                codigo=item["codigo_regiao_intermediaria"],
                nome=item["nome_regiao_intermediaria"],
                codigo_estado=municipio.codigo_estado,
            )
            anterior_intermediaria = intermediarias.setdefault(
                intermediaria.codigo,
                intermediaria,
            )
            if anterior_intermediaria != intermediaria:
                raise ValueError("Região Geográfica Intermediária conflitante")
            imediata = RegiaoGeograficaImediataCatalogoResumo(
                codigo=item["codigo_regiao_imediata"],
                nome=item["nome_regiao_imediata"],
                codigo_estado=municipio.codigo_estado,
                codigo_regiao_intermediaria=intermediaria.codigo,
            )
            anterior_imediata = imediatas.setdefault(imediata.codigo, imediata)
            if anterior_imediata != imediata:
                raise ValueError("Região Geográfica Imediata conflitante")
        if any(
            item.codigo_regiao_intermediaria not in intermediarias
            for item in imediatas.values()
        ):
            raise ValueError("Região Imediata relacionada a Intermediária inexistente")
        sentinela_municipio = next(
            (item for item in municipios if item.nome == "São Borja"),
            None,
        )
        if sentinela_municipio is None or sentinela_municipio.codigo != "4318002":
            raise ValueError("Sentinela São Borja ausente ou inválida")
        sentinela_intermediaria = intermediarias.get("4304")
        if sentinela_intermediaria != RegiaoGeograficaIntermediariaCatalogoResumo(
            codigo="4304",
            nome="Uruguaiana",
            codigo_estado="43",
        ):
            raise ValueError(
                "Sentinela regional intermediária ausente ou inválida"
            )
        sentinela_imediata = imediatas.get("430017")
        if sentinela_imediata != RegiaoGeograficaImediataCatalogoResumo(
            codigo="430017",
            nome="São Borja",
            codigo_estado="43",
            codigo_regiao_intermediaria="4304",
        ):
            raise ValueError("Sentinela regional imediata ausente ou inválida")
        return (
            estados,
            tuple(municipios),
            tuple(intermediarias.values()),
            tuple(imediatas.values()),
        )
