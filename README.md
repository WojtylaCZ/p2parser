# P2Parser toolkit

This is a set of parsers to automate and perform data extraction from P2P platforms.

It also contains a few statistics method to get overview of account statement (fees paid, total interests, last month account statement etc..)


## Zonky (zonky.cz)

Data extraction is based on an export file from account (penezenka) - wallet.xls

- Download the wallet.xls to ~/data folder
- Start with the python script zonky.cz
- To standardize I/O and to avoid XLS file handling, convert wallet.xls to zonky.csv using **-c** flag **first**.
- Execute ~/zonky.py -h to show help. 

## Mintos (mintos.com)
**_coming soon_**

## Twino (twino.eu)
**_coming soon_**

## Lendy (lendy.co.uk)
**_coming soon_**