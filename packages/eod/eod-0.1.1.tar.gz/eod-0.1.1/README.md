# EOD Historical data SDK

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://shields.io/) ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

# Contents

1. [General description](#general-description-arrow_up)
2. [Requirements](#requirements-arrow_up)
3. [Installation](#installation-arrow_up)
4. [Demo](#demo-arrow_up)
5. [Documentation](#documentation-arrow_up)
	- [Historical Prices, Splits and Dividends Data APIs](#historical-prices-splits-and-dividends-data-apis-arrow_up)
	- [Fundamental and Economic Financial Data APIs](#fundamental-and-economic-financial-data-apis-arrow_up)
	- [Exchanges Financial APIs](#exchanges-financial-apis-arrow_up)
6. [Disclaimer](#disclaimer-arrow_up)

## General description [:arrow_up:](#eod-historical-data-sdk)
This library is the Python 🐍 unofficial SDK for the EOD Historical data REST API. It's intended to be used for data extraction for financial valuations, macroeconomic analyses, sentiment analysis, option strategies, technical analysis, development of machine learning models, and more!

## Requirements [:arrow_up:](#eod-historical-data-sdk)
- You need to request an API key with the EOD team. Create your account at the following [link](https://eodhistoricaldata.com/)
	- ***Please be aware of the pricing plans and policies. Different plans have different data accesses.***
- ```Python``` >= 3.8

If any update or change is informed through the [Medium site](https://eod-historical-data.medium.com/) site of the API, I will implement it SDK. The revisions will be every month.

## Installation [:arrow_up:](#eod-historical-data-sdk)

```python
pip install #define a catchy name
```

## Demo [:arrow_up:](#eod-historical-data-sdk)

```python

```

## Documentation [:arrow_up:](#eod-historical-data-sdk)
Please be aware that some descriptions will come directly from the API's documentation because no further explanations were needed for the specific method. Additionally, for the sake of simplicity, I will use the following convention along with the whole document: 

```python

import # catchy library name
# create the instance of the SDK
api_key = 'YOUR_API_KEY_GOES_HERE'
client = EodHistoricalData(api_key)
```

### Historical Prices, Splits and Dividends Data APIs [:arrow_up:](#eod-historical-data-sdk)
- **Stock Price Data API (End-Of-Day Historical Data)**: Retrieve end-of-day data for Stocks, ETFs, Mutual Funds, Bonds (Government and Corporate), Cryptocurrencies, and FOREX pairs.
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```period```(str): Optional - Use ```'d'``` for daily, ```'w'``` for weekly, ```'m'``` for monthly prices. By default, daily prices will be shown.
		- ```order```(str): Optional - Use ```'a'``` for ascending dates (from old to new), ```'d'``` for descending dates (from new to old). By default, dates are shown in ascending order.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
	- Usage:
```python
# AngloAmerican stock that trades in the London Stock Exchange
resp = client.get_prices_eod('AAL.LSE', period='d', order='a', from_='2017-01-05')
# Swiss goverment Bond
resp = client.get_prices_eod('SW10Y.GBOND', period='w')
# Corportae Bond
resp = client.get_prices_eod('US00213MAS35.BOND')
```
- **Live (Delayed) Stock Prices API**: The method supports almost all symbols and exchanges worldwide, and the prices provided have a 15-20 minutes delay. The method also offers combinations of multiple tickers with just one request. The only supported interval is the 1-minute interval. **The UNIX standard is used for the timestamp**.
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```s```(str): Optional - Additional instruments to retrieve data.
		- ```filter_```(str): Optional - Name of the field to retrieve, check the response for the available fields.
	- Usage:
```python
# One instrument
resp = client.get_prices_live('AAL.LSE', filter_='close')
# Multple instruments
resp = client.get_prices_live('AAL.LSE', s='GLD,QVAL,QMOM,EUR.FOREX,VTI,SW10Y.GBOND')
```
- **Historical Splits, Dividends and Short Interest API**: Get the historical dividends, splits, and short interest for any stock.
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
	- Usage:
```python
# Get dividend data
resp = client.get_dividends('AAPL.US', from_='2000-03-01')
# Get short interest data (indicates how many shares of a company are currently sold short and not yet covered. Indicates the sentiment around a company)
resp = client.get_short_interest('AAPL.US')
# Get the splits for a company
resp = client.get_splits('AAPL.US', from_='1994-01-01', to='2020-10-24')
```
- **Technical Indicator API**: Retrieve technical data associated with the price action of an instrument. The data is mainly oriented to technical indicators rather than any other price-action methodology (e.g., Elliot Waves, Wyckoff, etc.)
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```function```(str): Required - The function that will be applied to data series to get technical indicator data.
		- ```period```(int): Optional - The number of data points used to calculate each indicator value. Valid range from 2 to 100000 with. The default value is 50.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
		- ```order```(str): Optional – Use ```'a'``` for ascending dates (from old to new) and ```'d'``` for descending dates (from new to old). By default, dates are shown in ascending order.
		- ```splitadjusted_only```(int): Optional – The default value is 0. By default, the API calculates data for some functions by closes adjusted with splits and dividends. If you need to calculate the data by closes adjusted only with splits, set this parameter to 1. The available functions for technical analysis are displayable via the ```get_get_indicator_name()``` method.
		- ```filter_```(str): Optional - Ability to get only the last value. The syntax is the following: ```last_indicator_name```, for instance, ```last_ema```, ```last_volume```, etc.
	- Usage:
```python
# Get the available indicators in the API. This method does not accept any parameter.
resp = client.get_indicator_name()
# Get data for a specific indicator, in this case the parabolic SAR
resp = client.get_instrument_ta('AAPL', function='sar', from_='2020-03-01', to='2021-06-30', period=50, filter_='last_sar')
```
- **Intraday Historical Data API**: Get intraday historical stock price data for US (NYSE and NASDAQ), Canada, and MOEX tickers. The 1-minute interval includes the pre-market and after-hours trading data from 2004 (more than 15 years of the data), and for the 5-minute intervals, the data starts from October 2020. For other tickers (mainly for international instruments), it is only available the 5-minute intervals and only from October 2020.
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```interval```(str): Required - use ```'5m'``` for 5-minutes intervals and ```'1m'``` for 1-minute intervals.
		- ```from_```(str) and ```to```(str): Optional - Use these parameters to filter data by datetime. Parameters should be passed in UNIX time with UTC timezone, for example, these values are correct: ```from_=1564752900``` and ```to=1564753200``` and correspond to 2019-08-02 13:35:00 and 2019-08-02 13:40:00 respectively. The maximum period between 'from_' and 'to' is 100 days. Try this site to converte dates into UNIX https://www.unixtimestamp.com/index.php
	- Usage:
```python
resp = client.get_prices_intraday('EUR.FOREX', interval='5m', from_='1620136800', to='1620414000')
```
- **Options Data API**:  Stock options data for top US stocks from NYSE and NASDAQ, the data for Options starts from April 2018. Options data is updated daily; however, the API does not provide a history for options contracts prices or other related data. That means: for each contract, there is only the current price, bid/ask, etc. 
1. **IMPORTANT!** For backward compatibility, you should use the ```from_``` parameter with any value before the expiration date, the API recommends '2000-01-01'. 
2. **Note**: option greeks and some additional value are available only for options with expiration date Feb 15, 2019, or later.
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
		- ```contract_name```(str): Optional - Name of a particular contract.
		- ```trade_date_to```(str): Optional - filters OPTIONS by ```lastTradeDateTime```. Default value: is blank.
	- Usage:
```python
resp = client.get_stock_options('AAPL.US')
```
### Fundamental and Economic Financial Data APIs [:arrow_up:](#eod-historical-data-sdk)
- **Insider Transactions API**: The insider transactions API data is available for all US companies that report Form 4 to the SEC. Insider trading involves trading in a public company’s stock by someone who has non-public, material information about that stock for any reason.
	- Parameters:
		- ```code```(str): Optional - Name of the company to retrieve data. By default, all possible symbols will be displayed.
		- ```limit```(int): Optional - The limit for entries per result, from 1 to 1000. Default value: 100.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
	- Usage:
```python
# Get the insider transactions for all companies
resp = client.get_insider_transactions()
# Get insider transactions for a specific company
resp = client.get_insider_transactions(code='AAPL.US')
```
- **Fundamental Data: Stocks, ETFs, Mutual Funds, Indices**: Access to fundamental data API for stocks, ETFs, Mutual Funds, and Indices from different exchanges and countries. Almost all major US, UK, EU, India, LATAM, and Asia exchanges are available.
	- Parameters:
		- ```symbol```(str): Required - Name of the instrument to retrieve data.
		- ```filter_```(str): Optional - Multi-layer filtering helps to reduce the output of the request. Different layers are divided with ```::``` and it’s possible to have as many layers as you need. Additionally, you can request multiple fields from a particular layer using ```,```. Be aware that the order of the layers is from the macro keys to the micro-level.
	- Usage:
```python
resp = client.get_fundamental_equity('QVAL.US') # ETF
# Stock - request the quarterly statements
resp = client.get_fundamental_equity('AAPL.US', filter_='Financials::Balance_Sheet::quarterly')
# Stock - Request specific fields from the General layer
resp = client.get_fundamental_equity('AAPL.US', filter_='General::Code,General,Earnings')
resp = client.get_fundamental_equity('SWPPX.US') # Mutual Fund
resp = client.get_fundamental_equity('GSPC.INDX') # Index
```
- **Calendar. Upcoming Earnings, Trends, IPOs and Splits**
	- Parameters:
		- ```symbols```(str): Required - You can request specific symbols to get historical and upcoming data. You can use one symbol: ```'AAPL.US'``` or several symbols separated by a comma: ```'AAPL.US,MS.US'```. For the upcoming IPOs and the Splits, the ```symbols``` parameter **is not required**.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
	- Usage:
```python
# Upcoming Earnings
resp = client.get_calendar_earnings(symbols='AAPL.US,MSFT.US,AI.PA', to='2020-12-01')
# Earnings Trends
resp = client.get_calendar_trends(symbols='AAPL.US,MSFT.US,AI.PA')
# Upcoming IPOs
resp = client.get_calendar_ipos(from_='2016-01-01')
# Upcoming Splits
resp = client.get_calendar_splits(from_='2016-01-01')
```
- **Macroeconomics Data and Macro Indicators API**: Macroeconomics is a part of economics dealing with the performance, structure, behavior, and decision-making of an economy as a whole. The Macroeconomics data API includes regional, national, and global economies. EOD provides the data for more than 30 macro indicators such as GDP, unemployment rates, national income, price indices, inflation rates, consumption, international trades, and many other significant indicators.
	- Parameters:
		- ```country```(str): Required - Defines the country for which the indicator will be shown. The country should be defined in the Alpha-3 ISO format. Possible values: CHL, FRA, DEU, etc.
		- ```indicator```(str): Optional - Defines which macroeconomics data indicator will be shown. The default value is ```'gdp_current_usd'```.
	- Usage:
```python
# Get the available macroindicators names
resp = client.get_macro_indicator_name()
# Request the Chilean interest rate
resp = client.get_macro_indicator('CHL', indicator='real_interest_rate')
```
- **Bonds Fundamentals API**: Bond covenants details.
	- Parameters:
		- ```cusip```(str): Required - CUSIP of a particular bond, it’s also could be an ISIN. Other IDs are not supported at the moment.
	- Usage:
```python
resp = client.get_fundamentals_bonds(cusip='US00213MAS35')
```
### Exchanges Financial APIs [:arrow_up:](#eod-historical-data-sdk)
- **Bulk API for EOD, Splits and Dividends**: This method allows you to download the data for an entire exchange for a particular day. It works for end-of-day historical data feed and splits and dividends data as well. You can also use NYSE or NASDAQ as exchange symbols for US tickers to get data only for NYSE or NASDAQ exchange. With this method is no longer necessary to perform thousands and thousands of API requests per day.
	- Parameters:
		- ```type_```(str): Optional - Which type of data to return. The available options are ```'splits'``` or ```'dividends'```. If it's blank, the default response will be the market end-of-day data.
		- ```date```(str): Optional - By default, the data for last trading day will be downloaded, but if you need any specific date enter a date with the following format YYYY-MM-DD
		- ```symbols```(str): Optional - Name of the instrument(s) to retrieve data.
		- ```filter_```(str): Optional - Extended the end-of-day market data to include technicals by using ```'extended'```. By default the value is blank.
	- Usage:
```python
# Request end-of-day data for the Santiago of Chile exchange.
resp = client.get_bulk_markets(exchange='SN')
# Request the latest dividends for the companies that trade in NYSE.
resp = client.get_bulk_markets(exchange='NYSE', type_='dividends')
# Request market and extended data for the selected US symbols.
resp = client.get_bulk_markets(exchange='US', date='2021-08-06', symbols='QVAL,MSFT,QMOM,HOOD', filter_='extended')
```
- **Get List of Tickers**: Request available exchanges, and instruments for each exchange or market.
	- Parameters:
		- ```exchange```(str): Required - Name of the exchange or market to request symbols. This parameter is only valid for especif exchanges, check the usage for details.
	- Usage:
```python
# Get List of available exchanges, this method does not allow any parameter.
resp = client.get_exchanges()
# Get List of Tickers for Borsa Italiana Certificates
resp = client.get_exchange_symbols(exchange='ETLX')
```
- **Trading Hours and Market Holidays**
	- Parameters:
		- ```exchange```(str): Required - Name of the exchange.
	- Usage:
```python
# Request the London Stock Exchange details
resp = client.get_exchange_details(exchange='LSE')
```
- **Financial News API**: The Financial News method is a powerful tool that helps you get company news and filter out them by date, type of news, and specific tickers according to the given parameters. Despite that all parameters are optional, you need to input at least one of them. See the usage for guidance.
	- Parameters:
		- ```s```(str): Optional - The ticker code to get news for.
		- ```t```(str): Optional - The tag to get news on a given topic. You can find the list of supported topics in the usage area.
		- ```limit```(str): Optional - The number of results should be returned with the query. Default value: 50, minimum value: 1, maximum value: 1000.
		- ```offset```(str): Optional - The offset of the data. Default value: 0, minimum value: 0, maximum value: 100. For example, to get 100 symbols starting from 200 you should use limit=100 and offset=200.
		- ```from_```(str) and ```to```(str): Optional - The format is 'YYYY-MM-DD'. If you need data from Jan 5, 2017, to Feb 10, 2017, you should use ```from_='2017-01-05'``` and ```to='2017-02-10'```
	- Usage:
```python
# Get the available financial tags
tags = client.get_financial_tags()
import random
specific_tag = random.choice(tags) # choose a random tag from the available list
# Request the news from Anglo American
resp = client.get_financial_news(s='AAL.LSE')
# Request data for the selected tag
resp = client.get_financial_news(t=specific_tag)
```
- **Stock Market Screener API**: Filter stocks based on some criteria. ***THIS METHOD IS UNDER BETA MODE; ONLY THE SIGNALS PARAMETER WORKS, THE FILTERS IS NOT. PLEASE USE IT SEPARATELY***
	- Parameters:
		- ```filters```(--): **DO NOT USE THIS PARAMTER, IS UNDER REVISION**
		- ```signals```(str): Required - Alert to use as a filter. The available options can be requested by the method ```get_screener_signals```.
		- ```sort```(str): Optional - Sorts all fields with type Number in ascending/descending order. Usage: ```sort='field_name.(asc|desc)'```.
		- ```limit```(str): Optional - The number of results should be returned with the query. Default value: 50, minimum value: 1, maximum value: 100.
		- ```offset```(str): Optional - The offset of the data. Default value: 0, minimum value: 0, maximum value: 100. For example, to get 100 symbols starting from 200 you should use limit=100 and offset=200.
	- Usage:
```python
# Request available signals
resp = client.get_screener_signals()
# Request companies with a new 200 day new high and a price bigger than expected by wallstreet analysts.
resp = client.get_instrument_screener(signals='200d_new_hi,wallstreet_hi')
```
- **Search API for Stocks, ETFs, Mutual Funds and Indices**: Search instruments by phrases or keywords.
	- Parameters:
		- ```query_string```(str): Required - Could be any string with a ticker code or company name. Examples: ```'AAPL'```, ```'Apple Inc'```, ```'Apple'```. You can also use ISINs for the search: ```'US0378331005'```. There are no limitations to a minimum number of symbols in the query string.
		- ```limit```(str): Optional - he number of results should be returned with the query. Default value: 15. If the limit is higher than 50, it will be automatically reset to 50.
		- ```bonds_only```(int): Optional - The default value is 0 and search returns only stocks, ETFs, and funds. To get bonds in result use value 1: ```bonds_only=1```.
	- Usage:
```python
# Search instrument with the word .com
resp = client.get_search_instrument(query_string='.com')
# Search bonds related to Chile
resp = client.get_search_instrument(query_string='Chile', bonds_only=1)
```

## Disclaimer [:arrow_up:](#eod-historical-data-sdk)

The information in this document is for informational and educational purposes only. Nothing in this document can be construed as financial, legal, or tax advice. The content of this document is solely the opinion of the author, who is not a licensed financial advisor or registered investment advisor. The author is not affiliated as a promoter of EOD Historical Data services.

This document is not an offer to buy or sell financial instruments. Never invest more than you can afford to lose. You should consult a registered professional advisor before making any investment.