import streamlit as st
from password_checker import *
import plotly.graph_objects as go

st.set_page_config(page_title="Cyber Password Analyzer", layout="wide")


# ---------------- CYBER UI CSS ----------------
st.markdown("""
<style>

.stApp{
background-color:#020617;
color:white;
}

h1{
color:#00ff9f;
text-shadow:0 0 10px #00ff9f;
}

h2,h3{
color:#22c55e;
}

.stButton>button{
background-color:#00ff9f;
color:black;
font-weight:bold;
border-radius:8px;
}

.stTextInput>div>div>input{
background-color:#111827;
color:#00ff9f;
border:1px solid #00ff9f;
}

.section-card{
background-color:#0f172a;
padding:20px;
border-radius:12px;
border:1px solid #1f2937;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)
# ------------------------------------------------


st.title("🔐 Cyber Password Strength Analyzer")

st.write("Analyze your password using cybersecurity rules.")


password = st.text_input("Enter your password", type="password")


def show_status(label, value):
    if value:
        st.markdown(f"{label}: :green[✔ Present]")
    else:
        st.markdown(f"{label}: :red[✖ Missing]")


# ----------- SPEEDOMETER METER -----------
def strength_meter(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Password Strength Score"},
        gauge={
            'axis': {'range': [0, 8]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 3], 'color': "#ef4444"},
                {'range': [3, 6], 'color': "#facc15"},
                {'range': [6, 8], 'color': "#22c55e"},
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)


# --------- SUGGESTIONS LOGIC ----------
def password_suggestions(password, chars, length, common):
    suggestions = []

    if not chars["uppercase"]:
        suggestions.append("Add uppercase letters (A-Z)")

    if not chars["digits"]:
        suggestions.append("Add numbers (0-9)")

    if not chars["special"]:
        suggestions.append("Add special characters (!@#$%)")

    if length < 12:
        suggestions.append("Use at least 12 characters")

    if common:
        suggestions.append("Avoid common passwords")

    return suggestions
# --------------------------------------


if st.button("Check Strength"):

    if password:

        # compute once
        chars = analyze_characters(password)
        length, status = analyze_length(password)
        entropy, estr = calculate_entropy(password)
        common = check_common_password(password)
        score, final = calculate_final_score(password)
        suggestions = password_suggestions(password, chars, length, common)

        # ----------- TOP DASHBOARD (2 COLUMN) -----------
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Character Analysis")

            show_status("Lowercase", chars["lowercase"])
            show_status("Uppercase", chars["uppercase"])
            show_status("Numbers", chars["digits"])
            show_status("Special Characters", chars["special"])

            # Suggestions moved here (left side under Character Analysis)
            if suggestions:
                st.markdown("---")
                st.subheader("Security Suggestions")
                for s in suggestions:
                    st.write("•", s)

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Password Strength Meter")

            strength_meter(score)

            if final == "Strong":
                st.success("🟢 STRONG PASSWORD")
            elif final == "Medium":
                st.warning("🟡 MEDIUM PASSWORD")
            else:
                st.error("🔴 WEAK PASSWORD")

            st.write("Security Score:", score, "/ 8")
            st.markdown('</div>', unsafe_allow_html=True)

        # ----------- SECOND ROW -----------
        col3, col4 = st.columns(2)

        with col3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Password Length")
            st.write("Length:", length)

            if status == "Strong":
                st.success("Strong Length")
            elif status == "Medium":
                st.warning("Medium Length")
            else:
                st.error("Weak Length")

            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Entropy Analysis")
            st.write("Entropy:", entropy, "bits")

            if estr == "Strong":
                st.success("Strong Entropy")
            elif estr == "Medium":
                st.warning("Medium Entropy")
            else:
                st.error("Weak Entropy")

            st.markdown('</div>', unsafe_allow_html=True)

        # ----------- COMMON PASSWORD (full width) -----------
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Common Password Check")

        if common:
            st.error("Password exists in common password database")
        else:
            st.success("Password not found in common password database")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Please enter a password.")