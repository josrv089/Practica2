import pandas as pd
import time
import sqlite3

# 1) Carga un subconjunto de un millon de registros
# Medir tiempo de carga
t0 = time.perf_counter()

DB_PATH = "power.db"
TABLE_NAME = "power_data"

df = pd.read_csv(
    "household_power_consumption.txt",
    sep=";",                 # <— IMPORTANTE: separador correcto, esto debido a que el dataset que se usa está con ;
    nrows=2000000,              # 
    na_values=["?"],         # los faltantes vienen como '?'
    low_memory=False
)
t1 = time.perf_counter()
print(f"Tiempo de carga: {t1 - t0:.2f} segundos")
# Inicialmente se realiza un brebe analisis exploratorio de datos, para ver un poco posibles problemas o cosas a conciderar
print("=== Información del Dataset ===")
print(df.info())

print("\n=== Primeras filas ===")
print(df.head())

print("\n=== Descripción ===")
print(df.describe)

print("\n=== Estadísticas numéricas ===")
print(df.select_dtypes(include="number").describe())

print("\n=== Nulos por columna ===")
print(df.isna().sum())

# Valores únicos de algunas columnas reales del dataset
for col in ["Date", "Time"]:
    if col in df.columns:
        print(f"\n=== Valores únicos en '{col}' (muestra) ===")
        print(df[col].head().unique())




# Ahora vamos con la conexión a SQLite.

# Se realiza la conexión:
conn = sqlite3.connect(DB_PATH)

tsql0 = time.perf_counter()
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
tsql1 = time.perf_counter()

print(f"Tiempo de carga en SQLite: {tsql1 - tsql0:.2f} segundos")



print("=== Consulta 1: Promedio de potencia activa global osea, el campo Global_active_power (El uso de la tabla lo estoy asumiendo por el nombre pero no estoy seguro si es el real) ===")
q1 = f"""
SELECT AVG(Global_active_power) AS avg_active_power
FROM {TABLE_NAME}
"""
print(pd.read_sql_query(q1, conn))

print("\n=== Consulta 2: Promedio de voltaje agrupado por día ===")
q2 = f"""
SELECT Date, AVG(Voltage) AS avg_voltage
FROM {TABLE_NAME}
GROUP BY Date
LIMIT 10
"""
print(pd.read_sql_query(q2, conn))

print("\n=== Consulta 3: Top 5 horas con mayor consumo promedio de Sub_metering_1, también para esta columna se asume el uso de esos datos ===")
q3 = f"""
SELECT Time, AVG(Sub_metering_1) AS avg_sub1
FROM {TABLE_NAME}
GROUP BY Time
ORDER BY avg_sub1 DESC
LIMIT 5
"""
print(pd.read_sql_query(q3, conn))

conn.close()