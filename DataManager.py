import json
from typing import Dict, List
from Libraries.ExcelLibs import GetData
import Models.DataSources as ds

def loadDataSettings_JSON(name: str) -> Dict:
    with open('Settings.json') as j:
        settings: dict = json.load(j)
        return settings["Data Sources"][name]

def GetJobsList():
    name='Jobs List'
    settings = loadDataSettings_JSON(name)
    jobs = ds.JobsList(settings['Default Path'], loadDataSettings_JSON, GetData)
    print(jobs._dataList)

GetJobsList()