from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.amazon.aws.hooks.athena import AthenaHook
from airflow.operators.python import PythonOperator
from datetime import datetime


AWS_CONN_ID = "conexion_aws"
BRONZE_BUCKET = "datalake-dev-bronze-714647503442"
SILVER_BUCKET = "datalake-dev-silver-714647503442"


def print_s3_files(ti):
    files = ti.xcom_pull(task_ids='list_s3_files')
    print("Archivos en S3:")
    print(files)


with DAG(
    dag_id="datalake_sensor_s3_to_athena",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["aws", "glue", "s3","athena","sensor"]
) as dag:

    # =========================================================
    # FLUJO 1: BRONZE → GLUE
    # =========================================================

    # Sensor: espera archivos en bronze
    wait_for_bronze = S3KeySensor(
        task_id="wait_for_bronze",
        bucket_name=BRONZE_BUCKET,
        bucket_key="sales/*.csv",  # ajusta a tu ruta real
        wildcard_match=True,
        aws_conn_id=AWS_CONN_ID,
        poke_interval=30,
        timeout=600
    )

    # Listar archivos en Bronze
    list_s3_files = S3ListOperator(
        task_id="list_s3_files",
        bucket=BRONZE_BUCKET,
        prefix="sales/",
        aws_conn_id=AWS_CONN_ID
    )

    print_files = PythonOperator(
        task_id="print_files",
        python_callable=print_s3_files
    )

    # Ejecutar Glue Job
    run_glue_job = GlueJobOperator(
        task_id="run_glue_job",
        job_name="datalake-dev-sales-etl",
        aws_conn_id=AWS_CONN_ID,
        region_name="us-east-1",
        wait_for_completion=True,
        script_args={
            "--env": "dev"
        }
    )

    # =========================================================
    # FLUJO 2: SILVER → ATHENA
    # =========================================================

    # Sensor: espera archivos en silver
    wait_for_silver = S3KeySensor(
        task_id="wait_for_silver",
        bucket_name=SILVER_BUCKET,
        bucket_key="sales/**/*.parquet",
        wildcard_match=True,
        aws_conn_id=AWS_CONN_ID,
        poke_interval=30,
        timeout=600
    )

    create_database = AthenaOperator(
        task_id="create_database",
        query="""
            CREATE DATABASE IF NOT EXISTS datalake_db
        """,
        database="default",
        output_location="s3://pragma-simulacion/resutados_athena/",
        aws_conn_id=AWS_CONN_ID
    )

    # Crear tabla si no existe en Athena
    create_table = AthenaOperator(
        task_id="create_table",
        query="""
            CREATE EXTERNAL TABLE IF NOT EXISTS datalake_db.sales_silver (
                order_id INT,
                customer_id INT,
                product STRING,
                amount DOUBLE,
                city STRING
            )
            PARTITIONED BY (date DATE)
            STORED AS PARQUET
            LOCATION 's3://datalake-dev-silver-714647503442/sales/';
        """,
        database="datalake_db",
        output_location="s3://pragma-simulacion/resutados_athena/",
        aws_conn_id=AWS_CONN_ID
    )

   
    # Query en Athena
    query_athena = AthenaOperator(
        task_id="query_athena",
        query="""
            SELECT 
                "date",
                SUM(CAST(amount AS DOUBLE)) AS total_sales
            FROM sales_silver
            GROUP BY "date"
            ORDER BY "date" DESC
            LIMIT 10
        """,
        database="datalake_db",
        output_location="s3://pragma-simulacion/resutados_athena/",
        aws_conn_id=AWS_CONN_ID
    )

    # Mostrar resultado (opcional)
    def print_athena_results(ti):
        hook = AthenaHook(aws_conn_id="conexion_aws")

        query_execution_id = ti.xcom_pull(task_ids='query_athena')

        results = hook.get_query_results(query_execution_id)

        print("Resultados Athena:")
        print(results)

    print_athena = PythonOperator(
        task_id="print_athena_results",
        python_callable=print_athena_results
    )  

    # =========================================================
    # DEPENDENCIAS
    # =========================================================

    # Flujo principal (bronze → glue)
    wait_for_bronze >> list_s3_files >> print_files >> run_glue_job

    # Flujo alternativo (silver → athena)
    wait_for_silver >> create_database >> create_table >> query_athena >> print_athena