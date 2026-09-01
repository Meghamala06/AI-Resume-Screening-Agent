import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDER = BASE_DIR / "data" / "resumes"
OUTPUT_FOLDER = BASE_DIR / "src" / "output"
SRC_FOLDER = BASE_DIR / "src"

DATA_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

if str(SRC_FOLDER) not in sys.path:
    sys.path.insert(0, str(SRC_FOLDER))


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from parser import extract_text, get_resume_files
from extractor import extract_candidate_info
from scorer import score_resume
from ranker import rank_candidates


# ============================================================
# OPTIONAL LLM EXPLAINER
# ============================================================

try:
    from llm.llm_explainer import generate_explanation
    LLM_AVAILABLE = True
except Exception:
    LLM_AVAILABLE = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Screening Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered resume screening, scoring and candidate ranking system.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def get_recommendation(score):

    try:
        score = float(score)
    except Exception:
        return "Unknown"

    if score >= 80:
        return "Strong Match"

    elif score >= 60:
        return "Moderate Match"

    else:
        return "Weak Match"


# ============================================================
# AI FALLBACK EXPLANATION
# ============================================================

def create_fallback_explanation(candidate):

    name = candidate.get("name", "Candidate")
    final_score = candidate.get("final_score", 0)

    matched_skills = candidate.get(
        "matched_skills",
        []
    )

    missing_skills = candidate.get(
        "missing_skills",
        []
    )

    education = candidate.get(
        "education",
        []
    )

    experience = candidate.get(
        "experience",
        []
    )

    recommendation = get_recommendation(
        final_score
    )

    if matched_skills:
        matched_text = ", ".join(
            str(skill)
            for skill in matched_skills
        )
    else:
        matched_text = "No major matched skills identified"

    if missing_skills:
        missing_text = ", ".join(
            str(skill)
            for skill in missing_skills
        )
    else:
        missing_text = "No major missing skills identified"

    if education:
        education_text = ", ".join(
            str(item)
            for item in education
        )
    else:
        education_text = "No education information found"

    if experience:
        experience_text = ", ".join(
            str(item)
            for item in experience
        )
    else:
        experience_text = "No experience information found"

    return (
        f"Candidate: {name}\n\n"
        f"Why the candidate matches: "
        f"The candidate received a final score of "
        f"{float(final_score):.2f}/100, indicating a "
        f"{recommendation.lower()} with the job requirements.\n\n"
        f"Strongest matching skills: "
        f"{matched_text}\n\n"
        f"Important missing skills: "
        f"{missing_text}\n\n"
        f"Relevant education: "
        f"{education_text}\n\n"
        f"Relevant experience: "
        f"{experience_text}\n\n"
        f"Final Recommendation: {recommendation}"
    )


# ============================================================
# UPLOAD JOB DESCRIPTION
# ============================================================

st.subheader("📥 Upload Job Description")

job_file = st.file_uploader(
    "Upload Job Description",
    type=["txt", "pdf", "docx"],
    help="Upload the job description file."
)


# ============================================================
# UPLOAD RESUMES
# ============================================================

st.subheader("📁 Upload Resumes")

resume_files = st.file_uploader(
    "Upload multiple resumes",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True,
    help="Upload multiple candidate resumes."
)


# ============================================================
# SCREEN RESUMES BUTTON
# ============================================================

if st.button(
    "🚀 Screen Resumes",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if job_file is None:

        st.error(
            "❌ Please upload a Job Description first."
        )

        st.stop()

    if not resume_files:

        st.error(
            "❌ Please upload at least one resume."
        )

        st.stop()


    # --------------------------------------------------------
    # CLEAR OLD UPLOADS
    # --------------------------------------------------------

    for old_file in DATA_FOLDER.iterdir():

        if old_file.is_file():

            try:
                old_file.unlink()
            except Exception:
                pass


    # --------------------------------------------------------
    # SAVE JOB DESCRIPTION
    # --------------------------------------------------------

    job_path = DATA_FOLDER / job_file.name

    with open(
        job_path,
        "wb"
    ) as file:

        file.write(
            job_file.getbuffer()
        )


    # --------------------------------------------------------
    # SAVE RESUMES
    # --------------------------------------------------------

    for uploaded_file in resume_files:

        resume_path = (
            DATA_FOLDER /
            uploaded_file.name
        )

        with open(
            resume_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )


    # --------------------------------------------------------
    # EXTRACT JOB DESCRIPTION
    # --------------------------------------------------------

    try:

        jd_text = extract_text(
            job_path
        )

    except Exception as error:

        st.error(
            f"❌ Error reading Job Description: {error}"
        )

        st.stop()


    if not jd_text.strip():

        st.error(
            "❌ The Job Description file is empty."
        )

        st.stop()


    # --------------------------------------------------------
    # FIND RESUMES
    # --------------------------------------------------------

    try:

        files = get_resume_files(
            DATA_FOLDER
        )

    except Exception as error:

        st.error(
            f"❌ Error finding resumes: {error}"
        )

        st.stop()


    if not files:

        st.error(
            "❌ No valid resume files were found."
        )

        st.stop()


    # --------------------------------------------------------
    # PROCESS RESUMES
    # --------------------------------------------------------

    candidates = []

    progress = st.progress(0)

    status = st.empty()

    total_files = len(files)

    for index, resume_file in enumerate(files):

        status.write(
            f"📄 Processing {resume_file.name}..."
        )

        try:

            # Extract resume text
            resume_text = extract_text(
                resume_file
            )

            if not resume_text.strip():

                st.warning(
                    f"⚠️ {resume_file.name} is empty. Skipping."
                )

                progress.progress(
                    (index + 1) / total_files
                )

                continue


            # Extract candidate information
            candidate_info = (
                extract_candidate_info(
                    resume_text
                )
            )


            # Calculate scores
            scores = score_resume(
                jd_text,
                resume_text
            )


            # Combine candidate information
            candidate = {

                "file": resume_file.name,

                **candidate_info,

                **scores

            }


            # Make sure missing skills exists
            if "missing_skills" not in candidate:

                candidate["missing_skills"] = []


            # Add recommendation
            candidate["recommendation"] = (
                get_recommendation(
                    candidate.get(
                        "final_score",
                        0
                    )
                )
            )


            candidates.append(
                candidate
            )


        except Exception as error:

            st.error(
                f"❌ Error processing "
                f"{resume_file.name}: {error}"
            )


        progress.progress(
            (index + 1) / total_files
        )


    # --------------------------------------------------------
    # CHECK PROCESSED RESUMES
    # --------------------------------------------------------

    if not candidates:

        st.error(
            "❌ No resumes could be processed."
        )

        st.stop()


    # --------------------------------------------------------
    # RANK CANDIDATES
    # --------------------------------------------------------

    try:

        ranked_candidates = rank_candidates(
            candidates
        )

    except Exception as error:

        st.error(
            f"❌ Error ranking candidates: {error}"
        )

        st.stop()


    # --------------------------------------------------------
    # GENERATE EXPLANATIONS
    # --------------------------------------------------------

    status.write(
        "🤖 Generating candidate explanations..."
    )

    for candidate in ranked_candidates:

        if LLM_AVAILABLE:

            try:

                candidate["explanation"] = (
                    generate_explanation(
                        candidate,
                        jd_text
                    )
                )

            except Exception:

                candidate["explanation"] = (
                    create_fallback_explanation(
                        candidate
                    )
                )

        else:

            candidate["explanation"] = (
                create_fallback_explanation(
                    candidate
                )
            )


        # Always make recommendation available
        candidate["recommendation"] = (
            get_recommendation(
                candidate.get(
                    "final_score",
                    0
                )
            )
        )


    # ========================================================
    # SAVE JSON
    # ========================================================

    json_file = (
        OUTPUT_FOLDER /
        "ranked_candidates.json"
    )

    try:

        with open(
            json_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                ranked_candidates,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:

        st.error(
            f"❌ Could not save JSON: {error}"
        )


    # ========================================================
    # SAVE CSV
    # ========================================================

    csv_file = (
        OUTPUT_FOLDER /
        "ranked_candidates.csv"
    )

    rows = []


    for candidate in ranked_candidates:

        matched_skills = candidate.get(
            "matched_skills",
            []
        )

        missing_skills = candidate.get(
            "missing_skills",
            []
        )


        if not isinstance(
            matched_skills,
            list
        ):

            matched_skills = [
                str(matched_skills)
            ]


        if not isinstance(
            missing_skills,
            list
        ):

            missing_skills = [
                str(missing_skills)
            ]


        rows.append({

            "rank": candidate.get(
                "rank",
                ""
            ),

            "name": candidate.get(
                "name",
                ""
            ),

            "email": candidate.get(
                "email",
                ""
            ),

            "file": candidate.get(
                "file",
                ""
            ),

            "final_score": candidate.get(
                "final_score",
                ""
            ),

            "recommendation": candidate.get(
                "recommendation",
                ""
            ),

            "skill_score": candidate.get(
                "skill_score",
                ""
            ),

            "similarity_score": candidate.get(
                "similarity_score",
                ""
            ),

            "education_score": candidate.get(
                "education_score",
                ""
            ),

            "experience_score": candidate.get(
                "experience_score",
                ""
            ),

            "matched_skills": ", ".join(
                matched_skills
            ),

            "missing_skills": ", ".join(
                missing_skills
            ),

            "explanation": candidate.get(
                "explanation",
                ""
            )

        })


    try:

        pd.DataFrame(
            rows
        ).to_csv(
            csv_file,
            index=False
        )

    except Exception as error:

        st.error(
            f"❌ Could not save CSV: {error}"
        )


    # --------------------------------------------------------
    # STORE RESULTS IN SESSION
    # --------------------------------------------------------

    st.session_state[
        "candidates"
    ] = ranked_candidates


    status.success(
        f"✅ Screening completed! "
        f"{len(ranked_candidates)} resumes processed."
    )


# ============================================================
# LOAD RESULTS
# ============================================================

candidates = st.session_state.get(
    "candidates",
    None
)


if candidates is None:

    json_file = (
        OUTPUT_FOLDER /
        "ranked_candidates.json"
    )

    if json_file.exists():

        try:

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as file:

                candidates = json.load(
                    file
                )

        except Exception:

            candidates = None


# ============================================================
# DISPLAY RESULTS
# ============================================================

if candidates:

    df = pd.DataFrame(
        candidates
    )


    # ========================================================
    # MAKE SURE REQUIRED COLUMNS EXIST
    # ========================================================

    required_columns = [

        "rank",
        "name",
        "email",
        "file",
        "final_score",
        "skill_score",
        "similarity_score",
        "education_score",
        "experience_score",
        "matched_skills",
        "missing_skills",
        "education",
        "experience",
        "explanation",
        "recommendation"

    ]


    for column in required_columns:

        if column not in df.columns:

            if column in [
                "matched_skills",
                "missing_skills",
                "education",
                "experience"
            ]:

                df[column] = [[] for _ in range(len(df))]

            else:

                df[column] = ""


    # Convert scores to numbers
    score_columns = [

        "final_score",
        "skill_score",
        "similarity_score",
        "education_score",
        "experience_score"

    ]


    for column in score_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)


    # ========================================================
    # SCREENING SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Screening Summary"
    )


    strong_count = len(
        df[
            df["final_score"] >= 80
        ]
    )


    moderate_count = len(
        df[
            (df["final_score"] >= 60)
            &
            (df["final_score"] < 80)
        ]
    )


    weak_count = len(
        df[
            df["final_score"] < 60
        ]
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Resumes",
            len(df)
        )


    with col2:

        st.metric(
            "Strong Matches",
            strong_count
        )


    with col3:

        st.metric(
            "Moderate Matches",
            moderate_count
        )


    with col4:

        st.metric(
            "Weak Matches",
            weak_count
        )


    # ========================================================
    # DASHBOARD
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Dashboard"
    )


    avg_score = round(
        df["final_score"].mean(),
        2
    )


    highest_score = round(
        df["final_score"].max(),
        2
    )


    lowest_score = round(
        df["final_score"].min(),
        2
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Score",
            f"{avg_score}/100"
        )


    with col2:

        st.metric(
            "Highest Score",
            f"{highest_score}/100"
        )


    with col3:

        st.metric(
            "Lowest Score",
            f"{lowest_score}/100"
        )


    # ========================================================
    # MATCH DISTRIBUTION
    # ========================================================

    st.write(
        "### 📊 Candidate Match Distribution"
    )


    match_counts = pd.Series({

        "Strong Match": strong_count,

        "Moderate Match": moderate_count,

        "Weak Match": weak_count

    })


    st.bar_chart(
        match_counts
    )


    # ========================================================
    # CANDIDATE RANKING
    # ========================================================

    st.divider()

    st.subheader(
        "🏆 Candidate Ranking"
    )


    ranking = df[

        [

            "rank",

            "name",

            "email",

            "final_score",

            "skill_score",

            "similarity_score",

            "education_score",

            "experience_score"

        ]

    ].copy()


    ranking[
        "recommendation"
    ] = ranking[
        "final_score"
    ].apply(
        get_recommendation
    )


    ranking.columns = [

        "Rank",

        "Candidate",

        "Email",

        "Final Score",

        "Skill Score",

        "Similarity Score",

        "Education Score",

        "Experience Score",

        "Recommendation"

    ]


    st.dataframe(

        ranking,

        use_container_width=True,

        hide_index=True

    )


    # ========================================================
    # CANDIDATE DETAILS
    # ========================================================

    st.divider()

    st.subheader(
        "🔎 Candidate Details"
    )


    candidate_names = (
        df["name"]
        .astype(str)
        .tolist()
    )


    selected_name = st.selectbox(

        "Select a candidate",

        candidate_names

    )


    candidate = df[
        df["name"].astype(str)
        == selected_name
    ].iloc[0]


    # ========================================================
    # CANDIDATE INFORMATION + SCORE
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "### 👤 Candidate Information"
        )


        st.write(
            f"**Name:** {candidate['name']}"
        )


        st.write(
            f"**Email:** {candidate['email']}"
        )


        st.write(
            f"**Resume:** {candidate['file']}"
        )


        st.write(
            f"**Final Score:** "
            f"{float(candidate['final_score']):.2f}/100"
        )


        recommendation = get_recommendation(
            candidate["final_score"]
        )


        if recommendation == "Strong Match":

            st.success(
                f"**Recommendation:** {recommendation}"
            )

        elif recommendation == "Moderate Match":

            st.warning(
                f"**Recommendation:** {recommendation}"
            )

        else:

            st.error(
                f"**Recommendation:** {recommendation}"
            )


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    with col2:

        st.write(
            "### 🎯 Score Breakdown"
        )


        score_data = pd.DataFrame(

            {

                "Score": [

                    candidate[
                        "skill_score"
                    ],

                    candidate[
                        "similarity_score"
                    ],

                    candidate[
                        "education_score"
                    ],

                    candidate[
                        "experience_score"
                    ]

                ]

            },

            index=[

                "Skill",

                "Similarity",

                "Education",

                "Experience"

            ]

        )


        st.bar_chart(
            score_data
        )


    # ========================================================
    # SKILLS
    # ========================================================

    st.write(
        "### 🛠️ Skills"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.success(
            "Matched Skills"
        )


        matched = candidate.get(
            "matched_skills",
            []
        )


        if isinstance(
            matched,
            list
        ):

            if matched:

                st.write(
                    ", ".join(
                        str(skill)
                        for skill in matched
                    )
                )

            else:

                st.write(
                    "None"
                )

        else:

            st.write(
                str(matched)
            )


    with col2:

        st.warning(
            "Missing Skills"
        )


        missing = candidate.get(
            "missing_skills",
            []
        )


        if isinstance(
            missing,
            list
        ):

            if missing:

                st.write(
                    ", ".join(
                        str(skill)
                        for skill in missing
                    )
                )

            else:

                st.write(
                    "No major missing skills"
                )

        else:

            st.write(
                str(missing)
            )


    # ========================================================
    # EDUCATION
    # ========================================================

    st.write(
        "### 🎓 Education"
    )


    education_list = candidate.get(
        "education",
        []
    )


    if isinstance(
        education_list,
        list
    ):

        if education_list:

            for education in education_list:

                st.write(
                    f"- {education}"
                )

        else:

            st.write(
                "No education information found."
            )

    else:

        st.write(
            f"- {education_list}"
        )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    st.write(
        "### 💼 Experience"
    )


    experience_list = candidate.get(
        "experience",
        []
    )


    if isinstance(
        experience_list,
        list
    ):

        if experience_list:

            for experience in experience_list:

                st.write(
                    f"- {experience}"
                )

        else:

            st.write(
                "No experience information found."
            )

    else:

        st.write(
            f"- {experience_list}"
        )


    # ========================================================
    # AI EXPLANATION
    # ========================================================

    st.write(
        "### 🤖 AI Screening Explanation"
    )


    explanation = candidate.get(
        "explanation",
        ""
    )


    if explanation:

        st.info(
            explanation
        )

    else:

        st.info(
            create_fallback_explanation(
                candidate
            )
        )


    # ========================================================
    # EXPORT RESULTS
    # ========================================================

    st.divider()

    st.subheader(
        "📥 Export Results"
    )


    csv_file = (
        OUTPUT_FOLDER /
        "ranked_candidates.csv"
    )


    json_file = (
        OUTPUT_FOLDER /
        "ranked_candidates.json"
    )


    col1, col2 = st.columns(2)


    with col1:

        if csv_file.exists():

            with open(
                csv_file,
                "rb"
            ) as file:

                st.download_button(

                    "⬇️ Download CSV",

                    file,

                    file_name="ranked_candidates.csv",

                    mime="text/csv",

                    use_container_width=True

                )


    with col2:

        if json_file.exists():

            with open(
                json_file,
                "rb"
            ) as file:

                st.download_button(

                    "⬇️ Download JSON",

                    file,

                    file_name="ranked_candidates.json",

                    mime="application/json",

                    use_container_width=True

                )


# ============================================================
# NO RESULTS
# ============================================================

else:

    st.info(
        "📌 Upload a Job Description and resumes, "
        "then click **Screen Resumes** to begin."
    )