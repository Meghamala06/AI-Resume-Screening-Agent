from pathlib import Path
import pymupdf
from docx import Document


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""

    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()

    return text.strip()


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    document = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    return text.strip()


def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    return Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def extract_text(file_path):
    """
    Extract text from PDF, DOCX, or TXT files.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Supported types: PDF, DOCX, TXT."
        )


def get_resume_files(resume_folder):
    """
    Return all supported resume files from a folder.
    """

    resume_folder = Path(resume_folder)

    if not resume_folder.exists():
        raise FileNotFoundError(
            f"Resume folder not found: {resume_folder}"
        )

    supported_extensions = {".pdf", ".docx", ".txt"}

    return sorted(
    file
    for file in resume_folder.iterdir()
    if file.is_file()
    and file.name.lower() != "job_description.txt"
    and file.suffix.lower() in supported_extensions
)
if __name__ == "__main__":
    resume_folder = "data/resumes"

    files = get_resume_files(resume_folder)

    print(f"Found {len(files)} resumes\n")

    for file in files:
        text = extract_text(file)

        print("=" * 60)
        print(f"FILE: {file.name}")
        print("=" * 60)
        print(text[:300])
        print()