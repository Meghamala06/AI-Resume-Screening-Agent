import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


REQUIRED_SKILLS = [
    "python",
    "machine learning",
    "natural language processing",
    "nlp",
    "data analysis",
    "generative ai",
    "sql",
    "pandas",
    "numpy",
    "git",
    "llm apis",
]


def normalize_text(text):
    """Normalize text for matching."""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_skill_score(jd_text, resume_text):
    """Calculate required-skill match percentage."""

    jd_text = normalize_text(jd_text)
    resume_text = normalize_text(resume_text)

    required_skills = [
        skill
        for skill in REQUIRED_SKILLS
        if skill in jd_text
    ]

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_text
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_text
    ]

    if not required_skills:
        return 0.0, matched_skills, missing_skills

    score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return (
        round(score, 2),
        matched_skills,
        missing_skills
    )


def calculate_similarity(jd_text, resume_text):
    """Calculate TF-IDF cosine similarity."""

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [
            jd_text,
            resume_text
        ]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


def calculate_education_score(resume_text):
    """
    Score education relevance.

    AI/ML/CS-related degrees receive higher scores.
    """

    text = normalize_text(
        resume_text
    )

    if (
        "artificial intelligence" in text
        or "machine learning" in text
        or "computer science" in text
        or "data science" in text
    ):
        return 100

    if (
        "information science" in text
        or "information technology" in text
    ):
        return 90

    if (
        "electronics" in text
        or "electrical" in text
    ):
        return 75

    if (
        "bachelor" in text
        or "b.e" in text
        or "btech" in text
    ):
        return 60

    if (
        "master" in text
        or "m.tech" in text
        or "mca" in text
    ):
        return 80

    return 0


def calculate_experience_score(resume_text):
    """
    Estimate relevance of experience
    for an AI Research Associate role.
    """

    text = normalize_text(
        resume_text
    )

    score = 0

    if "ai research" in text:
        score = max(score, 100)

    if (
        "machine learning" in text
        or "natural language processing" in text
        or "nlp" in text
    ):
        score = max(score, 95)

    if (
        "generative ai" in text
        or "large language models" in text
        or "llm" in text
        or "rag" in text
    ):
        score = max(score, 95)

    if (
        "data analyst" in text
        or "data analytics" in text
        or "data analysis" in text
    ):
        score = max(score, 85)

    if (
        "software developer" in text
        or "software engineer" in text
        or "qa engineer" in text
    ):
        score = max(score, 60)

    if "developer intern" in text:
        score = max(score, 55)

    if "intern" in text:
        score = max(score, 50)

    return score


def calculate_final_score(
    skill_score,
    similarity_score,
    education_score,
    experience_score
):
    """Calculate weighted final score."""

    final_score = (
        skill_score * 0.40
        + similarity_score * 0.30
        + education_score * 0.15
        + experience_score * 0.15
    )

    return round(
        final_score,
        2
    )


def score_resume(
    jd_text,
    resume_text
):
    """Calculate complete candidate score."""

    (
        skill_score,
        matched_skills,
        missing_skills
    ) = calculate_skill_score(
        jd_text,
        resume_text
    )

    similarity_score = calculate_similarity(
        jd_text,
        resume_text
    )

    education_score = calculate_education_score(
        resume_text
    )

    experience_score = calculate_experience_score(
        resume_text
    )

    final_score = calculate_final_score(
        skill_score,
        similarity_score,
        education_score,
        experience_score
    )

    return {
        "skill_score": skill_score,
        "similarity_score": similarity_score,
        "education_score": education_score,
        "experience_score": experience_score,
        "final_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }