def getTabbedStringFromValueList(dataToPrint):
    row = ''
    for item in dataToPrint:
        row = row + str(item or 0.0) + '\t'
    return row
