import streamlit as st
from database.db import create_subject

@st.dialog(title="Create Subject")
def create_subject_dialog(teacher_id):
    # --- ADD CSS HERE ---
    st.markdown("""
        <style>
            /* Style the dialog container */
            div[data-testid="stDialog"] div[role="dialog"]{
                background: linear-gradient(135deg, #0f1123 0%, #1a1f3c 60%, #0f1123 100%) !important;
                border: 2px solid #4F46E5;
            }
            /* Make inputs look cleaner */
            .stTextInput input {
                border-radius: 8px;
                border: 1px solid #d1d5db;
                color: #111827;
                padding: 10px;
            }
            /* Customizing the Primary Button */
            div.stButton > button:first-child {
                background-color: #4F46E5;
                color: white;
                border-radius: 8px;
                font-weight: 600;
                transition: 0.3s;
            }
            div.stButton > button:first-child:hover {
                background-color: #4338CA;
                border-color: #4338CA;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("Enter the name of the subject you want to create.")
    
    sub_id = st.text_input("Subject ID", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject Now", type="primary", use_container_width=True):
        if not sub_id or not sub_name or not sub_section:
            st.error("Please fill in all the fields.")
            return
        
        try:
            create_subject(sub_id, sub_name, sub_section, teacher_id)
            st.toast("Subject created successfully!", icon="✅")
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
