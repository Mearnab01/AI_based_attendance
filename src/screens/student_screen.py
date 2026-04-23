import cv2
import streamlit as st
from ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from pipelines.face_pipeline import (
    predict_attendance,
    extract_face_embedding,
    train_classifier
    )
from pipelines.voice_pipeline import get_voice_embedding
from database.db import get_all_students, create_student


def student_screen():
    style_base_layout()
    style_background_dashboard()
    
    if 'student_data' in  st.session_state:
        student_dashboard()
    else:
        student_login_screen()

# ── Dashboard ─────────────────────────────────────────────────────────────────
def student_dashboard():
    student_data = st.session_state['student_data']
    student_id = student_data['student_id']
    
    c1, c2 = st.columns([1,1], vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
        
    with c2:
        st.markdown(f"""
            <div style="text-align:right; padding:0.25rem 0;">
                <p style="margin:0; font-size:0.75rem; color:#8892b0;
                          text-transform:uppercase; letter-spacing:0.06em; font-weight:500;">
                    Signed in as
                </p>
                <p style="margin:0; font-size:1rem; font-weight:700; color:#1a1f3c;">
                    {student_data['name']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", type='secondary', key='student_logout_btn', shortcut="control+backspace"):
            del st.session_state.student_data 
            st.session_state['is_logged_in'] = False
            st.rerun()
    st.divider()
    
    c1, c2 = st.columns([2, 1], vertical_alignment='center')
    with c1:
        st.markdown("""
            <div>
                <h3 style="color:#1a1f3c; margin:0;">Your Enrolled Subjects</h3>
                <p style="color:#8892b0; margin:0.25rem 0 0 0; font-size:0.875rem;">
                    Track your attendance across all enrolled courses.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            st.header("Enroll in Subject")
            st.write("This feature is coming soon! Stay tuned for updates.")
    

# ── Login screen ──────────────────────────────────────────────────────────────
def student_login_screen():
    
    c1, c2 = st.columns([1,1], vertical_alignment='center', gap='large')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to Home", type='secondary', key='student_back_btn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.write("")
    st.write("")
    
    st.markdown("""
        <div style="text-align:center; padding:1.5rem 0 1rem 0;">
            <h3 style="color:#1a1f3c; margin:0;">Student Face Login</h3>
            <p style="color:#8892b0; margin:0.35rem 0 0 0; font-size:0.875rem;">
                Position your face clearly in the camera to sign in.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
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
        photo_source = st.camera_input("Position your face in the center")
        show_registration = False

        if photo_source is not None:
            show_registration = _handle_face_login(photo_source)
        if show_registration:
            _registration_panel(photo_source)
            
        footer_dashboard()
        
# ── Face login handler ────────────────────────────────────────────────────────
def _handle_face_login(photo_source):
    img = np.array(Image.open(photo_source))
    img = _preprocess_frame(img)
      
    with st.spinner("Processing..."):
        detected, all_ids, num_faces = predict_attendance(img) 
        # print(f"[debug_] Detected: {detected}, All IDs: {all_ids}, Num faces: {num_faces}")   
        
    if num_faces == 0:
        st.warning('No face detected. Please adjust your position and try again.')
        return False
 
    elif num_faces > 1:
        st.warning('Multiple faces detected. Please ensure only one face is visible.')
        return False
 
    if not detected:
        st.info('Face not recognised. You may be a new student — register below.')
        return True
 
    student_id   = list(detected.keys())[0]
    all_students = get_all_students()
    student      = next((s for s in all_students if s['student_id'] == student_id), None)
 
    if not student:
        st.info('Face not recognised. You may be a new student — register below.', icon="⚠️")
        return True
 
    _set_student_session(student)
    st.toast(f"Welcome back, {student['name']}!")
    st.rerun()
    return False

def _preprocess_frame(image_np: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2RGB)

# ── Registration panel ────────────────────────────────────────────────────────
def _registration_panel(photo_source):
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
 
    with st.container(border=True):
        st.markdown("""
            <div style="margin-bottom:0.75rem;">
                <h3 style="color:#1a1f3c; margin:0;">Create a New Profile</h3>
                <p style="color:#8892b0; margin:0.25rem 0 0 0; font-size:0.875rem;">
                    Your face will be enrolled from the photo above.
                </p>
            </div>
        """, unsafe_allow_html=True)
 
        new_name = st.text_input("Your Full Name", placeholder='e.g. Arnab Nath')
 
        st.markdown("""
            <p style="font-weight:600; color:#1a1f3c; font-size:0.875rem;
                      margin:0.75rem 0 0.25rem 0;">Voice Enrollment (Optional)</p>
            <p style="color:#8892b0; font-size:0.82rem; margin:0 0 0.5rem 0;">
                Record a 7-10 second audio clip.
            </p>
        """, unsafe_allow_html=True)
 
        audio_data = None
        try:
            audio_data = st.audio_input('Say something like "I am present" or state your name.')
        except Exception as e:
            print(f"[_registration_panel] audio error: {e}")
            st.error('Audio recording failed.')
 
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
 
        if st.button('Create Account', type='primary', width='stretch'):
            _handle_registration(new_name, photo_source, audio_data)
    
    
# ── Registration handler ──────────────────────────────────────────────────────
def _handle_registration(new_name:str, photo_source, audio_data):
    if not new_name:
        st.warning('Please enter your name to continue.')
        return
    
    with st.spinner("Creating your profile..."):
        img = np.array(Image.open(photo_source))
        encodings = extract_face_embedding(img)
        
        if not encodings:
            st.error('Could not capture facial features. Please retake the photo.')
            return
        
        face_emb = encodings[0].tolist()  # Assuming one face for registration
        voice_emb = get_voice_embedding(audio_data.read()) if audio_data else None
        print(voice_emb, "from line 220 student screen")
        response_data = create_student(
            new_name,
            face_embeddings=face_emb,
            voice_embeddings=voice_emb
        )
 
        if not response_data:
            st.error('Account creation failed. Please try again.')
            return
        train_classifier()
        _set_student_session(response_data[0])
        st.toast(f"Profile created! Welcome, {new_name}!")
        st.rerun()
        
# ── Helper functions ───────────────────────────────────────────────────────────
def _set_student_session(student):
    st.session_state.is_logged_in = True
    st.session_state.user_role    = 'student'
    st.session_state.student_data = student