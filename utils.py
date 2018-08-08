def getTabbedStringFromValueList(dataToPrint):
    row = ''
    for item in dataToPrint:
        row = row + str(item or 0.0).rjust(10).ljust(10) + '\t'
    return row
