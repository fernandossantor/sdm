import streamlit as st


class Session:

    CURRENT_CAMPAIGN = "current_campaign"

    @staticmethod
    def initialize():

        defaults = {

            Session.CURRENT_CAMPAIGN: None

        }

        for key, value in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = value

    @staticmethod
    def current_campaign():

        return st.session_state.get(

            Session.CURRENT_CAMPAIGN

        )

    @staticmethod
    def set_current_campaign(

        campaign_id

    ):

        st.session_state[

            Session.CURRENT_CAMPAIGN

        ] = campaign_id

    @staticmethod
    def clear_campaign():

        st.session_state[

            Session.CURRENT_CAMPAIGN

        ] = None

    @staticmethod
    def has_campaign():

        return (

            Session.current_campaign()

            is not None

        )