import pandas as pd
from pathlib import Path

def build_df(df, price):
    df_edited = df.copy()
    df_edited['Final price'] = price
  
    return df_edited
    
def save_to_csv(file_path, df):
    if Path(file_path).is_file():
      df.to_csv(file_path, mode='a', index=False, header=False)
   
    return df.to_csv(file_path, index=False)

def create_df(import_path):
    df = pd.read_csv(import_path, usecols = ['No.','Purchase price','Ranking by sales revenue'])
    df["Ranking by sales revenue"].fillna("B", inplace = True)
    
    return df

def combine_price_records(df):
    arr = []

    for record in df.to_dict('records'):
        arr.append([record['Purchase price'], record['Ranking by sales revenue']]) 
        
    return arr 