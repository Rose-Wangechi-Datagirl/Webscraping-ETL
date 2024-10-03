# This tells Docker to use the official Airflow image with Python 3.8
FROM apache/airflow:2.6.0-python3.8

# Install additional Python libraries
RUN pip install psycopg2-binary pandas requests

# Set the directory where Airflow will live inside the container
ENV AIRFLOW_HOME=/opt/airflow

# Copy the Python scripts (like your DAG and helper scripts) to the container
COPY ./dags /opt/airflow/dags
COPY ./scripts /opt/airflow/scripts

# This command starts the Airflow web interface inside the container
CMD ["airflow", "webserver"]
