from application.master_data.metadata import Metadata, Field

from components.crud.page import render

from application.services.master_data_service import MasterDataService


metadata = Metadata(

    title="Formatos",

    table="media_formats",

    fields=[

        Field(

            "channel_id",

            "Canal",

            "lookup",

            lookup_table="media_channels"

        ),

        Field(

            "name",

            "Nome",

            required=True

        ),

        Field(

            "description",

            "Descrição",

            "textarea"

        ),

        Field(

            "active",

            "Ativo",

            "bool",

            default=True

        )

    ]

)

render(

    metadata,

    MasterDataService(

        "media_formats"

    )

)