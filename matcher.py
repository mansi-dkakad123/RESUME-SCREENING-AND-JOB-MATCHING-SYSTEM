from sentence_transformers import SentenceTransformer, util
import torch

print("Loading BERT Model... (First time it downloads the model)")
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resumes(job_description, resumes_list):
    print("\nGenerating AI Embeddings...")
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embeddings = model.encode(resumes_list, convert_to_tensor=True)

    cosine_scores = util.cos_sim(jd_embedding, resume_embeddings)[0]

    results = []
    for i in range(len(resumes_list)):
        results.append({
            "Candidate ID": f"Candidate_{i+1}",
            "Resume Snippet": resumes_list[i][:50] + "...", 
            "Match Score": round(float(cosine_scores[i]) * 100, 2)
        })
    
    results = sorted(results, key=lambda x: x['Match Score'], reverse=True)
    return results

if __name__ == "__main__":
    # Employer's Requirement
    JD = "Looking for a Backend Developer who is highly skilled in Node.js, Express, MongoDB, and building scalable RESTful APIs. Must understand database architecture."

    # Candidates' Resumes
    Resumes = [
        "Experienced Backend Engineer with 3 years of hands-on experience in Node.js and Express. Strong background in designing database schemas in MongoDB and creating secure REST APIs.",
        "Python Developer specializing in Django and Flask. Experienced with SQL databases and building backend logic for web applications.",
        "Passionate Graphic Designer and UI/UX expert. Skilled in Figma, Adobe Illustrator, and creating beautiful user interfaces."
    ]

    print("\n--- Running AI Resume Screening ---")
    matched_candidates = match_resumes(JD, Resumes)

    print("\n🏆 Final Ranked List:")
    for rank, candidate in enumerate(matched_candidates, 1):
        print(f"Rank {rank} | {candidate['Candidate ID']} | Score: {candidate['Match Score']}%")