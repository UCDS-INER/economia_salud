#!/usr/bin/env python3
"""
Script de Análisis Exploratorio de Datos (EDA) para los datasets de resultados de pacientes.
Analiza cada archivo individual y el combinado, guardando resultados en archivos de texto.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def analyze_dataset(df, dataset_name, output_file):
    """Analiza un dataset y escribe los resultados en un archivo de texto."""
    
    output_file.write(f"\n{'='*80}\n")
    output_file.write(f"ANÁLISIS EXPLORATORIO DE DATOS - {dataset_name.upper()}\n")
    output_file.write(f"{'='*80}\n")
    output_file.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Información básica del dataset
    output_file.write("1. INFORMACIÓN BÁSICA DEL DATASET\n")
    output_file.write("-" * 50 + "\n")
    output_file.write(f"Dimensiones: {df.shape[0]:,} filas x {df.shape[1]} columnas\n")
    output_file.write(f"Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")
    output_file.write(f"Tipos de datos:\n")
    for col, dtype in df.dtypes.items():
        output_file.write(f"  - {col}: {dtype}\n")
    output_file.write("\n")
    
    # Información de columnas
    output_file.write("2. INFORMACIÓN DE COLUMNAS\n")
    output_file.write("-" * 50 + "\n")
    output_file.write(f"Columnas: {list(df.columns)}\n\n")
    
    # Valores faltantes
    output_file.write("3. VALORES FALTANTES\n")
    output_file.write("-" * 50 + "\n")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    missing_df = pd.DataFrame({
        'Valores_Faltantes': missing_data,
        'Porcentaje': missing_percent
    })
    missing_df = missing_df[missing_df['Valores_Faltantes'] > 0].sort_values('Valores_Faltantes', ascending=False)
    
    if len(missing_df) > 0:
        for col in missing_df.index:
            output_file.write(f"  - {col}: {missing_df.loc[col, 'Valores_Faltantes']:,} ({missing_df.loc[col, 'Porcentaje']:.2f}%)\n")
    else:
        output_file.write("  No hay valores faltantes\n")
    output_file.write("\n")
    
    # Estadísticas descriptivas
    output_file.write("4. ESTADÍSTICAS DESCRIPTIVAS\n")
    output_file.write("-" * 50 + "\n")
    
    # Columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        output_file.write("Columnas numéricas:\n")
        desc_stats = df[numeric_cols].describe()
        output_file.write(desc_stats.to_string())
        output_file.write("\n\n")
    
    # Columnas categóricas
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        output_file.write("Columnas categóricas:\n")
        for col in categorical_cols:
            output_file.write(f"\n{col}:\n")
            value_counts = df[col].value_counts()
            output_file.write(f"  Valores únicos: {df[col].nunique()}\n")
            output_file.write(f"  Top 5 valores más frecuentes:\n")
            for val, count in value_counts.head().items():
                output_file.write(f"    - {val}: {count:,} ({count/len(df)*100:.2f}%)\n")
        output_file.write("\n")
    
    # Análisis de fechas
    date_cols = ['fecha', 'fecha_egreso_general']
    for col in date_cols:
        if col in df.columns:
            output_file.write(f"5. ANÁLISIS DE {col.upper()}\n")
            output_file.write("-" * 50 + "\n")
            try:
                df[col] = pd.to_datetime(df[col])
                output_file.write(f"Rango de fechas: {df[col].min()} a {df[col].max()}\n")
                output_file.write(f"Duración total: {(df[col].max() - df[col].min()).days} días\n")
                output_file.write(f"Distribución por año:\n")
                year_counts = df[col].dt.year.value_counts().sort_index()
                for year, count in year_counts.items():
                    output_file.write(f"  - {year}: {count:,} registros\n")
                output_file.write("\n")
            except:
                output_file.write(f"No se pudo analizar la columna {col}\n\n")
    
    # Análisis de costos y montos
    cost_cols = ['costo_nivel_6', 'monto_nivel_1', 'monto_nivel_6']
    output_file.write("6. ANÁLISIS DE COSTOS Y MONTOS\n")
    output_file.write("-" * 50 + "\n")
    for col in cost_cols:
        if col in df.columns:
            output_file.write(f"\n{col}:\n")
            output_file.write(f"  Total: ${df[col].sum():,.2f}\n")
            output_file.write(f"  Promedio: ${df[col].mean():,.2f}\n")
            output_file.write(f"  Mediana: ${df[col].median():,.2f}\n")
            output_file.write(f"  Mínimo: ${df[col].min():,.2f}\n")
            output_file.write(f"  Máximo: ${df[col].max():,.2f}\n")
            output_file.write(f"  Desviación estándar: ${df[col].std():,.2f}\n")
    
    output_file.write("\n")
    
    # Análisis por área de servicio
    if 'area_servicio' in df.columns:
        output_file.write("7. ANÁLISIS POR ÁREA DE SERVICIO\n")
        output_file.write("-" * 50 + "\n")
        area_counts = df['area_servicio'].value_counts()
        output_file.write("Distribución por área de servicio:\n")
        for area, count in area_counts.head(10).items():
            output_file.write(f"  - {area}: {count:,} registros ({count/len(df)*100:.2f}%)\n")
        output_file.write("\n")
    
    # Análisis por origen
    if 'origen' in df.columns:
        output_file.write("8. ANÁLISIS POR ORIGEN\n")
        output_file.write("-" * 50 + "\n")
        origen_counts = df['origen'].value_counts()
        output_file.write("Distribución por origen:\n")
        for origen, count in origen_counts.items():
            output_file.write(f"  - {origen}: {count:,} registros ({count/len(df)*100:.2f}%)\n")
        output_file.write("\n")
    
    # Análisis de pacientes únicos
    if 'paciente' in df.columns:
        output_file.write("9. ANÁLISIS DE PACIENTES\n")
        output_file.write("-" * 50 + "\n")
        unique_patients = df['paciente'].nunique()
        output_file.write(f"Pacientes únicos: {unique_patients:,}\n")
        output_file.write(f"Promedio de registros por paciente: {len(df)/unique_patients:.2f}\n")
        
        # Top pacientes con más registros
        patient_counts = df['paciente'].value_counts()
        output_file.write(f"\nTop 10 pacientes con más registros:\n")
        for patient, count in patient_counts.head(10).items():
            output_file.write(f"  - Paciente {patient}: {count:,} registros\n")
        output_file.write("\n")
    
    output_file.write("\n" + "="*80 + "\n\n")

def main():
    # Crear directorio de resultados
    resultados_path = Path("resultados")
    resultados_path.mkdir(exist_ok=True)
    
    # Archivo de salida
    output_file_path = resultados_path / "eda_resultados.txt"
    
    print("Iniciando análisis exploratorio de datos...")
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("ANÁLISIS EXPLORATORIO DE DATOS - RESULTADOS DE PACIENTES\n")
        output_file.write("="*80 + "\n")
        output_file.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output_file.write("Este archivo contiene el análisis detallado de cada dataset individual y el combinado.\n\n")
        
        # Lista de archivos a analizar
        files_to_analyze = [
            ("data/raw/Resultados Pacientes Jan 2024 - Jul 2024.csv", "Jan 2024 - Jul 2024"),
            ("data/raw/Resultados Pacientes Jan-Jun 2025.csv", "Jan-Jun 2025"),
            ("data/raw/Resultados Pacientes Jul 2024 - Ene 2025.csv", "Jul 2024 - Ene 2025"),
            ("data/processed/resultados_pacientes_combinados.csv", "DATASET COMBINADO")
        ]
        
        # Analizar cada archivo
        for file_path, dataset_name in files_to_analyze:
            file_path = Path(file_path)
            if file_path.exists():
                print(f"Analizando: {dataset_name}")
                try:
                    # Leer el archivo
                    df = pd.read_csv(file_path, low_memory=False)
                    
                    # Analizar el dataset
                    analyze_dataset(df, dataset_name, output_file)
                    
                except Exception as e:
                    output_file.write(f"\nError analizando {dataset_name}: {str(e)}\n\n")
                    print(f"Error: {str(e)}")
            else:
                output_file.write(f"\nArchivo no encontrado: {file_path}\n\n")
                print(f"Archivo no encontrado: {file_path}")
        
        # Resumen final
        output_file.write("\n" + "="*80 + "\n")
        output_file.write("RESUMEN FINAL\n")
        output_file.write("="*80 + "\n")
        output_file.write("Análisis completado exitosamente.\n")
        output_file.write("Revisa cada sección para obtener información detallada de cada dataset.\n")
    
    print(f"\nAnálisis completado. Resultados guardados en: {output_file_path}")
    
    # Crear también un resumen ejecutivo
    create_executive_summary(resultados_path)

def create_executive_summary(resultados_path):
    """Crea un resumen ejecutivo con las métricas más importantes."""
    
    summary_path = resultados_path / "resumen_ejecutivo.txt"
    
    with open(summary_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write("RESUMEN EJECUTIVO - ANÁLISIS DE DATOS\n")
        summary_file.write("="*50 + "\n")
        summary_file.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Analizar archivos para el resumen
        files_info = [
            ("data/raw/Resultados Pacientes Jan 2024 - Jul 2024.csv", "Jan 2024 - Jul 2024"),
            ("data/raw/Resultados Pacientes Jan-Jun 2025.csv", "Jan-Jun 2025"),
            ("data/raw/Resultados Pacientes Jul 2024 - Ene 2025.csv", "Jul 2024 - Ene 2025"),
            ("data/processed/resultados_pacientes_combinados.csv", "COMBINADO")
        ]
        
        summary_file.write("MÉTRICAS PRINCIPALES POR DATASET:\n")
        summary_file.write("-" * 40 + "\n\n")
        
        for file_path, dataset_name in files_info:
            file_path = Path(file_path)
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path, low_memory=False)
                    
                    summary_file.write(f"{dataset_name}:\n")
                    summary_file.write(f"  - Registros: {len(df):,}\n")
                    summary_file.write(f"  - Columnas: {len(df.columns)}\n")
                    
                    if 'paciente' in df.columns:
                        unique_patients = df['paciente'].nunique()
                        summary_file.write(f"  - Pacientes únicos: {unique_patients:,}\n")
                        summary_file.write(f"  - Promedio registros/paciente: {len(df)/unique_patients:.1f}\n")
                    
                    if 'costo_nivel_6' in df.columns:
                        total_cost = df['costo_nivel_6'].sum()
                        summary_file.write(f"  - Total costo nivel 6: ${total_cost:,.0f}\n")
                    
                    if 'monto_nivel_6' in df.columns:
                        total_amount = df['monto_nivel_6'].sum()
                        summary_file.write(f"  - Total monto nivel 6: ${total_amount:,.0f}\n")
                    
                    summary_file.write("\n")
                    
                except Exception as e:
                    summary_file.write(f"  Error: {str(e)}\n\n")
    
    print(f"Resumen ejecutivo guardado en: {summary_path}")

if __name__ == "__main__":
    main() 