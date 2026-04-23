# Tarea — Modelo de Regresión Logística para Riesgo Crediticio

## Objetivo

Construir un modelo de regresión logística utilizando los datasets:

- train.csv
- test.csv

El objetivo es predecir la variable:

> default_in_last_6months

y replicar un flujo similar al visto en clase:

- Modelamiento
- Interpretación
- Score de riesgo
- Evaluación de negocio

---

# 1. Entendimiento del problema

Se busca estimar la probabilidad de que un cliente entre en default.

### Variable objetivo

| Variable                     | Tipo   | Descripción                                                                 |
|-----------------------------|--------|-----------------------------------------------------------------------------|
| default_in_last_6months     | Binaria| 1 = cliente en default, 0 = cliente sin default                            |

---

## Interpretación

El modelo responde:

> “¿Qué probabilidad tiene este cliente de caer en default en los próximos 6 meses?”

---

# 2. Diccionario de datos

Antes de modelar, se debe analizar y documentar las variables.

---

## 2.1 Variables del dataset

Clasificar todas las variables en:

### Numéricas
Ejemplo:
- ingresos
- deuda
- saldo
- edad

### Categóricas
Ejemplo:
- segmento
- tipo de producto
- región

### Técnicas (NO usar)
- id
- index

---

## 2.2 Validación crítica: Train vs Test

Comparar columnas entre:

- train.csv
- test.csv

---

## Problema detectado

El dataset `test.csv` contiene una variable adicional que no está en `train.csv`.

---

## Acción obligatoria

> El modelo solo puede usar variables vistas en entrenamiento.

Por lo tanto:

- eliminar columnas extra en test
- asegurar mismas variables en ambos datasets

---

## Regla clave

> Train y test deben tener exactamente las mismas columnas (excepto el target)

---

# 3. Exploración de datos

Analizar:

- distribución del target
- valores nulos
- outliers
- tipo de variables

Preguntas clave:

- ¿hay desbalance de clases?
- ¿hay variables irrelevantes?
- ¿hay variables con alta correlación?

---

# 4. Preprocesamiento

## 4.1 Manejo de nulos

- numéricas → media o mediana  
- categóricas → "missing"

---

## 4.2 Variables categóricas

- One Hot Encoding  
o  
- reducción de categorías

---

## 4.3 Escalamiento

Recomendado para regresión logística:

- StandardScaler

---

# 5. Separación de variables

Definir:

- X_train, y_train
- X_test, y_test

---

## Advertencia

Evitar:

- incluir target en features
- usar variables que generen leakage

---

# 6. Entrenamiento del modelo

Modelo a utilizar:

> Regresión logística

---

## Interpretación

El modelo estima:

P(y = 1 | X)

Es decir:

> Probabilidad de default dado el perfil del cliente

---

# 7. Predicción

Obtener:

- Probabilidades → score
- Clasificación → clase

---

## Interpretación

- score cercano a 1 → alto riesgo  
- score cercano a 0 → bajo riesgo  

---

# 8. Evaluación

## Métricas

- AUC
- Accuracy

---

## Enfoque banca

Gini:

Gini = 2 * AUC - 1

---

## Interpretación

- mayor AUC → mejor separación  
- mayor Gini → mejor ranking de riesgo  

---

# 9. Interpretación del modelo

Analizar coeficientes:

- coef > 0 → aumenta riesgo  
- coef < 0 → reduce riesgo  

---

## Ejemplo

- deuda ↑ → mayor riesgo  
- ingresos ↑ → menor riesgo  

---

# 10. Construcción del score

El modelo sigue:

z = β0 + β1X1 + β2X2 + ...

Luego:

P(y=1) = 1 / (1 + e^{-z})

---

## Interpretación simple

- z → score lineal  
- sigmoid → probabilidad  

---

## Analogía

El modelo combina todas las variables en un solo número que representa el riesgo.

---

# 11. Segmentación de clientes

Dividir el score en bandas:

- Muy alto riesgo  
- Alto  
- Medio  
- Bajo  
- Muy bajo  

---

## Validación

Para cada banda:

- número de clientes  
- tasa de default  

---

## Resultado esperado

> Las bandas deben ser monotónicas

---

# 12. Evaluación en test

Aplicar el modelo en test:

- sin reentrenar  
- solo inferencia  

---

## Validar

- AUC train vs test  
- estabilidad del modelo  

---

# 13. Conclusiones de negocio

Responder:

- ¿El modelo separa bien clientes?
- ¿Es útil para decisiones?
- ¿Las variables tienen sentido económico?

---

# Insight final

El modelo convierte múltiples variables en un score:

- permite ordenar clientes  
- facilita decisiones  
- simplifica problemas complejos  

---

# Advertencia final

Si train y test no tienen las mismas variables:

- el modelo fallará  
- o dará resultados incorrectos  

---

## Frase clave

> “Un buen modelo no sirve si los datos no son consistentes.”