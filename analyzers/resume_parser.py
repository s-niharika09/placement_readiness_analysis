from pathlib import Path
import pdfplumber


class ResumeParser:
    """
    Extracts plain text from a resume PDF.

    The Resume Parser extracts readable text from the uploaded resume PDF.
    Used the pdfplumber library to open the PDF, 
    read each page, extract the text, 
    and combine the extracted content into a single string. 
    This text is then passed to the Resume Analyzer for further analysis.”
    """

    def __init__(self):
        pass

    def extract_text(self, pdf_path):

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"Resume not found:\n{pdf_path}"
            )

        text = ""

        try:

            with pdfplumber.open(pdf_path) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        except Exception as e:

            raise RuntimeError(
                f"Failed to read PDF:\n{e}"
            )

        return text.strip()


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    resume_path = input("Enter Resume PDF Path: ")

    parser = ResumeParser()

    resume_text = parser.extract_text(resume_path)

    print("\n========== Resume Text ==========\n")

    print(resume_text)