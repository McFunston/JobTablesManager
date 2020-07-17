from datetime import datetime
import unittest
from Models.DataSources import CustomerReport, JobsList, PaceUpdate
import pandas as pd


def moqJobsListSettingsFunc(name: str):
    moqJobsListSettings = {"File Name": "BVM_Jobs.xlsx", "Default Path": "/Users/micafunston/Projects/BVMTools/BVM_Jobs.xlsx", "Type": "Data List", "Job Field": "Job", "Tab": "Sheet", "Publication Field": "Description", "Publication Number Separate": False, "Date Columns": [
        "Files In", "Approved", "Scheduled Ship Date", "Date Setup"], "True Dates": False, "Date Format": "%m/%d/%Y", "Columns Order": {"1": "Job", "2": "Description", "3": "Files In", "4": "Approved", "5": "Production Status", "6": "Scheduled Ship Date", "7": "Qty Ordered", "8": "CPC", "9": "Page Count", "10": "Date Setup", "11": "Samples", "12": "Deadline"}}
    return moqJobsListSettings


def moqJobsListFunc(path: str, tab: str):
    moqJobsList = [{"Job": "M511", "Description": "2656-Silver Valley-Academy Park Neighbou-Mar", "Files In": datetime.strptime("2/11/2020","%m/%d/%Y"), "Approved": datetime.strptime("3/3/2020","%m/%d/%Y"), "Production Status": "Closed",
                    "Scheduled Ship Date": datetime.strptime("03/09/2020","%m/%d/%Y"), "Qty Ordered": "2500", "CPC": "2089", "Page Count": "16 Pages", "Date Setup": datetime.strptime("02/03/2020","%m/%d/%Y"), "Samples": "316", "Deadline": "10"},
                   {"Job": "M532", "Description": "3254-Neighbours of Kirkendall and Durand-Mar", "Files In": datetime.strptime("02/28/2020","%m/%d/%Y"), "Approved": datetime.strptime("02/28/2020","%m/%d/%Y"), "Production Status": "Open",
                    "Scheduled Ship Date": datetime.strptime("03/05/2020","%m/%d/%Y"), "Qty Ordered": "4500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": datetime.strptime("02/03/2020","%m/%d/%Y"), "Samples": "216", "Deadline": "15"},
                   {"Job": "M999", "Description": "Bad Data1", "Files In": None, "Approved": datetime.strptime("02/28/2020","%m/%d/%Y"), "Production Status": "Open",
                    "Scheduled Ship Date": datetime.strptime("02/26/2020","%m/%d/%Y"), "Qty Ordered": "3500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": datetime.strptime("09/04/2050","%m/%d/%Y"), "Samples": "216", "Deadline": "15"},
                   {"Job": "M704", "Description": "3254-Neighbours of Kirkendall and Durand-Apr", "Files In": datetime.strptime("03/28/2020","%m/%d/%Y"), "Approved": None, "Production Status": "Open",
                    "Scheduled Ship Date": datetime.strptime("04/05/2020","%m/%d/%Y"), "Qty Ordered": "4500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": datetime.strptime("03/03/2020","%m/%d/%Y"), "Samples": "216", "Deadline": "15"},
                    {"Job": "", "Description": "3535-Neighbours of Perth-Jul", "Files In": datetime.strptime("03/28/2020","%m/%d/%Y"), "Approved": None, "Production Status": "Open",
                    "Scheduled Ship Date": datetime.strptime("04/05/2020","%m/%d/%Y"), "Qty Ordered": "4500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": datetime.strptime("03/03/2020","%m/%d/%Y"), "Samples": "216", "Deadline": "15"}]
    return pd.DataFrame(moqJobsList)


def moqPaceUpdateSettingsFunc(name: str):
    moqSettings = {"Type": "Data List", "True Dates": True, "Date Columns": ["Scheduled Ship Date", "Date Setup"], "Tab": "Report1", "Columns Order": {
        "1": "Job", "2": "Description", "3": "Production Status", "4": "Scheduled Ship Date", "5": "Qty Ordered", "6": "Production Notes", "7": "Item Template", "8": "Additional Description", "9": "Date Setup"}, "Date Format": "%m/%d/%Y", "Page Count Strings": {
            "16 page": "16 Pages", "20 page": "20 Pages", "24 page": "24 Pages", "28 page": "28 Pages", "32 page": "32 Pages", "36 page": "36 Pages", "40 page": "40 Pages"}}
    return moqSettings


def moqPaceUpdateFunc(path: str, tab: str):
    moqPaceUpdate = [{"Job": 'M1998', "Description": "2695-Neighbours of Whitemud Creek - Aug", "Production Status": "In Production", "Scheduled Ship Date": datetime.strptime("07-15-2020", "%m-%d-%Y"), "Qty Ordered": 2500, "Production Notes": "PW Count = 2200", "Item Template": "BVM 16 Page",
                      "Additional Description": "2500 16 page self cover Flat size 16.75 x 10.875, fold & stitch to 8.375 x 10.875 4 process / same  with bleeds Plastic strap band (cross) in 50's Carton pack with 3 strips of tape on the bottom Deliver to DLI", "Date Setup": datetime.strptime("06-30-2020", "%m-%d-%Y")},
                     {"Job": 'M532', "Description": "3254-Neighbours of Kirkendall and Durand-Mar", "Production Status": "In Production", "Scheduled Ship Date": datetime.strptime("07-15-2020", "%m-%d-%Y"), "Qty Ordered": 4500, "Production Notes": "PW Count = 4000", "Item Template": "BVM 16 Page",
                      "Additional Description": "4500 24 page self cover Flat size 16.75 x 10.875, fold & stitch to 8.375 x 10.875 4 process / same  with bleeds Plastic strap band (cross) in 50's Carton pack with 3 strips of tape on the bottom Deliver to DLI", "Date Setup": datetime.strptime("07-30-2020", "%m-%d-%Y")},
                     {"Job": 'M1800', "Description": "3535-Neighbours of Perth-Jul", "Production Status": "In Production", "Scheduled Ship Date": datetime.strptime("08-15-2020", "%m-%d-%Y"), "Qty Ordered": 4500, "Production Notes": "PW Count = 4000", "Item Template": "BVM 16 Page",
                      "Additional Description": "4500 24 page self cover Flat size 16.75 x 10.875, fold & stitch to 8.375 x 10.875 4 process / same  with bleeds Plastic strap band (cross) in 50's Carton pack with 3 strips of tape on the bottom Deliver to DLI", "Date Setup": datetime.strptime("08-30-2020", "%m-%d-%Y")}]
    return pd.DataFrame(moqPaceUpdate)


def moqCustomerReportSettingsFunc(name: str):
    moqSettings = {"Tab": "Sheet", "Type": "Report", "Last Column": "H", "True Dates": True, "Job Field": "Job", "Publication Field": "Description", "Publication Number Separate": False,
                                       "Columns Order": {"1": "Job", "2": "Deadline", "3": "Description", "4": "Files In", "5": "Approved", "6": "Production Status", "7": "Scheduled Ship Date", "8": "Qty Ordered"}}
    return moqSettings

def moqCustomerReportFunc(path: str, tab: str):
    moqCustomerReport = [{}]
    return pd.DataFrame(moqCustomerReport)

class TestDataSources(unittest.TestCase):

    def test_FindFirstRow(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')
        # Act
        actual = jobs._find_first_row('Job', 'M511')
        expected = moqjobs.iloc[[0]]
        areEqal = actual.equals(expected)

        # Assert
        self.assertTrue(areEqal)

    def test_FindAllRows(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')
        # Act
        actual = jobs._find_all_rows('Job', 'M532')
        expected = moqjobs.iloc[1]

        # Assert
        self.assertEqual(actual.iloc[0]['Job'], expected['Job'])

    def test_returnSavableList(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.return_savable_list()

        # Assert
        self.assertIsNotNone(actual)

    def test_columnIsDateTrue(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.column_is_date("Files In")

        # Assert
        self.assertTrue(actual)

    def test_columnIsDateFalse(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.column_is_date("Production Status")

        # Assert
        self.assertFalse(actual)

    def test_getTrueDate(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = datetime.strptime("2/11/2020", "%m/%d/%Y")
        actual = jobs.get_true_date('Files In', 0)

        # Assert
        self.assertEqual(expected, actual)

    def test_len(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = len(moqJobsListFunc('', ''))
        actual = jobs.len()

        # Assert
        self.assertEqual(expected, actual)

    def test_get_row(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = moqjobs.iloc[1]
        actual = jobs._get_row(1)
        are_equal = actual.equals(expected)

        # Assert
        self.assertTrue(are_equal)

    def test_get_cell(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = moqjobs.at[1, 'Description']
        actual = jobs._get_cell(1, 'Description')        

        # Assert
        self.assertEqual(actual, expected)

    def test_FindInAllRows(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        
        actual = jobs._find_in_all_rows('Description', '3254')
        actual = actual.iloc[0]["Job"]

        expected = moqjobs.iloc[1]["Job"]
        # areequal = actual.equals(expected)


        # Assert
        self.assertEqual(actual, expected)

    def test_GetMostRecentPub(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')
        

        # Act
        expected = moqjobs.iloc[[3]]        
        actual = jobs.get_most_recent_pub('3254')        
        are_equal = actual.equals(expected)

        # Assert
        self.assertTrue(are_equal)

    def test_jobIsApprovedTrue(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.job_is_approved("M532")

        # Assert
        self.assertTrue(actual)

    def test_jobIsApprovedFalse(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.job_is_approved("M704")

        # Assert
        self.assertFalse(actual)

    def test_jobIsApprovedMissing(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.job_is_approved("M1704")

        # Assert
        self.assertFalse(actual)

    def test_jobIsUploadedTrue(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.job_is_uploaded("M532")

        # Assert
        self.assertTrue(actual)

    def test_jobIsUploadedFalse(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.job_is_uploaded("M999")

        # Assert
        self.assertFalse(actual)

    def test_jobIsUploadedMissing(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.job_is_uploaded("M1704")

        # Assert
        self.assertFalse(actual)

    def test_getJob(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        actual = jobs.get_job('M704')        
        expected = moqjobs.iloc[[3]]
        are_equal = actual.equals(expected)

        # Assert
        self.assertTrue(are_equal)

    def test_SetUploadDate(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        
        Today = datetime.today()

        # Act
        jobs.set_upload_date('M704', Today)
        job = jobs.get_job('M704')
        actual = job.iloc[0]['Files In']
        expected = datetime.today().strftime('%m/%d/%Y')
        actual = actual.strftime('%m/%d/%Y')

        # Assert
        self.assertEqual(actual, expected)

    def test_SetApprovedDate(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        
        Today = datetime.today()

        # Act
        jobs.set_approved_date('M704', Today)
        job = jobs.get_job('M704')
        actual = job.iloc[0]['Approved']
        expected = datetime.today().strftime('%m/%d/%Y')
        actual = actual.strftime('%m/%d/%Y')        

        # Assert
        self.assertEqual(actual, expected)

    def test_updateField(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.get_job_index('M704')

        # Act
        
        jobs._update_field(job, jobs.CPC, '6666')
        expected = '6666'
        actual = jobs._dataList.iloc[3][jobs.CPC]

        # Assert
        self.assertEqual(actual, expected)

    def test__getFirstIndex(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = 3
        actual = jobs._get_first_index(jobs.Job, 'M704')

        # Assert
        self.assertEqual(actual, expected)

    def test_getStringDataListNone(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = "None"
        actual = jobs._get_string_datalist()[2]['Files In']

        # Assert
        self.assertEqual(actual, expected)

    def test_getStringDataListDateTime(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        jobs._dataList[2]['Files In'] = datetime.today()

        # Act
        expected = datetime.today().strftime('%m/%d/%Y')
        actual = jobs._get_string_datalist()[2]['Files In']

        # Assert
        self.assertEqual(actual, expected)

    def test_pu_getCPC(self):
        # Arrange
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = "2200"
        actual = paceUpdate._get_cpc(paceUpdate.DataDict[0])

        # Assert
        self.assertEqual(actual, expected)

    def test_pu_getPageCount(self):
        # Arrange
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = "24 Pages"
        actual = paceUpdate._get_page_count(paceUpdate.DataDict[1])

        # Assert
        self.assertEqual(actual, expected)

    def test_normalizeDates(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        normalDates = jobs._normalize_dates()

        # Act
        expected = datetime.strptime("02/03/2020", "%m/%d/%Y")
        actual = normalDates[1]["Date Setup"]

        # Assert
        self.assertEqual(actual, expected)

    def test_FindCommonColumnsPaceUD(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = 8
        commonColumns = jobs.find_common_columns(paceUpdate)
        actual = len(commonColumns)

        # Assert
        self.assertEqual(actual, expected)

    def test_FindCommonColumnsCustomerReport(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        customerReport = CustomerReport("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqCustomerReportSettingsFunc, moqCustomerReportFunc)

        # Act
        expected = 8
        commonColumns = customerReport.find_common_columns(jobs)
        actual = len(commonColumns)

        # Assert
        self.assertEqual(actual, expected)
    
    def test_get_consumable_list(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected=jobs.DataDict[0]['Job']
        actual=jobs.get_consumable_list(['Job'])[0]['Job']

        # Assert
        self.assertEqual(actual, expected)

    def test_ConsumeDataCR(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        customerReport = CustomerReport("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqCustomerReportSettingsFunc, moqCustomerReportFunc)
        
        # Act
        customerReport._consume_data(jobs, 'Job')
        expected = jobs._dataList[0]['Job']
        actual = customerReport._dataList[0]['Job']

        # Assert
        self.assertEqual(actual, expected)

    def test_ConsumeDataJL(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)
        paceUpdate._dataList = paceUpdate._get_string_datalist()
        
        # Act
        jobs._consume_data(paceUpdate, 'Description')
        expected = "M1800"
        actual = jobs._dataList[4]["Job"]

        # Assert
        self.assertEqual(actual, expected)

