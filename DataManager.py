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
    return jobs

def GetMISUpdateList():
    name='Pace Update'
    settings = loadDataSettings_JSON(name)
    updateList = ds.PaceUpdate(settings['Default Path'], loadDataSettings_JSON, GetData)
    print(updateList)
GetJobsList()
GetMISUpdateList()
