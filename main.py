import pandas as pd
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv
import os

path_to_dotenv = find_dotenv() 
load_dotenv(path_to_dotenv) 
apikey = os.environ.get("Name_of_api_key_env_variable", None)
api_key = apikey
start_date = '2000-01-01'
end_date = '2020-12-31'
freq = 'q'

series_id = 'PAYEMS'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&frequency={freq}&file_type=json'

response = requests.get(url)

response = response.json()

df_payems = pd.DataFrame(response['observations'])

#print(len(df_payems))

##
series_id = 'GDPC1'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&frequency={freq}&file_type=json'

response = requests.get(url)

response = response.json()

df_gdp = pd.DataFrame(response['observations'])

#print(len(df_gdp))

##
series_id = 'CPIAUCSL'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&frequency={freq}&file_type=json'

response = requests.get(url)

response = response.json()

df_cpi = pd.DataFrame(response['observations'])

df_cpi = df_cpi[['date', 'value']]
df_cpi = df_cpi.rename({'value': 'CPIAUCSL'}, axis = 1)


df_gdp = df_gdp[['date', 'value']]
df_gdp = df_gdp.rename({'value': 'GDPC1'}, axis = 1)

df_payems = df_payems[['date', 'value']]
df_payems = df_payems.rename({'value': 'PAYEMS'}, axis = 1)

df = pd.merge(pd.merge(df_cpi,df_gdp,on='date'),df_payems,on='date')
df.CPIAUCSL = df.CPIAUCSL.astype('float')
df.GDPC1 = df.GDPC1.astype('float')
df.PAYEMS = df.PAYEMS.astype('float')
df.date = pd.to_datetime(df.date)
#print(df.tail())

df.to_csv('cpi_gdp_payems_data')

fig = plt.figure()
plt.subplots_adjust(right=0.75)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
twin = ax.twinx()
twin1 = ax.twinx()
ax.plot(df['date'], df['CPIAUCSL'], label = 'CPI', c='r')
ax.set_ylabel('CPI Index 1982-1984=100')
twin1.plot(df['date'], df['GDPC1'], label = 'GDP', c = 'g')
twin1.set_ylabel('Billions of Chained 2012 Dollars,')
twin.plot(df['date'], df["PAYEMS"], label = 'PAYEMS', c = 'b')
twin.set_ylabel('Thousands of Persons')
twin1.spines['right'].set_position(('outward', 60))
ax.set_yticks([150, 175, 200, 225, 250])

#plt.legend()
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.15), ncol=2)
twin.legend(loc = "lower right", bbox_to_anchor=(.85, 1.15), ncol=2)
twin1.legend(loc = "lower left", bbox_to_anchor=(.20, 1.15), ncol=2)
plt.title('Nonfarm Employed US Workers, CPI for All Urban Consumers, and Real GDP')
plt.show()

plt.scatter(df['CPIAUCSL'], df['PAYEMS'], c = 'seagreen')
plt.title('Nonfarm American Employees vs CPI')
plt.ylabel('Thousands of Persons')
plt.xlabel('CPI Index 1982-1984=100')
plt.show()

plt.hist(df['PAYEMS'], bins = 15, color = 'goldenrod', edgecolor='darkorchid')
plt.title('Histogram of Total Nonfarm Employment in the USA')
plt.xlabel('Thousands of persons')
plt.ylabel('Frequency')
plt.show()

##
series_id = 'UNRATE'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&frequency={freq}&file_type=json'

response = requests.get(url)

response = response.json()

df_unemp = pd.DataFrame(response['observations'])

##
series_id = 'INDPRO'
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&frequency={freq}&file_type=json'

response = requests.get(url)

response = response.json()

df_prod = pd.DataFrame(response['observations'])

#print(df_prod.head())

df_prod.value = df_prod.value.astype('float')
df_unemp.value = df_unemp.value.astype('float')

plt.scatter(df_prod['value'], df_unemp['value'], c='orangered')
plt.title('Unemployment Rate vs Industrial Production')
plt.xlabel('Industrial Production (Index 2017=100)')
plt.ylabel('Unemployment Rate %')
plt.show()
