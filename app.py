import streamlit as st
from resume_matcher import (
    calculate_similarity,
    extract_matching_keywords,
    extract_missing_keywords
)
from utils import extract_text_from_uploaded_file


st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


def show_skill_badges(skills, badge_type="matched"):
    """
    Display skills as professional badges.
    """

    if not skills:
        st.write("No skills found.")
        return

    if badge_type == "matched":
        bg_color = "#123524"
        text_color = "#4ade80"
    else:
        bg_color = "#3b1f1f"
        text_color = "#f87171"

    badges = ""
    for skill in skills:
        badges += f"""
        <span style="
            display:inline-block;
            background-color:{bg_color};
            color:{text_color};
            padding:6px 12px;
            border-radius:20px;
            margin:4px;
            font-size:14px;
            font-weight:600;
        ">
        {skill}
        </span>
        """

    st.markdown(badges, unsafe_allow_html=True)


def show_match_status(score):
    """
    Display match status based on similarity score.
    """

    if score >= 75:
        st.success("Strong Match — This resume is highly aligned with the job description.")
    elif score >= 50:
        st.info("Moderate Match — The resume is relevant but still needs improvement.")
    else:
        st.error("Weak Match — The resume needs stronger alignment with the job description.")


def generate_analysis_report(score, matched_skills, missing_skills):
    """
    Generate a downloadable text report for resume-job matching analysis.
    """

    report = f"""
AI-Powered Resume Screening and Job Matching Report
==================================================

Resume Match Score:
{score}%

Matched Skills:
{", ".join(matched_skills) if matched_skills else "No major matched skills found."}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "No major missing skills found."}

Improvement Suggestions:
"""

    if missing_skills:
        for skill in missing_skills:
            report += f"- Add genuine project, coursework, internship, or practical experience related to {skill}.\n"
    else:
        report += "- The resume is well aligned with the detected technical requirements.\n"

    report += """

Technical Method:
This system uses TF-IDF vectorization and Cosine Similarity to calculate resume-job matching score.
Skill matching is performed using a curated technical skill dictionary with regex-based extraction.

Note:
Only add skills to your resume that you genuinely know and can explain confidently in an interview.
"""

    return report


st.title("AI-Powered Resume Screening and Job Matching System")

st.write(
    "Upload a resume or paste resume text, then compare it with a job description using NLP-based similarity matching."
)

st.markdown("---")

with st.expander("Project Overview"):
    st.write(
        """
        This system uses Natural Language Processing to compare a resume with a job description.
        It calculates a resume-job match score using TF-IDF and Cosine Similarity, then identifies
        matched and missing technical skills from the resume.
        """
    )

    st.write(
        """
        Core features:
        - Resume text extraction from TXT, PDF, and DOCX files
        - Resume-job similarity scoring
        - Matched skill detection
        - Missing skill detection
        - Resume improvement suggestions
        - Downloadable resume analysis report
        """
    )


col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume Input")

    uploaded_resume = st.file_uploader(
        "Upload resume file",
        type=["pdf", "docx", "txt"]
    )

    resume_text = ""

    if uploaded_resume is not None:
        resume_text = extract_text_from_uploaded_file(uploaded_resume)
        st.success("Resume file uploaded and text extracted successfully.")

    resume_text = st.text_area(
        "Resume text:",
        value=resume_text,
        height=320
    )


with col2:
    st.subheader("Job Description")

    job_description_text = st.text_area(
        "Paste job description here:",
        height=390
    )


st.markdown("---")

analyze_button = st.button("Analyze Resume Match", use_container_width=True)


if analyze_button:
    if resume_text.strip() == "" or job_description_text.strip() == "":
        st.warning("Please provide both resume and job description.")
    else:
        similarity_score = calculate_similarity(resume_text, job_description_text)
        matched_keywords = extract_matching_keywords(resume_text, job_description_text)
        missing_keywords = extract_missing_keywords(resume_text, job_description_text)

        st.subheader("Analysis Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric("Resume Match Score", f"{similarity_score}%")

        with result_col2:
            st.metric("Matched Skills", len(matched_keywords))

        with result_col3:
            st.metric("Missing Skills", len(missing_keywords))

        st.progress(int(similarity_score))

        show_match_status(similarity_score)

        st.markdown("---")

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:
            st.subheader("Matched Skills")
            show_skill_badges(matched_keywords, badge_type="matched")

        with skill_col2:
            st.subheader("Missing Skills")
            show_skill_badges(missing_keywords, badge_type="missing")

        st.markdown("---")

        st.subheader("Resume Improvement Suggestions")

        if missing_keywords:
            st.write("To improve the resume-job match, consider adding genuine evidence of the following skills:")

            for skill in missing_keywords:
                st.write(f"- Add project, internship, coursework, or practical experience related to **{skill}**.")

            st.warning(
                "Only add skills that you genuinely know and can explain confidently in an interview."
            )
        else:
            st.success(
                "The resume is well aligned with the detected technical requirements of the job description."
            )

        with st.expander("Technical Method Used"):
            st.write(
                """
                The system uses TF-IDF vectorization to convert resume and job description text into numerical vectors.
                Then it applies Cosine Similarity to measure how closely the resume matches the job description.
                Skill matching is performed using a curated technical skill dictionary with regex-based extraction.
                """
            )

        report_text = generate_analysis_report(
            similarity_score,
            matched_keywords,
            missing_keywords
        )

        st.download_button(
            label="Download Analysis Report",
            data=report_text,
            file_name="resume_screening_report.txt",
            mime="text/plain",
            use_container_width=True
        )