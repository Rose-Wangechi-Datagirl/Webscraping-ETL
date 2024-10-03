# importing 
import requests
from requests.exceptions import SSLError
import json
import time
import datetime
import pandas as pd
import logging

# extracting data from api (https://dashboard.kaiandkaro.com/api/v1/vehicles/)
    
def load_api_data(**kwargs):
    data_file= "appends.json"
    all_car_data=[]
    last_page=1

    #load existing data if available
    try:
        with open (data_file, 'r') as f:
            all_car_data =json.load(f)
            last_page= ((len(all_car_data)//100) + 1) # assume a page has a 100 items
            print(f"Resuming from page {last_page}")
    except FileNotFoundError:
        print(f"No existing cashe found, starting a fresh")

    new_additions= 0

    # extracting data from api (https://dashboard.kaiandkaro.com/api/v1/vehicles/)
    def extract_data(page):
        nonlocal new_additions
        while True:
            api_url= f"https://dashboard.kaiandkaro.com/api/v1/vehicles/?page={page}"
            try: 
                response= requests.get (api_url)
                # raise error for bad responses
                response.raise_for_status()
            except SSLError as e:
                print(f"SSLError encountered on page {page}: {e}")
                pass #continue the loop on ssl error
            except requests.exceptions.RequestException as e:
                print(f"Unable to fetch data from page {page}: {e}")
                break

            #extracting data from the response   
            car_data= response.json()
            next_page= car_data['next']
            results= car_data['results']

            #filter duplicates
            existing_ids= {item['id'] for item in all_car_data}
            new_car_data = [item for item in results if item['id'] not in existing_ids]

            #adding the new data
            all_car_data.extend(new_car_data)
            new_additions += len(new_car_data)

            print(f"Page {page} extracted with new {len(new_car_data)} additions")

            #rate limiting to avoid overloading server and also the website at somepoint stopped accepting to requests
            time.sleep(5)

            #chek if there is another page
            if not next_page:
                break
            page +=1

    extract_data(last_page)

    # Save the updated data to the cache file
    with open(data_file, 'w') as vehicles:
        json.dump(all_car_data, vehicles, indent=4)
        date = datetime.datetime.now()
        print(f"{new_additions} new vehicle ads added, total {len(all_car_data)} ads saved at {date}")

    #logging
    logging.info(f"total {len(all_car_data)} ads saved at {date}")
    
    # Push data to XCom for the next task (transform)
    kwargs['ti'].xcom_push(key='car_data', value=all_car_data)