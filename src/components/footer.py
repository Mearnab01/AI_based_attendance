import streamlit as st


def footer_home():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="
            margin-top: 2.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        ">
            <p style="
                font-size: 0.8rem;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.35);
                margin: 0;
                letter-spacing: 0.02em;
            ">Built by</p>
            <img src='{logo_url}' style='
                height: 20px;
                object-fit: contain;
                opacity: 0.7;
                filter: brightness(0) invert(1);
            ' />
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="
            margin-top: 2.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(0, 0, 0, 0.07);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        ">
            <p style="
                font-size: 0.8rem;
                font-weight: 500;
                color: #a0aec0;
                margin: 0;
                letter-spacing: 0.02em;
            ">Built by</p>
            <img src='{logo_url}' style='
                height: 20px;
                object-fit: contain;
                opacity: 0.55;
            ' />
        </div>
    """, unsafe_allow_html=True)