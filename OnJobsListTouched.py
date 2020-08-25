from DataManager import get_jobs_list, get_jobs_import
import sys

def check_jobs_list():
    jobs = get_jobs_list()
    job_import = get_jobs_import()
    jobs.check_mis_exports(job_import)
    

check_jobs_list()
    