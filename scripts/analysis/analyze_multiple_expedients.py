#!/usr/bin/env python3
"""
Script para identificar y analizar pacientes con múltiples expedientes o IAN.
Ayuda a entender las diferencias en los conteos de pacientes únicos.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def analyze_multiple_expedients():
    """Analiza pacientes con múltiples expedientes o IAN."""
    
    # Crear directorio de resultados si no existe
    resultados_path = Path("resultados")
    resultados_path.mkdir(exist_ok=True)
    
    # Leer el archivo combinado
    combined_file = Path("data/processed/resultados_pacientes_combinados.csv")
    if not combined_file.exists():
        print("Error: No se encontró el archivo combinado. Ejecuta primero join.py")
        return
    
    print("Leyendo archivo combinado...")
    df = pd.read_csv(combined_file, low_memory=False)
    print(f"Total de registros: {len(df):,}")
    
    # Crear archivo de resultados
    output_file = resultados_path / "analisis_multiples_expedientes.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS DE PACIENTES CON MÚLTIPLES EXPEDIENTES O IAN\n")
        f.write("="*70 + "\n")
        f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 1. Análisis básico de pacientes únicos
        f.write("1. ANÁLISIS BÁSICO DE PACIENTES\n")
        f.write("-" * 50 + "\n")
        
        total_patients = df['paciente'].nunique()
        total_expedients = df['n_expediente_hosp'].nunique()
        total_ians = df['ian_expediente_hosp'].nunique()
        
        f.write(f"Pacientes únicos (solo por ID): {total_patients:,}\n")
        f.write(f"Expedientes únicos: {total_expedients:,}\n")
        f.write(f"IAN únicos: {total_ians:,}\n")
        f.write(f"Total de registros: {len(df):,}\n\n")
        
        # 2. Pacientes con múltiples expedientes
        f.write("2. PACIENTES CON MÚLTIPLES EXPEDIENTES\n")
        f.write("-" * 50 + "\n")
        
        # Agrupar por paciente y contar expedientes únicos
        patient_expedient_counts = df.groupby('paciente')['n_expediente_hosp'].nunique()
        patients_multiple_expedients = patient_expedient_counts[patient_expedient_counts > 1]
        
        f.write(f"Pacientes con múltiples expedientes: {len(patients_multiple_expedients):,}\n")
        f.write(f"Porcentaje del total: {len(patients_multiple_expedients)/total_patients*100:.2f}%\n\n")
        
        # Distribución de número de expedientes por paciente
        expedient_distribution = patient_expedient_counts.value_counts().sort_index()
        f.write("Distribución de expedientes por paciente:\n")
        for num_expedients, count in expedient_distribution.items():
            f.write(f"  - {num_expedients} expediente(s): {count:,} pacientes ({count/total_patients*100:.2f}%)\n")
        f.write("\n")
        
        # Top 10 pacientes con más expedientes
        top_patients_expedients = patient_expedient_counts.sort_values(ascending=False).head(10)
        f.write("Top 10 pacientes con más expedientes:\n")
        for patient, num_expedients in top_patients_expedients.items():
            f.write(f"  - Paciente {patient}: {num_expedients} expedientes\n")
        f.write("\n")
        
        # 3. Pacientes con múltiples IAN
        f.write("3. PACIENTES CON MÚLTIPLES IAN\n")
        f.write("-" * 50 + "\n")
        
        # Agrupar por paciente y contar IAN únicos
        patient_ian_counts = df.groupby('paciente')['ian_expediente_hosp'].nunique()
        patients_multiple_ians = patient_ian_counts[patient_ian_counts > 1]
        
        f.write(f"Pacientes con múltiples IAN: {len(patients_multiple_ians):,}\n")
        f.write(f"Porcentaje del total: {len(patients_multiple_ians)/total_patients*100:.2f}%\n\n")
        
        # Distribución de número de IAN por paciente
        ian_distribution = patient_ian_counts.value_counts().sort_index()
        f.write("Distribución de IAN por paciente:\n")
        for num_ians, count in ian_distribution.items():
            f.write(f"  - {num_ians} IAN(s): {count:,} pacientes ({count/total_patients*100:.2f}%)\n")
        f.write("\n")
        
        # Top 10 pacientes con más IAN
        top_patients_ians = patient_ian_counts.sort_values(ascending=False).head(10)
        f.write("Top 10 pacientes con más IAN:\n")
        for patient, num_ians in top_patients_ians.items():
            f.write(f"  - Paciente {patient}: {num_ians} IAN\n")
        f.write("\n")
        
        # 4. Análisis detallado de pacientes con múltiples expedientes
        f.write("4. ANÁLISIS DETALLADO DE PACIENTES CON MÚLTIPLES EXPEDIENTES\n")
        f.write("-" * 70 + "\n")
        
        # Obtener datos de pacientes con múltiples expedientes
        patients_with_multiple = patients_multiple_expedients.index.tolist()
        df_multiple = df[df['paciente'].isin(patients_with_multiple)]
        
        f.write(f"Registros de pacientes con múltiples expedientes: {len(df_multiple):,}\n")
        f.write(f"Porcentaje del total de registros: {len(df_multiple)/len(df)*100:.2f}%\n\n")
        
        # Análisis por archivo de origen
        f.write("Distribución por archivo de origen:\n")
        origin_counts = df_multiple['archivo_origen'].value_counts()
        for origin, count in origin_counts.items():
            f.write(f"  - {origin}: {count:,} registros ({count/len(df_multiple)*100:.2f}%)\n")
        f.write("\n")
        
        # Análisis por área de servicio
        f.write("Top 10 áreas de servicio para pacientes con múltiples expedientes:\n")
        area_counts = df_multiple['area_servicio'].value_counts().head(10)
        for area, count in area_counts.items():
            f.write(f"  - {area}: {count:,} registros\n")
        f.write("\n")
        
        # 5. Ejemplos específicos
        f.write("5. EJEMPLOS ESPECÍFICOS\n")
        f.write("-" * 50 + "\n")
        
        # Mostrar detalles de los 5 pacientes con más expedientes
        f.write("Detalles de los 5 pacientes con más expedientes:\n\n")
        
        for i, (patient, num_expedients) in enumerate(top_patients_expedients.head(5).items()):
            f.write(f"Paciente {patient} ({num_expedients} expedientes):\n")
            
            patient_data = df[df['paciente'] == patient]
            expedients = patient_data['n_expediente_hosp'].unique()
            ians = patient_data['ian_expediente_hosp'].unique()
            
            f.write(f"  Expedientes: {list(expedients)}\n")
            f.write(f"  IAN: {list(ians)}\n")
            f.write(f"  Total registros: {len(patient_data):,}\n")
            f.write(f"  Rango de fechas: {patient_data['fecha'].min()} a {patient_data['fecha'].max()}\n")
            f.write(f"  Total costo nivel 6: ${patient_data['costo_nivel_6'].sum():,.2f}\n")
            f.write(f"  Total monto nivel 6: ${patient_data['monto_nivel_6'].sum():,.2f}\n")
            f.write("\n")
        
        # 6. Comparación de métodos de conteo
        f.write("6. COMPARACIÓN DE MÉTODOS DE CONTEO\n")
        f.write("-" * 50 + "\n")
        
        # Método 1: Solo por paciente
        count_method1 = df['paciente'].nunique()
        
        # Método 2: Por paciente + expediente
        count_method2 = df.groupby(['paciente', 'n_expediente_hosp']).size().reset_index().shape[0]
        
        # Método 3: Por paciente + expediente + IAN
        count_method3 = df.groupby(['paciente', 'n_expediente_hosp', 'ian_expediente_hosp']).size().reset_index().shape[0]
        
        f.write(f"Método 1 (solo paciente): {count_method1:,}\n")
        f.write(f"Método 2 (paciente + expediente): {count_method2:,}\n")
        f.write(f"Método 3 (paciente + expediente + IAN): {count_method3:,}\n")
        f.write(f"Diferencia Método 2 vs 1: {count_method2 - count_method1:,} (+{(count_method2-count_method1)/count_method1*100:.2f}%)\n")
        f.write(f"Diferencia Método 3 vs 1: {count_method3 - count_method1:,} (+{(count_method3-count_method1)/count_method1*100:.2f}%)\n")
        f.write(f"Diferencia Método 3 vs 2: {count_method3 - count_method2:,} (+{(count_method3-count_method2)/count_method2*100:.2f}%)\n\n")
        
        # 7. Recomendaciones
        f.write("7. RECOMENDACIONES\n")
        f.write("-" * 50 + "\n")
        f.write("Basado en el análisis:\n")
        f.write("1. El método más preciso para contar pacientes únicos es considerar paciente + expediente + IAN\n")
        f.write("2. Hay {:.1f}% de pacientes con múltiples expedientes\n".format(len(patients_multiple_expedients)/total_patients*100))
        f.write("3. Hay {:.1f}% de pacientes con múltiples IAN\n".format(len(patients_multiple_ians)/total_patients*100))
        f.write("4. Los pacientes con múltiples expedientes representan {:.1f}% de todos los registros\n".format(len(df_multiple)/len(df)*100))
        f.write("5. Se recomienda usar el método 3 para análisis de costos por paciente/episodio\n\n")
        
        f.write("="*70 + "\n")
        f.write("Análisis completado.\n")
    
    print(f"Análisis completado. Resultados guardados en: {output_file}")
    
    # Crear también un CSV con los pacientes con múltiples expedientes
    create_multiple_expedients_csv(df, resultados_path)

def create_multiple_expedients_csv(df, resultados_path):
    """Crea un CSV con los pacientes que tienen múltiples expedientes."""
    
    # Identificar pacientes con múltiples expedientes
    patient_expedient_counts = df.groupby('paciente')['n_expediente_hosp'].nunique()
    patients_multiple_expedients = patient_expedient_counts[patient_expedient_counts > 1]
    
    # Obtener datos de estos pacientes
    df_multiple = df[df['paciente'].isin(patients_multiple_expedients.index)]
    
    # Crear resumen por paciente
    summary_multiple = df_multiple.groupby(['paciente', 'n_expediente_hosp', 'ian_expediente_hosp']).agg({
        'fecha': ['min', 'max'],
        'costo_nivel_6': 'sum',
        'monto_nivel_6': 'sum',
        'cantidad': 'sum',
        'archivo_origen': 'first'
    }).reset_index()
    
    # Renombrar columnas
    summary_multiple.columns = [
        'paciente', 'n_expediente_hosp', 'ian_expediente_hosp',
        'fecha_inicio', 'fecha_fin', 'total_costo_nivel_6', 
        'total_monto_nivel_6', 'total_cantidad', 'archivo_origen'
    ]
    
    # Agregar número de expedientes por paciente
    expedient_counts = df_multiple.groupby('paciente')['n_expediente_hosp'].nunique()
    summary_multiple['num_expedientes_paciente'] = summary_multiple['paciente'].map(expedient_counts)
    
    # Guardar CSV
    csv_file = resultados_path / "pacientes_multiples_expedientes.csv"
    summary_multiple.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"CSV con pacientes múltiples expedientes guardado en: {csv_file}")

if __name__ == "__main__":
    analyze_multiple_expedients() 