import streamlit as st
from screens.home_screen import home_screen
from screens.student_screen import student_screen
from screens.teacher_screen import teacher_screen

from utils.logger import get_logger
logger = get_logger(__name__)
def main():
    
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
        
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()
        
   
    
try:
    main()
except Exception as e:
    logger.exception("Critical app crash")
    st.error("Unexpected error occurred")