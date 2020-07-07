from typing import Dict, List
import json
from datetime import datetime
import copy


class DataSource:

    def __base_init__(self, name: str, path: str, settingsFunc, dictFunc):
        self.name: str = name
        self.settings: dict = settingsFunc(self.name)
        if path == "":
            self.path: str = self.settings["Default Path"]
        else:
            self.path: str = path
        self.tab: str = self.settings["Tab"]
        self._dataList: list[dict] = dictFunc(self.path, self.tab)

    def _findFirstRow(self, column: str, searchTerm: str) -> dict:
        empty: dict[str, str] = {'None': ''}
        for row in self._dataList:
            if row[column] == searchTerm:
                return row
        return empty
    
    def _getColumnNames(self) -> list:
        return list(self._dataList[0].keys())
    
    Columns = property(_getColumnNames)

    def _normalizeDates(self) -> List[Dict]:
        dateDataList = copy.deepcopy(self._dataList)
        if self.settings['True Dates'] == False:
            for row in dateDataList:
                for column in self.settings["Date Columns"]:
                    if row[column] != None:
                        row[column] = datetime.strptime(row[column], self.settings['Date Format'])
        return dateDataList

    def _getStringDatalist(self) -> List[Dict[str, str]]:
        stringDataList = copy.deepcopy(self._dataList)
        for row in stringDataList:
            for x in row:
                if type(row[x]) != datetime:
                    row[x] = str(row[x])
                else:
                    row[x] = row[x].strftime(self.settings['Date Format'])
        return stringDataList

    def _findAllRows(self, column: str, searchTerm: str) -> List[Dict]:
        foundList: list[dict] = list()
        for row in self._dataList:
            if row[column] == searchTerm:
                foundList.append(row)
        return foundList

    def _findInAllRows(self, column: str, searchTerm: str) -> List[Dict]:
        foundList: list[dict] = list()
        for row in self._dataList:
            if searchTerm in row[column]:
                foundList.append(row)
        return foundList

    def _getRow(self, index: int) -> dict:
        return self._dataList[index]

    def _getCell(self, index: int, column: str):
        return self._getRow(index)[column]

    def getConsumableList(self, columns: list) -> List:
        consumableList = list()
        for row in self._dataList:
            entries = dict()
            for column in columns:
                entries[column]=row[column]
            consumableList.append(entries)
        return consumableList

    def returnSavableList(self) -> List:
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
    
    def _consumeData(self, dataSource, IdColumn: str):
        commonColumns = self.FindCommonColumns(dataSource)
        listToConsume = dataSource.getConsumableList(commonColumns)
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

    def getTrueDate(self, columnHeader: str, index: int,) -> datetime:
        return datetime.strptime(self._dataList[index][columnHeader], self.settings['Date Format'])

    def _setDate(self, searchColumn: str, ID: str, dateColumn: str, dateToSet: datetime):
        found = self._findFirstRow(searchColumn, ID)
        if dateColumn in self.settings['Date Columns']:
            found[dateColumn] = dateToSet.strftime(
                self.settings['Date Format'])

    def len(self):
        return len(self._dataList)

    def _cellToDate(self, cell: str) -> datetime:
        return datetime.strptime(cell, self.settings['Date Format'])

    def _updateField(self, row: dict, columnName: str, value: str) -> None:
        row[columnName] = value

    def _getFirstIndex(self, columnName: str, searchTerm: str) -> int:
        index = int()
        for i in range(len(self._dataList)):
            if self._dataList[i][columnName] == searchTerm:
                return i
        return index

    def FindCommonColumns(self, ds2) ->list:
        columnsSet = set(self.Columns)
        intersection = columnsSet.intersection(ds2.Columns)
        _columns = list(intersection)
        return _columns


def loadDataSettings_JSON(name: str) -> dict:
    with open('BVMSettings.json') as j:
        settings: dict = json.load(j)
        return settings["Data Sources"][name]


class JobsList(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Jobs List"
        self.__base_init__(self._type, path, settingsFunc, dictFunc)
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

    def GetMostRecentPub(self, pubNumber):
        candidates = self._findInAllRows(self.Description, pubNumber)
        found = dict()
        if len(candidates) > 0:
            found = candidates[0]
            for candidate in candidates:
                if self._cellToDate(candidate[self.DateSetup]) > self._cellToDate(found[self.DateSetup]):
                    found = candidate
        return found

    def GetJob(self, job: str) -> dict:
        found = self._findFirstRow(self.Job, job)
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
        self.__base_init__(self._type, path, settingsFunc, dictFunc)


class DesignerCopies(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Designer Copies"
        self.__base_init__(self._type, path, settingsFunc, dictFunc)


class Contacts(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Contacts"
        self.__base_init__(self._type, path, settingsFunc, dictFunc)

class PaceUpdate(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:    
        self._type: str = "Pace Update"
        self.__base_init__(self._type, path, settingsFunc, dictFunc)
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

class CustomerReport(DataSource):
    def __init__(self, path, settingsFunc, dictFunc) -> None:
        self._type: str = "Customer Report"
        self.__base_init__(self._type, path, settingsFunc, dictFunc)

    def _getColumnNames(self) -> list:
        return self.settings["Columns Order"].values()
    
    Columns = property(_getColumnNames)

