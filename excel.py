import pandas as pd
import random

# Lista de nombres y apellidos
nombres = ["Juan", "María", "Luis", "Ana", "Carlos", "Laura", "Pedro", "Sofía", "Diego", "Valentina"]
apellidos = ["Gómez", "Pérez", "Martínez", "López", "Rodríguez", "González", "Sánchez", "Díaz", "Hernández", "Muñoz"]

# Crear una lista de IDs de docente
ids_docente = [random.randint(1000000, 2000000) for _ in range(1000)]

# Asignar nombres y apellidos aleatorios a los docentes
nombres_docente = random.choices(nombres, k=1000)
apellidos_docente = random.choices(apellidos, k=1000)

# Generar carga de trabajo aleatoria (en horas)
carga_trabajo = [random.randint(10, 30) for _ in range(1000)]

# Definir áreas de especialización
areas_especializacion = ['Redes', 'Programación', 'Base de Datos', 'Inteligencia Artificial', 'Sistemas Operativos']

# Asignar áreas de especialización aleatorias a los docentes
areas_docente = random.choices(areas_especializacion, k=1000)

# Generar semestres aleatorios
semestres = [random.randint(1, 10) for _ in range(1000)]

# Definir lista de cursos
cursos = ['Curso{}'.format(i) for i in range(1, 11)]

# Asignar cursos a los semestres
cursos_semestre = [random.choice(cursos) for _ in range(1000)]

# Generar rendimiento académico aleatorio (en promedio)
rendimiento_academico = [round(random.uniform(2.0, 5.0), 2) for _ in range(1000)]

# Definir preferencias de estudiantes (porcentajes de preferencia)
preferencias_estudiantes = [random.randint(1, 100) for _ in range(1000)]

# Generar evaluaciones de docentes (en escala de 1 a 10)
evaluaciones_docentes = [round(random.uniform(5.0, 10.0), 2) for _ in range(1000)]

# Definir disponibilidad de recursos (porcentaje de disponibilidad)
disponibilidad_recursos = [random.randint(50, 100) for _ in range(1000)]

# Generar resultados de aprendizaje (porcentaje de logro)
resultados_aprendizaje = [random.randint(60, 100) for _ in range(1000)]

# Crear un DataFrame con los datos generados
data = pd.DataFrame({
    'ID del Docente': ids_docente,
    'Nombres del Docente': nombres_docente,
    'Apellidos del Docente': apellidos_docente,
    'Carga de Trabajo (horas)': carga_trabajo,
    'Áreas de Especialización': areas_docente,
    'Semestre/Ciclo': semestres,
    'Curso/Asignatura': cursos_semestre,
    'Rendimiento Académico (promedio)': rendimiento_academico,
    'Preferencias de Estudiantes (%)': preferencias_estudiantes,
    'Evaluación de Docentes (escala 1-10)': evaluaciones_docentes,
    'Disponibilidad de Recursos (%)': disponibilidad_recursos,
    'Resultados de Aprendizaje (%)': resultados_aprendizaje
})

# Guardar los datos en un archivo de Excel
data.to_excel('datos_docentes.xlsx', index=False, sheet_name='Sheet1')
