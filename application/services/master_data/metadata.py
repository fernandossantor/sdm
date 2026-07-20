from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Field:

    name: str

    label: str

    type: str = "text"

    required: bool = False
    default: object = None

    options: Optional[list] = None

    lookup_table: Optional[str] = None

    lookup_label: str = "name"

    default=None

    help: str = ""

    disabled: bool = False

    visible: bool = True

@dataclass
class Metadata:

    title: str

    table: str

    fields: List[Field] = field(default_factory=list)