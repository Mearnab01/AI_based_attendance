import streamlit as st
from PIL import Image
from ui.base_layout import apply_dialog_styles


@st.dialog("Add Classroom Photos")
def add_photos_dialog():
    apply_dialog_styles()

    st.markdown('<p class="dialog-hint">Add photos via camera or upload. Multiple photos improve recognition accuracy.</p>', unsafe_allow_html=True)

    # ── Tab toggle ────────────────────────────────────────────────────────────
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)
    with t1:
        type_t1 = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', width='stretch',
                     type=type_t1, icon=':material/camera:'):
            st.session_state.photo_tab = 'camera'
            st.rerun()
    with t2:
        type_t2 = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload', width='stretch',
                     type=type_t2, icon=':material/image_arrow_up:'):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    # ── Photo count badge ─────────────────────────────────────────────────────
    count = len(st.session_state.get('attendance_images', []))
    if count:
        st.markdown(
            f'<div style="background:rgba(88,101,242,0.1);border:1px solid rgba(88,101,242,0.25);'
            f'border-radius:8px;padding:8px 14px;font-size:0.83rem;color:#a5b4fc;margin-bottom:12px;">'
            f'📸 {count} photo{"s" if count > 1 else ""} added</div>',
            unsafe_allow_html=True
        )

    # ── Camera tab ────────────────────────────────────────────────────────────
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take a snapshot', key='dialog_cam', label_visibility='collapsed')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo captured!')
            st.rerun()

    # ── Upload tab ────────────────────────────────────────────────────────────
    if st.session_state.photo_tab == 'upload':
        uploaded = st.file_uploader(
            'Choose image files',
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key='dialog_upload',
            label_visibility='collapsed'
        )
        if uploaded:
            new = [Image.open(f) for f in uploaded]
            st.session_state.attendance_images.extend(new)
            st.toast(f'{len(new)} photo{"s" if len(new) > 1 else ""} added!')
            st.rerun()

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        if st.button('Clear All', width='stretch', type='tertiary',
                     icon=':material/delete:', disabled=not count):
            st.session_state.attendance_images = []
            st.rerun()
    with c2:
        if st.button('Done', type='primary', width='stretch', icon=':material/check:'):
            st.rerun()