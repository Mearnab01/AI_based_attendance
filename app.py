import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import streamlit as st
from screens.home_screen import home_screen
from screens.student_screen import student_screen
from screens.teacher_screen import teacher_screen

from components.dialog_auto_enroll import auto_enroll_dialog
from utils.logger import get_logger
logger = get_logger(__name__)

st.set_page_config(
    page_title="Snap Class | Advanced Attendance with AI Intelligent",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)
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
            
    join_code = st.query_params.get("join_code", [None])
    if join_code:
        if not(
            st.session_state.get('is_logged_in') and
            st.session_state.get('user_role') == 'student'
        ):
            st.session_state['login_type'] = 'student'
            st.rerun()
        auto_enroll_dialog(join_code)
        
        
   
    
try:
    main()
except Exception as e:
    logger.exception("Critical app crash")
    st.error("Unexpected error occurred")