from DataManager import get_est_file, get_job_projects, get_jobs_list, get_pdf_received
import sys

def receive_file():
    jobs = get_jobs_list()
    job_projects_received = get_job_projects()
    jobs.on_job_projects(job_projects_received)
    jobs.save()

# receive_file()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Wrong number of arguments")
    else:
        receive_file()