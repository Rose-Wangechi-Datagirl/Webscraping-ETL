# ETL Data Engineering Project

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Data Flow](#data-flow)
- [Data Transformation](#data-transformation)
- [Web Scraping](#web-scraping)



## Project Overview



This project demonstrates my data engineering skills through the development of an Extract, Transform, Load (ETL) pipeline. The goal of this project was to automate the process of scraping data from the **Khai** and **Kairo** website via their API, transforming that data into a usable format, and loading it into a PostgreSQL database for further analysis.


## System Architecture

![Architecture Diagram](https://github.com/Rose-Wangechi-Datagirl/Webscraping-ETL/blob/main/ETL.png)

## Technologies Used



- **Apache Airflow**: For orchestrating the ETL workflow and managing task dependencies.
- **PostgreSQL**: As the database to store the processed data.
- **Python**: For writing data transformation scripts and Airflow DAGs.
- **Docker**: To containerize the application, ensuring consistency across different environments.
- **APIs**: Used to extract data from the Khai and Kairo website.



## Project Structure


```plaintext
ETL/
├── dags/                # Directory for Airflow DAGs
│   └── example_dag.py  # Sample DAG for orchestrating the ETL process
├── scripts/             # Directory for Python scripts
│   ├── extract.py       # Script for extracting data via API
│   ├── transform.py     # Script for transforming the extracted data
│   └── load.py          # Script for loading data into PostgreSQL
├── docker-compose.yml    # Docker Compose file for setting up services
└── Dockerfile           # Dockerfile for building a custom Airflow image
```

## **Data Flow**

The ETL pipeline follows these steps:

1. Extract: Data is extracted from the Khai and Kairo websites using their APIs.
2. Transform: The extracted data is processed and transformed to clean and normalize it for analysis.
3. Load: Transformed data is loaded into the PostgreSQL database for storage and querying.



## **Data Transformation**


The transformation scripts handle data cleaning, normalization, and enrichment to ensure data quality and usability. Some key transformation steps include:
- Selecting the relevant columns for the DataFrame
- Removing duplicates and irrelevant entries.
- Converting data types to align with database schema.

## **Web Scraping**

- Source Websites: This project utilizes APIs from the Khai and Kairo websites to scrape relevant data.
- Data Extraction: The extract.py script makes API calls to retrieve data, processes the JSON responses, and prepares it for transformation.
- Error Handling: The extraction process includes error handling to manage API response failures or changes in the API structure.

## **Containerization with Docker**

All components of the ETL pipeline are containerized using Docker, which allows for easy deployment and scalability.
A custom Docker image for Apache Airflow is built using the Dockerfile, ensuring that all necessary dependencies are installed and configured.
