import re
def find_largest_column_element(rows, cols, matrix):
    large_column = []
    lengthArrayCol = []    
    for col in range(cols):
        for row in range(rows):
            lengthArrayCol.append(len(str(matrix[row][col])))
        lengthArrayCol.sort()
        largestElementLengthCOL = lengthArrayCol[-1]
        large_column.append(largestElementLengthCOL)
        lengthArrayCol = []
    return large_column


def createMatrix(rows, cols, matrixToWorkOn, matrix):
    for i in range(rows):
        matrixToWorkOn.append([])
        for j in range(cols):
            matrixToWorkOn[i].append(str(matrix[i][j]))


def makeNewRows(rows, cols, largestElementLengthCOL, rowLength, matrixToWorkOn, newfinalTable, color):
    for i in range(rows):
        currentRow = ""
        for j in range(cols):
            if ((color != None) and (j == 0 or i == 0)):
                currentEl = " " + "\033[38;2;" + str(color[0]) + ";" + str(color[1]) + ";" + str(color[2]) +"m" + matrixToWorkOn[i][j] + "\033[0m"
            else:
                currentEl = " " + matrixToWorkOn[i][j]
            
            if '\n' in currentEl:
                temp_element = ""
                currentEl = currentEl[:-1]
                currentEl_split = currentEl.split('\n')
                if len(currentEl_split) >= 2:
                    num = 1
                    for each in currentEl_split:
                        if num == 1:
                            temp_element += each +" " * (largestElementLengthCOL[j] - len(each) + 1) + " |\n"
                        else:
                            blank_row = re.sub('[a-zA-Z0-9.]', ' ', currentRow)
                            if num == len(currentEl_split):
                                temp_element += "|"+blank_row+" " + each +" " * (largestElementLengthCOL[j] - len(each) + 1)+ "|"
                            else:
                                temp_element += "|"+blank_row+" " + each + " " * (largestElementLengthCOL[j] - len(each) + 1) + "|\n"
                        num = num +1
                    currentRow += temp_element
                    # currentEl = temp_element
                    # currentRow += currentEl
                else:
                    currentEl = currentEl + " " * (largestElementLengthCOL[j] - len(currentEl) + 2) + "|"
                    currentRow += currentEl
            else:
                if (largestElementLengthCOL[j] != len(matrixToWorkOn[i][j])):
                    if (color != None):
                        if (j == 0 or i == 0):
                            currentEl = currentEl + " " * (largestElementLengthCOL[j] - (len(currentEl) - len("\033[38;2;" + str(color[0]) + ";" + str(color[1]) + ";" + str(color[2]) + "m" + "\033[0m")) + 2) + "|"
                        else:
                            currentEl = currentEl + " " * (largestElementLengthCOL[j] - len(currentEl) + 2) + "|"
                    else:
                        currentEl = currentEl + " " * (largestElementLengthCOL[j] - len(currentEl) + 2) + "|"
                else:
                    currentEl = currentEl + " " + "|"
                currentRow += currentEl
        newfinalTable.append("|" + currentRow)
    if (color != None):
        rowLength = len(currentRow) - len("\033[38;2;" + str(color[0]) + ";" + str(color[1]) + ";" + str(color[2]) + "m" + "\033[0m")
    else:
        rowLength = len(currentRow)  
    return rowLength

def removespace(newfinalTable):
    table = []
    check_list = []
    check = False
    for each in newfinalTable:
        # print(each)
        print(f'row => {each} && length => {len(each)}')
    #     last_from_string = each[-5:-1]
    #     check = last_from_string.isspace()
    #     check_list.append(check)
    # if all(check_list):
    #     for each in newfinalTable:
    #         line = each[:-5]+"|"
    #         table.append(line)
    #     table = removespace(table)
    # else:
    #     table = newfinalTable
    return table

def createWrappingRows(rowLength, newfinalTable):
    wrappingRows = ""
    for i in range(rowLength - 1):
        wrappingRows += "-"
    wrappingRows = "+" + wrappingRows
    wrappingRows += "+"
    newfinalTable.insert(0, wrappingRows)
    newfinalTable.append(wrappingRows)


def createRowUnderFieldsnew(largestElementLengthCOL, cols, newfinalTable):
    rowUnderFields = ""
    for j in range(cols):
        currentElUnderField = "+" 
        currentElUnderField = currentElUnderField + "-" * (largestElementLengthCOL[j] + 2)
        rowUnderFields += currentElUnderField
    rowUnderFields += "+"
    newfinalTable.insert(2, rowUnderFields)

def add_title(title, newfinalTable):
    newrow = " "
    index = len(newfinalTable[0])
    title_len = len(title)
    index = index+1 - title_len
    rem = index % 2
    place = (index // 2)-1
    if rem:
        newrow = f'{newrow * place}{title}{newrow * place}'
    else:
        newplace = place-1
        newrow = f'{newrow * place}{title}{newrow * newplace}'
    newrow = f'|{newrow}|'
    blank_line = newfinalTable[0]
    newfinalTable.insert(0, newrow)
    newfinalTable.insert(0, blank_line)


def printRowsInTable(newfinalTable):
    for row in newfinalTable:
        print(row)

def print_table(title, matrix, useFieldNames=False, color=None):
    rows = len(matrix)
    cols = len(matrix[0])
    rowLength = None
    matrixToWorkOn = []
    newfinalTable = []
    largestElementLengthCOL = find_largest_column_element(rows, cols, matrix)
    createMatrix(rows, cols, matrixToWorkOn, matrix)
    rownewLength = makeNewRows(rows, cols, largestElementLengthCOL, rowLength, matrixToWorkOn, newfinalTable, color)
    # newfinalTable = removespace(newfinalTable)
    createWrappingRows(rownewLength, newfinalTable)
    if (useFieldNames):
        createRowUnderFieldsnew(largestElementLengthCOL, cols, newfinalTable)
    if title:
        add_title(title, newfinalTable)
    printRowsInTable(newfinalTable)
