import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="CRM OS Chat Bot",
        page_icon="📎",
    )

    st.write("# Welcome to the CRM OS Chat Bot! 📎")
    st.write("## Please ask me a question!")

    




if __name__ == "__main__":
    run()