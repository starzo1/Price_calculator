import pandas as pd
from pathlib import Path


transformed_dict = {}

def read_file(import_path):
    df = pd.read_csv(import_path, usecols = ['No.','Purchase price','Ranking by sales revenue'])
    df["Ranking by sales revenue"].fillna("B", inplace = True)
    dictionaries_list = df.to_dict('records')
    df_read = df
    for record in dictionaries_list:
        header = str(record['No.'])
        transformed_dict[header] = [record['Purchase price'],record['Ranking by sales revenue']]
    return df_read

def markup_calculation(df_read, value_a1, value_a2, value_a3, value_a4, value_b1, value_b2, value_b3, value_b4, value_c1, value_c2, value_c3, value_c4, value_d1, value_d2, value_d3, value_d4, additional_tax):
    global df_edited

    df_edited = df_read.copy()
    final_price = []
    for cost, turnover in transformed_dict.values():
        float(cost)
    #A
        if  cost <= value_a1[1] and turnover == value_a1[0]:
            cost = (cost * (1 + value_a1[2]))  
        elif  value_a1[1] < cost <= value_a2[1] and turnover == value_a2[0]:
            cost = (cost * (1 + value_a2[2]))   
        elif  value_a2[1] < cost <= value_a3[1] and turnover == value_a3[0]:
            cost = (cost * (1 + value_a3[2])) 
        elif  value_a4[1] < cost and turnover == value_a4[0]:
            cost = (cost * (1 + value_a4[2]))  
         
    #B   
        elif  cost <= value_b1[1] and turnover == value_b1[0]:
            cost = (cost * (1 + value_b1[2]))
        elif  value_b1[1] < cost <= value_b2[1] and turnover == value_b2[0]:
            cost = (cost * (1 + value_b2[2]))
        elif  value_b2[1] < cost <= value_b3[1] and turnover == value_b3[0]:
            cost = (cost * (1 + value_b3[2])) 
        elif  value_b4[1] < cost and turnover == value_b4[0]:
            cost = (cost * (1 + value_b4[2]))  
        
    #C
        elif  cost <= value_c1[1] and turnover == value_c1[0]:
            cost = (cost * (1 + value_c1[2]))  
        elif  value_c1[1] < cost <= value_c2[1] and turnover == value_c2[0]:
            cost = (cost * (1 + value_c2[2]))
        elif  value_c2[1] < cost <= value_c3[1] and turnover == value_c3[0]:
            cost = (cost * (1 + value_c3[2]))
        elif  value_c4[1] < cost and turnover == value_c4[0]:
            cost = (cost * (1 + value_c4[2]))   
    #D
        elif  cost <= value_d1[1] and turnover == value_d1[0]:
            cost = (cost * (1 + value_d1[2]))  
        elif  value_d1[1] < cost <= value_d2[1] and turnover == value_d2[0]:
            cost = (cost * (1 + value_d2[2]))  
        elif  value_d2[1] < cost <= value_d3[1] and turnover == value_d3[0]:
            cost = (cost * (1 + value_d3[2]))  
        elif  value_d4[1] < cost and turnover == value_d4[0]:
            cost = (cost * (1 + value_d4[2]))  
        final_price.append(float("{:.2f}".format(cost * additional_tax)))
        
    df_edited['Final price'] = final_price
    return df_edited

def save_to_csv(file_path):
    my_file = Path(file_path)
    if my_file.is_file():
        df_edited.to_csv(file_path, mode='a', index=False, header=False)
    else:
        df_edited.to_csv(file_path, index=False)

 