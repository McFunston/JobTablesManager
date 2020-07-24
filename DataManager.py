import json
from pprint import pprint
from typing import Dict, List
from Libraries.ExcelLibs import GetData
from Libraries.PDFLibs import get_pdf_data
import Models.DataSources as ds
from Models.DataSources import Contacts, CustomerReport, DesignerCopies, Invoice, JobShipments, JobsList, PaceUpdate, PdfApproved, PdfReceived, Samples

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
    jobs: JobsList = ds.JobsList(settings['Default Path'], load_data_settings_json, GetData)
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

def get_pdf_received(path) -> PdfReceived:
    name: str = "PDF Received"
    pdf_received = ds.PdfReceived(path, load_data_settings_json, get_pdf_data)
    return pdf_received

def get_pdf_approved(path) -> PdfApproved:
    name: str = "PDF Received"
    pdf_approved = ds.PdfApproved(path, load_data_settings_json, get_pdf_data)
    return pdf_approved

pdf_rec = get_pdf_approved("Test_Data/319_2190_NeighboursOfStittsville_August2020.pdf")

pprint(pdf_rec._data_list)
