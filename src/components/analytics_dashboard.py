import streamlit as st
import pandas as pd
from src.database.config import supabase

def render_analytics(subject_id: int):
    res = supabase.table('attendance_logs') \
        .select("*, students(name)") \
        .eq('subject_id', subject_id) \
        .execute()

    if not res.data:
        st.info('No attendance data yet for this subject.')
        return

    df = pd.DataFrame([{
        'name':       r['students']['name'],
        'student_id': r['student_id'],
        'date':       r['timestamp'][:10],
        'present':    r['is_present'],
    } for r in res.data])

    total_sessions = df['date'].nunique()

    # ── Per-student compliance rate ───────────────────────────────────────────
    compliance = df.groupby('name')['present'].mean().reset_index()
    compliance.columns = ['Student', 'Rate']
    compliance['Rate %'] = (compliance['Rate'] * 100).round(1)
    compliance['Status'] = compliance['Rate'].apply(
        lambda r: '🟢 Compliant' if r >= 0.75 else ('🟡 At Risk' if r >= 0.5 else '🔴 Critical')
    )
    compliance = compliance.sort_values('Rate %')

    # ── Summary metrics ───────────────────────────────────────────────────────
    avg_rate    = compliance['Rate %'].mean()
    critical    = (compliance['Rate'] < 0.5).sum()
    at_risk     = ((compliance['Rate'] >= 0.5) & (compliance['Rate'] < 0.75)).sum()

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label in [
        (m1, total_sessions,     'Sessions'),
        (m2, f'{avg_rate:.1f}%', 'Avg Compliance'),
        (m3, at_risk,            'At Risk'),
        (m4, critical,           'Critical'),
    ]:
        with col:
            st.markdown(
                f'<div class="att-stat">'
                f'<span class="att-stat-val">{val}</span>'
                f'<span class="att-stat-label">{label}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # ── Compliance bar chart ──────────────────────────────────────────────────
    st.markdown('**Individual Compliance Rate**')
    st.bar_chart(
        compliance.set_index('Student')['Rate %'],
        color='#5865F2',
        width='stretch',
        height=260,
    )

    # ── Daily trend ───────────────────────────────────────────────────────────
    daily = df.groupby('date')['present'].mean().reset_index()
    daily.columns = ['Date', 'Rate']
    daily['Rate %'] = (daily['Rate'] * 100).round(1)

    st.markdown('**Daily Attendance Trend**')
    st.line_chart(
        daily.set_index('Date')['Rate %'],
        color='#EB459E',
        width='stretch',
        height=200,
    )

    # ── Critical students table ───────────────────────────────────────────────
    flagged = compliance[compliance['Rate'] < 0.75][['Student', 'Rate %', 'Status']]
    if not flagged.empty:
        st.markdown('**⚠️ Flagged Individuals**')
        st.dataframe(flagged, hide_index=True, width='stretch')