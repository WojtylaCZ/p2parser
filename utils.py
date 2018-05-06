def getTableLikeString(dataToPrint):
    row = ''
    for item in dataToPrint:
        row = row + str(item) + '\t'
    return row