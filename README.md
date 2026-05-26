# Resume Screening and Job Matching System


An AI/ML-powered web application designed to automate the process of screening resumes and matching them with the most relevant job descriptions. 
This tool helps HR teams and recruiters save time by parsing resumes and ranking them based on their compatibility with specific job requirements.


## 🚀 Features

* **Resume Parsing:** Extracts key details (Skills, Experience, Education) from uploaded resumes (PDF/Docx/Text).
* **Job Description Matching:** Matches parsed resume data with a given job description using NLP (Natural Language Processing) techniques.
* **Ranking & Scoring:** Generates a compatibility score for each candidate to find the best fit.
* **Interactive UI:** A simple and clean web interface for uploading files and viewing matching results.

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (or React if applicable)
* **Backend:** Python (Flask / Django) 
* **Machine Learning & NLP:** Scikit-learn, NLTK, Spacy (or TF-IDF / Cosine Similarity based on your `matcher.py`)
* **Environment:** Python Virtual Environment (`pyvenv.cfg`)


 ##Installation & Setup
1)Clone the Repository:
git clone (https://github.com/mansi-dkakad123/RESUME-SCREENING-AND-JOB-MATCHING-SYSTEM.git)
cd RESUME-SCREENING-AND-JOB-MATCHING-SYSTEM

##Set up Virtual Environment (Optional but Recommended):
python -m venv env
# Activate on Windows:
.\env\Scripts\activate
# Activate on Mac/Linux:
source env/bin/activate


##Install Dependencies:
  pip install -r requirements.txt

##python app.py
   Open http://127.0.0.1:5000/
