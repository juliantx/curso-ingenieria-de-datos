# Guía de QuickSight con Datasets Sales y Customers

## PARTE 1 — Entender los datasets

### Dataset: sales
Representa transacciones de ventas.

| Columna           | Explicación              |
|------------------|--------------------------|
| order_id         | ID único de la orden     |
| date             | Fecha de compra          |
| customer_id      | Cliente                  |
| city             | Ciudad                   |
| country          | País                     |
| product_category | Categoría                |
| product_name     | Producto                 |
| price            | Precio unitario          |
| quantity         | Cantidad                 |
| discount         | Descuento                |
| total_amount     | Total pagado             |
| payment_method   | Método de pago           |

---

### Dataset: customers
Información del cliente.

| Columna        | Explicación        |
|----------------|--------------------|
| customer_id    | ID                 |
| customer_name  | Nombre             |
| age            | Edad               |
| gender         | Género             |
| signup_date    | Registro           |
| segment        | Tipo cliente       |
| income_level   | Nivel ingreso      |
| region         | Región             |

---

## PARTE 2 — Join

Unir por `customer_id` (LEFT JOIN).

---

## PARTE 3 — Análisis

### Ventas por categoría
- X: `product_category`
- Y: `sum(total_amount)`

### Evolución en el tiempo
- X: `date`
- Y: `sum(total_amount)`

### Top productos
- X: `product_name`
- Y: `sum(total_amount)`

### Ventas por ciudad
- X: `city`
- Y: `sum(total_amount)`

### Método de pago
- Tipo: Pie chart

---

![alt text](image.png)


## PARTE 4 — Análisis cruzado

### Ventas por segmento
- X: `segment`
- Y: `sum(total_amount)`

### Ticket promedio

### Impacto descuento
- `discount` vs `total_amount`

### Edad vs compras
- `age` vs `total_amount`

### Región vs ingresos
- `region` vs `total_amount`

---

## PARTE 5 — Avanzado

### Cohortes
- `signup_date` vs ventas

### KPIs
- Total ventas  
- Total órdenes  

---

## Caso práctico

1. ¿Qué categoría vende más?  
2. ¿Qué segmento es más rentable?  
3. ¿Los descuentos ayudan?  
4. ¿Qué región genera más ingresos?  