from pathlib import Path
import csv
import json

from parser import extract_text, get_resume_files
from extractor import extract_candidate_info
from scorer import score_resume
from ranker import rank_candidates
from llm.llm_explainer import generate_explanation


DATA_FOLDER = Path("data/resumes")
JOB_DESCRIPTION = DATA_FOLDER / "job_description.txt"
OUTPUT_FOLDER = Path("src/output")


def save_results(ranked_candidates):
    """Save ranked candidates to CSV and JSON."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # Save JSON
    # -------------------------

    json_file = OUTPUT_FOLDER / "ranked_candidates.json"

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(
            ranked_candidates,
            file,
            indent=4,
            ensure_ascii=False
        )

    # -------------------------
    # Save CSV
    # -------------------------

    csv_file = OUTPUT_FOLDER / "ranked_candidates.csv"

    fieldnames = [
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
        "explanation"
    ]

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for candidate in ranked_candidates:

            row = {
                "rank": candidate.get("rank", ""),
                "name": candidate.get("name", ""),
                "email": candidate.get("email", ""),
                "file": candidate.get("file", ""),
                "final_score": candidate.get("final_score", ""),
                "skill_score": candidate.get("skill_score", ""),
                "similarity_score": candidate.get("similarity_score", ""),
                "education_score": candidate.get("education_score", ""),
                "experience_score": candidate.get("experience_score", ""),
                "matched_skills": ", ".join(
                    candidate.get("matched_skills", [])
                ),
                "explanation": candidate.get(
                    "explanation",
                    ""
                )
            }

            writer.writerow(row)

    print("\n" + "=" * 60)
    print("RESULTS SAVED")
    print("=" * 60)

    print(f"CSV : {csv_file}")
    print(f"JSON: {json_file}")


def main():

    print("=" * 60)
    print("AI RESUME SCREENING AGENT")
    print("=" * 60)

    # -------------------------
    # Read Job Description
    # -------------------------

    if not JOB_DESCRIPTION.exists():
        raise FileNotFoundError(
            f"Job description not found: {JOB_DESCRIPTION}"
        )

    jd_text = extract_text(JOB_DESCRIPTION)

    # -------------------------
    # Find resumes
    # -------------------------

    resume_files = get_resume_files(DATA_FOLDER)

    print(
        f"\nJob Description: "
        f"{JOB_DESCRIPTION.name}"
    )

    print(
        f"Resumes found: "
        f"{len(resume_files)}"
    )

    if not resume_files:
        print("No resumes found.")
        return

    candidates = []

    # -------------------------
    # Process resumes
    # -------------------------

    for resume_file in resume_files:

        print(
            f"\nProcessing: "
            f"{resume_file.name}"
        )

        resume_text = extract_text(resume_file)

        candidate_info = extract_candidate_info(
            resume_text
        )

        scores = score_resume(
            jd_text,
            resume_text
        )

        candidate = {
            "file": resume_file.name,
            **candidate_info,
            **scores
        }

        candidates.append(candidate)

    # -------------------------
    # Rank candidates
    # -------------------------

    ranked_candidates = rank_candidates(
        candidates
    )

    # -------------------------
    # Display ranking
    # -------------------------

    print("\n" + "=" * 60)
    print("FINAL CANDIDATE RANKING")
    print("=" * 60)

    for candidate in ranked_candidates:

        print(
            f"\nRank {candidate['rank']}: "
            f"{candidate['name']}"
        )

        print(
            f"Email: "
            f"{candidate['email']}"
        )

        print(
            f"Final Score: "
            f"{candidate['final_score']}"
        )

        print(
            f"Skill Score: "
            f"{candidate['skill_score']}"
        )

        print(
            f"Similarity Score: "
            f"{candidate['similarity_score']}"
        )

        print(
            f"Education Score: "
            f"{candidate['education_score']}"
        )

        print(
            f"Experience Score: "
            f"{candidate['experience_score']}"
        )

        print(
            "Matched Skills: "
            + ", ".join(
                candidate["matched_skills"]
            )
        )

        # -------------------------
        # Generate LLM explanation
        # -------------------------

        print("\nGenerating AI explanation...")

        try:

            explanation = generate_explanation(
                candidate,
                jd_text
            )

            candidate["explanation"] = explanation

            print("\nAI Explanation:")
            print(explanation)

        except Exception as error:

            fallback = (
                "LLM explanation unavailable. "
                "Ranking is based on skill matching, "
                "TF-IDF similarity, education, "
                "and experience scoring."
            )

            candidate["explanation"] = fallback

            print(
                f"AI explanation unavailable: "
                f"{error}"
            )

    # -------------------------
    # Save results
    # -------------------------

    save_results(
        ranked_candidates
    )

if __name__ == "__main__":
    main()