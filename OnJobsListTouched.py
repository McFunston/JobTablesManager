from DataManager import get_jobs_list, get_jobs_import
import sys

def check_jobs_list():
    jobs = get_jobs_list()
    job_imports = get_jobs_import()
    exported = jobs.check_mis_exports(job_imports)
    if exported:
        jobs.save()
        job_imports.fix_production_notes()
        job_imports.save()

check_jobs_list()
    