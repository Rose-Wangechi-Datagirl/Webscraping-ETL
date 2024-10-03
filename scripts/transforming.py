import pandas as pd
import logging

def clean_transform_data(**kwargs):
    # Pull data from XCom (the extracted data)
    all_car_data= kwargs['ti'].xcom_pull(key='car_data', task_ids='extract_task')

    df = pd.DataFrame(all_car_data) #coverting data into a data frame

    #selecting columns to keep
    columns_to_include= ['id', 'name', 'price_currency', 'price', 'body_type', 'mileage', 'annual_insurance',
                         'drive', 'color', 'source', 'thumbnail', 'agent_whatsapp_contact', 'estimated_arrival_days',
                         'slug']
                        
    df= df[columns_to_include]
    #dropping null values
    df.dropna (inplace=True)

    #coverting to the right data types 
    df['id'] = df['id'].astype(int)
    df['name'] = df['name'].astype(str)
    df['price_currency'] = df['price_currency'].astype(str)
    df['price'] = df['price'].astype(float)
    df['body_type'] = df['body_type'].astype(str)
    df['mileage'] = df['mileage'].astype(int)
    df['annual_insurance'] = df['annual_insurance'].astype(float)
    df['drive'] = df['drive'].astype(str)
    df['color'] = df['color'].astype(str)
    df['source'] = df['source'].astype(str)
    df['thumbnail'] = df['thumbnail'].astype(str)
    df['agent_whatsapp_contact'] = df['agent_whatsapp_contact'].astype(int)
    df['estimated_arrival_days'] = df['estimated_arrival_days'].astype(float)
    df['slug'] = df['slug'].astype(str)

    # return df

    #logging
    logging.info(f"Transformed data: {df.shape[0]} rows and {df.shape[1]} columns")
     # Push transformed data to XCom for the next task (load)
    kwargs['ti'].xcom_push(key='transformed_data', value=df)