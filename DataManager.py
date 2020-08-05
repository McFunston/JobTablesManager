import json
from logging import log
from pprint import pprint
from typing import Dict, List
from Libraries.ExcelLibs import GetData, get_data_csv
from Libraries.PDFLibs import get_pdf_data
import Models.DataSources as ds
from Models.DataSources import Contacts, CustomerReport, DesignerCopies, EstFile, Invoice, JobProjects, JobShipments, JobsList, PaceUpdate, PdfApproved, PdfReceived, Samples
import logging

logging.basicConfig(filename='log.txt',level=logging.DEBUG)

def load_data_settings_json(name: str) -> Dict:
    logging.info("Retrieving settings for " + name)
    with open('Settings.json') as j:
        settings: dict = json.load(j)
        return settings["Data Sources"][name]

def getEmptyDS(path: str, tab: str):
    empty_list = [{}]
    return empty_list

def get_jobs_list() -> JobsList:
    name='Jobs List'
    settings = load_data_settings_json(name)
    logging.info("Trying to retrieve jobs list")
    try:
        jobs: JobsList = ds.JobsList(settings['Default Path'], load_data_settings_json, GetData)
    except:
        logging.critical("Unable to load jobs list. Something is broken")
        exit()
    logging.info("Jobs list loaded successfully")        
    return jobs

def get_mis_update_list() -> PaceUpdate:
    name='Pace Update'
    settings = load_data_settings_json(name)
    logging.info("Trying to open the MIS Update")
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
    pdf_received = ds.PdfReceived(path, load_data_settings_json, get_pdf_data)
    return pdf_received

def get_pdf_approved(path) -> PdfApproved:    
    pdf_approved = ds.PdfApproved(path, load_data_settings_json, get_pdf_data)
    return pdf_approved

def get_est_file(path) -> EstFile:
    name: str = "EST File"
    est_file = ds.EstFile(path, load_data_settings_json, get_data_csv)
    return est_file

def get_job_projects() -> JobProjects:
    name = "Job Projects"
    settings = load_data_settings_json(name)
    job_projects = ds.JobProjects(settings["Default Path"], load_data_settings_json, GetData)
    return job_projects



