from pypdf import PdfReader
from docx import Document


def extract_text_from_txt(uploaded_file):
    """
    Extract text from a TXT file.
    """

    text = uploaded_file.read().decode("utf-8", errors="ignore")
    return text


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(uploaded_file):
    """
    Extract text from a DOCX file.
    """

    document = Document(uploaded_file)
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text_from_uploaded_file(uploaded_file):
    """
    Detect uploaded file type and extract text.
    Supported formats: PDF, DOCX, TXT
    """

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    elif file_name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    else:
        return ""