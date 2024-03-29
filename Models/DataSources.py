from logging import log
import math
from typing import Dict, List, Callable
import json
from datetime import date, datetime
import calendar
import copy
import pandas as pd
from Libraries.NameParse import NameParse
from Libraries.ExcelLibs import WriteData
import logging

logging.basicConfig(filename='log.txt',level=logging.DEBUG, format='%(asctime)s %(message)s')

class DataSource:
    """Base type for all data sources collected from Excel and comma delimited files.
    """

    def __init__(self, name: str, path: str, settingsFunc, dictFunc):
        self.name: str = name
        self.settings: dict = settingsFunc(self.name)
        if path == "":
            self.path: str = self.settings["Default Path"]
        else:
            self.path: str = path
        self.tab: str = self.settings["Tab"]
        self._data_list: List[dict] = dictFunc(self.path, self.tab)

    def _get_data_frame(self):
        return pd.DataFrame(self._data_list)

    Data_Frame = property(_get_data_frame)

    def _ready_to_export(self, row):
        return not any(
            row[column] is None or row[column] == "" or row["Exported"] != None
            for column in self.settings["Export On"]
        )


    def write_to_file(self, path: str, sheet: str, prep_data_funct, write_func):
        self.populate_static()
        prep_data_funct()     
        write_func(path, sheet, self.Data_Frame, self.ExportColumns)

    def prep_data_to_string(self):
        if self.settings["True Dates"] == False:
            self._data_list = self._get_string_data_list()
    
    def prep_data_add_columns(self):
        for row in self._data_list:
            for column in self.settings["Columns Order"].values():
                if column not in row:
                    row[column] = None

    def prep_data_none(self):
        return
    
    def add_one_month(self, orig_date):
        # advance year and month by one month
        new_year = orig_date.year
        new_month = orig_date.month + 1
        # note: in datetime.date, months go from 1 to 12
        if new_month > 12:
            new_year += 1
            new_month -= 12

        last_day_of_month = calendar.monthrange(new_year, new_month)[1]
        new_day = min(orig_date.day, last_day_of_month)

        return orig_date.replace(year=new_year, month=new_month, day=new_day)

    def add_months_from_now(self, number_of_months):
        # advance year and month by number_of_months
        orig_date=datetime.now()
        new_year = orig_date.year
        new_month = orig_date.month + number_of_months
        # note: in datetime.date, months go from 1 to 12
        if new_month > 12:
            new_year += 1
            new_month -= 12

        last_day_of_month = calendar.monthrange(new_year, new_month)[1]
        new_day = min(orig_date.day, last_day_of_month)

        return orig_date.replace(year=new_year, month=new_month, day=new_day)

    def _find_first_row(self, column: str, search_term: str) -> dict:
        """
        Finds the first row containing searchterm.

        Args:
            self (undefined):
            column (str): The column header to search under
            search_term(str):

        Returns:
            dict: Complete row. Empty if nothing found.

        """
        empty: Dict[str, str] = {'None': ''}
        for row in self._data_list:
            if row[column] == search_term:
                return row
        return empty

    def _get_column_names(self) -> list:
        """
        Returns a list of all columns used in the first element in _data_list

        Args:
            self (undefined):

        Returns:
            list of columns[str]

        """
        try:
            return list(self._data_list[0].keys())
        except:
            return list(self.settings["Columns Order"].values())

    def _get_export_columns(self):
        return [
            self.settings["Columns Order"][str(i)]
            for i in range(1, len(self.settings["Columns Order"]) + 1)
        ]

    Columns = property(_get_column_names)
    ExportColumns = property(_get_export_columns)

    def _normalize_dates(self) -> List[Dict]:
        """
        Change all dates in string format to proper DateTime dates

        Args:
            self (undefined):

        Returns:
            List[Dict]: A deep copy of current _data_list with proper dates

        """
        dateDataList = copy.deepcopy(self._data_list)

        for row in dateDataList:
            for column in self.settings["Date Columns"]:
                if row[column] != None and type(row[column]) == str:
                    row[column] = datetime.strptime(
                        row[column], self.settings['Date Format'])
        return dateDataList

    def _get_string_data_list(self) -> List[Dict[str, str]]:
        """
        Change all non string values to string. Datetimes are converted using the objects Date Format

        Args:
            self (undefined):

        Returns:
            List[Dict[str, str]]: A deep copy of the _data_list with all values as strings

        """
        stringDataList = copy.deepcopy(self._data_list)
        for row in stringDataList:
            for x in row:
                if type(row[x]) != datetime:
                    if type(row[x]) == float:
                        row[x] = int(row[x])
                    if row[x] != None:
                        row[x] = str(row[x])
                else:
                    row[x] = row[x].strftime(self.settings['Date Format'])
        return stringDataList

    def _find_all_rows(self, column: str, search_term: str) -> List[Dict]:
        """
        Find all rows which have a column equal to search_term

        Args:
            self (undefined):
            column (str): The column header to search in (ie Job)
            search_term(str):

        Returns:
            List[Dict]: List of all rows containing the search term

        """
        found_list: List[Dict] = list()
        for row in self._data_list:
            if row[column] == search_term:
                found_list.append(row)
        return found_list

    def _find_in_all_rows(self, column: str, search_term: str) -> List[Dict]:
        """[Find all rows that have a column containing (in) search_term]

        Args:
            column (str): Column header to search
            search_term (str): string to search for

        Returns:
            List[Dict]: List of rows
        """
        found_list: List[Dict] = list()
        for row in self._data_list:
            if search_term in row[column]:
                found_list.append(row)
        return found_list

    def _getRow(self, index: int) -> dict:
        """Get a row in _data_list by index

        Args:
            index (int): 0 based index to return

        Returns:
            dict: Row
        """
        return self._data_list[index]

    def _get_cell(self, index: int, column: str):
        """Get a single cell 

        Args:
            index (int): 0 based index of row
            column (str): Column header

        Returns:
            [type]: Data contained within the cell
        """
        return self._getRow(index)[column]

    def get_consumable_list(self, columns: list) -> List:
        """Get a list of _data_list conatining only the given columns

        Args:
            columns (list): The columns to include in the returned list

        Returns:
            List: List of columns
        """
        consumableList = []
        for row in self._data_list:
            entries = {}
            for column in columns:
                try:
                    entries[column] = row[column]
                except:
                    print("Key error "+ column)

            consumableList.append(entries)
        return consumableList

    def return_savable_list(self) -> List:
        """Returns a copy of the _data_list as a list of lists using the order stored in Columns Order of settings

        Returns:
            List: List of lists
        """
        savableList: List[List] = list()
        headers: List[str] = list()
        columnsOrder: Dict[str, str] = self.settings["Columns Order"]
        for row in self._data_list:
            rowList = []
            for columnNumber in range(1, len(columnsOrder)+1):
                columnName = columnsOrder[str(columnNumber)]
                rowList.append(row[columnName])
            savableList.append(rowList)

        for columnNumber in range(1, len(columnsOrder)+1):
            headers.append(columnsOrder[str(columnNumber)])
        savableList.insert(0, headers)
        return savableList

    def add_row(self, row):
        if len(self._data_list) > 1:
            self._data_list.append(row)
        else:
            self._data_list[0]=row

    def _add_column(self, name: str):
        for row in self._data_list:
            row[name] = None
    
    def _merge_data(self, data_source, id_columns: List, hit_funct: Callable, miss_funct: Callable):
        """Merge and/or add compatible data from another DataSource's _data_list. 
        If IDColunn exists in the source's _data_list its' columns are overwritten with matching ones from the DataSource it's consuming.

        Args:
            dataSource ([type]): DataSource to consume
            IdColumn (str): Column to match between self, and dataSource
        """
        self._create_common_column_names()
        data_source._create_common_column_names()
        commonColumns = self.find_common_columns(data_source)
        listToConsume = data_source.get_consumable_list(commonColumns)
        for newRow in listToConsume:
            found = False
            # if len(self._data_list) == 0:
            #     empty = dict()
            #     self._data_list.append(empty)

            if len(self._data_list[0]) == 0:
                miss_funct(newRow)

            for oldRow in self._data_list:
                data_match = True
                for id in id_columns:
                    if newRow[id] == oldRow[id] and data_match:
                        data_match = True
                    else:
                        data_match = False
                if data_match:
                    found = True
                    hit_funct(commonColumns, newRow, oldRow)

            if not found:
                miss_funct(newRow)


    def _hit_replace(self, columns, new_row, old_row):
        for column in columns:
            if column not in old_row:
                old_row[column] = new_row[column]
            if (
                old_row[column] is None
                or column not in self.settings["Write Once Columns"]
            ) and old_row[column] != new_row[column]:
                old_row[column] = new_row[column]
                logging.info("Replacing "+str(old_row[column])+" with "+str(new_row[column]))

    def _hit_add_missing(self, columns, new_row, old_row):
        for column in columns:
            if column not in old_row:
                old_row[column] = new_row[column]
                logging.info("Adding "+str(new_row[column])+" to "+column)
            if old_row[column] is None:
                old_row[column] = new_row[column]
                logging.info("Adding "+str(new_row[column])+" to "+column)

    def _miss_add_row(self, row: Dict):
        if len(self._data_list[0]) == 0:
            self._data_list[0] = row
        else:
            self._data_list.append(row)

    def _miss_add_row_record_addition(self, row: Dict):
        row["Added On"] = datetime.now()
        self._data_list.append(row)

    def _miss_not_add_row(self, row: Dict):
        row.clear()

    def populate_static(self):
        if "Static Columns" in self.settings:
            for row in self._data_list:
                for static_column in self.settings["Static Columns"]:
                    row[static_column] = self.settings["Static Columns"][static_column]

    def _create_common_column_names(self):
        if "Common Data Columns" in self.settings:
            for row in self._data_list:
                for common_column_name in self.settings["Common Data Columns"]:
                    for column in row.copy():
                        if column == common_column_name:
                            common_name = self.settings["Common Data Columns"][common_column_name]
                            row[common_name] = row[column]

    def nd_merge(self, data_source):
        self.populate_static()
        self._create_common_column_names()        
        data_source.populate_static()
        data_source._create_common_column_names()        
        # self._create_common_column_names()
        commonColumns = self.find_common_columns(data_source)
        list_to_merge = data_source.get_consumable_list(commonColumns)
        if len(self._data_list) > 1:
            self._data_list = self._data_list + list_to_merge
        else:
            self._data_list = list_to_merge

    def export(self, data_source) -> bool:
        exported=False
        if "Export On" in self.settings:
            self.populate_static()
            self._create_common_column_names()
            data_source.populate_static()
            data_source._create_common_column_names()
            # self._create_common_column_names()
            commonColumns = self.find_common_columns(data_source)
            for row in self._data_list:
                new_row = {}
                if self._ready_to_export(row):
                    for column in commonColumns:
                        new_row[column]=row[column]
                    row["Exported"]=datetime.now()

                    data_source.add_row(new_row)
                    exported=True
        return exported
            


    def column_is_date(self, columnHeader: str) -> bool:
        """Checks if a column contains dates or not as described by the DataSource's settings

        Args:
            columnHeader (str): 

        Returns:
            bool: Return true if found in 'Date Columns', false otherwise.
        """
        return columnHeader in self.settings['Date Columns']

    def get_true_date(self, columnHeader: str, index: int) -> datetime:
        """Returns the value at a given row, and column as a proper Python DateTime.

        Args:
            columnHeader (str): Column header under which the date can be found. 
            Must be listed under "Date Columns" in the object's settings.
            index (int): Row index of the date

        Returns:
            [datetime]: If the location has a string it is converted to datetime. 
            If it is already a datetime it is returned as is.
        """
        value = self._data_list[index][columnHeader]
        if type(value) != datetime:
            value = datetime.strptime(value, self.settings['Date Format'])
        return value

    def _set_date(self, search_column: str, search_term: str, date_column: str, date_to_set: datetime) -> None:
        """Finds a row in which [search_column] contains [search_term]. Sets [date_column] to [date_to_set]

        Args:
            search_column (str): Column to search in
            search_term (str): Value to search for
            date_column (str): Column that will have date assigned
            date_to_set (datetime): Date to assign
        """
        found = self._find_first_row(search_column, search_term)
        if date_column in self.settings['Date Columns']:
            found[date_column] = date_to_set.strftime(
                self.settings['Date Format'])

    def len(self) -> int:
        """Returns the current length of _data_list

        Returns:
            int: Current length of _data_list
        """
        return len(self._data_list)

    def _cell_to_date(self, cell) -> datetime:
        """Converts a cell to a datetime. It must contain a string. Uses the object's "Date Format" setting.

        Args:
            cell (str): String to convert to datetime

        Returns:
            datetime:
        """
        if type(cell) == datetime:
            return cell

        return datetime.strptime(cell, self.settings['Date Format'])

    def _update_field(self, row: dict, column_name: str, value: str) -> None:
        """Updates [column_name] in the supplied row with [value]

        Args:
            row (dict): Supplied row
            column_name (str): Name of the column to be updated
            value (str): Value to insert
        """
        row[column_name] = value

    def _get_first_index(self, column_name: str, search_term: str) -> int:
        """Searches the _data_list and returns the index of the first row in which column[column_name] matches search_term

        Args:
            column_name (str): Name of the column to search
            search_term (str): Value to search for

        Returns:
            int: Index of the found row
        """
        for i in range(len(self._data_list)):
            if self._data_list[i][column_name] == search_term:
                return i
        return int()

    def find_common_columns(self, ds2) -> List[str]:
        """Returns a list of all common columns between the current object, and a supplied DataSource

        Args:
            ds2 ([type]): Any DataSource

        Returns:
            list[str]: List of column names
        """
        columnsSet = set(self.Columns)
        intersection = columnsSet.intersection(ds2.Columns)
        return list(intersection)

    def _split_column(self, original_column_name: str, new_column_names: List[str], func):
        for row in self._data_list:
            new_column_values = func(row[original_column_name])
            for i, new_column_value in enumerate(new_column_values):
                row[new_column_names[i]] = new_column_value
    
    def _check_data_complete(self, columns_list: List[str], on_complete_func: Callable):
        """Checks to see which rows are 'Complete' based on a list of column names (that each column contains data)

        Args:
            columns_list (List): A list of column names
            on_complete_func (Function): Function to run if the row is complete

        Returns:
            [type]: A list of rows
        """

        for record in self._data_list:
            complete = all(record[column] is not None for column in columns_list)
            if complete:
                on_complete_func(record)



class JobsList(DataSource):
    """List of Jobs, including information about when the job was uploaded, approved, created, etc.

    Args:
        DataSource ([type]): [description]
    """

    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Jobs List"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self.Job: str = "Job"
        self.Description: str = "Description"
        self.FilesIn: str = "Files In"
        self.Approved: str = "Approved"
        self.ProductionStatus: str = "Production Status"
        self.ScheduledShipDate: str = "Scheduled Ship Date"
        self.QtyOrdered: str = "Qty Ordered"
        self.CPC: str = "CPC"
        self.PageCount: str = "Page Count"
        self.DateSetup: str = "Date Setup"
        self.Samples: str = "Samples"
        self.Deadline: str = "Deadline"
        self.AddedOn: str = "Added On"
        self.PublicationNumber: str = "Publication Number"
        self.DesignerEmail: str = "Designer Email"
        self.ShippingAdded: str = "Shipping Added"
        self.PageCountMatchedEstimate: str = "Page Count Matched Estimate"
        self.PublicationMonth = "Publication Month"
        self.ExportedToMIS = "Exported to MIS"
        self._data_list = self._normalize_dates()
        self.set_publication_month()
        try:
            self._set_publication_numbers()
        except:
            print("Unable to set all publication numbers")



    def get_most_recent_pub(self, pub_number: str) -> Dict:
        """Find the most recent publication.

        Args:
            pub_number (str): Publication number as a string

        Returns:
            Dict: The row containing the most recent publication
        """
        candidates = self._find_in_all_rows(self.Description, pub_number)
        found = {}
        if len(candidates) > 0:
            found = candidates[0]
            for candidate in candidates:
                if self._cell_to_date(candidate[self.DateSetup]) > self._cell_to_date(found[self.DateSetup]):
                    found = candidate
        return found

    def get_job(self, job: str) -> dict:
        """Return the row containing [job]

        Args:
            job (str): Job number as a string

        Returns:
            dict: Row containing the found job
        """
        return self._find_first_row(self.Job, job)

    def job_is_approved(self, job: str) -> bool:
        """Return true if a job has been approved, false if not.

        Args:
            job (str): Job number as a string

        Returns:
            bool: True if approved, false if not.
        """
        found = self.get_job(job)
        return len(found.keys()) > 1 and found[self.Approved] != None

    def job_is_uploaded(self, job: str) -> bool:
        """Return true if a job has been uploaded, false if not.

        Args:
            job (str): Job number as a string.

        Returns:
            bool: True if uploaded, false it not.
        """
        found = self.get_job(job)
        return len(found.keys()) > 1 and found[self.FilesIn] != None

    def set_upload_date(self, job: str, date: datetime):
        """Set the upload date for a given job number

        Args:
            job (str): Job number
            date (datetime): Date to set
        """
        self._set_date(self.Job, job, self.FilesIn, date)

    def set_approved_date(self, job: str, date: datetime):
        """Set the approval date for a given job number

        Args:
            job (str): Job number as a string
            date (datetime): Date to set.
        """
        self._set_date(self.Job, job, self.Approved, date)

    def set_publication_month(self):
        month_string = str()
        day_string = "01"
        for row in self._data_list:
            month_string = ""
            if self.PublicationMonth not in row:
                row[self.PublicationMonth]=None
            if row[self.PublicationMonth] is None:
                if (
                    row[self.Description] != None
                    and len(row[self.Description].split("-")[-1]) < 5
                ):
                    month_string = row[self.Description].split("-")[-1]
                    #print("Used the Description "+row[self.Description])
                if month_string == "" and row[self.DateSetup] != None:
                    date_to_set: datetime = row[self.DateSetup]
                    date_to_set = self.add_one_month(date_to_set)
                    if date_to_set.day > 25:
                        date_to_set = self.add_one_month(date_to_set)
                    month_string = date_to_set.strftime("%b")
                    #print("Unable to use " + row[self.Description])
                if month_string == "" and row[self.AddedOn] != None:
                    date_to_set: datetime = row[self.AddedOn]
                    date_to_set = self.add_one_month(date_to_set)
                    if date_to_set.day > 25:
                        date_to_set = self.add_one_month(date_to_set)
                    month_string = date_to_set.strftime("%b")
                    #print("Used the Added On date")
            if month_string != "":

                year_to_set = datetime.now().year
                month_string = month_string.strip()
                if month_string == "Jan" and datetime.now().month == 12:
                    year_to_set = year_to_set+1
                date_string = month_string+"/"+day_string+"/"+str(year_to_set)
                # print(date_string)
                row[self.PublicationMonth] = datetime.strptime(
                    date_string, "%b/%d/%Y")

    def _set_publication_numbers(self):
        for row in self._data_list:

            pub_number: str = row[self.Description].split("-")[0]
            pub_number = pub_number.strip()
            #pub_number = pub_number.rjust(4, "0")
            row[self.PublicationNumber] = int(pub_number)

    def _update_quantities(self):
        for row in self._data_list:
            if row["CPC"] != None and row["Samples"] != None:
                qty = int(row["CPC"]) + int(row["Samples"])
                if int(math.ceil(qty / 500.000) * 500) % qty < 150:
                    qty += 500
                qty = int(math.ceil(qty / 500.000) * 500)  # round up to the next 500
                row["Qty Ordered"]=qty

    def _set_item_templates(self):
        for row in self._data_list:
            if row["True Page Count"] != None and row["itemTemplate"] is None:
                row["itemTemplate"] = "BVM-"+str(int(row["True Page Count"]))+"P"
    
    def on_file_upload(self, file_upload):
        self._merge_data(file_upload, ["Publication Number"], self._hit_add_missing, self._miss_not_add_row)
        self._set_item_templates()
    
    def on_approval(self, approved):
        self._merge_data(approved, ["Publication Number"], self._hit_add_missing, self._miss_not_add_row)
        self._set_item_templates()

    def save(self):
        self.write_to_file(self.path, self.tab, self.prep_data_add_columns, WriteData)

    def on_mis_list(self, mis_list):
        self._merge_data(mis_list, ["Description"], self._hit_replace, self._miss_not_add_row)        
    
    def on_job_projects(self, mis_list):
        self._merge_data(mis_list, ["Description"], self._hit_add_missing, self._miss_add_row_record_addition)
    
    def on_est_received(self, est_file):
        self._merge_data(est_file, ["Publication Number", "Publication Month"], self._hit_replace, self._miss_not_add_row)

    def on_samples_received(self, flattened_samples):
        self._merge_data(flattened_samples, ["id", "Publication Month"], self._hit_add_missing, self._miss_not_add_row)
        self._update_quantities()
        self._set_item_templates()

    def check_mis_exports(self, job_imports) -> bool:
        exported = self.export(job_imports)
        job_imports.populate_static()
        return exported
        # if exported:
        #     self.save()
        #     job_imports.fix_production_notes()
        #     job_imports.save()

        

class Samples(DataSource):
    """Mailing list of sample counts for publishers, advertisers, etc.

    Args:
        DataSource ([type]): [description]
    """

    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Samples"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._split_column(
            "Customer", ["First Name", "Last Name"], self._name_split)
        self._data_list = self._normalize_dates()
        self._add_column("job")

    def _name_split(self, name: str) -> List[str]:
        namesList = []
        name = name.split('(')[0]
        names = name.split()
        firstName = ''
        for x in range(len(names)-1):
            if firstName != '':
                firstName = firstName+' ' + names[x]
            else:
                firstName += names[x]
        namesList.append(firstName)
        lastName = names[-1]
        namesList.append(lastName)
        return namesList

    def write_to_file(self, path: str, sheet: str, prep_data_funct, write_func):
        self.populate_static()        
        write_func(path, sheet, self.Data_Frame, self.Columns)
    
    def save(self, path):
        self.write_to_file(path, self.tab, self.prep_data_none, WriteData)


class DesignerCopies(DataSource):
    """Mailing list of designers. Does not include counts since they only receive one sample.

    Args:
        DataSource ([type]): [description]
    """

    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Designer Copies"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._data_list = self._normalize_dates()
        self._add_column("job")

class ExportList(DataSource):
    def _get_column_names(self) -> list:
        return list(self.settings["Columns Order"].values())

    Columns = property(_get_column_names)
    
    def save(self):
        self.write_to_file(self.path, self.tab, self.prep_data_none, WriteData)

class FlattenedSamples(ExportList):

    def __init__(self, samples: Samples, designer_copies: DesignerCopies, file_name: str, settingsFunc, dictFunc) -> None:
        self._type: str = "Flattened Samples"
        temp_settings = settingsFunc(self._type)
        path = temp_settings["Default Path"]+file_name
        super().__init__(self._type, path, settingsFunc, dictFunc)
        samples.nd_merge(designer_copies)
        self.nd_merge(samples)
        for row in self._data_list:
            row["Samples"] = self.get_pub_samples_quantity(row["id"])
        self._add_column("Exported")
        self._add_column("jobContactID")
        self._add_column("globalContactID")
    
    def get_pub_samples_quantity(self, pub) -> int:
        return sum(
            int(row["U_shipmentNotes"])
            for row in self._data_list
            if row["id"] == pub
        )
    
    def get_pubs(self) -> List[str]:
        pubs = []
        for row in self._data_list:
            if row["id"] not in pubs:
                pubs.append(row["id"])
        return pubs

class Contacts(DataSource):
    """List of Contacts from the MIS. Used for substitution when updating the records in the MIS

    Args:
        DataSource ([type]): [description]
    """

    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Contacts"
        super().__init__(self._type, path, settingsFunc, dictFunc)


class PaceUpdate(DataSource):
    """The data about customer jobs retrieved from the MIS

    Args:
        DataSource ([type]): [description]
    """

    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Pace Update"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._job = "Job"
        self._description = "Description"
        self._productionStatus = "Production Status"
        self._scheduledShipDate = "Scheduled Ship Date"
        self._qtyOrdered = "Qty Ordered"
        self._productionNotes = "Production Notes"
        self._itemTemplate = "Item Template"
        self._additionalDescription = "Additional Description"
        self._dateSetup = "Date Setup"
        self._pageCountStrings = self.settings['Page Count Strings']
        self._addExtraColumns()

    def _get_cpc(self, row: dict) -> str:
        """Get the mailing count from a row

        Args:
            row (dict): Row from MIS export

        Returns:
            str: Mailing count as string
        """
        return row[self._productionNotes].split()[-1]

    def _get_page_count(self, row: dict) -> str:
        """Return the page count in a supplied row

        Args:
            row (dict): Row from MIS export

        Returns:
            str: Page count as string
        """
        pageCount = ''
        for key in self._pageCountStrings:
            if key in row[self._additionalDescription]:
                pageCount = self._pageCountStrings[key]
        return pageCount

    def _addExtraColumns(self):
        for row in self._data_list:
            row['CPC'] = self._get_cpc(row)
            row['Page Count'] = self._get_page_count(row)

class CustomerReport(ExportList):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Customer Report"
        super().__init__(self._type, path, settingsFunc, dictFunc)


class JobShipments(ExportList):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Job Shipments"
        super().__init__(self._type, path, settingsFunc, dictFunc)


class Invoice(ExportList):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Invoice"
        super().__init__(self._type, path, settingsFunc, dictFunc)

class JobImport(ExportList):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Job Import"
        super().__init__(self._type, path, settingsFunc, dictFunc)

    def fix_production_notes(self):
        for row in self._data_list:
            row["U_productionNotes"] = "PW Count = " + str(row["U_productionNotes"])


class PdfFile(DataSource):

    def _get_column_names(self) -> list:
        return list(self.settings["Columns Order"].values())

    Columns = property(_get_column_names)

class PdfReceived(PdfFile):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "PDF Received"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._data_list[0]["Files In"] = self._data_list[0]["DateTime"]
        self._data_list[0]["Publication Number"] = int(NameParse(self._data_list[0]["Name"]))

class PdfApproved(PdfFile):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "PDF Approved"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._data_list[0]["Approved"] = self._data_list[0]["DateTime"]
        self._data_list[0]["Publication Number"] = int(NameParse(self._data_list[0]["Name"]))

class EstFile(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self.type: str = "EST File"
        self.settings = settingsFunc("EST File")
        columns = self.settings["Columns Order"].values()        
        self._data_list = dictFunc(path, columns)
        for i in range(len(self._data_list)-1, 0, -1):
            self._data_list[0]["Houses"] += self._data_list[i]["Houses"]
            self._data_list[0]["Apartments"] += self._data_list[i]["Apartments"]
            self._data_list[0]["Farms"] += self._data_list[i]["Farms"]
            self._data_list[0]["Businesses"] += self._data_list[i]["Businesses"]
            self._data_list.pop(i)
        self._data_list[0]["CPC"]=self._data_list[0]["Houses"]+self._data_list[0]["Apartments"]+self._data_list[0]["Farms"]

        self._data_list[0]["Publication Number"] = int(path.split("/")[-1].split("\\")[-1].split()[0])
        if datetime.now().day<=15:
            pub_date=self.add_months_from_now(1)
            self._data_list[0]["Publication Month"]=self.add_months_from_now(1)
            
        else:
            pub_date=self.add_months_from_now(2)
            self._data_list[0]["Publication Month"]=self.add_months_from_now(2)
        pub_month=pub_date.month
        pub_year=pub_date.year
        pub_day="01"
        self._data_list[0]["Publication Month"]=datetime.strptime(str(pub_month)+"/"+pub_day+"/"+str(pub_year), "%m/%d/%Y")
        

class JobProjects(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Job Projects"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._get_publication_month()
        self._get_descriptions()
    
    def _get_publication_month(self):
        today = datetime.now()
        publication_month = today
        publication_month = self.add_one_month(today)
        publication_month = self.add_one_month(publication_month)
        publication_month.replace(day = 1)
        month = publication_month.month
        year = publication_month.year
        day = "01"
        date_string = str(month)+"/"+day+"/"+str(year)
        for row in self._data_list:
            row["Publication Month"] = datetime.strptime(date_string, "%m/%d/%Y")
    
    def _get_descriptions(self):
        for row in self._data_list:
            short_month = row["Publication Month"].strftime("%b")
            short_year = row["Publication Month"].strftime("%y")
            row["Description"] = row["Name"][:40]
            row["Description"] += " - "+short_month+" - "+short_year

