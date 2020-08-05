from DataManager import get_est_file, get_jobs_list, get_pdf_received
import sys

def receive_file(path):
    jobs = get_jobs_list()
    est_received = get_est_file(path)
    jobs.on_est_received(est_received)
    jobs.save()

receive_file("Test_Data/Good_txt/457 Old Thornhill #457.txt")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Wrong number of arguments")
#     else:
#         receive_file(sys.argv[1])