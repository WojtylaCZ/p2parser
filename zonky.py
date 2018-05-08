#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P2P platform Zonky.cz parser for wallet.xls file and set of statistics functions
"""

import pandas as pd
import csv
from datetime import datetime
import argparse

import utils

DATA_FOLDER = 'data/'

ZONKY_ORIGINAL_FILE = 'wallet.xls'
ZONKY_CSV_FILE = 'zonky.csv'


def convertXLStoCSV():
    zonkySourceFile = DATA_FOLDER + ZONKY_ORIGINAL_FILE

    try:
        print('Trying to convert', zonkySourceFile, 'to', ZONKY_CSV_FILE)
        df = pd.read_excel(zonkySourceFile, 'all')

        print('File', zonkySourceFile, 'loaded.')

        df.to_csv(DATA_FOLDER + ZONKY_CSV_FILE, header=[str(x) for x in range(len(df.columns))], encoding='utf-8', index=False)
        print('File', zonkySourceFile, 'exported to', DATA_FOLDER + ZONKY_CSV_FILE)
    except Exception as e:
        print('Conversion failed.', e)


def getDataFromCSVfile(filename):
    dataTable = False

    with open(DATA_FOLDER+ZONKY_CSV_FILE) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')

        for row in reader:
            if dataTable:
                if not row['3']:
                    row['3'] = 0.0
                if not row['4']:
                    row['4'] = 0.0
                if not row['5']:
                    row['5'] = 0.0
                yield row
                continue
            if row['0'] == 'Datum':
                dataTable = True
                continue

def getRowData(row):
    fee = None
    principalRepaid = None
    interestReceived = None
    chargesReceived = None

    try:
        if row['2'] == 'Poplatek za investování':
            fee = float(row['3'])

        if row['2'] == 'Splátka půjčky':
            totalReceived = float(row['3'])
            principalRepaid = float(row['4'])
            interestReceived = float(row['5'])

            if round(totalReceived, 2) != round(principalRepaid+interestReceived, 2):
                chargesReceived = abs(totalReceived-(principalRepaid+interestReceived))

        return {'rawDate': row['0'], 'fee': fee, 'principalRepaid': principalRepaid, 'interestReceived': interestReceived, 'chargesReceived': chargesReceived}
    except Exception as e:
        print(e, row)


def getFees():
    fees = 0.0

    for row in getDataFromCSVfile(DATA_FOLDER + ZONKY_CSV_FILE):
        rowData = getRowData(row)
        if rowData['fee']:
            yield (rowData['fee'], rowData['rawDate'])
            fees = fees + rowData['fee']

    yield (round(fees, 2), 'Total fees paid')


def getTotals():
    principalRepaid = 0.0
    interestsReceived = 0.0
    charges = 0.0
    fees = 0.0

    for row in getDataFromCSVfile(DATA_FOLDER+ZONKY_CSV_FILE):
        rowData = getRowData(row)

        if rowData['principalRepaid']:
            principalRepaid = principalRepaid + rowData['principalRepaid']
        if rowData['interestReceived']:
            interestsReceived = interestsReceived + rowData['interestReceived']
        if rowData['chargesReceived']:
            charges = charges + rowData['chargesReceived']
        if rowData['fee']:
            fees = fees + rowData['fee']

    yield(round(principalRepaid, 2), 'Total principal repaid')
    yield(round(interestsReceived, 2), 'Total interests received')
    yield(round(charges, 2), 'Total charges received')
    yield(round(fees, 2), 'Total fees paid')


def getTotalByMonth():
    principalRepaid = 0.0
    interestsReceived = 0.0

    previousMonthPrincipalRepaid = 0
    previousMonthInterestsReceived = 0

    currentMonthDate = datetime.strptime('1.1.2000', '%d.%m.%Y')

    yield('Month', 'X', 'Prinp.', 'Inter.', 'Fee')

    for row in getDataFromCSVfile(DATA_FOLDER+ZONKY_CSV_FILE):
        rowData = getRowData(row)

        rowDate = datetime.strptime(rowData['rawDate'], '%d.%m.%Y')

        if rowDate.month != currentMonthDate.month:
            previousMonthPrincipalRepaid = principalRepaid
            principalRepaid = 0
            previousMonthInterestsReceived = interestsReceived
            interestsReceived = 0
            currentMonthDate = rowDate

        if rowData['principalRepaid']:
            principalRepaid = principalRepaid + rowData['principalRepaid']
        if rowData['interestReceived']:
            interestsReceived = interestsReceived + rowData['interestReceived']

        if rowData['fee']:
            previousMonthFee = rowData['fee']

            # fee is the last transaction of the previous month
            if currentMonthDate.month - 1 > 0:
                previousMonthYear = currentMonthDate.month - 1, currentMonthDate.year
            else:
                previousMonthYear = 12, currentMonthDate.year - 1

            yield('Month', str(previousMonthYear[0])+"."+str(previousMonthYear[1]), round(
                previousMonthPrincipalRepaid, 2), round(previousMonthInterestsReceived, 2), round(previousMonthFee, 2))

    yield('Month', currentMonthDate.strftime('%-m.%Y'), round(principalRepaid, 2), round(interestsReceived, 2))


def getPreviousMonth():
    feePaid = None
    principalRepaid = 0.0
    interestsReceived = 0.0

    if datetime.today().month - 1 > 0:
        previousMonth = datetime.today().month - 1, datetime.today().year
    else:
        previousMonth = 12, datetime.today().year - 1

    for row in getDataFromCSVfile(DATA_FOLDER+ZONKY_CSV_FILE):
        rowData = getRowData(row)

        date = datetime.strptime(rowData['rawDate'],  '%d.%m.%Y')

        if previousMonth == (date.month, date.year):
            if rowData['principalRepaid']:
                principalRepaid = principalRepaid + rowData['principalRepaid']
            if rowData['interestReceived']:
                interestsReceived = interestsReceived + rowData['interestReceived']
        if rowData['fee']:
            feePaid = rowData['fee']

    yield (round(principalRepaid, 2), 'Total principal repaid')
    yield (round(interestsReceived, 2), 'Total interests received')
    yield (round(feePaid, 2), 'Fee paid')


def main():
    parser = argparse.ArgumentParser(description='This script produces statistics based on Zonky\'s export file.')
    parser.add_argument('-c', '--convertxls', dest='convertXls', action='store_true',
                        default=False, help='Converting ./data/wallet.xls to ./data/wallet.csv')
    parser.add_argument('-f',  '--fees', dest='getFees', action='store_true', default=False, help='Paid fees to Zonky')
    parser.add_argument('-t', '--total', dest='getTotals', action='store_true', default=False, help='Account statement')
    parser.add_argument('-tbm', '--totalbymonth', dest='getTotalByMonth', action='store_true', default=False, help='Account statement per month')
    parser.add_argument('-p', '--previousmonth', dest='getPreviousMonth', action='store_true', default=False, help='Account statement for last month')

    args = parser.parse_args()
    resultValues = []

    if args.convertXls:
        convertXLStoCSV()
    elif args.getFees:
        resultValues = getFees()
    elif args.getTotals:
        resultValues = getTotals()
    elif args.getTotalByMonth:
        resultValues = getTotalByMonth()
    elif args.getPreviousMonth:
        resultValues = getPreviousMonth()
    else:
        parser.print_help()

    for list in resultValues:
        print(utils.getTabbedStringFromValueList(list))

    return


if __name__ == '__main__':
    main()
