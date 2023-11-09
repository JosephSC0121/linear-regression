import random
from openpyxl import Workbook
import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
import os
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

# Cargar configuración desde un archivo .yml
with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

python_path = config.get('python_path')
os.environ['PYSPARK_PYTHON'] = python_path

def cargarDatos():
    return pd.read_excel('datos_docentes.xlsx') 

def prepararDatosParaRegresion(df):
    spark = SparkSession.builder.appName("ejemplo_regresion_lineal").getOrCreate()
    df_spark = spark.createDataFrame(df)

    vector_assembler = VectorAssembler(inputCols=["Carga de Trabajo (horas)", "Semestre/Ciclo", "Rendimiento Académico (promedio)", "Preferencias de Estudiantes (%)", "Evaluación de Docentes (escala 1-10)", "Disponibilidad de Recursos (%)"], outputCol="features")
    df_assembled = vector_assembler.transform(df_spark)

    return df_assembled, spark

def entrenarModelo(df_assembled, spark):
    train_df, test_df = df_assembled.randomSplit([0.8, 0.2], seed=42)
    lr = LinearRegression(featuresCol="features", labelCol="Resultados de Aprendizaje (%)") 
    lr_model = lr.fit(train_df)

    predictions = lr_model.transform(test_df)
    evaluator = RegressionEvaluator(labelCol="Resultados de Aprendizaje (%)", predictionCol="prediction", metricName="rmse") 
    rmse = evaluator.evaluate(predictions)

    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Coeficientes: {lr_model.coefficients}")
    print(f"Intercepción: {lr_model.intercept}")

    # Obtener las predicciones en un DataFrame de Pandas
    predictions_df = predictions.toPandas()

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Graficar los puntos reales
    plt.scatter(predictions_df["Resultados de Aprendizaje (%)"], predictions_df["prediction"], alpha=0.5, color='green') 

    # Graficar la línea de regresión
    sns.regplot(x="Resultados de Aprendizaje (%)", y="prediction", data=predictions_df, scatter=False, color='green')  

    plt.title('Regresión Lineal')
    plt.xlabel('Resultados de Aprendizaje (%)')
    plt.ylabel('Resultados de Aprendizaje Predichos')
    plt.show()

    # Visualizar la relación entre "Carga de Trabajo (horas)" y predicciones
    visualizarRelacionCaracteristica(predictions_df)

    spark.stop()

def visualizarRelacionCaracteristica(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Graficar la relación entre "Carga de Trabajo (horas)" y las predicciones
    plt.scatter(df["Carga de Trabajo (horas)"], df["prediction"], alpha=0.5, color='blue') 

    plt.title('Relación entre Carga de Trabajo y Predicciones')
    plt.xlabel('Carga de Trabajo (horas)')
    plt.ylabel('Resultados de Aprendizaje Predichos')
    plt.show()
def calcularModa(df, columna):
    if df[columna].dtype == 'int64':
        return df[columna].mode()[0]
    return None

def calcularMediana(df, columna):
    if df[columna].dtype == 'int64':
        return df[columna].median()
    return None

def calcularMedia(df, columna):
    if df[columna].dtype == 'int64':
        return df[columna].mean()
    return None

def estadisticaDescriptiva(df):
    columnas_numericas = df.select_dtypes(include='int64').columns

    for columna in columnas_numericas:
        if columna != 'ID del Docente':
            moda = calcularModa(df, columna)
            mediana = calcularMediana(df, columna)
            media = calcularMedia(df, columna)

            if moda is not None and mediana is not None and media is not None:
                print(f'*****************{columna}*****************')
                print(f'Moda: {moda}')
                print(f'Mediana: {mediana}')
                print(f'Media: {media}')
    
    columnas_interes = df.columns[1:] 
    describe = df[columnas_interes].describe()
    print(describe)

if __name__ == "__main__":
    datos = cargarDatos()
    df_assembled, spark = prepararDatosParaRegresion(datos)
    entrenarModelo(df_assembled, spark)
    estadisticaDescriptiva(datos)
