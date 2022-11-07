import pandas as pd
from pathlib import Path


def read_file(import_path):
    global transformed_dict
    transformed_dict = {}
    df = pd.read_csv(import_path, usecols = ['Nav','Cost','Turnover rating'])
#jei nenurodytas apyvartumas ima default B apyvartuma
    df["Turnover rating"].fillna("B", inplace = True)
    
#padaro atitinkama dictionary kad paprasciau iteruot
    dictionaries_list = df.to_dict('records')
    df_read = df
    for x in dictionaries_list:
        header = str(x['Nav'])
        transformed_dict[header] = [x['Cost'],x['Turnover rating']]
    return df_read

def markup_calculation(df_read, value_a1, value_a2, value_a3, value_a4, value_b1, value_b2, value_b3, value_b4, value_c1, value_c2, value_c3, value_c4, value_d1, value_d2, value_d3, value_d4, additional_taxes):
    global df_edited
    df_edited = df_read
    final_price = []
    for x, y in transformed_dict.values():
    #A
        if  x <= value_a1[1] and y == value_a1[0]:
            x = (x * (1 + value_a1[2]))  
        elif  value_a1[1] < x <= value_a2[1] and y == value_a2[0]:
            x = (x * (1 + value_a2[2]))   
        elif  value_a2[1] < x <= value_a3[1] and y == value_a3[0]:
            x = (x * (1 + value_a3[2])) 
        elif  value_a4[1] < x and y == value_a4[0]:
            x = (x * (1 + value_a4[2]))  
         
    #B   
        elif  x <= value_b1[1] and y == value_b1[0]:
            x = (x * (1 + value_b1[2]))
        elif  value_b1[1] < x <= value_b2[1] and y == value_b2[0]:
            x = (x * (1 + value_b2[2]))
        elif  value_b2[1] < x <= value_b3[1] and y == value_b3[0]:
            x = (x * (1 + value_b3[2])) 
        elif  value_b4[1] < x and y == value_b4[0]:
            x = (x * (1 + value_b4[2]))  
        
    #C
        elif  x <= value_c1[1] and y == value_c1[0]:
            x = (x * (1 + value_c1[2]))  
        elif  value_c1[1] < x <= value_c2[1] and y == value_c2[0]:
            x = (x * (1 + value_c2[2]))
        elif  value_c2[1] < x <= value_c3[1] and y == value_c3[0]:
            x = (x * (1 + value_c3[2]))
        elif  value_c4[1] < x and y == value_c4[0]:
            x = (x * (1 + value_c4[2]))   
        
    #D
        elif  x <= value_d1[1] and y == value_d1[0]:
            x = (x * (1 + value_d1[2]))  
        elif  value_d1[1] < x <= value_d2[1] and y == value_d2[0]:
            x = (x * (1 + value_d2[2]))  
        elif  value_d2[1] < x <= value_d3[1] and y == value_d3[0]:
            x = (x * (1 + value_d3[2]))  
        elif  value_d4[1] < x and y == value_d4[0]:
            x = (x * (1 + value_d4[2]))  
        final_price.append(float("{:.2f}".format(x * additional_taxes)))
        
    df_edited['Final price'] = final_price
    return df_edited

def config_import_strip(text):
    stripped = text.rstrip("')\n")
    stripped = stripped.replace("('", "").replace("'", "")
    result = stripped.split(", ")
    return result

#nuspaudus mygtuka issaugoti i csv sukuria nauja faila, jei yra failas tada prideda duomenis
def save_to_csv(file_path):
    my_file = Path(file_path)
    if my_file.is_file():
        df_edited.to_csv(file_path, mode='a', index=False, header=False)
    else:
        df_edited.to_csv(file_path, index=False)

 