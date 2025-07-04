#!/usr/bin/env python3
"""
Ejemplos simples y directos para filtrar un DataFrame
"""

import pandas as pd
import numpy as np

# Crear un DataFrame de ejemplo
np.random.seed(42)
df = pd.DataFrame({
    'id': range(1, 21),
    'nombre': [f'Paciente_{i}' for i in range(1, 21)],
    'edad': np.random.randint(25, 80, 20),
    'genero': np.random.choice(['M', 'F'], 20),
    'diagnostico': np.random.choice(['Diabetes', 'Hipertensión', 'Cardiopatía', 'Cáncer'], 20),
    'costo': np.random.uniform(5000, 40000, 20).round(2),
    'estado': np.random.choice(['Activo', 'Inactivo', 'Alta'], 20)
})

print("📊 DATAFRAME ORIGINAL:")
print(df)
print(f"\nDimensiones: {df.shape}")

print("\n" + "="*50)
print("EJEMPLOS DE FILTRADO")
print("="*50)

# 1. Filtrar por valor exacto
print("\n1️⃣ FILTRAR POR VALOR EXACTO")
print("Pacientes con estado 'Activo':")
activos = df[df['estado'] == 'Activo']
print(activos)

# 2. Filtrar por múltiples valores
print("\n2️⃣ FILTRAR POR MÚLTIPLES VALORES")
print("Pacientes con diagnóstico 'Diabetes' o 'Hipertensión':")
diabetes_hipertension = df[df['diagnostico'].isin(['Diabetes', 'Hipertensión'])]
print(diabetes_hipertension)

# 3. Filtrar por rango de valores
print("\n3️⃣ FILTRAR POR RANGO DE VALORES")
print("Pacientes entre 40 y 60 años:")
edad_media = df[(df['edad'] >= 40) & (df['edad'] <= 60)]
print(edad_media)

# 4. Filtrar por valor mayor que
print("\n4️⃣ FILTRAR POR VALOR MAYOR QUE")
print("Pacientes con costo mayor a $20,000:")
costo_alto = df[df['costo'] > 20000]
print(costo_alto)

# 5. Filtrar por texto que contenga
print("\n5️⃣ FILTRAR POR TEXTO QUE CONTENGA")
print("Pacientes con diagnóstico que contenga 'ia':")
contiene_ia = df[df['diagnostico'].str.contains('ia', case=False)]
print(contiene_ia)

# 6. Filtrar con múltiples condiciones
print("\n6️⃣ FILTRAR CON MÚLTIPLES CONDICIONES")
print("Pacientes activos, mayores de 50 años y costo > $15,000:")
complejo = df[
    (df['estado'] == 'Activo') & 
    (df['edad'] > 50) & 
    (df['costo'] > 15000)
]
print(complejo)

# 7. Usando query() - más legible
print("\n7️⃣ USANDO QUERY() - MÁS LEGIBLE")
print("Pacientes femeninos con costo entre $10,000 y $30,000:")
query_result = df.query("genero == 'F' and 10000 <= costo <= 30000")
print(query_result)

# 8. Filtrar por valores nulos
print("\n8️⃣ FILTRAR POR VALORES NULOS")
print("Columnas con valores nulos:")
print(df.isnull().sum())

# 9. Filtrar por valores únicos
print("\n9️⃣ VALORES ÚNICOS EN COLUMNAS")
print("Diagnósticos únicos:", df['diagnostico'].unique())
print("Estados únicos:", df['estado'].unique())

# 10. Contar resultados de filtros
print("\n🔢 RESUMEN DE FILTROS:")
print(f"Total de pacientes: {len(df)}")
print(f"Pacientes activos: {len(df[df['estado'] == 'Activo'])}")
print(f"Pacientes inactivos: {len(df[df['estado'] == 'Inactivo'])}")
print(f"Pacientes con alta: {len(df[df['estado'] == 'Alta'])}")
print(f"Pacientes con costo > $25,000: {len(df[df['costo'] > 25000])}")

print("\n✅ Ejemplos completados!") 