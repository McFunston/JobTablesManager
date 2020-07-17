from copy import copy
import json
from typing import Dict, List
from Libraries.ExcelLibs import GetData, get_dataframe
import Models.DataSources as ds
from Models.DataSources import Contacts, CustomerReport, DesignerCopies, Invoice, JobShipments, JobsList, PaceUpdate, Samples
import copy

def load_data_settings_json(name: str) -> Dict:
    with open('Settings.json') as j:
        settings: dict = json.load(j)
        return settings["Data Sources"][name]

def getEmptyDS(path: str, tab: str):
    empty_list = [{}]
    return empty_list

def get_jobs_list() -> JobsList:
    name='Jobs List'
    settings = load_data_settings_json(name)
    jobs: JobsList = ds.JobsList(settings['Default Path'], load_data_settings_json, get_dataframe)
    return jobs

def get_mis_update_list() -> PaceUpdate:
    name='Pace Update'
    settings = load_data_settings_json(name)
    updateList: PaceUpdate = ds.PaceUpdate(settings['Default Path'], load_data_settings_json, GetData)
    return updateList

def get_customer_report_list() -> CustomerReport:
    name = 'Customer Report'
    settings = load_data_settings_json(name)
    customerReportList: CustomerReport = ds.CustomerReport(settings['Default Path'], load_data_settings_json, getEmptyDS)
    return customerReportList

def get_contacts_list() -> Contacts:
    name = 'Contacts'
    settings = load_data_settings_json(name)
    contactsList: Contacts = ds.Contacts(settings['Default Path'], load_data_settings_json, GetData)
    return contactsList

def get_samples_list(path) -> Samples:
    samplesList: Samples = ds.Samples(path, load_data_settings_json, GetData)
    return samplesList

def get_designer_copies_list(path) -> DesignerCopies:
    designerCopiesList: DesignerCopies = ds.DesignerCopies(path, load_data_settings_json, GetData)
    return designerCopiesList

def get_shipments_list() -> JobShipments:
    name: str = 'Job Shipments'
    settings = load_data_settings_json(name)
    shipmentsList: JobShipments = ds.JobShipments(settings['Default Path'], load_data_settings_json, getEmptyDS)
    return shipmentsList

def get_invoice() -> Invoice:
    name: str = "Invoice"
    settings = load_data_settings_json(name)
    invoice: Invoice = ds.Invoice(settings['Default Path'], load_data_settings_json, getEmptyDS)
    return invoice


test = get_jobs_list()
df = copy.deepcopy(test._dataList)
dd = test.DataDict
#dd[0]['Approved'] = "10/10/2030"
test.DataDict=dd
print(df.equals(test._dataList))
print(test.DataDict[0]['Approved'])
print('')