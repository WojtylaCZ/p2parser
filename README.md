# P2Parser toolkit

This is a set of parsers to automate and perform data extraction from P2P platforms.

It contains statistics methods to get your account statement (ROI, fees paid, total interests, last month stats.)

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

```python
python zonky.py -h
```
```python
python twino.py -tbm
```

## P2P platforms parsers

## General info

1. Download an export file from your account first.
2. Convert it to **.csv** file using the script. Reason behind this is to standardize a common source and to avoid _.xls, .xlsx, .pages etc._ file types handling.
3. Run the appropriate script with the **-h** parameter to know what the parser can do for you.


## Zonky (zonky.cz)

Data extraction is based on exported file from your account (penezenka) - wallet.xls

- To convert data/wallet.xls to data/zonky.csv,  use **zonky.py -c** flag first.
- Execute python zonky.py -h to show options.

## Mintos (mintos.com)
**_coming soon_**

## Twino (twino.eu)
- To convert data/InvestorAccountEntry_XXXX.xlsx to data/twino.csv,  use **twino.py -c XXXX** first.
- Execute python twino.py -h to show options.

## Lendy (lendy.co.uk)
**_coming soon_**


## Contributing
1. Fork it (<https://github.com/WojtylaCZ/p2parser/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
