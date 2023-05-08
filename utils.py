def get_field_value (field):
    return float(field.get())

def get_field_value_in_percentages (field):
    return float(field.get()) / 100

def get_table_data(rank, cost, field):
    return {
        'rank': rank,
        'cost': get_field_value(cost),
        'value': get_field_value_in_percentages(field)
    }

