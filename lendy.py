#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P2P platform Lendy.co.uk parser for Lendy_Statement_YYYYMMDD-YYYYMMDD.csv file and set of statistics functions
"""

import pandas as pd
import csv
from datetime import datetime
import argparse
import os

import utils

DATA_FOLDER = 'data/'

LENDY_CSV_FILE = 'lendy.csv'


def convertToStandardCSV(sourceFile):
    try:
        destinationFile = os.path.dirname(os.path.realpath(__file__)) + '/' + DATA_FOLDER + LENDY_CSV_FILE
        print('Trying to load', sourceFile)

        df = pd.read_csv(sourceFile)
        print('File', sourceFile, 'loaded.')

        # quick content check
        if list(df) == [
            'Txn Date',
            'Transaction type',
            'Loan part ID',
            'Loan part value',
            'Loan part detail',
            'Loan ID',
            'Start date',
            'End date',
            'Txn Amount',
                'Balance']:
            print('File content format looks good.')
        else:
            raise Exception('File content format looks bad. Sorry')

        # reverse row order
        df = df[::-1]

        df.to_csv(destinationFile, header=[str(x) for x in range(len(df.columns))], encoding='utf-8', index=False)
        print('File', sourceFile, 'converted to', destinationFile)

        print('First 2 lines of the content:')
        print(df.head(2).to_string(index=False, header=False))

        print('Last 2 lines of the content:')
        print(df.tail(2).to_string(index=False, header=False))
    except Exception as e:
        print('Conversion failed.', e)


def getDataFromCSVfile(filepath):

    with open(filepath) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')

        for row in reader:
            if not row['0']:
                continue
            if not row['5']:
                row['5'] = 0.0
            yield row


def getRowData(row):
    fee = None
    principalRepaid = None
    interestReceived = None
    chargesReceived = None
    cashFlowChange = None

    try:
        if row['1'] == 'Deposit':
            cashFlowChange = float(row['8'])

        # TODO withdrawal?
        # if row['1'] == 'Deposit':
        #     cashFlowChange = float(row['8'])

        if row['1'] == 'Interest':
            interestReceived = float(row['8'])

        if row['1'] == 'Bonus':
            interestReceived = float(row['8'])

        if row['1'] == 'Capital Repayment' or row['1'] == 'Capital repayment':
            principalRepaid = float(row['8'])

        return {'rawDate': row['0'], 'fee': fee, 'principalRepaid': principalRepaid,
                'interestReceived': interestReceived, 'chargesReceived': chargesReceived, 'cashFlowChange': cashFlowChange}
    except Exception as e:
        print(e, row)


def getCashInGame(cashInGame, rowData):
    if rowData['cashFlowChange']:
        cashInGame = cashInGame + rowData['cashFlowChange']
    if rowData['interestReceived']:
        cashInGame = cashInGame + rowData['interestReceived']
    if rowData['chargesReceived']:
        cashInGame = cashInGame + rowData['chargesReceived']
    if rowData['fee']:
        cashInGame = cashInGame + rowData['fee']
    return cashInGame


def getFees():
    fees = 0.0

    for row in getDataFromCSVfile(DATA_FOLDER + LENDY_CSV_FILE):
        rowData = getRowData(row)
        if rowData['fee']:
            yield (rowData['rawDate'], format(rowData['fee'], '.2f'))
            fees = fees + rowData['fee']

    yield ('Total fee', format(fees, '.2f'))


def getTotals():
    principalRepaid = 0.0
    interestsReceived = 0.0
    charges = 0.0
    fees = 0.0
    cashInGame = 0.0

    for row in getDataFromCSVfile(DATA_FOLDER + LENDY_CSV_FILE):
        rowData = getRowData(row)
        cashInGame = getCashInGame(cashInGame, rowData)

        if rowData['principalRepaid']:
            principalRepaid = principalRepaid + rowData['principalRepaid']
        if rowData['interestReceived']:
            interestsReceived = interestsReceived + rowData['interestReceived']
        if rowData['chargesReceived']:
            charges = charges + rowData['chargesReceived']
        if rowData['fee']:
            fees = fees + rowData['fee']

    yield(format(cashInGame, '.2f'), 'Cash in game')
    yield(format(interestsReceived, '.2f'), 'Total interests received')
    yield(format(charges, '.2f'), 'Total charges received')
    yield(format(fees, '.2f'), 'Total fees paid')
    yield(format(principalRepaid, '.2f'), 'Total principal repaid')


def getPreviousMonth():
    cashInGame = 0.0

    feePaid = 0.0
    principalRepaid = 0.0
    interestsReceived = 0.0
    cashInGameForThisMonth = None

    if datetime.today().month - 1 > 0:
        previousMonth = datetime.today().month - 1, datetime.today().year
    else:
        previousMonth = 12, datetime.today().year - 1

    yield (str(previousMonth[0]) + "." + str(previousMonth[1]), 'Considered month')

    for row in getDataFromCSVfile(DATA_FOLDER + LENDY_CSV_FILE):
        rowData = getRowData(row)

        date = datetime.strptime(rowData['rawDate'], '%d/%m/%Y')

        if previousMonth == (date.month, date.year):
            if rowData['principalRepaid']:
                principalRepaid = principalRepaid + rowData['principalRepaid']
            if rowData['interestReceived']:
                interestsReceived = interestsReceived + rowData['interestReceived']
            if rowData['chargesReceived']:
                interestsReceived = interestsReceived + rowData['chargesReceived']
            if not cashInGameForThisMonth:
                cashInGameForThisMonth = cashInGame

        cashInGame = getCashInGame(cashInGame, rowData)
        if rowData['fee']:
            feePaid = rowData['fee']

    yield (format(cashInGameForThisMonth, '.2f'), 'Cash in game for this month')
    yield (format(principalRepaid, '.2f'), 'Total principal repaid')
    yield (format(interestsReceived, '.2f'), 'Total interests received')
    yield (format(feePaid, '.2f'), 'Fee paid   ')


def getTotalByMonth():
    principalRepaid = 0.0
    interestsReceived = 0.0
    cashInGame = 0.0

    previousMonthPrincipalRepaid = 0
    previousMonthInterestsReceived = 0
    previousMonthCashInGame = 0

    currentMonthDate = datetime.strptime('1.1.2000', '%d.%m.%Y')
    currentMonthCashInGame = 0

    newMonth = False

    roi = 0.0

    yield('Month', 'CashInGame', 'Inter.', 'Fee', 'ROI', 'Princip.')

    for row in getDataFromCSVfile(DATA_FOLDER + LENDY_CSV_FILE):
        rowData = getRowData(row)

        rowDate = datetime.strptime(rowData['rawDate'], '%d/%m/%Y')

        if rowDate.month != currentMonthDate.month:
            previousMonthPrincipalRepaid = principalRepaid
            principalRepaid = 0
            previousMonthInterestsReceived = interestsReceived
            interestsReceived = 0
            previousMonthCashInGame = currentMonthCashInGame

            currentMonthCashInGame = cashInGame
            currentMonthDate = rowDate
            newMonth = True

        cashInGame = getCashInGame(cashInGame, rowData)

        if rowData['principalRepaid']:
            principalRepaid = principalRepaid + rowData['principalRepaid']
        if rowData['interestReceived']:
            interestsReceived = interestsReceived + rowData['interestReceived']
        if rowData['chargesReceived']:
            interestsReceived = interestsReceived + rowData['chargesReceived']
        if newMonth:
            previousMonthFee = rowData['fee'] or 0.0
            newMonth = False

            # fee is negative number
            if previousMonthCashInGame > 0:
                roi = (previousMonthInterestsReceived + previousMonthFee) / previousMonthCashInGame

            # fee is the last transaction of the previous month
            if currentMonthDate.month - 1 > 0:
                previousMonthYear = currentMonthDate.month - 1, currentMonthDate.year
            else:
                previousMonthYear = 12, currentMonthDate.year - 1

            yield(str(previousMonthYear[0]) + "." + str(previousMonthYear[1]), format(previousMonthCashInGame, '.2f'),
                  format(previousMonthInterestsReceived, '.2f'), format(previousMonthFee, '.2f'), format(roi, '.4f'),
                  format(previousMonthPrincipalRepaid, '.2f'))

    # ongoing month
    # yield(currentMonthDate.strftime('%-m.%Y'), round(cashInGame, 2), round(interestsReceived, 2), '', '', round(principalRepaid, 2))


def getCashFlow():
    for row in getDataFromCSVfile(DATA_FOLDER + LENDY_CSV_FILE):
        rowData = getRowData(row)

        if rowData['cashFlowChange']:
            yield (rowData['rawDate'], format(rowData['cashFlowChange'], '.2f'))


def main():
    parser = argparse.ArgumentParser(description='This script produces statistics based on Lendy\'s transactions file from My Account - Transactions tab.')
    parser.add_argument('-c', '--convert', dest='convert', action='store', default=False, metavar=('FILEPATH'),
                        help='Converting FILEPATH to ' + DATA_FOLDER + LENDY_CSV_FILE)
    parser.add_argument('-f', '--fees', dest='getFees', action='store_true', default=False, help='Paid fees to Lendy')
    parser.add_argument('-t', '--total', dest='getTotals', action='store_true', default=False, help='Account statement')
    parser.add_argument('-tbm', '--totalbymonth', dest='getTotalByMonth', action='store_true', default=False, help='Account statement per month')
    parser.add_argument('-p', '--previousmonth', dest='getPreviousMonth', action='store_true', default=False, help='Account statement for last month')
    parser.add_argument('-cf', '--cashflow', dest='getCashFlow', action='store_true', default=False, help='Cashflow actions within the account')

    args = parser.parse_args()
    resultValues = []

    if args.convert:
        convertToStandardCSV(args.convert)
    elif args.getFees:
        resultValues = getFees()
    elif args.getTotals:
        resultValues = getTotals()
    elif args.getTotalByMonth:
        resultValues = getTotalByMonth()
    elif args.getPreviousMonth:
        resultValues = getPreviousMonth()
    elif args.getCashFlow:
        resultValues = getCashFlow()
    else:
        parser.print_help()

    for list in resultValues:
        print(utils.getTabbedStringFromValueList(list))

    return


if __name__ == '__main__':
    main()
