import streamlit as st

def _footer_css():
    st.markdown("""
        <style>
        .footer {
            margin-top: 2.5rem;
            padding: 1.25rem 0;
            border-top: 1px solid rgba(255,255,255,0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }
        .footer-brand {
            font-size: 0.82rem;
            font-weight: 600;
            color: rgba(255,255,255,0.5);
            letter-spacing: 0.03em;
        }
        .footer-brand span {
            color: #5865F2;
        }
        .footer-links {
            display: flex;
            gap: 20px;
        }
        .footer-link {
            font-size: 0.78rem;
            color: rgba(255,255,255,0.3);
            text-decoration: none;
            letter-spacing: 0.02em;
            transition: color 0.2s;
        }
        .footer-link:hover {
            color: rgba(255,255,255,0.7);
        }
        .footer-dot {
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: rgba(255,255,255,0.15);
            display: inline-block;
            margin: 0 2px;
            vertical-align: middle;
        }
        </style>
    """, unsafe_allow_html=True)


def footer_home():
    _footer_css()
    st.markdown("""
        <div class="footer">
            <span class="footer-brand">
                Snap<span>Class</span> &nbsp;·&nbsp; AI Attendance System
            </span>
            <div class="footer-links">
                <a class="footer-link" href="#">Privacy</a>
                <a class="footer-link" href="#">Terms</a>
                <a class="footer-link" href="#">Built by Arnab Nath</a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    _footer_css()
    st.markdown("""
        <div class="footer">
            <span class="footer-brand">
                Snap<span>Class</span> &nbsp;·&nbsp; © 2026
            </span>
            <span class="footer-brand" style="font-weight:400; font-size:0.76rem;">
                Built by Arnab Nath
            </span>
        </div>
    """, unsafe_allow_html=True)