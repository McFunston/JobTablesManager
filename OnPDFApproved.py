from DataManager import get_jobs_list, get_pdf_approved, get_pdf_received
import sys

def receive_file(path):
    jobs = get_jobs_list()
    pdf_approved = get_pdf_approved(path)
    jobs.on_approval(pdf_approved)
    jobs.save()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
    else:
        receive_file(sys.argv[1])