import streamlit as st
from ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
def student_dashboard():
    student_data = st.session_state['student_data']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()
    st.divider()
    st.subheader(f"""Welcome Back, {student_data['name']} """)
    

def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    if "student_data" in st.session_state:
        student_dashboard()
        return 
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.write("")
    st.write("")
    
    # state init
    if "open_camera" not in st.session_state:
        st.session_state["open_camera"] = False


    # buttons row
    btn1, btn2 = st.columns(2)

    # Open camera
    with btn1:
        if st.button("Open Camera", type="primary", use_container_width=True):
            st.session_state["open_camera"] = True


    # Close camera
    with btn2:
        if st.button("Close Camera", type="secondary", use_container_width=True):
            st.session_state["open_camera"] = False
            st.rerun()


    # Camera section
    if st.session_state["open_camera"]:
        photo_source = st.camera_input("Scan your face")

        if photo_source is not None:
            st.success("Image captured!")
            np.array(Image.open(photo_source))