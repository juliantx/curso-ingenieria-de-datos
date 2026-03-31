# Guía: Data Lake en AWS con Terraform

## 1. Introducción
Esta guía explica cómo desplegar un Data Lake en AWS usando Terraform con una arquitectura basada en capas:
- **Bronze**: datos crudos
- **Silver**: datos procesados
- **Gold**: datos agregados

Incluye:
- S3 (Data Lake)
- IAM (roles y políticas)
- AWS Glue (ETL)
- CloudWatch (monitoreo)

---

## 2. Estructura del Proyecto

```
modules/
  s3_lake/
  iam/
  glue/
  cloudwatch/
envs/
  dev/
```

---

## 3. Módulo S3 (Data Lake)

### main.tf
```hcl
resource "aws_s3_bucket" "this" {
  bucket = "${var.project}-${var.env}-${var.bucket_name}-${var.account_id}"
  tags = var.tags
}
```

### Explicación
- Crea buckets dinámicos por entorno
- Usa naming estándar: `project-env-layer-account`

### Seguridad
```hcl
sse_algorithm = "AES256"
```
- Cifrado en reposo habilitado

### Lifecycle
```hcl
transition {
  days = 180
  storage_class = "STANDARD_IA"
}
```
- Reduce costos moviendo datos antiguos

---

## 4. Módulo IAM

### Rol de Glue
Permite que AWS Glue ejecute jobs.

### Políticas:
- Lectura en Bronze
- Escritura en Silver
- Acceso a bucket temporal
- Logs en CloudWatch

Ejemplo:
```hcl
Action = ["s3:GetObject", "s3:ListBucket"]
```

---

## 5. Módulo Glue

### main.tf
```hcl
resource "aws_glue_job" "sales_etl" {
  name     = "${var.project}-${var.env}-sales-etl"
  role_arn = var.glue_role_arn
}
```

### Explicación
- Ejecuta ETL desde Bronze → Silver
- Usa script en S3

Parámetros:
```hcl
"--input_path"
"--output_path"
```

---

## 6. Módulo CloudWatch

Incluye:
- Log Group
- Alarmas
- Dashboard

### Alarma
```hcl
metric_name = "glue.driver.aggregate.numFailedTasks"
```

---

## 7. Variables

Ejemplo:
```hcl
variable "project" {
  type = string
}
```

Se usan para:
- Reutilización
- Multi-entorno
- Buenas prácticas

---

## 8. Flujo Completo

1. Datos llegan a Bronze (S3)
2. Glue procesa → Silver
3. CloudWatch monitorea
4. IAM controla accesos

---

## 9. Despliegue

```bash
terraform init
terraform plan
terraform apply
```

---

## 10. Buenas Prácticas

- Usar módulos reutilizables
- Separar entornos
- Habilitar cifrado
- Monitorear con CloudWatch

---

## 11. Conclusión

Este proyecto implementa un Data Lake moderno siguiendo buenas prácticas de AWS y Terraform.
