from DataManager import get_designer_copies_list, get_flattened_samples, get_jobs_list, get_mis_update_list, get_samples_list
import sys

def receive_file(path: str):
    file_name=path.split("/")[-1]
    file_name=file_name.split("\\")[-1]
    ext=file_name.split(".")[-1]
    file_name=file_name.split(".")[0]
    file_name=file_name+"-flat."+ext
    samples = get_samples_list(path)
    designer_samples = get_designer_copies_list(path)    
    flattened_list = get_flattened_samples(file_name, samples, designer_samples)
    jobs_list=get_jobs_list()
    jobs_list.on_samples_received(flattened_list)
    jobs_list.save()    
    flattened_list.save()
    

receive_file("Test_Data/1st deadline_Sample Magazine Orders_September 2020_Canada.xlsx")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Wrong number of arguments")
#     else:
#         receive_file(sys.argv[1])