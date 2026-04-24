import streamlit as st
from database.config import supabase
import pandas as pd 
import numpy as np
from datetime import datetime
from ui.base_layout import (
    style_base_layout, 
    style_background_dashboard,
    apply_attendance_styles,
    apply_dialog_styles, 
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
from components.dialog_attendance_results import attendance_result_dialog

from components.audit_export import render_audit_export
from components.analytics_dashboard import render_analytics
# pipelines
from pipelines.face_pipeline import predict_attendance

# services
from services.teacher_services import (
    register_teacher_service, 
    login_teacher_service
    )
# database
from database.db import get_teacher_subjects, get_attendance_for_teacher

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
        selected_label = st.selectbox("Select Subject", list(subject_options.keys()), index=0)
    with col2:
        st.write("")  # for spacing
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
                st.image(img, width='content')
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
            detected, _, _= predict_attendance(np.array(img.convert('RGB')))
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

    attendance_result_dialog(pd.DataFrame(results), attendance_log)

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


    teacher_id = st.session_state.teacher_data['teacher_id']

    st.markdown('<p class="att-header">Attendance Records</p>', unsafe_allow_html=True)
    st.markdown('<p class="att-sub">Session logs, compliance analytics and audit export.</p>', unsafe_allow_html=True)

    # ── Subject filter ────────────────────────────────────────────────────────
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.info('No subjects yet — create one to begin.')
        return

    options = {f"{s['name']} — {s['subject_code']}": s for s in subjects}
    choice  = st.selectbox('Filter by Subject', list(options.keys()), key='records_subject')
    subject = options[choice]

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(['📋 Session Logs', '📊 Analytics', '🔐 Audit Export'])

    # ── Tab 1: Session logs ───────────────────────────────────────────────────
    with tab1:
        records = get_attendance_for_teacher(teacher_id)
        if not records:
            st.info('No records yet.')
        else:
            data = []
            for r in records:
                if r['subjects']['subject_code'] != subject['subject_code']:
                    continue
                ts = r.get('timestamp')
                data.append({
                    'ts_group': ts.split('.')[0] if ts else None,
                    'Time': datetime.fromisoformat(ts).strftime('%b %d, %Y  %I:%M %p') if ts else 'N/A',
                    'Subject':      r['subjects']['name'],
                    'Subject Code': r['subjects']['subject_code'],
                    'is_present':   bool(r.get('is_present', False)),
                })

            if not data:
                st.info('No records for this subject.')
            else:
                df = pd.DataFrame(data)
                summary = (
                    df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
                    .agg(Present=('is_present', 'sum'), Total=('is_present', 'count'))
                    .reset_index()
                )
                summary['Rate'] = (summary['Present'] / summary['Total'] * 100).round(1)
                summary['Attendance'] = (
                    '✅ ' + summary['Present'].astype(str)
                    + ' / ' + summary['Total'].astype(str) + ' Students'
                )
                summary['Compliance'] = summary['Rate'].apply(
                    lambda r: '🟢 High' if r >= 75 else ('🟡 Medium' if r >= 50 else '🔴 Low')
                )

                display_df = (
                    summary.sort_values('ts_group', ascending=False)
                    [['Time', 'Subject', 'Subject Code', 'Attendance', 'Rate', 'Compliance']]
                )

                # ── Quick summary bar ─────────────────────────────────────────
                total_sessions = len(display_df)
                avg_rate       = summary['Rate'].mean()
                best_session   = summary['Rate'].max()

                m1, m2, m3 = st.columns(3)
                for col, val, label in [
                    (m1, total_sessions,     'Total Sessions'),
                    (m2, f'{avg_rate:.1f}%', 'Avg Attendance'),
                    (m3, f'{best_session:.1f}%', 'Best Session'),
                ]:
                    with col:
                        st.markdown(
                            f'<div class="att-stat">'
                            f'<span class="att-stat-val">{val}</span>'
                            f'<span class="att-stat-label">{label}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

                # ── Search / filter ───────────────────────────────────────────
                col1, col2 = st.columns([2, 1])
                with col1:
                    search = st.text_input('🔍 Search session', placeholder='Date or subject...', label_visibility='collapsed')
                with col2:
                    show_low_only = st.toggle('Show low compliance only', value=False)

                if search:
                    mask = display_df['Time'].str.contains(search, case=False) | \
                           display_df['Subject'].str.contains(search, case=False)
                    display_df = display_df[mask]

                if show_low_only:
                    display_df = display_df[display_df['Compliance'] == '🔴 Low']

                st.dataframe(display_df, width='stretch', hide_index=True)

                # ── Quick CSV download ────────────────────────────────────────
                st.download_button(
                    '⬇ Export Session Log',
                    data=display_df.to_csv(index=False),
                    file_name=f"sessions_{subject['subject_code']}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime='text/csv',
                    icon=':material/download:',
                )

    # ── Tab 2: Analytics ──────────────────────────────────────────────────────
    with tab2:
        render_analytics(subject['subject_id'])

    # ── Tab 3: Audit Export ───────────────────────────────────────────────────
    with tab3:
        render_audit_export(subject['subject_id'], subject['name'])