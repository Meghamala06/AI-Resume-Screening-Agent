import re


def extract_email(text):
    """Extract email address from resume text."""

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else "Not found"


def extract_name(text):
    """Extract candidate name from the beginning of the resume."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return lines[0] if lines else "Unknown"


def extract_skills(text):
    """Extract known technical skills from resume."""

    skills_list = [
        "Python",
        "Machine Learning",
        "Natural Language Processing",
        "NLP",
        "Generative AI",
        "Large Language Models",
        "LLM APIs",
        "RAG",
        "SQL",
        "Pandas",
        "NumPy",
        "Git",
        "Statistics",
        "Data Analysis",
        "Power BI",
        "Excel",
        "Scikit-learn",
        "Java",
        "Kotlin",
        "JavaScript",
        "React",
        "Node.js",
        "Firebase",
        "Android",
        "Playwright",
        "Selenium",
        "API Testing",
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_education(text):
    """Extract education information from the education section."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    education_keywords = [
        "bachelor",
        "b.e",
        "b.tech",
        "master",
        "m.tech",
        "mca",
        "degree",
        "computer science",
        "information technology",
        "artificial intelligence",
        "data science",
    ]

    education = []

    in_education_section = False

    for line in lines:
        line_lower = line.lower()

        # Detect start of education section
        if line_lower in {
            "education",
            "academic background",
            "academic qualifications",
            "qualifications",
        }:
            in_education_section = True
            continue

        # Detect another major section
        if line_lower in {
            "experience",
            "work experience",
            "professional experience",
            "skills",
            "technical skills",
            "projects",
            "certifications",
            "achievements",
        }:
            if in_education_section:
                break

        if in_education_section:
            if any(keyword in line_lower for keyword in education_keywords):
                education.append(line)

    # Fallback for resumes without clear section headings
    if not education:
        for line in lines:
            line_lower = line.lower()

            if any(
                keyword in line_lower
                for keyword in [
                    "bachelor",
                    "b.e",
                    "b.tech",
                    "master",
                    "m.tech",
                    "mca",
                ]
            ):
                education.append(line)

    return education


def extract_experience(text):
    """Extract only work/project experience from the experience section."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    experience = []

    in_experience_section = False

    section_headers = {
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
        "skills",
        "technical skills",
        "projects",
        "certifications",
        "achievements",
        "languages",
    }

    experience_headers = {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
    }

    for line in lines:
        line_lower = line.lower()

        # Start experience section
        if line_lower in experience_headers:
            in_experience_section = True
            continue

        # Stop at the next major section
        if in_experience_section and line_lower in section_headers:
            break

        if in_experience_section:
            experience.append(line)

    # Fallback for resumes without a clear EXPERIENCE heading
    if not experience:
        experience_keywords = [
            "intern",
            "developer intern",
            "analyst intern",
            "engineer intern",
            "research intern",
            "software developer",
            "data analyst",
            "machine learning engineer",
            "ai engineer",
            "ai researcher",
        ]

        for line in lines:
            line_lower = line.lower()

            if any(
                keyword in line_lower
                for keyword in experience_keywords
            ):
                experience.append(line)

    return experience


def extract_candidate_info(text):
    """Extract structured candidate information."""

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
    }