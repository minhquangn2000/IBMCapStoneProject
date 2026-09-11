from datetime import datetime, timedelta
import os
import re
import tarfile

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

def extract_data():
    input_file = 'data/accesslog.txt'
    output_file = 'output/extracted_data.txt'
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        
    with open(input_file, 'r', encoding='utf-8') as f:
        log_content = f.read()
    ip_addresses = re.findall(ip_pattern, log_content)
    with open(output_file, 'w', encoding='utf-8') as f:
        for ip in ip_addresses:
            f.write(f"{ip}\n")
    print(f"Successfully inserted {len(ip_addresses)} IP addresses into {output_file}.")
    return output_file
    
def transform_data():
    input_file = 'output/extracted_data.txt'
    output_file = 'output/transformed_data.txt'
    ip_to_filter = "198.46.149.143"
    with open(input_file, 'r', encoding='utf-8') as f:
        all_ips = [line.strip() for line in f if line.strip()]

    filtered_ips = [ip for ip in all_ips if ip != ip_to_filter]

    with open(output_file, 'w', encoding='utf-8') as f:
            for ip in filtered_ips:
                f.write(f"{ip}\n")
    removed_count = len(all_ips) - len(filtered_ips)
    print(f"Transform completed! Removed {removed_count} with {ip_to_filter}.")
    print(f"New file saved at {output_file} with {len(filtered_ips)} line.")
    return output_file

def load_data():
    input_file = 'output/transformed_data.txt'
    tar_filename = 'output/weblog.tar'
    with tarfile.open(tar_filename, 'w') as tar:
        tar.add(input_file, arcname=os.path.basename(input_file))
    print(f"Load completed! Archived '{'transformed_data.txt'}' at '{tar_filename}'.")
    return tar_filename

# 2. Define the DAG
default_args = {
    'owner': 'quang',
    'start_date': datetime(2026, 8, 31),
    'email': ['your_email@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='process_web_log',
    default_args=default_args,
    description='A DAG process web log',
    schedule="@daily"
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )


extract_task >> transform_task >> load_task