import streamlit as st
import pandas as pd
from datetime import datetime
from pipelines.voice_pipeline import process_bulk_audio
from database.config import supabase
from components.dialog_attendance_results import show_attendance_result
from ui.base_layout import apply_dialog_styles


@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):
    apply_dialog_styles()

    st.markdown('<p class="dialog-hint">Record students saying "I am present" one by one. AI matches each voice to enrolled profiles.</p>', unsafe_allow_html=True)

    audio_data = st.audio_input('Record classroom audio', label_visibility='visible')

    # ── Enrolled / voice-registered counts ───────────────────────────────────
    enrolled_res = supabase.table('subject_students') \
        .select("*, students(*)") \
        .eq('subject_id', selected_subject_id) \
        .execute()
    enrolled = enrolled_res.data or []

    total_enrolled  = len(enrolled)
    voice_profiles  = sum(1 for s in enrolled if s['students'].get('voice_embeddings'))

    if total_enrolled:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="att-stat"><span class="att-stat-val">{total_enrolled}</span>'
                f'<span class="att-stat-label">Enrolled</span></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f'<div class="att-stat"><span class="att-stat-val">{voice_profiles}</span>'
                f'<span class="att-stat-label">Voice Profiles</span></div>',
                unsafe_allow_html=True
            )
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    if voice_profiles == 0:
        st.warning('No voice profiles registered yet. Students must enroll their voice first.')

    # ── Analyze ───────────────────────────────────────────────────────────────
    if st.button('Analyze Audio', width='stretch', type='primary',
                 icon=':material/graphic_eq:', disabled=not audio_data):
        if not enrolled:
            st.warning('No students enrolled in this subject.')
            return

        candidates = {
            s['students']['student_id']: s['students']['voice_embeddings']
            for s in enrolled if s['students'].get('voice_embeddings')
        }
        if not candidates:
            st.error('No voice profiles found.')
            return

        with st.spinner('Analysing audio...'):
            audio_data.seek(0)
            scores    = process_bulk_audio(audio_data.read(), candidates)
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            results, logs = [], []

            for node in enrolled:
                student   = node['students']
                score     = scores.get(student['student_id'], 0.0)
                present   = score > 0

                results.append({
                    'Name':       student['name'],
                    'ID':         student['student_id'],
                    'Confidence': f"{score:.2f}" if present else '—',
                    'Status':     '✅ Present' if present else '❌ Absent',
                })
                logs.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp':  timestamp,
                    'is_present': present,
                })

        st.session_state.voice_attendance_results = (pd.DataFrame(results), logs)

    # ── Show results inline ───────────────────────────────────────────────────
    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df, logs = st.session_state.voice_attendance_results
        show_attendance_result(df, logs)