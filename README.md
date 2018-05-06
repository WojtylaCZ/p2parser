# P2Parser toolkit

This is a set of parsers to automate and perform data extraction from P2P platforms.

It contains a few statistics (fees paid, total interests, last month account statement etc..)


## Zonky (zonky.cz)

Data extraction is based on an export file from account wallet.xls (penezenka) - wallet.xls

- It starts with the python script zonky.cz
- Download the wallet.xls to ~/data folder
- To standardize I/O and to avoid XLS file handling, convert wallet.xls to zonky.csv using **-c** flag **first**.
- Execute ~/zonky.py -h to show help. 

## Mintos (mintos.com)
**_coming soon_**

## Twino (twino.eu)
**_coming soon_**

## Lendy (lendy.co.uk)
**_coming soon_**