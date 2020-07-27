from typing import Dict, List
import json
from datetime import date, datetime
import calendar
import copy
import pandas as pd
from Libraries.NameParse import NameParse

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
        self._data_list: list[dict] = dictFunc(self.path, self.tab)

    def _get_data_frame(self):
        return pd.DataFrame(self._data_list)

    Data_Frame = property(_get_data_frame)

    def write_to_file(self, path: str, sheet: str, write_func):
        self.populate_static()
        write_func(path, sheet, self.Data_Frame, self.ExportColumns)

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
        empty: dict[str, str] = {'None': ''}
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
        return list(self._data_list[0].keys())

    def _get_export_columns(self):
        columns_list = list()
        for i in range(1, len(self.settings["Columns Order"])+1):
            columns_list.append(self.settings["Columns Order"][str(i)])
        return columns_list

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
        if self.settings['True Dates'] == False:
            for row in dateDataList:
                for column in self.settings["Date Columns"]:
                    if row[column] != None:
                        if type(row[column]) == str:
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
        found_list: list[dict] = list()
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
        found_list: list[dict] = list()
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
        consumableList = list()
        for row in self._data_list:
            entries = dict()
            for column in columns:
                entries[column] = row[column]
            consumableList.append(entries)
        return consumableList

    def return_savable_list(self) -> List:
        """Returns a copy of the _data_list as a list of lists using the order stored in Columns Order of settings

        Returns:
            List: List of lists
        """
        savableList: list[list] = list()
        headers: list[str] = list()
        columnsOrder: dict[str, str] = self.settings["Columns Order"]
        for row in self._data_list:
            rowList = list()
            for columnNumber in range(1, len(columnsOrder)+1):
                columnName = columnsOrder[str(columnNumber)]
                rowList.append(row[columnName])
            savableList.append(rowList)

        for columnNumber in range(1, len(columnsOrder)+1):
            headers.append(columnsOrder[str(columnNumber)])
        savableList.insert(0, headers)
        return savableList

    def _add_column(self, name: str):
        for row in self._data_list:
            row[name] = None

    def _merge_data_ow(self, data_source, id_columns: List, missing_funct):
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
            if len(self._data_list[0]) == 0:
                missing_funct(newRow)
            for oldRow in self._data_list:
                data_match = True
                for id in id_columns:
                    if newRow[id] == oldRow[id] and data_match == True:
                        data_match = True
                    else:
                        data_match = False
                if data_match:
                    found = True
                    for column in commonColumns:
                        if column not in oldRow:
                            oldRow[column] = newRow[column]                            
                        if oldRow[column] == None or column not in self.settings["Date Columns"]:
                            oldRow[column] = newRow[column]
            if found == False:
                missing_funct(newRow)

    def _add_row(self, row: Dict):
        if len(self._data_list[0]) == 0:
            self._data_list[0] = row
        else:
            self._data_list.append(row)

    def _add_row_record_addition(self, row: Dict, record_column: str):
        row[record_column] = datetime.now().strftime(
            self.settings["Date Format"])
        self._data_list.append(row)

    def _not_add_row(self, row: Dict):
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
        self._create_common_column_names()
        self.populate_static()
        data_source._create_common_column_names()
        data_source.populate_static()
        # self._create_common_column_names()
        commonColumns = self.find_common_columns(data_source)
        list_to_merge = data_source.get_consumable_list(commonColumns)
        if len(self._data_list) > 1:
            self._data_list = self._data_list + list_to_merge
        else:
            self._data_list = list_to_merge

    def column_is_date(self, columnHeader: str) -> bool:
        """Checks if a column contains dates or not as described by the DataSource's settings

        Args:
            columnHeader (str): 

        Returns:
            bool: Return true if found in 'Date Columns', false otherwise.
        """
        if columnHeader in self.settings['Date Columns']:
            return True
        else:
            return False

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

        dateReturn = datetime.strptime(cell, self.settings['Date Format'])
        return dateReturn

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
        index = int()
        for i in range(len(self._data_list)):
            if self._data_list[i][column_name] == search_term:
                return i
        return index

    def find_common_columns(self, ds2) -> List[str]:
        """Returns a list of all common columns between the current object, and a supplied DataSource

        Args:
            ds2 ([type]): Any DataSource

        Returns:
            list[str]: List of column names
        """
        columnsSet = set(self.Columns)
        intersection = columnsSet.intersection(ds2.Columns)
        _columns = list(intersection)
        return _columns

    def _split_column(self, original_column_name: str, new_column_names: List[str], func):
        for row in self._data_list:
            new_column_values = func(row[original_column_name])
            i = 0
            for new_column_value in new_column_values:
                row[new_column_names[i]] = new_column_value
                i = i + 1


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
        self._set_publication_numbers()

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

    def get_most_recent_pub(self, pub_number: str) -> Dict:
        """Find the most recent publication.

        Args:
            pub_number (str): Publication number as a string

        Returns:
            Dict: The row containing the most recent publication
        """
        candidates = self._find_in_all_rows(self.Description, pub_number)
        found = dict()
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
        found = self._find_first_row(self.Job, job)
        return found

    def job_is_approved(self, job: str) -> bool:
        """Return true if a job has been approved, false if not.

        Args:
            job (str): Job number as a string

        Returns:
            bool: True if approved, false if not.
        """
        found = self.get_job(job)
        if len(found.keys()) > 1:
            if found[self.Approved] != None:
                return True
        return False

    def job_is_uploaded(self, job: str) -> bool:
        """Return true if a job has been uploaded, false if not.

        Args:
            job (str): Job number as a string.

        Returns:
            bool: True if uploaded, false it not.
        """
        found = self.get_job(job)
        if len(found.keys()) > 1:
            if found[self.FilesIn] != None:
                return True
        return False

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
            if row[self.PublicationMonth] == None:
                if row[self.Description] != None:
                    if len(row[self.Description].split("-")[-1]) < 5:
                        month_string = row[self.Description].split("-")[-1]
                        #print("Used the Description "+row[self.Description])
                if month_string == "":
                    if row[self.DateSetup] != None:
                        date_to_set: datetime = row[self.DateSetup]
                        date_to_set = self.add_one_month(date_to_set)
                        if date_to_set.day > 25:
                            date_to_set = self.add_one_month(date_to_set)
                        month_string = date_to_set.strftime("%b")
                        #print("Unable to use " + row[self.Description])
                if month_string == "":
                    if row[self.AddedOn] != None:
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
            row[self.PublicationNumber] = pub_number

    def add_from_mis_list(self, mis_list):
        self._merge_data_ow(mis_list, ["Job"], self._add_row)


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
        namesList = list()
        name = name.split('(')[0]
        names = name.split()
        firstName = ''
        for x in range(len(names)-1):
            if firstName != '':
                firstName = firstName+' ' + names[x]
            else:
                firstName = firstName+names[x]
        namesList.append(firstName)
        lastName = names[-1]
        namesList.append(lastName)
        return namesList


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
        cpc = row[self._productionNotes].split()[-1]
        return cpc

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


class ExportList(DataSource):
    def _get_column_names(self) -> list:
        return list(self.settings["Columns Order"].values())

    Columns = property(_get_column_names)


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

class PdfFile(DataSource):

    def _get_column_names(self) -> list:
        return list(self.settings["Columns Order"].values())

    Columns = property(_get_column_names)

class PdfReceived(PdfFile):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "PDF Received"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._data_list[0]["Files In"] = self._data_list[0]["DateTime"]
        self._data_list[0]["Publication Number"] = NameParse(self._data_list[0]["Name"])

class PdfApproved(PdfFile):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "PDF Approved"
        super().__init__(self._type, path, settingsFunc, dictFunc)
        self._data_list[0]["Approved"] = self._data_list[0]["DateTime"]
        self._data_list[0]["Publication Number"] = NameParse(self._data_list[0]["Name"])