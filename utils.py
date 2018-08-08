def getTabbedStringFromValueList(dataToPrint):
    row = ''
    for item in dataToPrint:
        try:
            value = format(item, '.2f')
        except:
            value = str(item or 0.0)
        row = row + value.rjust(10).ljust(10) + '\t'
    return row
