import json
from pathlib import Path

from mediad_planner.application.dto.catalogo_territorial import (
    EstadoCatalogoResumo,
    MunicipioCatalogoResumo,
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

    def _carregar_se_necessario(self) -> None:
        if self._estados is not None:
            return
        try:
            dados = json.loads(self._caminho_snapshot.read_text(encoding="utf-8"))
            estados, municipios = self._validar_e_converter(dados)
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
        agrupados: dict[str, list[MunicipioCatalogoResumo]] = {}
        for municipio in municipios:
            agrupados.setdefault(municipio.codigo_estado, []).append(municipio)
        self._estados = estados
        self._municipios_por_estado = {
            codigo: tuple(itens) for codigo, itens in agrupados.items()
        }

    @staticmethod
    def _validar_e_converter(
        dados: object,
    ) -> tuple[
        tuple[EstadoCatalogoResumo, ...],
        tuple[MunicipioCatalogoResumo, ...],
    ]:
        if not isinstance(dados, dict):
            raise TypeError("Raiz do snapshot inválida")
        metadados = dados["metadados"]
        estados_dados = dados["estados"]
        municipios_dados = dados["municipios"]
        if not isinstance(metadados, dict):
            raise TypeError("Metadados inválidos")
        if not isinstance(estados_dados, list) or not isinstance(municipios_dados, list):
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
        municipios = tuple(
            MunicipioCatalogoResumo(
                codigo=item["codigo"],
                nome=item["nome"],
                codigo_estado=item["codigo_estado"],
            )
            for item in municipios_dados
        )
        if len({item.codigo for item in municipios}) != len(municipios):
            raise ValueError("Código de Município duplicado")
        if any(item.codigo_estado not in codigos_estados for item in municipios):
            raise ValueError("Município relacionado a UF inexistente")
        sentinela = next((item for item in municipios if item.nome == "São Borja"), None)
        if sentinela is None or sentinela.codigo != "4318002":
            raise ValueError("Sentinela São Borja ausente ou inválida")
        return estados, municipios
