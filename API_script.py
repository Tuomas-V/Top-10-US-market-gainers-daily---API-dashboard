import requests
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.widgets import Button



# pulling top 20 daily gainers & losers
gain_url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=API_key_here'
gain_request = requests.get(gain_url)
gain_data = gain_request.json()

df = pd.json_normalize(gain_data['top_gainers'],meta=['ticker', 'price', 'change_amount', 'change_percentage', 'volume'])
df['ticker'] = df['ticker'].replace(r'[^\w\s]|_', '', regex=True)

data = df.head(10)
ticker_list = data['ticker'].values.tolist()

company_df = pd.DataFrame()

# pulling company names for each ticker
for tick in ticker_list:
    ticker_url = 'https://financialmodelingprep.com/stable/search-symbol?query={0}&apikey=API_key_here'.format(tick)
    ticker_request = requests.get(ticker_url)
    ticker_data = ticker_request.json()

    new_df = pd.json_normalize(ticker_data)
    company_df = pd.concat([company_df, new_df], ignore_index=True)

# cleanup of results
company_df.drop_duplicates(inplace=True)
company_df.rename(columns= {'symbol':'ticker'}, inplace=True)
company_df = company_df[company_df['ticker'].isin(ticker_list)]

merged_data = data.merge(company_df[['ticker', 'name']], on='ticker')

# formatting data before visualization
merged_data['change_float'] = merged_data['change_percentage'].str.strip('%').astype(float)
merged_data['change_float'] = round(merged_data['change_float'], 2)
merged_data['price'] = round(merged_data['price'].astype(float), 2)
merged_data['price_str'] = '$' + merged_data['price'].astype(str)
merged_data['short_name'] = merged_data['name'].str.slice(0,35)
merged_data.sort_values('change_float', ascending=True, inplace=True)



# Visualization
#===============

background_color = "#232323"
text_color = "#E7E7E7"
price_color = "#000000"
title_color = "#FFFFFF"
bar_color = "#01A7A4"
highlight_color = "#CD7100"
button_default = "#1A1A1A"
button_clicked = "#424242"

# figure & plots
fig, ax = plt.subplots(figsize=(13,7))
bars = plt.barh(merged_data['ticker'], merged_data['change_float'], height=0.45, color=bar_color)
plt.title('Top 10 Gainers, US market', fontweight='bold', color=title_color, y=1.05)
plt.subplots_adjust(left=0.23)
plt.figtext(0.44, 0.08, 'End of day data for top 10 US market gainers', color=text_color)

# spines
ax.spines[['right', 'top', 'bottom']].set_visible(False)
ax.xaxis.set_visible(False)
ax.spines['left'].set_color(text_color)
ax.tick_params(axis='y', colors=text_color)

# bar labels
ax.bar_label(bars, padding=2, fmt='%0.2f%%', color=text_color)
ax.bar_label(bars, merged_data['price_str'], label_type='center', padding=0, color=price_color)

# background
ax.set_facecolor(background_color)
fig.patch.set_facecolor(background_color)

ax.margins(y=0.01)

# buttons
def c_button(change):
    ax.yaxis.set_ticklabels(merged_data['short_name'])
    company_button.color = button_clicked
    ticker_button.color = button_default
    plt.draw()

def t_button(change):
    ax.yaxis.set_ticklabels(merged_data['ticker'])
    ticker_button.color = button_clicked
    company_button.color = button_default
    plt.draw()

company_axes = plt.axes([0.1, 0.9, 0.08, 0.055])
company_button = Button(company_axes, 'Company', color=button_default)
company_button.label.set_color(text_color)
company_button.label.set_size(11)
company_button.hovercolor = button_clicked
company_button.on_clicked(c_button)

ticker_axes = plt.axes([0.18, 0.9, 0.08, 0.055])
ticker_button = Button(ticker_axes, 'Ticker', color=button_clicked)
ticker_button.label.set_color(text_color)
ticker_button.label.set_size(11)
ticker_button.hovercolor = button_clicked
ticker_button.on_clicked(t_button)

plt.show()