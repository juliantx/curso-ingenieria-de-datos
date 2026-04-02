from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

# Función para imprimir un mensaje simple (usada con PythonOperator)
def print_message():
    print("Esta es una tarea simple de PythonOperator.")

# Definir el DAG
dag = DAG(
    'python_dummy_operator_bifurcacion',
    description='Ejemplo con PythonOperator y DummyOperator con bifurcación',
    schedule_interval=None,  # Este DAG no tiene una programación (se ejecuta manualmente)
    start_date=days_ago(1),
    catchup=False,
)

# Tarea 1: Imprimir un mensaje
task_print = PythonOperator(
    task_id='print_message_task',
    python_callable=print_message,
    dag=dag,
)

# Tarea 2: DummyOperator para simular una bifurcación en el flujo
branch_task = DummyOperator(
    task_id='branch_task',
    dag=dag,
)

# Tarea 3: Tarea de impresión si la bifurcación sigue este camino
def print_branch_1():
    print("Has seguido el camino 1.")

branch_1 = PythonOperator(
    task_id='branch_1',
    python_callable=print_branch_1,
    dag=dag,
)

# Tarea 4: Tarea de impresión si la bifurcación sigue este otro camino
def print_branch_2():
    print("Has seguido el camino 2.")

branch_2 = PythonOperator(
    task_id='branch_2',
    python_callable=print_branch_2,
    dag=dag,
)

# Tarea final: DummyOperator que se ejecuta después de cualquiera de las bifurcaciones
final_task = DummyOperator(
    task_id='final_task',
    dag=dag,
)

# Definir las dependencias
task_print >> branch_task  # Primero se ejecuta la tarea de impresión
branch_task >> [branch_1, branch_2]  # Después de la bifurcación, se elige entre branch_1 y branch_2
[branch_1, branch_2] >> final_task  # Después de cualquiera de las bifurcaciones, se va a la tarea final
