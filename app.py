import streamlit as st
from components.header import header_home, header_dashboard
from components.subject_card import subject_card
from components.footer import footer_home, footer_dashboard
from utils.logger import get_logger
logger = get_logger(__name__)

def main():
    st.set_page_config(page_title="SNAP CLASS", page_icon=":school:", layout="centered")
    
    header_home()
    header_dashboard()
    # subject_card()
    footer_home()
    footer_dashboard()

    logger.info("Application started successfully.")
    
    
main()