import streamlit as st
from database.db import create_attendance
from ui.base_layout import apply_dialog_styles


def show_attendance_result(df, logs):
    apply_dialog_styles()

    # ── Summary stats ─────────────────────────────────────────────────────────
    total   = len(df)
    present = int(df['Status'].str.contains('Present').sum())
    absent  = total - present
    rate    = round((present / total * 100)) if total else 0

    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, total,   'Total'),
        (s2, present, 'Present'),
        (s3, absent,  'Absent'),
        (s4, f'{rate}%', 'Rate'),
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

    # ── Results table ─────────────────────────────────────────────────────────
    st.markdown('<p class="dialog-hint">Review before confirming — this cannot be undone.</p>', unsafe_allow_html=True)
    st.dataframe(df, hide_index=True)

    # ── Actions ───────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button('Discard', width='stretch', type='tertiary', icon=':material/close:'):
            st.session_state.pop('voice_attendance_results', None)
            st.session_state.attendance_images = []
            st.rerun()
    with c2:
        if st.button('Confirm & Save', width='stretch', type='primary', icon=':material/save:'):
            try:
                create_attendance(logs)
                st.toast(f'Attendance saved — {present}/{total} present', icon='✅')
                st.session_state.pop('voice_attendance_results', None)
                st.session_state.attendance_images = []
                st.rerun()
            except Exception as e:
                st.error(f'Save failed: {e}')


@st.dialog("Attendance Report")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)