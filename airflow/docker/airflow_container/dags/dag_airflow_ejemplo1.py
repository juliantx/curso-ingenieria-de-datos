from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

# Función de ejemplo para PythonOperator
def task_1():
    print("Ejecutando la tarea 1 - PythonOperator")

# Definición de los argumentos por defecto
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 11, 15, 15, 0),  # Comienza a las 3 de la tarde del 15 de noviembre de 2024
}

# Definición del DAG
dag = DAG(
    'three_tasks_dag',
    default_args=default_args,
    description='Un DAG con 3 tareas: PythonOperator, BashOperator y EmailOperator',
    schedule_interval='0 15 * * *',  # Todos los días a las 3 de la tarde
    catchup=False,  # No ejecutar tareas pasadas
)

# Tarea 1: PythonOperator
task1 = PythonOperator(
    task_id='task_1',
    python_callable=task_1,
    dag=dag
)

# Tarea 2: BashOperator
task2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Ejecutando la tarea 2 - BashOperator"',
    dag=dag
)

# Tarea 3: DummyOperator (sustituyendo el EmailOperator)
task3 = DummyOperator(
    task_id='task_3',  # Simplemente una tarea de marcador de posición
    dag=dag
)

# Establecer dependencias entre las tareas
task1 >> task2 >> task3

