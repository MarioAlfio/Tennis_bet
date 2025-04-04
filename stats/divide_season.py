# Funzione per determinare la stagione in base al mese
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Inverno'
    elif month in [3, 4, 5]:
        return 'Primavera'
    elif month in [6, 7, 8]:
        return 'Estate'
    elif month in [9, 10, 11]:
        return 'Autunno'