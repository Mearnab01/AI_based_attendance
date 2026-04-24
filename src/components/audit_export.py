import streamlit as st
import pandas as pd
from datetime import datetime
from src.database.config import supabase

def render_audit_export(subject_id: int, subject_name: str):
    st.markdown("""
        <div style="background:rgba(88,101,242,0.07);border:1px solid rgba(88,101,242,0.2);
        border-radius:12px;padding:16px 20px;margin-bottom:16px;">
            <p style="color:#a5b4fc;font-size:0.78rem;font-weight:700;
            text-transform:uppercase;letter-spacing:0.08em;margin:0 0 4px">
            🔐 Audit Trail</p>
            <p style="color:#8892b0;font-size:0.82rem;margin:0;">
            Export full attendance logs as a signed evidence record.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input('From', key='audit_from')
    with col2:
        date_to = st.date_input('To', key='audit_to')

    if st.button('Generate Audit Report', type='primary',
                 icon=':material/download:', width='stretch'):
        res = supabase.table('attendance_logs') \
            .select("*, students(name)") \
            .eq('subject_id', subject_id) \
            .gte('timestamp', str(date_from)) \
            .lte('timestamp', str(date_to)) \
            .execute()

        if not res.data:
            st.warning('No records found for this period.')
            return

        rows = [{
            'Timestamp':  r['timestamp'],
            'Student':    r['students']['name'],
            'Student ID': r['student_id'],
            'Status':     '✅ Present' if r['is_present'] else '❌ Absent',
        } for r in res.data]

        df = pd.DataFrame(rows)
        filename = f"audit_{subject_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.csv"

        st.download_button(
            label='⬇ Download Audit CSV',
            data=df.to_csv(index=False),
            file_name=filename,
            mime='text/csv',
            width='stretch',
        )
        st.dataframe(df, hide_index=True, width='stretch')