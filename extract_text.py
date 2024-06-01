import requests
from io import BytesIO
from PyPDF2 import PdfReader


def extract_text(files):

    content = []
    for i in range(len(files)):

        file = files[i]

        file_url = file.url
        file_name = file.name

        remote_file = requests.get(file_url)
        remote_file.raise_for_status()

        pdf_file_obj = BytesIO(remote_file.content)
        pdf_reader = PdfReader(pdf_file_obj)

        for page_num in range(1, len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            page_name = f"Page {page_num + 1} of {file_name}"
            content.append({page_name: page_obj.extract_text()})
        pdf_file_obj.close()

    return content
