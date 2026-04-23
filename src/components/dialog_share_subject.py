import streamlit as st
import segno
import io


@st.dialog("Share Subject", width=400)
def share_subject_dialog(subject_name, subject_code):
    app_domain = "http://localhost:8501"
    join_url = f"{app_domain}/join?code={subject_code}"
       
    # Generate QR code
    qr = segno.make(join_url)
    buffer = io.BytesIO()
    
    qr.save(buffer, kind='png', scale=5, border=1)
    
    col1, col2 = st.columns([2, 1], vertical_alignment='center')
    with col1:
        st.markdown(f"Share the following link to invite students to join **{subject_name}**:")
        st.code(join_url, language='markdown')
        st.code(subject_code, language='text')
        st.info("Copy this link and share it with your students.")
        
    with col2:
        st.markdown("Scan the QR code to join:")
        st.image(buffer.getvalue(), caption="Scan to Join")
        
    
    
    