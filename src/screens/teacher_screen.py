import streamlit as st
import supabase
import pandas as pd 
import numpy as np
from datetime import datetime
from ui.base_layout import (
    style_base_layout, 
    style_background_dashboard,
    apply_attendance_styles,
    apply_dialog_styles
    )
# components
from components.header import header_dashboard
from components.footer import footer_dashboard
from components.subject_card import subject_card
from components.dialog_create_subject import create_subject_dialog
from components.dialog_share_subject import share_subject_dialog
from components.dialog_add_photo import add_photos_dialog
from components.dialog_add_photo import add_photos_dialog
from components.dialog_voice_attendance import voice_attendance_dialog

# pipelines
from pipelines.face_pipeline import predict_attendance

# services
from services.teacher_services import (
    register_teacher_service, 
    login_teacher_service
    )
# database
from database.db import get_teacher_subjects

LOGIN = "Login"
REGISTER = "Register"

## Teacher screen
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    apply_dialog_styles()

    if 'teacher_data' in st.session_state:
        teacher_dashborad()
        return
    if 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type'] = LOGIN

    # show auth screen
    if st.session_state['teacher_login_type'] == LOGIN:
        teacher_screen_login()
    else:
        teacher_screen_register()
        
## ================================================================================

## Teacher dashboard
def teacher_dashborad():
    teacher_data = st.session_state['teacher_data']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Logout", icon=":material/logout:", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data 
            st.rerun()
    st.title(f"""Welcome Back, {teacher_data['name']} """)
    st.divider()
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state['current_teacher_tab'] = 'take_attendance'
    
    tab1, tab2, tab3 = st.columns([1,1,1], gap='large')
    with tab1:
        type1 = "primary" if st.session_state['current_teacher_tab'] == 'take_attendance' else "tertiary"
        
        if st.button('Take Attendance', icon=":material/face:", type=type1, width='stretch'):
            st.session_state['current_teacher_tab'] = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state['current_teacher_tab'] == 'manage_subjects' else "tertiary"
        
        if st.button('Manage Subjects', icon=":material/book:", type=type2, width='stretch'):
            st.session_state['current_teacher_tab'] = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state['current_teacher_tab'] == 'attendance_records' else "tertiary"
        
        if st.button('Attendance Records', icon=":material/history:", type=type3, width='stretch'):
            st.session_state['current_teacher_tab'] = 'attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    st.divider()
    footer_dashboard()

## ================================================================================
## Teacher login screen
def login_teacher(teacher_username, teacher_pass):
    if not teacher_username or not teacher_pass:
        return False, "Missing credentials"
    success, teacher = login_teacher_service(teacher_username, teacher_pass)
    if teacher:
        st.session_state["user_role"] = "teacher"
        st.session_state["teacher_data"] = teacher
        st.session_state["is_logged_in"] = True
        return True, teacher
    return False, teacher

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",
            icon=":material/arrow_back:",
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
        if st.button("LOGIN", icon=":material/login:", type="primary", key='loginBtn', shortcut='control+enter', width='stretch'):
            success, result = login_teacher(teacher_username, teacher_pass)
            if success:
                st.toast(f"Welcome Back {teacher_username}", icon="👋")
                st.rerun()
            else:
                st.error("Invalid Username or Password!", result)
            
            
    with btnc2:
        if st.button(f"{REGISTER} instead", icon=":material/assignment_ind:", key='registerBtn',type='secondary', width='stretch'):
            st.session_state.teacher_login_type=REGISTER
            st.rerun()
        

## ================================================================================

## Teacher register screen
def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", 
                     icon=":material/arrow_back:",
                     type='primary',
                     key='login_back_btn_register'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Register using password')

    st.write("")
    st.write("")

    c3, c4 = st.columns(2, vertical_alignment='center', gap='small')
    with c3:
        teacher_name = st.text_input(
            "Enter name",
            placeholder='ananyaroy'
        )
    with c4:
        teacher_username = st.text_input(
            "Enter username",
            placeholder='ananyaroy123'
        )

    teacher_pass = st.text_input(
        "Enter password",
        type='password',
    )
    teacher_conf_pass = st.text_input(
        "Enter confirm password",
        type='password'
    )

    st.divider()
    
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("LOGIN instead", icon=":material/login:", key='loginBtn', shortcut='control+enter', width='stretch'):
            st.session_state.teacher_login_type=LOGIN
            st.rerun()
            
    with btnc2:
        if st.button("REGISTER", icon=":material/assignment_ind:", key='registerBtn',type='primary', width='stretch'):
            success, message = register_teacher_service(
                teacher_name, teacher_username, teacher_pass, teacher_conf_pass
            )
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state['teacher_login_type'] = LOGIN
                st.rerun()
            else:
                st.error(message)
                
            
## ================================================================================

## Teacher dashboard tabs
def teacher_tab_take_attendance():
    apply_attendance_styles()
    teacher_id = st.session_state.teacher_data['teacher_id']
    
    st.markdown('<p class="att-header">Take AI Attendance</p>', unsafe_allow_html=True)
    st.markdown('<p class="att-sub">Select a subject, add class photos, and run face or voice analysis.</p>', unsafe_allow_html=True)
    
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("No subjects found. Please add a subject to get started.")
        return
    
    # ── Subject selector + add photos ────────────────────────────────────────
    if 'attendance_images' not in st.session_state:
        st.session_state['attendance_images'] = []
    subject_options = {f"{s['name']} — {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='center', gap='large')
    with col1:
        selected_label = st.selectbox("Select Subject", options=list(subject_options.keys()))
    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()
            
    selected_subject_id = subject_options[selected_label]
    st.write(f"Selected Subject ID: {selected_subject_id}")
    st.divider()
    
    # ── Photo gallery ─────────────────────────────────────────────────────────
    images = st.session_state.attendance_images
    if images:
        st.markdown('<p class="att-header" style="font-size:1.1rem">Added Photos</p>', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, img in enumerate(images):
            with cols[i % 4]:
                st.image(img, use_column_width=True)
                st.markdown(f'<p class="gallery-caption">Photo {i + 1}</p>', unsafe_allow_html=True)
                
    # ── Action buttons ────────────────────────────────────────────────────────
    has_photos = bool(images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear Photos', width='stretch', type='tertiary',
                     icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary',
                     icon=':material/analytics:', disabled=not has_photos):
            _run_face_analysis(selected_subject_id, images)

    with c3:
        if st.button('Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)
            
def _run_face_analysis(subject_id:int, images:list):
    with st.spinner("Deep Scanning classroom photos... "):
        all_detected = {}
        for i, img in enumerate(images):
            detected, _, _= predict_attendance(np.array(img.convert('RGB')), subject_id)
            for sid in (detected or {}).keys():
                if sid not in all_detected:
                    all_detected.setdefault(int(sid), []).append(f"Photo {i + 1}")
        
        enrolled_res = supabase.table('subject_students') \
            .select("*, students(*)") \
            .eq('subject_id', subject_id) \
            .execute()

        if not enrolled_res.data:
            st.warning('No students enrolled in this subject.')
            return

        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        results, attendance_log = [], []

        for node in enrolled_res.data:
            student = node['students']
            sid     = int(student['student_id'])
            sources = all_detected.get(sid, [])
            present = bool(sources)

            results.append({
                "Name":   student['name'],
                "ID":     sid,
                "Source": ", ".join(sources) if present else "—",
                "Status": "✅ Present" if present else "❌ Absent",
            })
            attendance_log.append({
                'student_id': sid,
                'subject_id': subject_id,
                'timestamp':  timestamp,
                'is_present': present,
            })

    # attendance_result_dialog(pd.DataFrame(results), attendance_log)

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2, vertical_alignment='center', gap='large')
    with col1:
        st.header("Manage Subjects", width='stretch')
    with col2:
        if st.button("Add Subject", icon=":material/assignment_ind:", type='primary', width='stretch'):
            create_subject_dialog(teacher_id)
            
    ## LIST OF SUBJECTS
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👨‍🎓", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats
            )
            
            if st.button(
                f"Share code {sub['name']}", 
                key=f"share_{sub['subject_code']}",
                icon=":material/share:"       
            ):
                share_subject_dialog(sub['name'], sub['subject_code'])

           

    else:
        st.info("No subjects found. Please add a subject to get started.")    
    
def teacher_tab_attendance_records():
    pass