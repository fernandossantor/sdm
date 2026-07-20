from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Campaign:

    id: str | None = None

    code: str | None = None

    name: str = ""

    client: str = ""

    brand: str = ""

    product: str = ""

    objective: str = ""

    start_date: date | None = None

    end_date: date | None = None

    notes: str = ""

    status: str = "draft"

    created_at: datetime | None = None

    updated_at: datetime | None = None