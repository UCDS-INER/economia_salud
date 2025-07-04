#!/usr/bin/env python3
"""
Script para analizar el archivo de resumen original y compararlo con los datos procesados.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def analyze_summary_file():
    """Analiza el archivo de resumen original."""
    
    # Crear directorio de resultados si no existe
    resultados_path = Path("resultados")
    resultados_path.mkdir(exist_ok=True)
    
    # Leer el archivo de resumen original
    summary_file = Path("data/raw/Resumen Pacientes 2024-2025.csv")
    if not summary_file.exists():
        print("Error: No se encontró el archivo de resumen original")
        return
    
    print("Leyendo archivo de resumen original...")
    df_summary = pd.read_csv(summary_file, low_memory=False)
    print(f"Total de registros: {len(df_summary):,}")
    
    # Crear archivo de análisis
    output_file = resultados_path / "analisis_archivo_resumen.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS DEL ARCHIVO DE RESUMEN ORIGINAL\n")
        f.write("="*60 + "\n")
        f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 1. Información básica del dataset
        f.write("1. INFORMACIÓN BÁSICA DEL DATASET\n")
        f.write("-" * 50 + "\n")
        f.write(f"Dimensiones: {df_summary.shape[0]:,} filas x {df_summary.shape[1]} columnas\n")
        f.write(f"Tamaño en memoria: {df_summary.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")
        f.write(f"Tipos de datos:\n")
        for col, dtype in df_summary.dtypes.items():
            f.write(f"  - {col}: {dtype}\n")
        f.write("\n")
        
        # 2. Lista de columnas
        f.write("2. LISTA DE COLUMNAS\n")
        f.write("-" * 50 + "\n")
        f.write("Columnas disponibles:\n")
        for i, col in enumerate(df_summary.columns, 1):
            f.write(f"  {i:2d}. {col}\n")
        f.write("\n")
        
        # 3. Valores faltantes
        f.write("3. VALORES FALTANTES\n")
        f.write("-" * 50 + "\n")
        missing_data = df_summary.isnull().sum()
        missing_percent = (missing_data / len(df_summary)) * 100
        missing_df = pd.DataFrame({
            'Valores_Faltantes': missing_data,
            'Porcentaje': missing_percent
        })
        missing_df = missing_df[missing_df['Valores_Faltantes'] > 0].sort_values('Valores_Faltantes', ascending=False)
        
        if len(missing_df) > 0:
            for col in missing_df.index:
                f.write(f"  - {col}: {missing_df.loc[col, 'Valores_Faltantes']:,} ({missing_df.loc[col, 'Porcentaje']:.2f}%)\n")
        else:
            f.write("  No hay valores faltantes\n")
        f.write("\n")
        
        # 4. Análisis de pacientes únicos
        f.write("4. ANÁLISIS DE PACIENTES ÚNICOS\n")
        f.write("-" * 50 + "\n")
        
        # Identificar columnas de paciente
        patient_cols = [col for col in df_summary.columns if 'paciente' in col.lower()]
        f.write(f"Columnas relacionadas con pacientes: {patient_cols}\n\n")
        
        for col in patient_cols:
            unique_count = df_summary[col].nunique()
            f.write(f"{col}:\n")
            f.write(f"  - Valores únicos: {unique_count:,}\n")
            f.write(f"  - Valores nulos: {df_summary[col].isnull().sum():,}\n")
            if unique_count > 0:
                f.write(f"  - Ejemplos: {list(df_summary[col].dropna().unique()[:5])}\n")
            f.write("\n")
        
        # 5. Análisis de expedientes
        f.write("5. ANÁLISIS DE EXPEDIENTES\n")
        f.write("-" * 50 + "\n")
        
        # Identificar columnas de expediente
        expedient_cols = [col for col in df_summary.columns if 'expediente' in col.lower()]
        f.write(f"Columnas relacionadas con expedientes: {expedient_cols}\n\n")
        
        for col in expedient_cols:
            unique_count = df_summary[col].nunique()
            f.write(f"{col}:\n")
            f.write(f"  - Valores únicos: {unique_count:,}\n")
            f.write(f"  - Valores nulos: {df_summary[col].isnull().sum():,}\n")
            if unique_count > 0:
                f.write(f"  - Ejemplos: {list(df_summary[col].dropna().unique()[:5])}\n")
            f.write("\n")
        
        # 6. Análisis de gastos
        f.write("6. ANÁLISIS DE GASTOS\n")
        f.write("-" * 50 + "\n")
        
        # Identificar columnas de gastos
        gasto_cols = [col for col in df_summary.columns if 'gasto' in col.lower()]
        f.write(f"Columnas relacionadas con gastos: {gasto_cols}\n\n")
        
        for col in gasto_cols:
            if col in df_summary.columns:
                f.write(f"{col}:\n")
                f.write(f"  - Total: ${df_summary[col].sum():,.2f}\n")
                f.write(f"  - Promedio: ${df_summary[col].mean():,.2f}\n")
                f.write(f"  - Mediana: ${df_summary[col].median():,.2f}\n")
                f.write(f"  - Mínimo: ${df_summary[col].min():,.2f}\n")
                f.write(f"  - Máximo: ${df_summary[col].max():,.2f}\n")
                f.write(f"  - Valores nulos: {df_summary[col].isnull().sum():,}\n")
                f.write("\n")
        
        # 7. Análisis de fechas
        f.write("7. ANÁLISIS DE FECHAS\n")
        f.write("-" * 50 + "\n")
        
        # Identificar columnas de fechas
        date_cols = [col for col in df_summary.columns if 'fecha' in col.lower()]
        f.write(f"Columnas relacionadas con fechas: {date_cols}\n\n")
        
        for col in date_cols:
            if col in df_summary.columns:
                f.write(f"{col}:\n")
                try:
                    df_summary[col] = pd.to_datetime(df_summary[col])
                    f.write(f"  - Rango: {df_summary[col].min()} a {df_summary[col].max()}\n")
                    f.write(f"  - Duración: {(df_summary[col].max() - df_summary[col].min()).days} días\n")
                    f.write(f"  - Valores nulos: {df_summary[col].isnull().sum():,}\n")
                except:
                    f.write(f"  - No se pudo convertir a fecha\n")
                    f.write(f"  - Valores nulos: {df_summary[col].isnull().sum():,}\n")
                f.write("\n")
        
        # 8. Análisis de días de estancia
        f.write("8. ANÁLISIS DE DÍAS DE ESTANCIA\n")
        f.write("-" * 50 + "\n")
        
        if 'dias_hopit' in df_summary.columns:
            dias_col = 'dias_hopit'
        elif 'dias_hosp' in df_summary.columns:
            dias_col = 'dias_hosp'
        else:
            dias_col = None
        
        if dias_col:
            f.write(f"Columna de días de estancia: {dias_col}\n")
            f.write(f"  - Promedio: {df_summary[dias_col].mean():.2f} días\n")
            f.write(f"  - Mediana: {df_summary[dias_col].median():.2f} días\n")
            f.write(f"  - Mínimo: {df_summary[dias_col].min():.2f} días\n")
            f.write(f"  - Máximo: {df_summary[dias_col].max():.2f} días\n")
            f.write(f"  - Valores nulos: {df_summary[dias_col].isnull().sum():,}\n")
        else:
            f.write("No se encontró columna de días de estancia\n")
        f.write("\n")
        
        # 9. Comparación con datos procesados
        f.write("9. COMPARACIÓN CON DATOS PROCESADOS\n")
        f.write("-" * 50 + "\n")
        
        # Leer datos procesados
        processed_file = Path("data/processed/resultados_pacientes_estandarizados.csv")
        if processed_file.exists():
            df_processed = pd.read_csv(processed_file, low_memory=False)
            
            f.write("Comparación de métricas principales:\n\n")
            
            # Pacientes únicos
            summary_patients = df_summary['paciente'].nunique()
            processed_patients = df_processed['paciente'].nunique()
            f.write(f"Pacientes únicos:\n")
            f.write(f"  - Resumen original: {summary_patients:,}\n")
            f.write(f"  - Datos procesados: {processed_patients:,}\n")
            f.write(f"  - Diferencia: {summary_patients - processed_patients:,} ({((summary_patients-processed_patients)/summary_patients)*100:+.2f}%)\n\n")
            
            # Gastos
            if 'gasto_nivel_6' in df_summary.columns and 'monto_nivel_6' in df_processed.columns:
                summary_gasto = df_summary['gasto_nivel_6'].sum()
                processed_gasto = df_processed['monto_nivel_6'].sum()
                f.write(f"Total gastos nivel 6:\n")
                f.write(f"  - Resumen original: ${summary_gasto:,.2f}\n")
                f.write(f"  - Datos procesados: ${processed_gasto:,.2f}\n")
                f.write(f"  - Diferencia: ${summary_gasto - processed_gasto:,.2f} ({((summary_gasto-processed_gasto)/summary_gasto)*100:+.2f}%)\n\n")
            
            # Días de estancia
            if dias_col and 'dias_estancia' in df_processed.columns:
                summary_dias = df_summary[dias_col].mean()
                processed_dias = df_processed['dias_estancia'].mean()
                f.write(f"Promedio días de estancia:\n")
                f.write(f"  - Resumen original: {summary_dias:.2f} días\n")
                f.write(f"  - Datos procesados: {processed_dias:.2f} días\n")
                f.write(f"  - Diferencia: {summary_dias - processed_dias:+.2f} días ({((summary_dias-processed_dias)/summary_dias)*100:+.2f}%)\n\n")
        else:
            f.write("No se encontró el archivo de datos procesados para comparación\n")
        
        # 10. Resumen y recomendaciones
        f.write("10. RESUMEN Y RECOMENDACIONES\n")
        f.write("-" * 50 + "\n")
        f.write("Hallazgos principales:\n")
        f.write(f"1. El archivo de resumen contiene {len(df_summary):,} registros\n")
        f.write(f"2. Hay {len(df_summary.columns)} columnas con información detallada\n")
        f.write(f"3. Los datos incluyen información de urgencias y hospitalización\n")
        f.write(f"4. Se pueden identificar pacientes únicos por múltiples campos\n")
        f.write("5. El archivo parece ser un resumen consolidado por episodio\n\n")
        
        f.write("Recomendaciones:\n")
        f.write("1. Usar este archivo como referencia para validar los datos procesados\n")
        f.write("2. Considerar la información adicional disponible (diagnósticos, procedencia, etc.)\n")
        f.write("3. Analizar las diferencias en conteos para entender las metodologías\n")
        f.write("4. Usar los gastos del resumen como benchmark para validación\n\n")
        
        f.write("="*60 + "\n")
        f.write("Análisis completado.\n")
    
    print(f"Análisis completado. Resultados guardados en: {output_file}")
    
    # Crear también un resumen ejecutivo
    create_summary_executive_summary(df_summary, resultados_path)

def create_summary_executive_summary(df_summary, resultados_path):
    """Crea un resumen ejecutivo del archivo de resumen."""
    
    summary_file = resultados_path / "resumen_ejecutivo_archivo_resumen.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("RESUMEN EJECUTIVO - ARCHIVO DE RESUMEN ORIGINAL\n")
        f.write("="*60 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Métricas principales
        f.write("MÉTRICAS PRINCIPALES:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Registros totales: {len(df_summary):,}\n")
        f.write(f"Columnas: {len(df_summary.columns)}\n")
        f.write(f"Pacientes únicos: {df_summary['paciente'].nunique():,}\n")
        
        # Gastos
        if 'gasto_nivel_6' in df_summary.columns:
            total_gasto = df_summary['gasto_nivel_6'].sum()
            f.write(f"Total gasto nivel 6: ${total_gasto:,.0f}\n")
        
        if 'gasto_nivel_1' in df_summary.columns:
            total_gasto_n1 = df_summary['gasto_nivel_1'].sum()
            f.write(f"Total gasto nivel 1: ${total_gasto_n1:,.0f}\n")
        
        # Días de estancia
        if 'dias_hopit' in df_summary.columns:
            avg_dias = df_summary['dias_hopit'].mean()
            f.write(f"Promedio días de estancia: {avg_dias:.2f}\n")
        
        # Información adicional
        f.write("\nINFORMACIÓN ADICIONAL DISPONIBLE:\n")
        f.write("-" * 40 + "\n")
        
        # Contar columnas por categoría
        urgencias_cols = [col for col in df_summary.columns if 'urg' in col.lower()]
        hospitalizacion_cols = [col for col in df_summary.columns if 'hosp' in col.lower()]
        diagnostico_cols = [col for col in df_summary.columns if 'diagnostico' in col.lower()]
        
        f.write(f"Columnas de urgencias: {len(urgencias_cols)}\n")
        f.write(f"Columnas de hospitalización: {len(hospitalizacion_cols)}\n")
        f.write(f"Columnas de diagnóstico: {len(diagnostico_cols)}\n")
        
        # Ejemplos de columnas importantes
        f.write("\nCOLUMNAS PRINCIPALES:\n")
        f.write("-" * 40 + "\n")
        important_cols = ['paciente', 'n_expediente_hosp', 'ian_expediente_hosp', 'gasto_nivel_6', 'gasto_nivel_1']
        for col in important_cols:
            if col in df_summary.columns:
                f.write(f"✓ {col}\n")
            else:
                f.write(f"✗ {col} (no encontrada)\n")
    
    print(f"Resumen ejecutivo guardado en: {summary_file}")

if __name__ == "__main__":
    analyze_summary_file() 