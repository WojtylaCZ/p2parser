# P2Parser toolkit

This toolkit provides an overview about your money/investments on major P2P platforms. For example, would you like to know **how much money have you received on interests last month** or **what is your ROI at different P2P platforms**? 
Then this toolkit is for you.

This toolkit is a set of same functions for different P2P platforms. 

It contains statistics methods to get your account statement (ROI, fees paid, total interests, last month stats.)

So far, there are following summary statistic functions (if you wish to have more or different one, open an issue, write me!):

```
  -f,   --fees              Fees paid
  -t,   --total             Total account statement
  -tbm, --totalbymonth      Account statement per month
  -p,   --previousmonth     Account statement for last month
  -cf,  --cashflow          Cashflow actions within the account
```

The output looks like following example. Values are separated by a tab space, so you can conveniently copy that to any spreadsheet while keeping the table layout.

```
Month       CashInGame  Inter.	    Fee         ROI         Prinp.
1.2018	    85541.03	362.69	    -20.62      0.009625    1816.37
2.2018	    77761.64	254.37	    -18.05	0.008512    2172.83
3.2018	    67995.41	159.05	    -18.26	0.005029    2061.62
4.2018	    58136.41	151.41	    -15.19	0.004841    1604.14
5.2018	    40025.03	241.57	    -14.46	0.011341    1439.91
```

## Getting Started

### Prerequisites

```
python, pip
```

### Installing

Install requirements packages.

```
pip install -r requirements.txt
```

## Usage example

```
python zonky.py -h
```
```
python twino.py -tbm
```

## P2P platforms parsers

## General info

1. Download an account statement, transaction export or other log file within your account from the platform first.
2. Convert it to **.csv** file using the script. The reason behind this is to standardize a common source and to avoid _.xls, .xlsx, .pages etc._ file types handling.
3. Run the appropriate script with the **-h** parameter to know what the parser can do for you. You can run it in a fashion `python foo.py -h` or `./foo.py -h`.

## Zonky ([zonky.cz](https://zonky.cz))

Data extraction is based on exported file from your account (penezenka) - `wallet.xls`

- To convert `wallet.xls` at `FILEPATH` to `data/zonky.csv`,  use first:
```
python zonky.py -c FILEPATH
```

- Execute python `python zonky.py -h` to show options.

## Mintos ([mintos.com](https://mintos.com))
**_coming soon_**

## Twino ([twino.eu](https://twino.eu))

- To convert `InvestorAccountEntry_WXYZ.xlsx` at `FILEPATH` to `data/twino.csv`, start with:

```
python twino.py -c FILEPATH
```
- Execute python `python twino.py -h` to show options.

## Lendy ([lendy.co.uk](https://lendy.co.uk))

- Lendy's transaction history logfile is already a CSV file, but it still needs to be converted to get better and standardized output.
- Therefore, start with the command below using whatever FILEPATH to the original file. That will create `data/lendy.csv` file.

```
python lendy.py -c FILEPATH
````
- Then, you can run the script to get different statistics as usual, run `python lendy.py -h`


## Lending club ([lendingclub.com](https://lendingclub.com/))
**_coming soon_**

## Contributing
1. Fork it (<https://github.com/WojtylaCZ/p2parser/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

### Codestyle:
To follow pep8 codestyle, see mistakes by:
```
pycodestyle --show-pep8 FILEPATH
```

To auto apply possible changes, use:
```
autopep8 -v --in-place --aggressive --aggressive FILEPATH
```