import unittest
import Models.DataSources
import DataManager as dm

class TestObjectsInitialization(unittest.TestCase):

    def test_jobs_list(self):
        jobs_list = dm.get_jobs_list()
        self.assertIsNotNone(jobs_list)
    
    def test_mis_update_list(self):
        mis_update_list = dm.get_mis_update_list()
        self.assertIsNotNone(mis_update_list)
    
    def test_customer_report_list(self):
        customer_report_list = dm.get_customer_report_list()
        self.assertIsNotNone(customer_report_list)

    def test_contacts_list(self):
        contacts_list = dm.get_contacts_list()
        self.assertIsNotNone(contacts_list)

    def test_samples_list(self):
        samples_list = dm.get_samples_list("Test_Data/1st deadline_Sample Magazine Orders_July 2020_Canada.xlsx")
        self.assertIsNotNone(samples_list)

    def test_designer_copies_list(self):
        designer_copies_list = dm.get_designer_copies_list("Test_Data/20th deadline_Sample Magazine Order_June 2020_Canada.xlsx")
        self.assertIsNotNone(designer_copies_list)

    def test_shipments_list(self):
        shipments_list = dm.get_shipments_list()
        self.assertIsNotNone(shipments_list)

    def test_invoice(self):
        invoice = dm.get_mis_update_list()
        self.assertIsNotNone(invoice)

    def test_samples_dc_merge(self):
        sample_list = dm.get_samples_list("Test_Data/1st deadline_Sample Magazine Orders_July 2020_Canada.xlsx")
        designer_copies_list = dm.get_designer_copies_list("Test_Data/20th deadline_Sample Magazine Order_June 2020_Canada.xlsx")        
        expected = len(sample_list._data_list)+len(designer_copies_list._data_list)
        sample_list.nd_merge(designer_copies_list)
        
        actual = len(sample_list._data_list)

        self.assertEqual(actual, expected)

    def test_deliveries_merge(self):
        sample_list = dm.get_samples_list("Test_Data/1st deadline_Sample Magazine Orders_July 2020_Canada.xlsx")
        designer_copies_list = dm.get_designer_copies_list("Test_Data/20th deadline_Sample Magazine Order_June 2020_Canada.xlsx")
        shipments_list = dm.get_shipments_list()

        sample_list.nd_merge(designer_copies_list)
        shipments_list.nd_merge(sample_list)

        self.assertEqual(len(sample_list._data_list), len(shipments_list._data_list))
