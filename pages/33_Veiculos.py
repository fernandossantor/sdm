from application.master_data.metadata import Metadata, Field

from components.crud.page import render

from application.services.master_data_service import MasterDataService


metadata = Metadata(

    title="Veículos",

    table="media_vehicles",

    fields=[

        Field("name", "Nome"),

        Field("company", "Empresa"),

        Field("website", "Website"),

        Field("country", "País"),

        Field("description", "Descrição", "textarea"),

        Field("active", "Ativo", "bool")

    ]

)

render(

    metadata,

    MasterDataService("media_vehicles")

)