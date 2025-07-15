import pdfplumber
import re
import nltk
nltk.download('punkt')

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_contact_info(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d\s\-]{8,15}\d', text)
    return email[0] if email else "Not found", phone[0] if phone else "Not found"

def get_skill_match(resume_text, jd_text, skills_list):
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    found_skills = [skill for skill in skills_list if skill.lower() in resume_text]
    missing_skills = [skill for skill in skills_list if skill.lower() not in resume_text]

    score = int((len(found_skills)/len(skills_list)) * 100)
    return found_skills, missing_skills, score

# List of common technical skills
skills_list = [
    'Python', 'Django', 'Flask', 'SQL', 'REST', 'Git', 'OOP', 'APIs', 'Unit Testing'
]

# Load resume and JD
resume_text = extract_text_from_pdf("sample_resume.pdf")

with open("job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

email, phone = extract_contact_info(resume_text)
found_skills, missing_skills, score = get_skill_match(resume_text, jd_text, skills_list)

# Final Output
print("\n📄 Resume Analysis Report:")
print(f"Email: {email}")
print(f"Phone: {phone}\n")

print(f"✅ Skills Found ({len(found_skills)}): {found_skills}")
print(f"❌ Skills Missing ({len(missing_skills)}): {missing_skills}")
print(f"\n📊 Matching Score: {score}%")

if score < 50:
    print("⚠️ Recommendation: Add more relevant skills to your resume.")
else:
    print("✅ Good job! Your resume matches well with the job description.")
