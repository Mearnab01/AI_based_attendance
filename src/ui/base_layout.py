import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f1123 0%, #1a1f3c 60%, #0f1123 100%) !important;
                min-height: 100vh;
            }

            .stApp div[data-testid="stColumn"] {
                background: rgba(255, 255, 255, 0.04) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                padding: 2.5rem !important;
                border-radius: 1.5rem !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: #f4f5fb !important;
                min-height: 100vh;
            }

            .stApp div[data-testid="stColumn"] {
                background: transparent !important;
                padding: 0 !important;
                border-radius: 0 !important;
                border: none !important;
                box-shadow: none !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

        /* ── Reset & Hide Streamlit Chrome ── */
        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.75rem !important;
            padding-bottom: 2rem !important;
            max-width: 960px;
        }

        /* ── Typography ── */
        h1 {
            font-family: 'Syne', sans-serif !important;
            font-weight: 800 !important;
            font-size: 3rem !important;
            line-height: 1.05 !important;
            letter-spacing: -0.02em !important;
            margin-bottom: 0.25rem !important;
        }

        h2 {
            font-family: 'Syne', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.75rem !important;
            line-height: 1.1 !important;
            letter-spacing: -0.015em !important;
            margin-bottom: 0.25rem !important;
        }

        h3 {
            font-family: 'Syne', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.2rem !important;
            letter-spacing: -0.01em !important;
        }

        h4, p, span, li, label {
            font-family: 'DM Sans', sans-serif !important;
        }

        p {
            font-size: 0.95rem !important;
            line-height: 1.65 !important;
            font-weight: 400 !important;
        }

        /* ── Buttons: Primary ── */
        button[kind="primary"],
        .stButton > button {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            letter-spacing: 0.01em !important;
            border-radius: 0.6rem !important;
            background: #4361EE !important;
            color: #ffffff !important;
            padding: 0.55rem 1.4rem !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(67, 97, 238, 0.35) !important;
            transition: all 0.2s ease !important;
        }

        button[kind="primary"]:hover,
        .stButton > button:hover {
            background: #3451d1 !important;
            box-shadow: 0 4px 16px rgba(67, 97, 238, 0.45) !important;
            transform: translateY(-1px) !important;
        }

        button[kind="primary"]:active,
        .stButton > button:active {
            transform: translateY(0) !important;
            box-shadow: 0 1px 4px rgba(67, 97, 238, 0.3) !important;
        }

        /* ── Buttons: Secondary ── */
        button[kind="secondary"] {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            border-radius: 0.6rem !important;
            background: #F72585 !important;
            color: #ffffff !important;
            padding: 0.55rem 1.4rem !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(247, 37, 133, 0.3) !important;
            transition: all 0.2s ease !important;
        }

        button[kind="secondary"]:hover {
            background: #d91e72 !important;
            box-shadow: 0 4px 16px rgba(247, 37, 133, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* ── Buttons: Tertiary ── */
        button[kind="tertiary"] {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            border-radius: 0.6rem !important;
            background: #1a1f3c !important;
            color: #ffffff !important;
            padding: 0.55rem 1.4rem !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.2s ease !important;
        }

        button[kind="tertiary"]:hover {
            background: #0f1123 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
            transform: translateY(-1px) !important;
        }

        /* ── Inputs ── */
        .stTextInput input,
        .stSelectbox select,
        .stTextArea textarea {
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.9rem !important;
            border-radius: 0.6rem !important;
            border: 1px solid #dde1f0 !important;
            background: #ffffff !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #4361EE !important;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.12) !important;
            outline: none !important;
        }

        /* ── Divider ── */
        hr {
            border: none !important;
            border-top: 1px solid rgba(0, 0, 0, 0.07) !important;
            margin: 1.5rem 0 !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {
            width: 5px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: #c7cbe8;
            border-radius: 999px;
        }
        </style>
    """, unsafe_allow_html=True)