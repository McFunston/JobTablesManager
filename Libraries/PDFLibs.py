import re
from typing import List
from PyPDF2 import PdfFileReader
from typing import Dict, List
from datetime import datetime

def get_page_count(path) -> int:
    pdf = PdfFileReader(open(path,'rb'))
    return pdf.getNumPages()


def get_pdf_data(path: str, file_name) -> List[Dict]:
    return_list = []
    return_dict = {}
    name = path.split("/")[-1]
    name = name.split('\\')[-1]
    return_dict["Name"] = name
    return_dict["DateTime"] = datetime.now()
    return_dict["True Page Count"] = get_page_count(path)
    return_list.append(return_dict)
    return return_list


