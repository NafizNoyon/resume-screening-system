import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_PATTERNS = {
    "Python": [r"\bpython\b"],
    "pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "scikit-learn": [r"\bscikit-learn\b", r"\bsklearn\b"],
    "Machine Learning": [r"\bmachine learning\b"],
    "Deep Learning": [r"\bdeep learning\b"],
    "NLP": [r"\bnlp\b", r"\bnatural language processing\b"],
    "Data Cleaning": [r"\bdata cleaning\b"],
    "Data Preprocessing": [r"\bdata preprocessing\b", r"\bpreprocessing\b"],
    "Feature Engineering": [r"\bfeature engineering\b"],
    "Model Evaluation": [r"\bmodel evaluation\b"],
    "Logistic Regression": [r"\blogistic regression\b"],
    "XGBoost": [r"\bxgboost\b"],
    "Random Forest": [r"\brandom forest\b"],
    "Streamlit": [r"\bstreamlit\b"],
    "FastAPI": [r"\bfastapi\b"],
    "GitHub": [r"\bgithub\b"],
    "Deployment": [r"\bdeployment\b"],
    "SQL": [r"\bsql\b"],
    "Excel": [r"\bexcel\b"],
    "Power BI": [r"\bpower bi\b"],
    "Tableau": [r"\btableau\b"],
    "TensorFlow": [r"\btensorflow\b"],
    "PyTorch": [r"\bpytorch\b"],
    "Transformers": [r"\btransformers\b"],
    "Sentence Embeddings": [r"\bsentence embeddings\b"],
    "TF-IDF": [r"\btf-idf\b", r"\btfidf\b"],
    "Cosine Similarity": [r"\bcosine similarity\b"]
}


def calculate_similarity(resume_text, job_description_text):
    """
    Calculate similarity between resume and job description using TF-IDF and cosine similarity.
    """

    documents = [resume_text, job_description_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity_score * 100, 2)


def extract_skills(text):
    """
    Extract relevant technical skills from text using regex-based matching.
    """

    text = text.lower()
    found_skills = []

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return sorted(list(set(found_skills)))


def extract_matching_keywords(resume_text, job_description_text):
    """
    Find technical skills common between resume and job description.
    """

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description_text))

    matched_skills = resume_skills.intersection(jd_skills)

    return sorted(list(matched_skills))


def extract_missing_keywords(resume_text, job_description_text):
    """
    Find technical skills required in the job description but missing from resume.
    """

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description_text))

    missing_skills = jd_skills.difference(resume_skills)

    return sorted(list(missing_skills))