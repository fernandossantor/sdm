import streamlit as st

from application.services.master_data_service import MasterDataService


def render(metadata, values=None):

    if values is None:
        values = {}

    result = {}

    with st.form(metadata.table):

        for field in metadata.fields:

            if not field.visible:
                continue

            value = values.get(field.name)

            if value is None:

                value = field.default

            if field.type == "text":

                result[field.name] = st.text_input(

                    field.label,

                    value or "",

                    help=field.help,

                    disabled=field.disabled

                )

            elif field.type == "textarea":

                result[field.name] = st.text_area(

                    field.label,

                    value or "",

                    help=field.help,

                    disabled=field.disabled

                )

            elif field.type == "number":

                result[field.name] = st.number_input(

                    field.label,

                    value=float(value or 0),

                    help=field.help,

                    disabled=field.disabled

                )

            elif field.type == "bool":

                result[field.name] = st.checkbox(

                    field.label,

                    value if value is not None else True

                )

            elif field.type == "select":

                options = field.options or []

                index = 0

                if value in options:

                    index = options.index(value)

                result[field.name] = st.selectbox(

                    field.label,

                    options,

                    index=index,

                    help=field.help

                )

            elif field.type == "lookup":

                service = MasterDataService(

                    field.lookup_table

                )

                rows = service.list()

                labels = {

                    row["id"]: row[field.lookup_label]

                    for row in rows

                }

                ids = list(labels.keys())

                captions = [

                    labels[i]

                    for i in ids

                ]

                index = 0

                if value in ids:

                    index = ids.index(value)

                if ids:

                    result[field.name] = ids[
                        st.selectbox(

                            field.label,

                            range(len(ids)),

                            index=index,

                            format_func=lambda i: captions[i]

                        )
                    ]

                else:

                    st.warning(

                        f"Cadastre dados em {field.lookup_table}."

                    )

                    result[field.name] = None

        salvar = st.form_submit_button(

            "Salvar",

            use_container_width=True

        )

    return salvar, result