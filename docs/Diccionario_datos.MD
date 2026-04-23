# Diccionario de Datos — Modelo de Riesgo Crediticio

## Variable objetivo

| Variable                     | Tipo    | Descripción                                                                 |
|-----------------------------|---------|-----------------------------------------------------------------------------|
| default_in_last_6months     | Binaria | 1 = cliente entró en default en los últimos 6 meses, 0 = no entró en default |

---

## Variables de entrada

### 1. Variables demográficas

| Variable | Tipo | Descripción |
|----------|------|-------------|
| age | Num | Edad del cliente |
| gender | Cat | Género del cliente |
| marital_status | Cat | Estado civil |
| dependents | Num | Número de dependientes |

---

### 2. Variables financieras

| Variable | Tipo | Descripción |
|----------|------|-------------|
| income | Num | Ingreso mensual del cliente |
| debt | Num | Deuda total |
| credit_limit | Num | Límite de crédito disponible |
| balance | Num | Saldo actual |
| utilization_rate | Num | Uso del crédito (balance / límite) |

---

### 3. Variables de comportamiento

| Variable | Tipo | Descripción |
|----------|------|-------------|
| number_of_loans | Num | Número de créditos activos |
| late_payments | Num | Número de pagos atrasados |
| delinquency_days | Num | Días de atraso acumulados |
| avg_payment | Num | Pago promedio mensual |
| transactions_count | Num | Número de transacciones recientes |

---

### 4. Variables de historial crediticio

| Variable | Tipo | Descripción |
|----------|------|-------------|
| credit_history_length | Num | Antigüedad crediticia |
| previous_defaults | Num | Número de defaults previos |
| inquiries_last_6m | Num | Número de consultas de crédito recientes |

---

### 5. Variables categóricas de producto

| Variable | Tipo | Descripción |
|----------|------|-------------|
| product_type | Cat | Tipo de producto financiero |
| segment | Cat | Segmento del cliente |
| region | Cat | Región geográfica |

---

### 6. Variables técnicas (NO usar en el modelo)

| Variable | Tipo | Descripción |
|----------|------|-------------|
| id | ID | Identificador único del cliente |
| index | ID | Índice del dataset |

---

## Validación Train vs Test

### Problema detectado

El dataset `test.csv` contiene una variable adicional que no está en `train.csv`.

---

## Interpretación

Esa variable adicional probablemente es:

- un identificador
- una columna técnica
- o una variable no disponible en entrenamiento

---

## Acción requerida

Eliminar la variable adicional en test antes de predecir.

---

## Regla crítica

> El modelo SOLO puede recibir variables con las que fue entrenado.

---

## Validación final

Antes de inferencia:

- mismas columnas en train y test  
- mismo orden  
- mismos tipos de datos  

---

## Interpretación del modelo

La regresión logística asigna un peso a cada variable:

- coeficiente positivo → aumenta riesgo  
- coeficiente negativo → reduce riesgo  

---

## Ejemplo interpretativo

- mayor deuda → mayor probabilidad de default  
- mayor ingreso → menor probabilidad de default  
- más atrasos → mayor riesgo  

---

## Insight final

El modelo convierte todas estas variables en un score único que representa:

> Probabilidad de default del cliente

---

## Frase clave

Un modelo no falla por el algoritmo, falla cuando las variables no son consistentes entre entrenamiento y producción.