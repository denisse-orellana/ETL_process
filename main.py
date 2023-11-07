import requests
import pandas as pd

from datetime import datetime
from fugue.api import fugue_sql

import os
from dotenv import load_dotenv
load_dotenv()

# Access environment variables
news_api_key = os.getenv('NEWS_API_KEY')

### 0. Import data
url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}'
header = {'Content-Type': 'application/json', 
           'Accept-Encoding': 'deflate'}

response = requests.get(url, headers = header)
print(response) # 200

responseData = response.json()
# print(responseData)

df = pd.json_normalize(responseData, 'articles')
# print(df.head(5))

### 1. Inspecting data
df.head(15)
df.shape # (89010, 61)
df.dtypes
# df.info()
df.describe()
print(df.shape) # (20, 9)

### 2. Transform data

# Delete duplicates
df.drop_duplicates

# Missing values
df.fillna('NaN', inplace=True)

# Transform date to datetime format
# df['author'] = df['author'].astype('string') 
df['publishedAt'] = pd.to_datetime(df['publishedAt'], utc=True).dt.tz_convert(None)

# Delete rows with [Removed] news
df_filtered_index = df[df['title'] == '[Removed]'].index
df.drop(df_filtered_index, inplace=True)
df.reset_index(drop=True, inplace=True)
df.head(15)
df.shape # (19, 9)

# Change column name 
df.rename(columns = {'source.name':'source'}, inplace = True)

### 3. Export to csv file
df.to_csv('top_headlines.csv', index=False)

### 4. SQL: DDM - DDL
query = """
  SELECT 
    `publishedAt` AS `date`,
    `source`,
    `author`,
    `title`,
    `description`
    `content`,
    `url`,
    `urlToImage` AS `image`
  FROM 
    df 
  PRINT
"""

# 5. Export sql data to csv
sql_table = fugue_sql(query)
print(sql_table)
df2 = pd.DataFrame(sql_table)
df2.to_csv('top_headlines_after_sql.csv', index=False)
