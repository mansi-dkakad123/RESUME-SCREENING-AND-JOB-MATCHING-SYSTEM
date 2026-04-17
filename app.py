import os
import datetime
import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import docx
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 📍 MONGODB CONNECTION
MONGO_URI = "mongodb+srv://mansi_dhakad:TK%23P25FB@cluster0.fuhkpq2.mongodb.net/?appName=Cluster0"
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['NexusAI_Database']
    history_collection = db['scan_results']
    client.admin.command('ping')
    print("✅ Database Connected Successfully!")
except Exception as e:
    print(f"❌ Database Error: {e}")

# AI Model Loading
print("🚀 Loading Neural Engine (all-MiniLM-L6-v2)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- LOGIC 1: Skill Comparison (Matched vs Missing) ---
def analyze_skills_comparison(jd, resume_text):
    """
    Ye function JD ke basis par check karega ki resume mein kya mila aur kya nahi.
    """
    skill_bank = [
        "python", "java", "javascript", "react", "node", "mongodb", "sql", 
        "aws", "docker", "machine learning", "flask", "django", "html", 
        "css", "tailwind", "cpp", "c++", "data structures", "algorithms", "linux"
    ]
    matched = []
    missing = []
    jd_lower = jd.lower()
    resume_lower = resume_text.lower()
    
    for skill in skill_bank:
        # Agar skill JD mein maangi gayi hai
        if skill in jd_lower:
            # Toh check karo resume mein hai ya nahi
            if skill in resume_lower:
                matched.append(skill.capitalize())
            else:
                missing.append(skill.capitalize())
                
    return matched, missing

# --- LOGIC 2: GitHub Analysis ---
def get_github_projects(text):
    github_pattern = r'github\.com/([\w-]+)/([\w-]+)'
    matches = re.findall(github_pattern, text.lower())
    projects = []
    seen_repos = set()
    for owner, repo in matches:
        if repo not in seen_repos and len(projects) < 2:
            try:
                api_url = f"https://api.github.com/repos/{owner}/{repo}"
                response = requests.get(api_url, timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    projects.append({
                        "name": repo,
                        "stars": data.get('stargazers_count', 0),
                        "language": data.get('language', 'Unknown')
                    })
                    seen_repos.add(repo)
            except: continue
    return projects

def get_text_from_file(file):
    try:
        if file.filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            return " ".join([page.extract_text() or "" for page in reader.pages])
        elif file.filename.endswith('.docx'):
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading {file.filename}: {e}")
    return ""

@app.route('/scan', methods=['POST'])
def scan_resumes():
    jd = request.form.get('jd')
    files = request.files.getlist('resumes')
    
    if not jd or not files:
        return jsonify({"status": "error", "message": "Missing JD or Resumes"}), 400

    results = []
    jd_vector = model.encode(jd, convert_to_tensor=True)

    for file in files:
        text = get_text_from_file(file)
        if not text: continue
        
        # AI Scoring
        resume_vector = model.encode(text, convert_to_tensor=True)
        cosine_score = util.cos_sim(jd_vector, resume_vector)[0]
        base_score = float(cosine_score) * 100
        
        # Skill Comparison (Matched vs Missing)
        matched, missing = analyze_skills_comparison(jd, text)
        projects = get_github_projects(text)
        
        github_bonus = 8 if projects else 0
        final_score = min(round(base_score + github_bonus, 2), 100)
        
        status = "Shortlisted" if final_score >= 65 else "Under Review" if final_score >= 40 else "Rejected"
        
        res_entry = {
            "name": file.filename,
            "score": final_score,
            "matched_skills": matched,  # Naya Field
            "missing_skills": missing,  # Naya Field
            "projects": projects,
            "status": status
        }
        results.append(res_entry)

    try:
        if results:
            history_collection.insert_one({
                "timestamp": datetime.datetime.now(),
                "jd_preview": jd[:150],
                "data": results
            })
    except: pass

    return jsonify(sorted(results, key=lambda x: x['score'], reverse=True))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')