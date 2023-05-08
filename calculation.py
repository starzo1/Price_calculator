def calculate_price(cost, value):
    return cost * (1 + value) 

def calculate_additional_taxes(obj):
    return (1 + obj['vat'] / 100) * (1 + obj['trnsp_cost'] / 100) * (1 + obj['additional_cost'] / 100)

def is_equal_rank(rank, input_rank): 
    return rank == input_rank

def markup_calculation(price_records, taxes, data):
    val = 0
    final_price = []
    ranks = ['a','b','c','d']
    
    for cost, rank in price_records:
      for id in ranks:  
        if cost <= data[f'{id}1']['cost'] and is_equal_rank(rank, data[f'{id}1']['rank']):
          val = data[f'{id}1']['value']
        elif data[f'{id}1']['cost'] < cost <= data[f'{id}2']['cost'] and is_equal_rank(rank, data[f'{id}2']['rank']): 
          val = data[f'{id}2']['value'] 
        elif data[f'{id}2']['cost'] < cost <= data[f'{id}3']['cost'] and is_equal_rank(rank, data[f'{id}3']['rank']): 
          val = data[f'{id}3']['value']
        elif data[f'{id}4']['cost'] < cost and is_equal_rank(rank, data[f'{id}4']['rank']): 
          val = data[f'{id}1']['value']
        
      final_price.append(float("{:.2f}".format(calculate_price(cost, val) * calculate_additional_taxes(taxes))))
        
    return final_price


 