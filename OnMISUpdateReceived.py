from DataManager import get_jobs_list, get_mis_update_list
import sys

def receive_file():
    jobs = get_jobs_list()
    mis_update_received = get_mis_update_list()
    jobs.on_mis_list(mis_update_received)
    
    jobs.save()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Wrong number of arguments")
    else:
        receive_file()