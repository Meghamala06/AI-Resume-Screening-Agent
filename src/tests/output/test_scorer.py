from src.scorer import (
    calculate_skill_score,
    calculate_education_score,
    calculate_experience_score,
    calculate_final_score,
)


def test_skill_score_full_match():
    jd = """
    Python, Machine Learning, Natural Language Processing,
    NLP, Data Analysis, Generative AI, SQL, Pandas, NumPy, Git,
    LLM APIs
    """

    resume = """
    Python, Machine Learning, Natural Language Processing,
    NLP, Data Analysis, Generative AI, SQL, Pandas, NumPy, Git,
    LLM APIs
    """

    score, matched, missing = calculate_skill_score(
        jd,
        resume
    )

    assert score == 100
    assert len(matched) == 11
    assert missing == []


def test_skill_score_partial_match():
    jd = """
    Python, Machine Learning, Natural Language Processing,
    Data Analysis, SQL
    """

    resume = """
    Python, SQL
    """

    score, matched, missing = calculate_skill_score(
        jd,
        resume
    )

    assert score == 40
    assert "python" in matched
    assert "sql" in matched
    assert "machine learning" in missing


def test_skill_score_no_match():
    jd = """
    Python, Machine Learning, Natural Language Processing,
    Data Analysis
    """

    resume = """
    Java, React, HTML, CSS
    """

    score, matched, missing = calculate_skill_score(
        jd,
        resume
    )

    assert score == 0
    assert matched == []
    assert len(missing) == 4


def test_experience_score():
    assert calculate_experience_score(
        "AI Research Intern working on AI research"
    ) == 100

    assert calculate_experience_score(
        "Machine Learning and NLP Intern"
    ) == 95

    assert calculate_experience_score(
        "Software Developer Intern"
    ) == 60

    assert calculate_experience_score(
        "Intern"
    ) == 50


def test_education_score():
    assert calculate_education_score(
        "Bachelor of Engineering in Computer Science"
    ) == 100

    assert calculate_education_score(
        "Bachelor of Engineering in Information Science"
    ) == 90

    assert calculate_education_score(
        "Bachelor of Engineering in Electronics"
    ) == 75

    assert calculate_education_score(
        "Bachelor of Engineering"
    ) == 60


def test_final_score():
    score = calculate_final_score(
        skill_score=100,
        similarity_score=50,
        education_score=100,
        experience_score=100,
    )

    assert score == 85


def test_final_score_low_candidate():
    score = calculate_final_score(
        skill_score=0,
        similarity_score=10,
        education_score=60,
        experience_score=50,
    )

    assert score == 19.5