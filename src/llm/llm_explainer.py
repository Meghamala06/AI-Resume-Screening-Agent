import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def generate_local_explanation(candidate):
    """Generate a recruitment explanation without using the OpenAI API."""

    name = candidate["name"]

    skill_score = candidate["skill_score"]
    similarity_score = candidate["similarity_score"]
    education_score = candidate["education_score"]
    experience_score = candidate["experience_score"]
    final_score = candidate["final_score"]

    matched_skills = candidate.get("matched_skills", [])
    candidate_skills = candidate.get("skills", [])
    education = candidate.get("education", [])
    experience = candidate.get("experience", [])

    # Determine recommendation
    if final_score >= 80:
        recommendation = "Strong Match"
    elif final_score >= 60:
        recommendation = "Moderate Match"
    else:
        recommendation = "Weak Match"

    # Find missing skills from the job description if available
    missing_skills = candidate.get("missing_skills", [])

    if matched_skills:
        strongest_skills = ", ".join(matched_skills)
    elif candidate_skills:
        strongest_skills = ", ".join(candidate_skills[:5])
    else:
        strongest_skills = "No specific skills identified"

    if missing_skills:
        missing_text = ", ".join(missing_skills)
    else:
        missing_text = "No major missing skills identified"

    education_text = ", ".join(education) if education else "No education information available"
    experience_text = ", ".join(experience) if experience else "No experience information available"

    explanation = f"""
Candidate: {name}

Why the candidate matches:
The candidate received a final score of {final_score}/100, indicating a {recommendation.lower()} with the job requirements.

Strongest matching skills:
{strongest_skills}

Important missing skills:
{missing_text}

Relevant education:
{education_text}

Relevant experience:
{experience_text}

Score breakdown:
- Skill Score: {skill_score}
- Similarity Score: {similarity_score}
- Education Score: {education_score}
- Experience Score: {experience_score}
- Final Score: {final_score}

Final Recommendation:
{recommendation}
"""

    return explanation.strip()


def generate_explanation(candidate, job_description):
    """Generate an AI explanation, with a local fallback if the API is unavailable."""

    api_key = os.getenv("OPENAI_API_KEY")

    # If API key is missing, use local explanation
    if not api_key:
        return generate_local_explanation(candidate)

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are an AI recruitment assistant.

Analyze the candidate against the job description.

JOB DESCRIPTION:
{job_description}

CANDIDATE:
Name: {candidate["name"]}
Skills: {", ".join(candidate["skills"])}
Education: {", ".join(candidate["education"])}
Experience: {", ".join(candidate["experience"])}

SCORING:
Skill Score: {candidate["skill_score"]}
Similarity Score: {candidate["similarity_score"]}
Education Score: {candidate["education_score"]}
Experience Score: {candidate["experience_score"]}
Final Score: {candidate["final_score"]}

Matched Skills:
{", ".join(candidate["matched_skills"])}

Provide a concise recruitment explanation containing:

1. Why the candidate matches the role
2. Strongest matching skills
3. Important missing skills, if any
4. Relevant education or experience
5. Final recommendation:
   Strong Match, Moderate Match, or Weak Match

Do not invent information.
Only use information provided above.
"""

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        print(f"AI explanation unavailable: {e}")
        print("Using local fallback explanation instead.")

        return generate_local_explanation(candidate)
