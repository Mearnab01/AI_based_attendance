import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #e8ecf4;
            border-left: 4px solid #4361EE;
            padding: 20px 22px 16px 22px;
            margin-bottom: 14px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05), 0 4px 16px rgba(0, 0, 0, 0.04);
            transition: box-shadow 0.2s ease;
        ">
            <h3 style="
                margin: 0 0 8px 0;
                color: #1a1f3c;
                font-size: 1.1rem;
                font-weight: 700;
                letter-spacing: -0.01em;
            ">{name}</h3>

            <p style="
                color: #8892b0;
                margin: 0 0 12px 0;
                font-size: 0.85rem;
                font-weight: 400;
                display: flex;
                align-items: center;
                gap: 6px;
            ">
                Code:&nbsp;<span style="
                    background: #eef0fc;
                    color: #4361EE;
                    font-weight: 600;
                    padding: 2px 9px;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    letter-spacing: 0.02em;
                ">{code}</span>
                <span style="color: #dde1f0; margin: 0 2px;">|</span>
                Section:&nbsp;<span style="
                    color: #4a5568;
                    font-weight: 500;
                ">{section}</span>
            </p>
    """

    if stats:
        html += """
            <div style="
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                margin-top: 4px;
            ">
        """
        for icon, label, value in stats:
            html += f"""
                <div style="
                    background: #f8f9fe;
                    border: 1px solid #e8ecf4;
                    padding: 5px 12px;
                    border-radius: 8px;
                    font-size: 0.82rem;
                    color: #4a5568;
                    font-weight: 400;
                    white-space: nowrap;
                ">
                    {icon}&nbsp;<b style="color: #1a1f3c; font-weight: 600;">{value}</b>&nbsp;{label}
                </div>
            """
        html += "</div>"

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()