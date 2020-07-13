from typing import Dict, List
import json
from datetime import datetime
import copy


class DataSource:
    
    def __init__(self, name: str, path: str, settingsFunc, dictFunc):
        self.name: str = name
        self.settings: dict = settingsFunc(self.name)
        if path == "":
            self.path: str = self.settings["Default Path"]
        else:
            self.path: str = path
        self.tab: str = self.settings["Tab"]
        self._dataList: list[dict] = dictFunc(self.path, self.tab)

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
        for row in self._dataList:
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
        return list(self._dataList[0].keys())
    
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
                        if  type(row[column]) == str:
                            row[column] = datetime.strptime(row[column], self.settings['Date Format'])
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
        for row in self._dataList:
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
        for row in self._dataList:
            if search_term in row[column]:
                found_list.append(row)
        return found_list

    def _getRow(self, index: int) -> dict:
        """Get a row in _datalist by index

        Args:
            index (int): 0 based index to return

        Returns:
            dict: Row
        """        
        return self._dataList[index]

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
        """Get a list of _datalist conatining only the given columns

        Args:
            columns (list): The columns to include in the returned list

        Returns:
            List: List of columns
        """        
        consumableList = list()
        for row in self._dataList:
            entries = dict()
            for column in columns:
                entries[column]=row[column]
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
    
    def _consume_data(self, dataSource, IdColumn: str):
        """Merge and/or add compatible data from another DataSource's _datalist. 
        If IDColunn exists in the source's _datalist its' columns are overwritten with matching ones from the DataSource it's consuming.

        Args:
            dataSource ([type]): DataSource to consume
            IdColumn (str): Column to match between self, and dataSource
        """        
        commonColumns = self.FindCommonColumns(dataSource)
        listToConsume = dataSource.get_consumable_list(commonColumns)
        for newRow in listToConsume:
            found = False
            if len(self._dataList[0]) == 0:
                self._dataList[0]=newRow
            for oldRow in self._dataList:
                if newRow[IdColumn]==oldRow[IdColumn]:
                    found = True
                    for column in commonColumns:
                        oldRow[column]=newRow[column]
            if found == False:
                self._dataList.append(newRow)

    def columnIsDate(self, columnHeader: str) -> bool:
        if columnHeader in self.settings['Date Columns']:
            return True
        else:
            return False

    def getTrueDate(self, columnHeader: str, index: int):
        value = self._dataList[index][columnHeader]
        if type(value)==str:
            value = datetime.strptime(value, self.settings['Date Format'])
        return value

    def _setDate(self, searchColumn: str, ID: str, dateColumn: str, dateToSet: datetime):
        found = self._find_first_row(searchColumn, ID)
        if dateColumn in self.settings['Date Columns']:
            found[dateColumn] = dateToSet.strftime(
                self.settings['Date Format'])

    def len(self):
        return len(self._dataList)

    def _cellToDate(self, cell):
        dateReturn = cell
        if type(cell) == str:
            dateReturn = datetime.strptime(cell, self.settings['Date Format'])
        return dateReturn

    def _updateField(self, row: dict, columnName: str, value: str) -> None:
        row[columnName] = value

    def _getFirstIndex(self, columnName: str, search_term: str) -> int:
        index = int()
        for i in range(len(self._dataList)):
            if self._dataList[i][columnName] == search_term:
                return i
        return index

    def FindCommonColumns(self, ds2) ->list:
        columnsSet = set(self.Columns)
        intersection = columnsSet.intersection(ds2.Columns)
        _columns = list(intersection)
        return _columns

class JobsList(DataSource):
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
        self._dataList = self._normalize_dates()

    def GetMostRecentPub(self, pubNumber):
        candidates = self._find_in_all_rows(self.Description, pubNumber)
        found = dict()
        if len(candidates) > 0:
            found = candidates[0]
            for candidate in candidates:
                if self._cellToDate(candidate[self.DateSetup]) > self._cellToDate(found[self.DateSetup]):
                    found = candidate
        return found

    def GetJob(self, job: str) -> dict:
        found = self._find_first_row(self.Job, job)
        return found

    def jobIsApproved(self, job: str) -> bool:
        found = self.GetJob(job)
        if len(found.keys()) > 1:
            if found[self.Approved] != None:
                return True
        return False

    def jobIsUploaded(self, job: str) -> bool:
        found = self.GetJob(job)
        if len(found.keys()) > 1:
            if found[self.FilesIn] != None:
                return True
        return False

    def SetUploadDate(self, job: str, date: datetime):
        self._setDate(self.Job, job, self.FilesIn, date)

    def SetApprovedDate(self, job: str, date: datetime):
        self._setDate(self.Job, job, self.Approved, date)


class Samples(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Samples"
        super().__init__(self._type, path, settingsFunc, dictFunc)


class DesignerCopies(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Designer Copies"
        super().__init__(self._type, path, settingsFunc, dictFunc)


class Contacts(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Contacts"
        super().__init__(self._type, path, settingsFunc, dictFunc)

class PaceUpdate(DataSource):
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

    def _getCPC(self, row: dict) -> str:
        cpc = row[self._productionNotes].split()[-1]
        return cpc
    
    def _getPageCount(self, row: dict) -> str:
        pageCount=''        
        for key in self._pageCountStrings:
            if key in row[self._additionalDescription]:
                pageCount = self._pageCountStrings[key]
        return pageCount

    def _addExtraColumns(self):
        for row in self._dataList:
            row['CPC'] = self._getCPC(row)
            row['Page Count'] = self._getPageCount(row)

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

