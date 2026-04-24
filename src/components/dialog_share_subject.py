import streamlit as st
import segno
import io
from ui.base_layout import apply_dialog_styles


@st.dialog("Share Subject", width=400)
def share_subject_dialog(subject_name, subject_code):
    apply_dialog_styles()
    app_domain = "http://localhost:8501"
    join_url = f"{app_domain}/join?code={subject_code}"
       
    # Generate QR code
    qr = segno.make(join_url)
    buffer = io.BytesIO()
    
    qr.save(buffer, kind='png', scale=5, border=1, dark='#5865F2', light='#ffffff')
    
    col1, col2 = st.columns([2, 1], vertical_alignment='center')
    with col1:
        st.markdown(
            f'<span style="color:#fff;font-weight:600;">{subject_name}</span><br>',
            unsafe_allow_html=True
        )
        st.code(join_url, language='markdown')
        st.code(subject_code, language='text')
        st.markdown(
            '<p class="dialog-hint" style="margin-top:8px;">📲 Share via WhatsApp, Email, or let students scan the QR.</p>',
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown("Scan the QR code to join:")
        st.image(buffer.getvalue(), caption="Scan to Join")
        
    
    
    