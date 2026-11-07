"""Streamlit user interface for PathForge AI."""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data import SKILLS, ROLES
from engine import extract_skills, analyse
from database import init_db, save_assessment, history
from resume_parser import extract_resume_text
from ml_models import train_readiness_model, predict_readiness

st.set_page_config(page_title="PathForge AI", page_icon="🧭", layout="wide")
init_db()

@st.cache_resource
def get_readiness_model():
    return train_readiness_model()[0]

def attach_ml_readiness(result):
    model = get_readiness_model()
    result["ml_readiness"] = predict_readiness(model, result["profile"], result["target_role"])
    return result

st.markdown("""
<style>
.main {background: #f7f9fc;}
.block-container {padding-top: 2rem; max-width: 1200px;}
div[data-testid="stMetric"] {background: white; padding: 16px; border-radius: 12px;
 border: 1px solid #e6eaf0;}
</style>
""", unsafe_allow_html=True)

st.title("🧭 PathForge AI")
st.caption("Know your skills. Discover your gaps. Build your next career step.")
with st.sidebar:
    st.header("Your workspace")
    student = st.text_input("Display name", value="Student")
    page = st.radio("Navigate", ["Career Assessment", "Skill Analysis", "4-Week Roadmap", "Progress History", "About"])
    st.divider()
    st.caption("Local demo • SQLite storage • No account required")

if "profile" not in st.session_state:
    st.session_state.profile = {}
if "result" not in st.session_state:
    st.session_state.result = None

if page == "Career Assessment":
    st.subheader("1. Build your skill profile")
    st.write("Choose manual assessment or upload a resume. Resume extraction detects skill mentions; it does not verify proficiency.")
    mode = st.radio("Input method", ["Manual self-assessment", "Upload resume"], horizontal=True)
    profile = {}
    if mode == "Manual self-assessment":
        st.info("Rate each skill from 0 (no experience) to 100 (can use it confidently in a project).")
        with st.form("skills_form"):
            cols = st.columns(3)
            for i, skill in enumerate(SKILLS):
                with cols[i % 3]:
                    profile[skill] = st.slider(skill, 0, 100, int(st.session_state.profile.get(skill, 0)), 5)
            role = st.selectbox("Target career role", list(ROLES))
            submitted = st.form_submit_button("Analyse my career fit", type="primary")
        if submitted:
            st.session_state.profile = profile
            st.session_state.result = attach_ml_readiness(analyse(profile, role))
            save_assessment(student, st.session_state.result)
            st.success("Assessment completed and saved locally.")
    else:
        upload = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
        role = st.selectbox("Target career role", list(ROLES))
        level = st.slider("Default level assigned to detected skills", 0, 100, 55, 5)
        if st.button("Extract skills and analyse", type="primary", disabled=upload is None):
            try:
                resume_text = extract_resume_text(upload)
                profile = extract_skills(resume_text, default_level=level)
                if not profile:
                    st.warning("No supported skills were detected. Try manual assessment or check resume text.")
                else:
                    st.session_state.profile = profile
                    st.session_state.result = attach_ml_readiness(analyse(profile, role))
                    save_assessment(student, st.session_state.result)
                    st.success(f"Detected {len(profile)} skills. Review the assigned levels below.")
                    st.dataframe(pd.DataFrame([{"Skill": k, "Assigned level": v} for k, v in profile.items()]),
                                 use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"Could not read this file: {exc}")

elif page == "Skill Analysis":
    st.subheader("2. Skill-gap analysis")
    result = st.session_state.result
    if not result:
        st.info("Complete a Career Assessment first.")
    else:
        a, b, c = st.columns(3)
        a.metric("Weighted match", f"{result['match_score']:.1f}/100")
        b.metric("ML readiness estimate", result.get("ml_readiness", result["readiness"]))
        c.metric("Cosine similarity", f"{result['cosine_similarity']:.1f}%")
        st.caption("The Decision Tree is trained on synthetic profiles. This category is a learning aid, not a hiring probability. The transparent score band is: " + result["readiness"] + ".")
        st.markdown("#### Highest-priority skill gaps")
        if result["gaps"]:
            gaps = pd.DataFrame(result["gaps"])
            st.dataframe(gaps[["skill","current","target","shortfall","importance","priority"]],
                         use_container_width=True, hide_index=True)
            fig, ax = plt.subplots(figsize=(9, 4))
            show = gaps.head(8).sort_values("priority")
            ax.barh(show["skill"], show["priority"])
            ax.set_xlabel("Priority = importance × skill shortfall")
            ax.set_title("Skills to improve first")
            st.pyplot(fig)
        else:
            st.success("No gaps found in the curated requirements for this role.")
        st.markdown("#### Best-fit roles")
        st.dataframe(pd.DataFrame(result["role_ranking"]), use_container_width=True, hide_index=True)

elif page == "4-Week Roadmap":
    st.subheader("3. Your personalised learning roadmap")
    result = st.session_state.result
    if not result:
        st.info("Complete a Career Assessment first.")
    else:
        for item in result["learning_plan"]:
            with st.expander(f"Week {item['week']} — {item['focus']}", expanded=True):
                for activity in item["activities"]:
                    st.write("• " + activity)
        st.download_button("Download roadmap (CSV)",
            pd.DataFrame([{"Week": x["week"], "Focus": x["focus"],
                           "Activity": a} for x in result["learning_plan"] for a in x["activities"]])
              .to_csv(index=False).encode("utf-8"),
            file_name="pathforge_learning_plan.csv", mime="text/csv")

elif page == "Progress History":
    st.subheader("4. Your progress over time")
    rows = history(student.strip() or "Student")
    if not rows:
        st.info("No saved assessments for this display name yet.")
    else:
        df = pd.DataFrame(rows)
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.line_chart(df.set_index("created_at")["match_score"])
        st.caption("History is stored locally in data/pathforge.db on this computer.")

else:
    st.subheader("About PathForge AI")
    st.write("PathForge AI compares a student's skill profile with eight curated technology-role profiles.")
    st.markdown("""
    **Core methods**
    - Synonym-aware resume skill extraction using regular expressions
    - Weighted, capped skill-match scoring
    - Cosine similarity for secondary role comparison
    - Gap prioritisation using importance × shortfall
    - Four-week content-based learning roadmap
    - SQLite assessment history
    - Synthetic-data Decision Tree and K-Means evaluation script

    **Limitations**
    - Resume keyword detection cannot confirm actual proficiency.
    - Role requirements are curated project assumptions and should be reviewed periodically.
    - Synthetic model evaluation does not establish real-world career or hiring accuracy.
    - The application is an educational prototype, not professional recruitment advice.
    """)
    if st.button("Run synthetic ML evaluation"):
        with st.spinner("Training the reproducible Decision Tree..."):
            _, metrics = train_readiness_model()
        st.metric("Synthetic held-out accuracy", f"{metrics['accuracy']*100:.1f}%")
        st.code(metrics["report"])
        st.warning("This result is measured on generated synthetic profiles only.")
