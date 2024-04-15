import pandas
class ExcelReader():
    def __init__(self, fileName):
        self.fileName = fileName
        self.xlsFile = pandas.ExcelFile(fileName)

    def getTableTitleListBySheetName(self, sheetName):
        columnNameList = pandas.read_excel(self.fileName, sheet_name=sheetName).columns.values
        return columnNameList

    # 获取所有的表名
    def getAllSheetsNames(self):
        return self.xlsFile.sheet_names

    # 返回表名对应的sheet的行数和列数
    def getSheetSize(self, sheetName):
        if not sheetName in self.getAllSheetsNames():
            return 0, 0
        sheet = self.xlsFile.parse(sheetName)
        return sheet.nrows, sheet.ncols

    # 以二位列表，返回sheet的内容
    def getSheetContent(self, sheetName):
        if not sheetName in self.getAllSheetsNames():
            return []
        sheet = self.xlsFile.parse(sheet_name=sheetName)
        return sheet.values