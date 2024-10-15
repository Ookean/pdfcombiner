import os
from PyPDF2 import PdfMerger

def merge_pdfs(pdf_files, output_directory, output_filename):
    """Merge selected PDF files into a single output file.

    Args:
        pdf_files (list): List of paths to PDF files.
        output_directory (str): The directory where the output PDF should be saved.
        output_filename (str): The name of the output PDF file.

    Raises:
        Exception: If an error occurs during the merge process.
    """
    if len(pdf_files) < 2:
        raise ValueError("At least two PDF files are required for merging.")

    output_file = os.path.join(output_directory, output_filename)
    if not output_filename.lower().endswith(".pdf"):
        output_file += ".pdf"

    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output_file)
    merger.close()
