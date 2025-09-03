# Informe de Práctica: Carga y Manejo de Datasets Grandes

## 1. Carga de datos con pandas
- **Dataset:** Individual Household Electric Power Consumption  
- **Filas cargadas:** 2,000,000  
- **Tiempo de carga con pandas:** **2.70 segundos**  
- **Columnas:** 9 (2 categóricas: `Date`, `Time`; 7 numéricas de consumo eléctrico).  
- **Memoria usada:** ~137 MB  

### Problemas detectados
- 25,978 valores nulos en las variables numéricas (`Global_active_power`, `Voltage`, etc.).  
- Variables de fecha y hora (`Date`, `Time`) aparecen separadas y pueden combinarse en una columna `datetime` para análisis temporal.  

### Estadísticas descriptivas (resumen)
- **Global Active Power:** media = 1.09 kW, máx = 11.12 kW.  
- **Voltage:** media = 240.8 V, rango = [223.2 – 254.1].  
- **Global Intensity:** media = 4.6 A, máx = 48.4 A.  
- **Sub_metering:** valores bajos en la mayoría de registros, con picos hasta 88 en `Sub_metering_1` y 80 en `Sub_metering_2`.  

---

## 2. Carga en SQLite
- **Filas insertadas:** 2,000,000  
- **Tiempo de carga en SQLite:** **11.03 segundos**  
- **Base de datos generada:** `power.db`  
- **Tabla creada:** `power_data`  

---

## 3. Consultas SQL realizadas

### Consulta 1: Promedio de potencia activa global
```sql
SELECT AVG(Global_active_power) AS avg_active_power
FROM power_data;
```
Resultado: 1.09 kW

![Histograma](/hist_global_active_power.png)


Consulta 2: Promedio de voltaje agrupado por día
```sql
SELECT Date, AVG(Voltage) AS avg_voltage
FROM power_data
GROUP BY Date
LIMIT 10;
```

Resultado:
        Date  avg_voltage
0   1/1/2007   240.128979
1   1/1/2008   241.036674
2   1/1/2009   242.836062
3   1/1/2010   242.565722
4  1/10/2007   239.239917
5  1/10/2008   241.128611
6  1/10/2009   241.529521
7  1/10/2010   240.801979
8  1/11/2007   240.938403
9  1/11/2008   241.810236

![Consumo por hora](/line_global_active_power_by_hour.png)


Consulta 3: Top 5 horas con mayor consumo promedio en Sub_metering_1
```sql
SELECT Time, AVG(Sub_metering_1) AS avg_sub1
FROM power_data
GROUP BY Time
ORDER BY avg_sub1 DESC
LIMIT 5;
```
Resultado:
       Time  avg_sub1
0  20:53:00  3.440320
1  20:52:00  3.411936
2  20:43:00  3.373362
3  20:49:00  3.340611
4  20:50:00  3.338428

![Sub-meterings promedio](/bar_sub_meterings_mean.png)
