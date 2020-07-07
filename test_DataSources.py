from datetime import datetime
import unittest
from Models.DataSources import CustomerReport, JobsList, PaceUpdate


def moqJobsListSettingsFunc(name: str):
    moqJobsListSettings = {"File Name": "BVM_Jobs.xlsx", "Default Path": "/Users/micafunston/Projects/BVMTools/BVM_Jobs.xlsx", "Type": "Data List", "Job Field": "Job", "Tab": "Sheet", "Publication Field": "Description", "Publication Number Separate": False, "Date Columns": [
        "Files In", "Approved", "Scheduled Ship Date", "Date Setup"], "True Dates": False, "Date Format": "%m/%d/%Y", "Columns Order": {"1": "Job", "2": "Description", "3": "Files In", "4": "Approved", "5": "Production Status", "6": "Scheduled Ship Date", "7": "Qty Ordered", "8": "CPC", "9": "Page Count", "10": "Date Setup", "11": "Samples", "12": "Deadline"}}
    return moqJobsListSettings


def moqJobsListFunc(path: str, tab: str):
    moqJobsList = [{"Job": "M511", "Description": "2656-Silver Valley-Academy Park Neighbou-Mar", "Files In": "2/11/2020", "Approved": "3/3/2020", "Production Status": "Closed",
                    "Scheduled Ship Date": "03/09/2020", "Qty Ordered": "2500", "CPC": "2089", "Page Count": "16 Pages", "Date Setup": "02/03/2020", "Samples": "316", "Deadline": "10"},
                   {"Job": "M532", "Description": "3254-Neighbours of Kirkendall and Durand-Mar", "Files In": "02/28/2020", "Approved": "02/28/2020", "Production Status": "Open",
                    "Scheduled Ship Date": "03/05/2020", "Qty Ordered": "4500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": "02/03/2020", "Samples": "216", "Deadline": "15"},
                   {"Job": "M999", "Description": "Bad Data1", "Files In": None, "Approved": "02/28/2020", "Production Status": "Open",
                    "Scheduled Ship Date": "02/26/2020", "Qty Ordered": "3500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": "09/04/2050", "Samples": "216", "Deadline": "15"},
                   {"Job": "M704", "Description": "3254-Neighbours of Kirkendall and Durand-Apr", "Files In": "03/28/2020", "Approved": None, "Production Status": "Open",
                    "Scheduled Ship Date": "04/05/2020", "Qty Ordered": "4500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": "03/03/2020", "Samples": "216", "Deadline": "15"},
                    {"Job": "", "Description": "3535-Neighbours of Perth-Jul", "Files In": "03/28/2020", "Approved": None, "Production Status": "Open",
                    "Scheduled Ship Date": "04/05/2020", "Qty Ordered": "4500", "CPC": "4000", "Page Count": "24 Pages", "Date Setup": "03/03/2020", "Samples": "216", "Deadline": "15"}]
    return moqJobsList


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
    return moqPaceUpdate


def moqCustomerReportSettingsFunc(name: str):
    moqSettings = {"Tab": "Sheet", "Type": "Report", "Last Column": "H", "True Dates": True, "Job Field": "Job", "Publication Field": "Description", "Publication Number Separate": False,
                                       "Columns Order": {"1": "Job", "2": "Deadline", "3": "Description", "4": "Files In", "5": "Approved", "6": "Production Status", "7": "Scheduled Ship Date", "8": "Qty Ordered"}}
    return moqSettings

def moqCustomerReportFunc(path: str, tab: str):
    moqCustomerReport = [{}]
    return moqCustomerReport

class TestDataSources(unittest.TestCase):

    def test_FindFirstRow(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')
        # Act
        actual = jobs._findFirstRow('Job', 'M511')
        expected = moqjobs[0]

        # Assert
        self.assertDictEqual(actual, expected)

    def test_FindAllRows(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')
        # Act
        actual = jobs._findAllRows('Job', 'M532')
        expected = moqjobs[1]

        # Assert
        self.assertEqual(actual[0]['Job'], expected['Job'])

    def test_returnSavableList(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.returnSavableList()

        # Assert
        self.assertIsNotNone(actual)

    def test_columnIsDateTrue(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.columnIsDate("Files In")

        # Assert
        self.assertTrue(actual)

    def test_columnIsDateFalse(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.columnIsDate("Production Status")

        # Assert
        self.assertFalse(actual)

    def test_getTrueDate(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = datetime.strptime("2/11/2020", "%m/%d/%Y")
        actual = jobs.getTrueDate('Files In', 0)

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

    def test_getRow(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = moqjobs[1]
        actual = jobs._getRow(1)

        # Assert
        self.assertDictEqual(expected, actual)

    def test_getCell(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = moqjobs[1]['Description']
        actual = jobs._getCell(1, 'Description')

        # Assert
        self.assertEqual(expected, actual)

    def test_FindInAllRows(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = list()
        actual = jobs._findInAllRows('Description', '3254')
        expected.append(moqjobs[1])
        expected.append(moqjobs[3])
        

        # Assert
        self.assertListEqual(expected, actual)

    def test_GetMostRecentPub(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = moqjobs[3]
        actual = jobs.GetMostRecentPub('3254')

        # Assert
        self.assertDictEqual(expected, actual)

    def test_jobIsApprovedTrue(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.jobIsApproved("M532")

        # Assert
        self.assertTrue(actual)

    def test_jobIsApprovedFalse(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.jobIsApproved("M704")

        # Assert
        self.assertFalse(actual)

    def test_jobIsApprovedMissing(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.jobIsApproved("M1704")

        # Assert
        self.assertFalse(actual)

    def test_jobIsUploadedTrue(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.jobIsUploaded("M532")

        # Assert
        self.assertTrue(actual)

    def test_jobIsUploadedFalse(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.jobIsUploaded("M999")

        # Assert
        self.assertFalse(actual)

    def test_jobIsUploadedMissing(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs.jobIsUploaded("M1704")

        # Assert
        self.assertFalse(actual)

    def test_getJob(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        actual = jobs.GetJob('M704')
        expected = moqjobs[3]

        # Assert
        self.assertDictEqual(actual, expected)

    def test_SetUploadDate(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.GetJob('M704')
        Today = datetime.today()

        # Act
        jobs.SetUploadDate('M704', Today)
        actual = job['Files In']
        expected = datetime.today().strftime('%m/%d/%Y')

        # Assert
        self.assertEqual(actual, expected)

    def test_SetApprovedDate(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.GetJob('M704')
        Today = datetime.today()

        # Act
        jobs.SetApprovedDate('M704', Today)
        actual = job['Approved']
        expected = datetime.today().strftime('%m/%d/%Y')

        # Assert
        self.assertEqual(actual, expected)

    def test_updateField(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.GetJob('M704')

        # Act
        jobs._updateField(job, jobs.CPC, '6666')
        expected = '6666'
        actual = jobs._dataList[3][jobs.CPC]

        # Assert
        self.assertEqual(actual, expected)

    def test__getFirstIndex(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = 3
        actual = jobs._getFirstIndex(jobs.Job, 'M704')

        # Assert
        self.assertEqual(actual, expected)

    def test_getStringDataListNone(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected = "None"
        actual = jobs._getStringDatalist()[2]['Files In']

        # Assert
        self.assertEqual(actual, expected)

    def test_getStringDataListDateTime(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        jobs._dataList[2]['Files In'] = datetime.today()

        # Act
        expected = datetime.today().strftime('%m/%d/%Y')
        actual = jobs._getStringDatalist()[2]['Files In']

        # Assert
        self.assertEqual(actual, expected)

    def test_pu_getCPC(self):
        # Arrange
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = "2200"
        actual = paceUpdate._getCPC(paceUpdate._dataList[0])

        # Assert
        self.assertEqual(actual, expected)

    def test_pu_getPageCount(self):
        # Arrange
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = "24 Pages"
        actual = paceUpdate._getPageCount(paceUpdate._dataList[1])

        # Assert
        self.assertEqual(actual, expected)

    def test_normalizeDates(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        normalDates = jobs._normalizeDates()

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
        commonColumns = jobs.FindCommonColumns(paceUpdate)
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
        commonColumns = customerReport.FindCommonColumns(jobs)
        actual = len(commonColumns)

        # Assert
        self.assertEqual(actual, expected)
    
    def test_GetConsumableList(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        expected=jobs._dataList[0]['Job']
        actual=jobs.getConsumableList(['Job'])[0]['Job']

        # Assert
        self.assertEqual(actual, expected)

    def test_ConsumeDataCR(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        customerReport = CustomerReport("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqCustomerReportSettingsFunc, moqCustomerReportFunc)
        
        # Act
        customerReport._consumeData(jobs, 'Job')
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
        paceUpdate._dataList = paceUpdate._getStringDatalist()
        
        # Act
        jobs._consumeData(paceUpdate, 'Description')
        expected = "M1800"
        actual = jobs._dataList[4]["Job"]

        # Assert
        self.assertEqual(actual, expected)

