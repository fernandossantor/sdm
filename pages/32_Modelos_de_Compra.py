from application.master_data.metadata import Metadata, Field

from components.crud.page import render

from application.services.master_data_service import MasterDataService


metadata = Metadata(

    title="Modelos de Compra",

    table="media_buying_models",

    fields=[

        Field("name", "Nome"),

        Field("billing_metric", "Métrica de Cobrança"),

        Field("description", "Descrição", "textarea"),

        Field("active", "Ativo", "bool")

    ]

)

render(

    metadata,

    MasterDataService("media_buying_models")

)