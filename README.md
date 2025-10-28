# Top-10-US-market-gainers-daily---API-dashboard
The graph lists top 10 US market gainers (end of day data) through Alpha Vantage API &amp; Financial Modeling Prep API

<img src="/Screenshots/output1.png">

This python graph pulls end of day data from two US market APIs. The data is then automatically cleaned and formatted properly.<br/> 
It shows the company name (or alternatively ticker) and orders them by stock value increase percentage and displays the current stock price.

First it pulls top gainers & losers from one API, which gives the company tickers. Then the company names are pulled from second API using corresponding tickers.

<img src="Screenshots/output2.png">

Alpha Vantage API allows 25 request per day and Financial Modeling Prep API allows 250 request per day, which both are enough as this is end of day data and thus needs to only update once per day.

The project was initially developed as python notebook to allow for testing without sending excess API requests.

Considerations:<br/> 
- What if two companies share similar name?
  - The data is handled by the tickers which are always unique
- What if API pull results less than 10 companies?
  - The graph shows any amount of companies it can, up to ten
- What if one company has a very high percentage compared to the other companies?
  - The bars in the graph scale to fit every company
- What if the company name is extremely long?
  - Company names are trimmed to maximum of 35 characters

Data sources:<br/> 
- [Alpha Vantage API](https://www.alphavantage.co/)<br/> 
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/)
