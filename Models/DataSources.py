from typing import Dict, List
import json
from datetime import date, datetime
import copy
import Libraries.ExcelLibs as el
import numpy as np
import pandas as pd


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
        self._dataList = dictFunc(self.path, self.tab)        
        
        # self.df = el.get_dataframe(self.path, self.tab)

    def _find_first_row(self, column: str, search_term: str) -> pd.DataFrame:
        """
        Finds the first row containing searchterm.

        Args:
            self (undefined):
            column (str): The column header to search under
            search_term(str):

        Returns:
            dict: Complete row. Empty if nothing found.

        """
        try: 
            found = self._find_all_rows(column, search_term)
        except:
            return pd.DataFrame()
        if found.empty:
            return found
        return found.iloc[[0]]

    def _get_column_names(self) -> list:
        """
        Returns a list of all columns used in the first element in _data_list

        Args:
            self (undefined):

        Returns:
            list of columns[str]

        """
        return self._dataList.columns.tolist()

    def _get_data_dict(self) -> List[Dict]:
        data_dict = self.dataDict = self._dataList.to_dict('records')
        return data_dict
    
    def _set_data_dict(self, value):
        new_dict = copy.deepcopy(value)        
        self._dataList = pd.DataFrame(new_dict)

    DataDict = property(_get_data_dict, _set_data_dict)

    Columns = property(_get_column_names)

    def _normalize_dates(self) -> List[Dict]:
        """
        Change all dates in string format to proper DateTime dates

        Args:
            self (undefined):

        Returns:
            List[Dict]: A deep copy of current _datalist with proper dates

        """
        dateDataList = copy.deepcopy(self._dataList)
        if self.settings['True Dates'] == False:
            for row in dateDataList:
                for column in self.settings["Date Columns"]:
                    if row[column] != None:
                        if type(row[column]) == str:
                            row[column] = datetime.strptime(
                                row[column], self.settings['Date Format'])
        return dateDataList

    def _get_string_datalist(self) -> List[Dict[str, str]]:
        """
        Change all non string values to string. Datetimes are converted using the objects Date Format

        Args:
            self (undefined):

        Returns:
            List[Dict[str, str]]: A deep copy of the _datalist with all values as strings

        """
        stringDataList = copy.deepcopy(self._dataList)
        for row in stringDataList:
            for x in row:
                if type(row[x]) != datetime:
                    row[x] = str(row[x])
                else:
                    row[x] = row[x].strftime(self.settings['Date Format'])
        return stringDataList

    def _find_all_rows(self, column: str, search_term: str) -> pd.DataFrame:
        """
        Find all rows which have a column equal to search_term

        Args:
            self (undefined):
            column (str): The column header to search in (ie Job)
            search_term(str):

        Returns:
            List[Dict]: List of all rows containing the search term

        """
        found_list = self._dataList.loc[self._dataList[column]==search_term]
        # found_list: list[dict] = list()
        # for row in self._dataList:
        #     if row[column] == search_term:
        #         found_list.append(row)
        return found_list

    def _find_in_all_rows(self, column: str, search_term: str) -> pd.DataFrame:
        """[Find all rows that have a column containing (in) search_term]

        Args:
            column (str): Column header to search
            search_term (str): string to search for

        Returns:
            List[Dict]: List of rows
        """
        found = self._dataList.loc[self._dataList[column].str.contains(search_term)]

        return found

    def _get_row(self, index: int) -> pd.DataFrame:
        """Get a row in _datalist by index

        Args:
            index (int): 0 based index to return

        Returns:
            dict: Row
        """
        return self._dataList.iloc[index]

    def _get_cell(self, index: int, column: str):
        """Get a single cell 

        Args:
            index (int): 0 based index of row
            column (str): Column header

        Returns:
            [type]: Data contained within the cell
        """
        return self._dataList.at[index, column]

    def get_consumable_list(self, columns: list) -> List:
        """Get a list of _datalist conatining only the given columns

        Args:
            columns (list): The columns to include in the returned list

        Returns:
            List: List of columns
        """
        consumableList = list()
        for row in self.DataDict:
            entries = dict()
            for column in columns:
                entries[column] = row[column]
            consumableList.append(entries)
        return consumableList

    def return_savable_list(self) -> List:
        """Returns a copy of the _datalist as a list of lists using the order stored in Columns Order of settings

        Returns:
            List: List of lists
        """
        savableList: list[list] = list()
        headers: list[str] = list()
        columnsOrder: dict[str, str] = self.settings["Columns Order"]
        for row in self._dataList:
            rowList = list()
            for columnNumber in range(1, len(columnsOrder)+1):
                columnName = columnsOrder[str(columnNumber)]
                rowList.append(row[columnName])
            savableList.append(rowList)

        for columnNumber in range(1, len(columnsOrder)+1):
            headers.append(columnsOrder[str(columnNumber)])
        savableList.insert(0, headers)
        return savableList

    def _consume_data(self, data_source, id_column: str):
        """Merge and/or add compatible data from another DataSource's _datalist. 
        If IDColunn exists in the source's _datalist its' columns are overwritten with matching ones from the DataSource it's consuming.

        Args:
            dataSource ([type]): DataSource to consume
            IdColumn (str): Column to match between self, and dataSource
        """
        commonColumns = self.find_common_columns(data_source)
        listToConsume = data_source.get_consumable_list(commonColumns)
        for newRow in listToConsume:
            found = False
            if len(self._dataList[0]) == 0:
                self._dataList[0] = newRow
            for oldRow in self._dataList:
                if newRow[id_column] == oldRow[id_column]:
                    found = True
                    for column in commonColumns:
                        oldRow[column] = newRow[column]
            if found == False:
                self._dataList.append(newRow)

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
        value = self._dataList.iloc[index][columnHeader]
        #print(value)
        if type(value) == str:
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
        index = self._get_first_index(search_column, search_term)
        #print(found.at[0, date_column])
        if date_column in self.settings['Date Columns']:
            self._dataList.at[index, date_column] = date_to_set.strftime(
                self.settings['Date Format'])
        

    def len(self) -> int:
        """Returns the current length of _dataList

        Returns:
            int: Current length of _dataList
        """        
        return len(self._dataList)

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
        row.at[0, column_name] = value
        # print(row.at[0, column_name])
        # print("pause")

    def _get_first_index(self, column: str, search_term: str) -> int:
        """Searches the _datalist and returns the index of the first row in which column[column_name] matches search_term

        Args:
            column_name (str): Name of the column to search
            search_term (str): Value to search for

        Returns:
            int: Index of the found row
        """        
        index = int()
        for i in range(len(self.DataDict)):
            if self.DataDict[i][column] == search_term:
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
        # self._dataList = self._normalize_dates()

    def get_most_recent_pub(self, pub_number: str) -> pd.DataFrame:
        """Find the most recent publication.

        Args:
            pub_number (str): Publication number as a string

        Returns:
            Dict: The row containing the most recent publication
        """        
        candidates = self._find_in_all_rows(self.Description, pub_number)        
        if len(candidates) == 1:
            found = candidates.iloc[[0]]
        else:
            candidates.sort_values([self.DateSetup])
            found = candidates.tail(1)
        return found

    def get_job_index(self, job: str) -> int:
        """Return the row containing [job]

        Args:
            job (str): Job number as a string

        Returns:
            dict: Row containing the found job
        """        
        found = self._get_first_index(self.Job, job)
        return found
  

    def job_is_approved(self, job: str) -> bool:
        """Return true if a job has been approved, false if not.

        Args:
            job (str): Job number as a string

        Returns:
            bool: True if approved, false if not.
        """        
        found = self.get_job(job)
        
        if found.empty == True:
            return False
        approved = pd.notnull(found.iloc[0][self.Approved])

        return approved


    def job_is_uploaded(self, job: str) -> bool:
        """Return true if a job has been uploaded, false if not.

        Args:
            job (str): Job number as a string.

        Returns:
            bool: True if uploaded, false it not.
        """        
        found = self.get_job(job)
        if found.empty ==True:
            return False
        
        return pd.notnull(found.iloc[0][self.FilesIn])

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


class Samples(DataSource):
    """Mailing list of sample counts for publishers, advertisers, etc.

    Args:
        DataSource ([type]): [description]
    """    
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Samples"
        super().__init__(self._type, path, settingsFunc, dictFunc)


class DesignerCopies(DataSource):
    """Mailing list of designers. Does not include counts since they only receive one sample.

    Args:
        DataSource ([type]): [description]
    """    
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Designer Copies"
        super().__init__(self._type, path, settingsFunc, dictFunc)


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
        new_dict = self.DataDict
        for row in new_dict:
            row['CPC'] = self._get_cpc(row)
            row['Page Count'] = self._get_page_count(row)        
        self.DataDict=new_dict


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