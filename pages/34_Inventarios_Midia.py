from application.master_data.metadata import Metadata, Field

from components.crud.page import render

from application.services.master_data_service import MasterDataService


metadata = Metadata(

    title="Inventários",

    table="media_inventory",

    fields=[

        Field(

            "vehicle_id",

            "Veículo",

            "lookup",

            lookup_table="media_vehicles"

        ),

        Field(

            "channel_id",

            "Canal",

            "lookup",

            lookup_table="media_channels"

        ),

        Field(

            "format_id",

            "Formato",

            "lookup",

            lookup_table="media_formats"

        ),

        Field(

            "buying_model_id",

            "Modelo",

            "lookup",

            lookup_table="media_buying_models"

        ),

        Field(

            "inventory_name",

            "Nome"

        ),

        Field(

            "placement",

            "Placement"

        ),

        Field(

            "description",

            "Descrição",

            "textarea"

        ),

        Field(

            "supports_video",

            "Vídeo",

            "bool"

        ),

        Field(

            "supports_image",

            "Imagem",

            "bool",

            default=True

        ),

        Field(

            "supports_audio",

            "Áudio",

            "bool"

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

        "media_inventory"

    )

)