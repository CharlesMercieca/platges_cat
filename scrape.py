import pandas as pd
import requests
import time

def table_platges_cat_beach(url):
    '''
    Returns a pandas data frame of relevant data from the Platges Cat app page.
    '''

    r = requests.get(url)
    response = r.json()

    relevant_fields = {
    'scrape_time': pd.Timestamp.now(),
    'page_date': response['estadoPlaya']['fecha'],
    'page_hour': response['estadoPlaya']['hora'],
    'bay_id': response['playa']['id'],
    'bay_name': response['playa']['nombre'],
    'lat': response['playa']['coordenadasPC'][0]['coordenaday'],
    'lon': response['playa']['coordenadasPC'][0]['coordenadax'],
    'jellyfish_lab': response['medusas']['peligrosidadTrad'],
    'jellyfish_lab2': response['medusas']['peligrosidadEtiqueta'],
    'jellyfish_icon': response['medusas']['icono'],
    'jellyfish_list': [response['medusas']['llistatMeduses']]
    }

    return pd.DataFrame(relevant_fields)

beach_list = list(range(0, 280))
beach_list.append(300)

catalonia_beaches = []

for beach in beach_list:
    #form request url & send it
    url=f"https://aplicacions.aca.gencat.cat/platgescat2/agencia-catalana-del-agua-backend/web/app.php/api/playadetalle/{beach}"
    try:
        #not all of them have jellyfish status, wrapping in a try block
        beach_response = table_platges_cat_beach(url)
        catalonia_beaches.append(beach_response)
    except:
        pass
    
    #small delay to be polite
    time.sleep(0.2)


catalonia_beaches_df = pd.concat(catalonia_beaches)

fname = f"data/catalonia_jellyfish_{pd.Timestamp.now().strftime(format='%Y%m%d_%H')}.csv"

catalonia_beaches_df.to_csv(fname, index=False)