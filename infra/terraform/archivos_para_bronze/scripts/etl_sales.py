import sys
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

# Leer parámetros
args = getResolvedOptions(sys.argv, ['input_path', 'output_path'])

input_path = args['input_path']
output_path = args['output_path']

spark = SparkSession.builder.getOrCreate()

# Leer CSV desde bronze
df = spark.read.option("header", "true").csv(input_path)

# Transformaciones
df_transformed = (
    df.withColumn("order_id", col("order_id").cast("int"))
      .withColumn("customer_id", col("customer_id").cast("int"))
      .withColumn("amount", col("amount").cast("double"))
      .withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
)

# Guardar en silver en formato Parquet
df_transformed.write \
    .mode("overwrite") \
    .partitionBy("date") \
    .parquet(output_path)