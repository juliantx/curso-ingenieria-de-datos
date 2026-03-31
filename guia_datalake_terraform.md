# Guía Completa: Data Lake en AWS con Terraform (Nivel Detallado)

---

# 1. Arquitectura General

```
        +-------------------+
        |   Fuente Datos    |
        +--------+----------+
                 |
                 v
        +-------------------+
        |   S3 Bronze       |  (datos crudos)
        +--------+----------+
                 |
                 v
        +-------------------+
        |   AWS Glue Job    |  (ETL)
        +--------+----------+
                 |
                 v
        +-------------------+
        |   S3 Silver       |  (datos limpios)
        +--------+----------+
                 |
                 v
        +-------------------+
        |   S3 Gold         |  (agregados)
        +-------------------+

        +-------------------+
        | CloudWatch        |
        | Logs + Alarmas    |
        +-------------------+

        +-------------------+
        | IAM Roles         |
        +-------------------+
```

---

# 2. Buckets: Bronze, Silver, Gold

## Archivo: modules/s3_lake/main.tf

```hcl
resource "aws_s3_bucket" "this" {
  bucket = "${var.project}-${var.env}-${var.bucket_name}-${var.account_id}"
  tags   = var.tags
}
```

### Línea por línea

- `resource "aws_s3_bucket"` → define un bucket
- `"this"` → nombre interno del recurso
- `bucket =` → nombre dinámico del bucket
- `${var.project}` → nombre del proyecto
- `${var.env}` → ambiente (dev, prod)
- `${var.bucket_name}` → bronze/silver/gold
- `${var.account_id}` → evita duplicados globales

👉 Resultado:
```
datalake-dev-bronze-123456789
```

---

## Encriptación

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
```

- Habilita cifrado en reposo
- `AES256` → estándar AWS

---

## Lifecycle

```hcl
transition {
  days          = 180
  storage_class = "STANDARD_IA"
}
```

- Después de 180 días → más barato
- Optimización de costos

---

# 3. Flujo de Datos entre Buckets

```
Bronze (raw CSV)
   ↓
Glue Job
   ↓
Silver (parquet limpio)
   ↓
(agregaciones futuras)
   ↓
Gold
```

---

# 4. Glue Job

## Archivo: modules/glue/main.tf

```hcl
resource "aws_glue_job" "sales_etl" {
```

### Explicación

- Define un job ETL administrado
- Usa Spark por debajo

---

### Parámetros clave

```hcl
role_arn = var.glue_role_arn
```

- Conecta con IAM
- Permisos para S3 y logs

---

```hcl
script_location = var.script_location
```

- Script ETL almacenado en S3

---

```hcl
"--input_path"  = "s3://${var.bronze_bucket}/sales_small.csv"
"--output_path" = "s3://${var.silver_bucket}/sales/"
```

👉 Aquí ocurre la conexión:

- Entrada → Bronze
- Salida → Silver

---

### Workers

```hcl
worker_type       = "G.1X"
number_of_workers = 2
```

- Define capacidad
- Controla costo

---

# 5. CloudWatch

## Archivo: modules/cloudwatch/main.tf

### Log Group

```hcl
name = "/aws-glue/jobs/${var.project}-${var.env}"
```

- Guarda logs del job

---

### Alarma

```hcl
metric_name = "glue.driver.aggregate.numFailedTasks"
threshold   = 0
```

- Si hay fallos → alerta

---

### Dashboard

- Métricas de éxito vs fallos
- Visualización operativa

---

# 6. IAM (Seguridad)

## Archivo: modules/iam/main.tf

---

## Rol

```hcl
resource "aws_iam_role" "glue_role"
```

- Define identidad de Glue

---

## Trust Policy

```hcl
Service = "glue.amazonaws.com"
```

- Permite a Glue asumir el rol

---

## Política S3

```hcl
Action = [
  "s3:GetObject",
  "s3:ListBucket"
]
```

- Leer Bronze

```hcl
"s3:PutObject"
```

- Escribir en Silver

---

## Política Logs

```hcl
logs:CreateLogGroup
logs:PutLogEvents
```

- Permite escribir logs

---

## Attachments

```hcl
aws_iam_role_policy_attachment
```

- Une políticas al rol

---

# 7. Variables y Conexiones

## Ejemplo

```hcl
variable "project" {}
```

---

## Flujo de variables

```
env/dev → variables.tf
   ↓
main.tf (root)
   ↓
modules (inputs)
   ↓
resources
```

---

## Outputs

Ejemplo:

```hcl
output "glue_role_arn"
```

👉 Se usa en:

```
module.iam → output
module.glue → input
```

---

# 8. Cómo todo se conecta

```
IAM Role → Glue Job
Glue Job → S3 Bronze/Silver
CloudWatch → monitorea Glue
S3 → almacena datos
```

---

# 9. Flujo completo

1. Se crean buckets
2. Se crea IAM role
3. Glue usa ese rol
4. Job lee Bronze
5. Escribe Silver
6. CloudWatch monitorea

---

# 10. Despliegue

```bash
terraform init
terraform plan
terraform apply
```

---

# 11. Errores comunes

- Permisos IAM insuficientes
- Bucket names duplicados
- Script Glue mal ubicado

---

# 12. Mejores prácticas

- Separar módulos
- Usar variables
- Versionar infraestructura
- Monitorear siempre

---

# CONCLUSIÓN

Este Data Lake sigue arquitectura moderna:
- Modular
- Escalable
- Seguro
- Optimizado en costos

