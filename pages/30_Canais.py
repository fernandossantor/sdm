from application.master_data.metadata import Metadata, Field

from components.crud.page import render

from application.services.master_data_service import MasterDataService


metadata = Metadata(

    title="Canais",

    table="media_channels",

    fields=[

        Field("name","Nome"),

        Field("description","Descrição","textarea"),

        Field("active","Ativo","bool")

    ]

)

render(

    metadata,

    MasterDataService("media_channels")

)