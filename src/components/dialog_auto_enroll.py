import streamlit as st
from database.db import get_subject_by_code, is_student_enrolled, enroll_student_to_subject
from ui.base_layout import apply_dialog_styles
from utils.logger import get_logger

logger = get_logger(__name__)


@st.dialog("Auto Enroll", width=400)
def auto_enroll_dialog(subject_code: str):
    apply_dialog_styles()
    student_id = st.session_state.student_data['student_id']
    subject = get_subject_by_code(subject_code)
    
    if not subject:
        st.error("Invalid subject code")
        if st.button("Clear", icon=":material/delete_sweep"):
            st.query_params.clear()
            st.rerun()
        return
    
    if is_student_enrolled(student_id, subject['subject_id']):
        st.info(f"Already enrolled in {subject['name']}")
        if st.button("Got it", icon=":material/check_circle:"):
            st.query_params.clear()
            st.rerun()
        return
    
    st.markdown(f"Would you like to enroll in **{subject['name']}**?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("No thanks", icon=":material/frame_exclamation:", width='stretch'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Yes, enroll now!", icon=":material/check_circle:", type='primary', width='stretch'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('Joined successfully!')
            st.query_params.clear()
            st.rerun() 
            
        
    