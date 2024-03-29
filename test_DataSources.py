from datetime import datetime
import unittest
from Models.DataSources import CustomerReport, JobsList, PaceUpdate


def moqJobsListSettingsFunc(name: str):
    return {
        "File Name": "BVM_Jobs.xlsx",
        "Default Path": "/Users/micafunston/Projects/BVMTools/BVM_Jobs.xlsx",
        "Type": "Data List",
        "Job Field": "Job",
        "Tab": "Sheet",
        "Publication Field": "Description",
        "Publication Number Separate": False,
        "Date Columns": [
            "Files In",
            "Approved",
            "Scheduled Ship Date",
            "Date Setup",
        ],
        "True Dates": False,
        "Date Format": "%m/%d/%Y",
        "Columns Order": {
            "1": "Job",
            "2": "Description",
            "3": "Files In",
            "4": "Approved",
            "5": "Production Status",
            "6": "Scheduled Ship Date",
            "7": "Qty Ordered",
            "8": "CPC",
            "9": "Page Count",
            "10": "Date Setup",
            "11": "Samples",
            "12": "Deadline",
        },
        "Write Once Columns": [
            "Files In",
            "Approved",
            "Date Setup",
            "Added On",
            "Publication Month",
            "Exported to MIS",
        ],
    }


def moqJobsListFunc(path: str, tab: str):
    return [
        {
            "Job": "M511",
            "Description": "2656-Silver Valley-Academy Park Neighbou-Mar",
            "Files In": datetime.strptime("2/11/2020", "%m/%d/%Y"),
            "Approved": datetime.strptime("3/3/2020", "%m/%d/%Y"),
            "Production Status": "Closed",
            "Scheduled Ship Date": datetime.strptime("03/09/2020", "%m/%d/%Y"),
            "Qty Ordered": "2500",
            "CPC": "2089",
            "Page Count": "16 Pages",
            "Date Setup": datetime.strptime("02/03/2020", "%m/%d/%Y"),
            "Samples": "316",
            "Deadline": "10",
            "Publication Month": None,
        },
        {
            "Job": "M532",
            "Description": "3254-Neighbours of Kirkendall and Durand-Mar",
            "Files In": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Approved": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Production Status": "Open",
            "Scheduled Ship Date": datetime.strptime("03/05/2020", "%m/%d/%Y"),
            "Qty Ordered": "4500",
            "CPC": "4000",
            "Page Count": "24 Pages",
            "Date Setup": datetime.strptime("02/03/2020", "%m/%d/%Y"),
            "Samples": "216",
            "Deadline": "15",
            "Publication Month": None,
        },
        {
            "Job": "M999",
            "Description": "Bad Data1",
            "Files In": None,
            "Approved": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Production Status": "Open",
            "Scheduled Ship Date": datetime.strptime("02/26/2020", "%m/%d/%Y"),
            "Qty Ordered": "3500",
            "CPC": "4000",
            "Page Count": "24 Pages",
            "Date Setup": datetime.strptime("09/04/2050", "%m/%d/%Y"),
            "Samples": "216",
            "Deadline": "15",
            "Publication Month": None,
        },
        {
            "Job": "M704",
            "Description": "3254-Neighbours of Kirkendall and Durand-Apr",
            "Files In": datetime.strptime("03/28/2020", "%m/%d/%Y"),
            "Approved": None,
            "Production Status": "Open",
            "Scheduled Ship Date": datetime.strptime("04/05/2020", "%m/%d/%Y"),
            "Qty Ordered": "4500",
            "CPC": "4000",
            "Page Count": "24 Pages",
            "Date Setup": datetime.strptime("03/03/2020", "%m/%d/%Y"),
            "Samples": "216",
            "Deadline": "15",
            "Publication Month": None,
        },
        {
            "Job": "",
            "Description": "3535-Neighbours of Perth-Jul",
            "Files In": datetime.strptime("03/28/2020", "%m/%d/%Y"),
            "Approved": None,
            "Production Status": "Open",
            "Scheduled Ship Date": datetime.strptime("04/05/2020", "%m/%d/%Y"),
            "Qty Ordered": "4500",
            "CPC": "4000",
            "Page Count": "24 Pages",
            "Date Setup": datetime.strptime("03/03/2020", "%m/%d/%Y"),
            "Samples": "216",
            "Deadline": "15",
            "Publication Month": None,
        },
        {
            "Job": "M1532",
            "Description": "3299-Neighbours of Something or Other",
            "Files In": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Approved": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Production Status": "Open",
            "Scheduled Ship Date": datetime.strptime("03/05/2020", "%m/%d/%Y"),
            "Qty Ordered": "4500",
            "CPC": "4000",
            "Page Count": "24 Pages",
            "Date Setup": datetime.strptime("02/03/2020", "%m/%d/%Y"),
            "Samples": "216",
            "Deadline": "15",
            "Publication Month": None,
        },
        {
            "Job": "M1777",
            "Description": "3298-Neighbours of Nowhere",
            "Files In": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Approved": datetime.strptime("02/28/2020", "%m/%d/%Y"),
            "Production Status": "Open",
            "Scheduled Ship Date": datetime.strptime("03/05/2020", "%m/%d/%Y"),
            "Qty Ordered": "4500",
            "CPC": "4000",
            "Page Count": "24 Pages",
            "Date Setup": datetime.strptime("02/27/2020", "%m/%d/%Y"),
            "Samples": "216",
            "Deadline": "15",
            "Publication Month": None,
        },
    ]


def moqPaceUpdateSettingsFunc(name: str):
    return {
        "Type": "Data List",
        "True Dates": True,
        "Date Columns": ["Scheduled Ship Date", "Date Setup"],
        "Tab": "Report1",
        "Columns Order": {
            "1": "Job",
            "2": "Description",
            "3": "Production Status",
            "4": "Scheduled Ship Date",
            "5": "Qty Ordered",
            "6": "Production Notes",
            "7": "Item Template",
            "8": "Additional Description",
            "9": "Date Setup",
        },
        "Date Format": "%m/%d/%Y",
        "Page Count Strings": {
            "16 page": "16 Pages",
            "20 page": "20 Pages",
            "24 page": "24 Pages",
            "28 page": "28 Pages",
            "32 page": "32 Pages",
            "36 page": "36 Pages",
            "40 page": "40 Pages",
            "Write Once Columns": [],
        },
    }


def moqPaceUpdateFunc(path: str, tab: str):
    return [
        {
            "Job": 'M1998',
            "Description": "2695-Neighbours of Whitemud Creek - Aug",
            "Production Status": "In Production",
            "Scheduled Ship Date": datetime.strptime("07-15-2020", "%m-%d-%Y"),
            "Qty Ordered": 2500,
            "Production Notes": "PW Count = 2200",
            "Item Template": "BVM 16 Page",
            "Additional Description": "2500 16 page self cover Flat size 16.75 x 10.875, fold & stitch to 8.375 x 10.875 4 process / same  with bleeds Plastic strap band (cross) in 50's Carton pack with 3 strips of tape on the bottom Deliver to DLI",
            "Date Setup": datetime.strptime("06-30-2020", "%m-%d-%Y"),
        },
        {
            "Job": 'M532',
            "Description": "3254-Neighbours of Kirkendall and Durand-Mar",
            "Production Status": "In Production",
            "Scheduled Ship Date": datetime.strptime("07-15-2020", "%m-%d-%Y"),
            "Qty Ordered": 4500,
            "Production Notes": "PW Count = 4000",
            "Item Template": "BVM 16 Page",
            "Additional Description": "4500 24 page self cover Flat size 16.75 x 10.875, fold & stitch to 8.375 x 10.875 4 process / same  with bleeds Plastic strap band (cross) in 50's Carton pack with 3 strips of tape on the bottom Deliver to DLI",
            "Date Setup": datetime.strptime("07-30-2020", "%m-%d-%Y"),
        },
        {
            "Job": 'M1800',
            "Description": "3535-Neighbours of Perth-Jul",
            "Production Status": "In Production",
            "Scheduled Ship Date": datetime.strptime("08-15-2020", "%m-%d-%Y"),
            "Qty Ordered": 4500,
            "Production Notes": "PW Count = 4000",
            "Item Template": "BVM 16 Page",
            "Additional Description": "4500 24 page self cover Flat size 16.75 x 10.875, fold & stitch to 8.375 x 10.875 4 process / same  with bleeds Plastic strap band (cross) in 50's Carton pack with 3 strips of tape on the bottom Deliver to DLI",
            "Date Setup": datetime.strptime("08-30-2020", "%m-%d-%Y"),
        },
    ]


def moqCustomerReportSettingsFunc(name: str):
    return {
        "Tab": "Sheet",
        "Type": "Report",
        "Last Column": "H",
        "True Dates": True,
        "Job Field": "Job",
        "Publication Field": "Description",
        "Publication Number Separate": False,
        "Date Columns": ["Files In", "Approved", "Scheduled Ship Date"],
        "Columns Order": {
            "1": "Job",
            "2": "Deadline",
            "3": "Description",
            "4": "Files In",
            "5": "Approved",
            "6": "Production Status",
            "7": "Scheduled Ship Date",
            "8": "Qty Ordered",
        },
        "Write Once Columns": [],
    }

def moqCustomerReportFunc(path: str, tab: str):
    return [{}]

class TestDataSources(unittest.TestCase):

    def test_FindFirstRow(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)

        # Act
        actual = jobs._find_first_row('Job', 'M511')
        expected = jobs._data_list[0]

        # Assert
        self.assertDictEqual(actual, expected)

    def test_FindAllRows(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')
        # Act
        actual = jobs._find_all_rows('Job', 'M532')
        expected = jobs._data_list[1]

        # Assert
        self.assertEqual(actual[0]['Job'], expected['Job'])

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

    def test_getRow(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)        

        # Act
        expected = jobs._data_list[1]
        actual = jobs._getRow(1)

        # Assert
        self.assertDictEqual(expected, actual)

    def test_get_cell(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        moqjobs = moqJobsListFunc('', '')

        # Act
        expected = moqjobs[1]['Description']
        actual = jobs._get_cell(1, 'Description')

        # Assert
        self.assertEqual(expected, actual)

    def test_FindInAllRows(self):

        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)        

        # Act
        expected = []
        actual = jobs._find_in_all_rows('Description', '3254')
        expected.append(jobs._data_list[1])
        expected.append(jobs._data_list[3])     

        # Assert
        self.assertListEqual(expected, actual)    

    def test_updateField(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.get_job('M704')

        # Act
        jobs._update_field(job, jobs.CPC, '6666')
        expected = '6666'
        actual = jobs._data_list[3][jobs.CPC]

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
        expected = None
        actual = jobs._get_string_data_list()[2]['Files In']

        # Assert
        self.assertEqual(actual, expected)

    def test_getStringDataListDateTime(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        jobs._data_list[2]['Files In'] = datetime.today()

        # Act
        expected = datetime.today().strftime('%m/%d/%Y')
        actual = jobs._get_string_data_list()[2]['Files In']

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
        expected=jobs._data_list[0]['Job']
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
        customerReport._merge_data(jobs, ['Job'], customerReport._hit_add_missing, customerReport._miss_add_row)
        expected = jobs._data_list[0]['Job']
        actual = customerReport._data_list[0]['Job']

        # Assert
        self.assertEqual(actual, expected)

    def test_ConsumeDataJL(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)
        paceUpdate._data_list = paceUpdate._get_string_data_list()
        
        # Act
        jobs._merge_data(paceUpdate, ['Description'], jobs._hit_replace,jobs._miss_add_row)
        expected = "M1800"
        actual = jobs._data_list[4]["Job"]

        # Assert
        self.assertEqual(actual, expected)

class TestJobsList(unittest.TestCase):
    def test_GetMostRecentPub(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
               

        # Act
        expected = jobs._data_list[3]
        actual = jobs.get_most_recent_pub('3254')

        # Assert
        self.assertDictEqual(expected, actual)

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
        

        # Act
        actual = jobs.get_job('M704')
        expected = jobs._data_list[3]

        # Assert
        self.assertDictEqual(actual, expected)

    def test_SetUploadDate(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.get_job('M704')
        Today = datetime.today()

        # Act
        jobs.set_upload_date('M704', Today)
        actual = job['Files In']
        expected = datetime.today().strftime('%m/%d/%Y')

        # Assert
        self.assertEqual(actual, expected)

    def test_SetApprovedDate(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        job = jobs.get_job('M704')
        Today = datetime.today()

        # Act
        jobs.set_approved_date('M704', Today)
        actual = job['Approved']
        expected = datetime.today().strftime('%m/%d/%Y')

        # Assert
        self.assertEqual(actual, expected)

    def test_set_publication_month_descrip(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        
        # Act
        jobs.set_publication_month()
        actual = jobs._data_list[0]["Publication Month"]
        expected = datetime.strptime("03/01/2020","%m/%d/%Y")

        # Assert
        self.assertEqual(actual, expected)

    def test_set_publication_month_setup(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        
        # Act
        jobs.set_publication_month()
        actual = jobs._data_list[5]["Publication Month"]
        expected = datetime.strptime("03/01/2020","%m/%d/%Y")

        # Assert
        self.assertEqual(actual, expected)

    def test_set_publication_month_setup_eom(self):
        # Arrange
        jobs = JobsList("BVM_Jobs.xlsx",
                        moqJobsListSettingsFunc, moqJobsListFunc)
        
        # Act
        jobs.set_publication_month()
        actual = jobs._data_list[6]["Publication Month"]
        expected = datetime.strptime("04/01/2020","%m/%d/%Y")

        # Assert
        self.assertEqual(actual, expected)


class TestPaceUpdate(unittest.TestCase):
    def test_pu_getCPC(self):
        # Arrange
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = "2200"
        actual = paceUpdate._get_cpc(paceUpdate._data_list[0])

        # Assert
        self.assertEqual(actual, expected)

    def test_pu_getPageCount(self):
        # Arrange
        paceUpdate = PaceUpdate("BVM+Job+Grouped+For+Tracking+Report.xls",
                                moqPaceUpdateSettingsFunc, moqPaceUpdateFunc)

        # Act
        expected = "24 Pages"
        actual = paceUpdate._get_page_count(paceUpdate._data_list[1])

        # Assert
        self.assertEqual(actual, expected)