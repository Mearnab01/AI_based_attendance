import streamlit as st
from ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard


LOGIN = "login"
REGISTER = "register"

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type'] = LOGIN

    if st.session_state['teacher_login_type'] == LOGIN:
        teacher_screen_login()
    elif st.session_state['teacher_login_type'] == REGISTER:
        teacher_screen_register()
        
        


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type='secondary',
            key='login_back_btn_login'
        ):
            st.session_state['login_type']=None
            st.rerun()
        

    st.header('Login using password')

    st.write("")
    st.write("")

    teacher_username = st.text_input(
        "Enter username",
        placeholder='ananyaroy'
    )

    teacher_pass = st.text_input(
        "Enter password",
        type='password'
    )

    st.divider()
    
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        st.button(LOGIN, key='loginBtn', shortcut='control+enter', width='stretch')
    with btnc2:
        if st.button(REGISTER, key='registerBtn',type='secondary', width='stretch'):
            st.session_state.teacher_login_type=REGISTER
            st.rerun()
        
        # DB_PASS: ijE6WD27tc6cvsuY
def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",
                type='secondary',
                key='login_back_btn_register'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Register using password')

    st.write("")
    st.write("")

    teacher_name = st.text_input(
        "Enter name",
        placeholder='ananyaroy'
    )
    teacher_username = st.text_input(
        "Enter username",
        placeholder='ananyaroy123'
    )

    teacher_pass = st.text_input(
        "Enter password",
        type='password'
    )
    teacher_conf_pass = st.text_input(
        "Enter confirm password",
        type='password'
    )

    st.divider()
    
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button(LOGIN, key='loginBtn', shortcut='control+enter', width='stretch'):
            st.session_state.teacher_login_type=LOGIN
            st.rerun()
    with btnc2:
        st.button(REGISTER, key='registerBtn',type='secondary', width='stretch')
        