import pandas as pd
import streamlit as st

from application.master_data.lookup_cache import LookupCache


def render(metadata, data):

    if not data:

        st.info("Nenhum registro.")

        return

    rows = []

    for row in data:

        record = {}

        for field in metadata.fields:

            if not field.visible:
                continue

            value = row.get(field.name)

            if field.type == "lookup":

                labels = LookupCache.labels(

                    field.lookup_table,

                    field.lookup_label

                )

                value = labels.get(value, "")

            record[field.label] = value

        rows.append(record)

    df = pd.DataFrame(rows)

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )