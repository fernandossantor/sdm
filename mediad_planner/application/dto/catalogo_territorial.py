from dataclasses import dataclass


def _validar_codigo(valor: str, tamanho: int, mensagem: str) -> str:
    if not isinstance(valor, str) or len(valor) != tamanho or not valor.isdigit():
        raise ValueError(mensagem)
    return valor


def _normalizar_texto(valor: str, mensagem: str) -> str:
    if not isinstance(valor, str):
        raise TypeError(mensagem)
    normalizado = valor.strip()
    if not normalizado:
        raise ValueError(mensagem)
    return normalizado


def _normalizar_opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise TypeError("Metadado territorial inválido")
    return valor.strip() or None


@dataclass(frozen=True, slots=True)
class EstadoCatalogoResumo:
    codigo: str
    sigla: str
    nome: str
    codigo_regiao: str | None
    sigla_regiao: str | None
    nome_regiao: str | None

    def __post_init__(self) -> None:
        codigo = _validar_codigo(self.codigo, 2, "Código de UF inválido")
        if not isinstance(self.sigla, str):
            raise TypeError("Sigla de UF inválida")
        sigla = self.sigla.strip().upper()
        if len(sigla) != 2 or not sigla.isalpha():
            raise ValueError("Sigla de UF inválida")
        object.__setattr__(self, "codigo", codigo)
        object.__setattr__(self, "sigla", sigla)
        object.__setattr__(self, "nome", _normalizar_texto(self.nome, "Nome de UF inválido"))
        object.__setattr__(self, "codigo_regiao", _normalizar_opcional(self.codigo_regiao))
        object.__setattr__(self, "sigla_regiao", _normalizar_opcional(self.sigla_regiao))
        object.__setattr__(self, "nome_regiao", _normalizar_opcional(self.nome_regiao))


@dataclass(frozen=True, slots=True)
class MunicipioCatalogoResumo:
    codigo: str
    nome: str
    codigo_estado: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "codigo",
            _validar_codigo(self.codigo, 7, "Código de Município inválido"),
        )
        object.__setattr__(self, "nome", _normalizar_texto(self.nome, "Nome inválido"))
        object.__setattr__(
            self,
            "codigo_estado",
            _validar_codigo(self.codigo_estado, 2, "Código de UF inválido"),
        )


@dataclass(frozen=True, slots=True)
class RegiaoGeograficaIntermediariaCatalogoResumo:
    codigo: str
    nome: str
    codigo_estado: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "codigo",
            _validar_codigo(
                self.codigo,
                4,
                "Código de Região Geográfica Intermediária inválido",
            ),
        )
        object.__setattr__(
            self,
            "nome",
            _normalizar_texto(self.nome, "Nome inválido"),
        )
        object.__setattr__(
            self,
            "codigo_estado",
            _validar_codigo(self.codigo_estado, 2, "Código de UF inválido"),
        )


@dataclass(frozen=True, slots=True)
class RegiaoGeograficaImediataCatalogoResumo:
    codigo: str
    nome: str
    codigo_estado: str
    codigo_regiao_intermediaria: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "codigo",
            _validar_codigo(
                self.codigo,
                6,
                "Código de Região Geográfica Imediata inválido",
            ),
        )
        object.__setattr__(
            self,
            "nome",
            _normalizar_texto(self.nome, "Nome inválido"),
        )
        object.__setattr__(
            self,
            "codigo_estado",
            _validar_codigo(self.codigo_estado, 2, "Código de UF inválido"),
        )
        object.__setattr__(
            self,
            "codigo_regiao_intermediaria",
            _validar_codigo(
                self.codigo_regiao_intermediaria,
                4,
                "Código de Região Geográfica Intermediária inválido",
            ),
        )
