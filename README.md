# ETL Process

Project that performs ETL process with extraction, cleaning, transformation, and loading data to GCP BigQuery.

* __Time of analysis v1:__ November 7, 2023.
* __Tools v1:__ .CSV, Python, SQL, BigQuery GCP.

## Background

This project extracts the top headlines of the [News API](https://newsapi.org/).

## Getting started

Clone the repository in the folder:

```console
git clone git@github.com:denisseee/ETL_process.git ETL_process
cd ETL_process
```

Check your python version and install the dependencies:

```console
which python3
pip3 install pandas
pip3 install requests
pip3 install fugue
pip3 install "fugue[sql]"
python3 -m pip install python-dotenv
```

Run the code to start the process: 

```console
python3 main.py
```

2 Files will generated:
* top_headlines.csv
* top_headlines_after_sql.csv

## Workflow description

### 1. Inspect

```py
df.head(5)
df.dtypes
# df.info()
df.describe()
print(df.shape) # (20, 9)
```

### 2. Transform 

```py
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
```

### 3. SQL 

```sql
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
```

## BigQuery: Load data with GCP SDK
