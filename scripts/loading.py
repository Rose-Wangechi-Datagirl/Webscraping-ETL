import psycopg2
import logging

def load_data_to_postgres(**kwargs):
    # Retrieve the transformed data from XCom
    transformed_data = kwargs['ti'].xcom_pull(key='df', task_ids='transform_task')

    # PostgreSQL connection setup
    connection = psycopg2.connect(
        user="myuser",
        password="mysecretpassword",
        host="localhost",  
        port="5432",
        database="vehicle_data"
    )
    
    cursor = connection.cursor()

    # Check if the 'cars' table exists and create it if not
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        price_currency VARCHAR(10),
        price FLOAT,
        body_type VARCHAR(50),
        mileage INT,
        annual_insurance FLOAT,
        drive VARCHAR(50),
        color VARCHAR(50),
        source VARCHAR(255),
        thumbnail VARCHAR(255),
        agent_whatsapp_contact BIGINT,
        estimated_arrival_days FLOAT,
        slug VARCHAR(255)
    );
    '''
    
    cursor.execute(create_table_query)
    logging.info("Checked and ensured 'cars' table exists or has been created.")
    
    # Define the SQL INSERT query with appropriate column names
    insert_query = '''
    INSERT INTO cars (
        id, name, price_currency, price, body_type, mileage, 
        annual_insurance, drive, color, source, thumbnail, 
        agent_whatsapp_contact, estimated_arrival_days, slug
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;  -- Handle conflicts by ignoring duplicates
    '''
    
    # Insert data row by row into the database
    for _, car in transformed_data.iterrows():
        try:
            cursor.execute(insert_query, (
                car['id'],
                car['name'],
                car['price_currency'],
                car['price'],
                car['body_type'],
                car['mileage'],
                car['annual_insurance'],
                car['drive'],
                car['color'],
                car['source'],
                car['thumbnail'],
                car['agent_whatsapp_contact'],
                car['estimated_arrival_days'],
                car['slug']
            ))
        except Exception as e:
            logging.error(f"Error inserting data for car ID {car['id']}: {e}")
    
    # Commit the transaction to save changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    logging.info("Data successfully loaded into PostgreSQL.")
