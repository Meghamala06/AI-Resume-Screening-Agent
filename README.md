\# 📄 AI Resume Screening Agent



An AI-powered resume screening system that automatically analyzes resumes against a job description, calculates candidate scores, ranks applicants, and generates AI-based screening explanations.



\## 🚀 Features



\* 📄 Upload a Job Description

\* 📁 Upload multiple resumes

\* 🔍 Extract candidate information

\* 🛠️ Match candidate skills with job requirements

\* 📊 Calculate resume similarity using TF-IDF

\* 🎓 Evaluate education relevance

\* 💼 Evaluate experience relevance

\* 🧮 Calculate an overall candidate score

\* 🏆 Rank candidates automatically

\* 🤖 Generate AI-powered screening explanations

\* 📈 Display screening dashboard and candidate statistics

\* 📥 Export results as CSV and JSON

\* 🌐 Interactive Streamlit web interface



\## 🧠 How It Works



```text

Job Description

&#x20;      │

&#x20;      ▼

Resume Upload

&#x20;      │

&#x20;      ▼

Text Extraction

&#x20;      │

&#x20;      ▼

Candidate Information Extraction

&#x20;      │

&#x20;      ▼

Skill Matching

&#x20;      │

&#x20;      ▼

TF-IDF Similarity Analysis

&#x20;      │

&#x20;      ▼

Education + Experience Scoring

&#x20;      │

&#x20;      ▼

Final Score Calculation

&#x20;      │

&#x20;      ▼

Candidate Ranking

&#x20;      │

&#x20;      ▼

AI Screening Explanation

&#x20;      │

&#x20;      ▼

Dashboard + CSV/JSON Export

```



\## 📊 Scoring System



Each candidate receives scores based on multiple factors:



| Component        | Description                                                |

| ---------------- | ---------------------------------------------------------- |

| Skill Score      | Measures required skills found in the resume               |

| Similarity Score | Measures similarity between the JD and resume using TF-IDF |

| Education Score  | Evaluates relevant educational qualifications              |

| Experience Score | Evaluates relevant experience                              |

| Final Score      | Combined overall candidate score                           |



\### Candidate Recommendations



|    Score | Recommendation    |

| -------: | ----------------- |

|   80–100 | 🟢 Strong Match   |

| 60–79.99 | 🟡 Moderate Match |

| Below 60 | 🔴 Weak Match     |



\## 🛠️ Tech Stack



\* Python

\* Streamlit

\* Pandas

\* Scikit-learn

\* TF-IDF

\* OpenAI API

\* JSON

\* CSV

\* Git \& GitHub



\## 📁 Project Structure



```text

AI-Resume-Screening-Agent/

│

├── app.py

├── .gitignore

├── .env

│

├── data/

│   └── resumes/

│       ├── job\_description.txt

│       ├── resume\_01.txt

│       ├── resume\_02.txt

│       ├── resume\_03.txt

│       ├── ...

│       └── resume\_10.txt

│

└── src/

&#x20;   ├── extractor.py

&#x20;   ├── parser.py

&#x20;   ├── ranker.py

&#x20;   ├── scorer.py

&#x20;   │

&#x20;   ├── llm/

&#x20;   │   └── llm\_explainer.py

&#x20;   │

&#x20;   ├── parsers/

&#x20;   │

&#x20;   ├── scoring/

&#x20;   │

&#x20;   ├── tests/

&#x20;   │

&#x20;   └── output/

```



\## ⚙️ Installation



Clone the repository:



```bash

git clone https://github.com/Meghamala06/AI-Resume-Screening-Agent.git

```



Move into the project:



```bash

cd AI-Resume-Screening-Agent

```



Create a virtual environment:



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.venv\\Scripts\\Activate.ps1

```



Install the required packages:



```bash

pip install -r requirements.txt

```



\## 🔑 API Key Setup



Create a `.env` file in the project root:



```text

OPENAI\_API\_KEY=your\_api\_key\_here

```



Do not upload your API key to GitHub.



The `.gitignore` file excludes `.env` from the repository.



\## ▶️ Run the Application



Start the Streamlit application:



```bash

streamlit run app.py

```



The application will open in your browser.



\## 🖥️ Using the Application



\### Step 1 — Upload Job Description



Upload a `.txt`, `.pdf`, or `.docx` job description.



\### Step 2 — Upload Resumes



Upload multiple candidate resumes.



\### Step 3 — Screen Resumes



Click:



```text

🚀 Screen Resumes

```



The system processes every resume automatically.



\### Step 4 — Review Results



The dashboard displays:



\* Total resumes

\* Strong matches

\* Moderate matches

\* Weak matches

\* Average score

\* Highest score

\* Lowest score

\* Candidate ranking

\* Score breakdown

\* Matched skills

\* Missing skills

\* Education

\* Experience

\* AI screening explanation



\### Step 5 — Export Results



Screening results can be downloaded as:



\* CSV

\* JSON



\## 🤖 AI Explanation



For each candidate, the system generates an explanation containing:



\* Candidate name

\* Overall match assessment

\* Strongest matching skills

\* Missing skills

\* Relevant education

\* Relevant experience

\* Individual score breakdown

\* Final recommendation



\## 📈 Example Result



Example candidate:



```text

Candidate: MEERA KRISHNA



Final Score: 83.72/100



Recommendation: Strong Match



Skill Score: 100

Similarity Score: 45.74

Education Score: 100

Experience Score: 100

```



The candidate is ranked as a strong match because of relevant Python, Machine Learning, NLP, Data Analysis, SQL, Pandas, NumPy, Generative AI and LLM-related skills.



\## 🧪 Testing



The project includes automated tests for the scoring functionality.



Run tests using:



```bash

pytest

```



\## 🔐 Security



Sensitive information such as API keys should never be committed to GitHub.



The project uses `.gitignore` to exclude:



```text

.env

.venv/

\_\_pycache\_\_/

.pytest\_cache/

src/output/

.streamlit/secrets.toml

```



\## 🎯 Future Improvements



Possible future enhancements include:



\* Resume PDF preview

\* Advanced semantic similarity using embeddings

\* Recruiter login

\* Candidate filtering

\* Search and sorting

\* Job-description history

\* Multiple job openings

\* Interview recommendation system

\* Resume feedback for candidates

\* Deployment using Streamlit Cloud

\* Database integration



\## 👩‍💻 Author



\*\*Meghamala\*\*



AI Resume Screening Agent — 2026



\## ⭐ Project Goal



The goal of this project is to demonstrate how AI, Natural Language Processing, machine learning-based similarity analysis, and automated scoring can be combined to build a practical recruitment-support application.



