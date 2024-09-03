import streamlit as st
from customer_service.chat_interface import display_chat_interface

def main():
    st.set_page_config(page_title="Évasions Élégantes - Assistant de Voyage IA", page_icon="🌴", layout="wide")
    display_chat_interface()

if __name__ == "__main__":
    main()