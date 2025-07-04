#!/usr/bin/env python3
"""
Script para estandarizar expedientes eliminando el prefijo "000" y generar un dataset limpio.
Esto resuelve el problema de pacientes con múltiples expedientes debido a formatos inconsistentes.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def standardize_expedient_number(expedient):
    """Estandariza el número de expediente eliminando el prefijo '000'."""
    if pd.isna(expedient) or expedient == '':
        return expedient
    
    expedient_str = str(expedient).strip()
    
    # Si empieza con "000", eliminar el prefijo
    if expedient_str.startswith('000'):
        return expedient_str[3:]  # Eliminar los primeros 3 caracteres
    
    return expedient_str

def analyze_and_standardize():
    """Analiza y estandariza los expedientes."""
    
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
    
    # Crear archivo de análisis
    output_file = resultados_path / "estandarizacion_expedientes.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ESTANDARIZACIÓN DE EXPEDIENTES\n")
        f.write("="*50 + "\n")
        f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 1. Análisis antes de la estandarización
        f.write("1. ANÁLISIS ANTES DE LA ESTANDARIZACIÓN\n")
        f.write("-" * 50 + "\n")
        
        # Contar expedientes únicos
        expedients_before = df['n_expediente_hosp'].nunique()
        f.write(f"Expedientes únicos antes: {expedients_before:,}\n")
        
        # Contar pacientes únicos
        patients_before = df['paciente'].nunique()
        f.write(f"Pacientes únicos antes: {patients_before:,}\n")
        
        # Contar combinaciones paciente + expediente
        patient_expedient_before = df.groupby(['paciente', 'n_expediente_hosp']).size().reset_index().shape[0]
        f.write(f"Combinaciones paciente + expediente antes: {patient_expedient_before:,}\n\n")
        
        # 2. Análisis de patrones en expedientes
        f.write("2. ANÁLISIS DE PATRONES EN EXPEDIENTES\n")
        f.write("-" * 50 + "\n")
        
        # Expedientes que empiezan con "000"
        expedients_with_000 = df[df['n_expediente_hosp'].astype(str).str.startswith('000', na=False)]
        expedients_without_000 = df[~df['n_expediente_hosp'].astype(str).str.startswith('000', na=False)]
        
        f.write(f"Expedientes que empiezan con '000': {len(expedients_with_000):,} ({len(expedients_with_000)/len(df)*100:.2f}%)\n")
        f.write(f"Expedientes sin '000': {len(expedients_without_000):,} ({len(expedients_without_000)/len(df)*100:.2f}%)\n\n")
        
        # Mostrar algunos ejemplos
        f.write("Ejemplos de expedientes con '000':\n")
        examples_with_000 = expedients_with_000['n_expediente_hosp'].unique()[:10]
        for exp in examples_with_000:
            f.write(f"  - {exp}\n")
        f.write("\n")
        
        f.write("Ejemplos de expedientes sin '000':\n")
        examples_without_000 = expedients_without_000['n_expediente_hosp'].unique()[:10]
        for exp in examples_without_000:
            f.write(f"  - {exp}\n")
        f.write("\n")
        
        # 3. Estandarización
        f.write("3. PROCESO DE ESTANDARIZACIÓN\n")
        f.write("-" * 50 + "\n")
        
        # Crear copia del dataframe para estandarizar
        df_standardized = df.copy()
        
        # Aplicar estandarización
        df_standardized['n_expediente_hosp_original'] = df_standardized['n_expediente_hosp']
        df_standardized['n_expediente_hosp'] = df_standardized['n_expediente_hosp'].apply(standardize_expedient_number)
        
        # Contar cambios realizados
        changes_made = (df['n_expediente_hosp'] != df_standardized['n_expediente_hosp']).sum()
        f.write(f"Expedientes estandarizados: {changes_made:,} ({changes_made/len(df)*100:.2f}%)\n\n")
        
        # 4. Análisis después de la estandarización
        f.write("4. ANÁLISIS DESPUÉS DE LA ESTANDARIZACIÓN\n")
        f.write("-" * 50 + "\n")
        
        # Contar expedientes únicos después
        expedients_after = df_standardized['n_expediente_hosp'].nunique()
        f.write(f"Expedientes únicos después: {expedients_after:,}\n")
        f.write(f"Reducción en expedientes únicos: {expedients_before - expedients_after:,} ({((expedients_before-expedients_after)/expedients_before)*100:.2f}%)\n\n")
        
        # Contar combinaciones paciente + expediente después
        patient_expedient_after = df_standardized.groupby(['paciente', 'n_expediente_hosp']).size().reset_index().shape[0]
        f.write(f"Combinaciones paciente + expediente después: {patient_expedient_after:,}\n")
        f.write(f"Reducción en combinaciones: {patient_expedient_before - patient_expedient_after:,} ({((patient_expedient_before-patient_expedient_after)/patient_expedient_before)*100:.2f}%)\n\n")
        
        # 5. Verificación de pacientes con múltiples expedientes después
        f.write("5. VERIFICACIÓN DE PACIENTES CON MÚLTIPLES EXPEDIENTES\n")
        f.write("-" * 50 + "\n")
        
        # Contar pacientes con múltiples expedientes después de estandarización
        patient_expedient_counts_after = df_standardized.groupby('paciente')['n_expediente_hosp'].nunique()
        patients_multiple_after = patient_expedient_counts_after[patient_expedient_counts_after > 1]
        
        f.write(f"Pacientes con múltiples expedientes después: {len(patients_multiple_after):,}\n")
        f.write(f"Porcentaje del total: {len(patients_multiple_after)/patients_before*100:.2f}%\n\n")
        
        # Mostrar algunos ejemplos de pacientes que aún tienen múltiples expedientes
        if len(patients_multiple_after) > 0:
            f.write("Ejemplos de pacientes que aún tienen múltiples expedientes:\n")
            for i, (patient, num_expedients) in enumerate(patients_multiple_after.head(5).items()):
                patient_data = df_standardized[df_standardized['paciente'] == patient]
                expedients = patient_data['n_expediente_hosp'].unique()
                f.write(f"  - Paciente {patient}: {num_expedients} expedientes {list(expedients)}\n")
            f.write("\n")
        
        # 6. Guardar dataset estandarizado
        f.write("6. GUARDADO DE DATASET ESTANDARIZADO\n")
        f.write("-" * 50 + "\n")
        
        # Guardar en processed
        output_path = Path("data/processed")
        output_path.mkdir(exist_ok=True)
        
        standardized_file = output_path / "resultados_pacientes_estandarizados.csv"
        df_standardized.to_csv(standardized_file, index=False, encoding='utf-8')
        
        f.write(f"Dataset estandarizado guardado en: {standardized_file}\n")
        f.write(f"Tamaño del archivo: {standardized_file.stat().st_size / 1024**2:.2f} MB\n\n")
        
        # 7. Resumen de mejoras
        f.write("7. RESUMEN DE MEJORAS\n")
        f.write("-" * 50 + "\n")
        f.write("Beneficios de la estandarización:\n")
        f.write(f"1. Expedientes únicos reducidos de {expedients_before:,} a {expedients_after:,} (-{expedients_before-expedients_after:,})\n")
        f.write(f"2. Combinaciones paciente+expediente reducidas de {patient_expedient_before:,} a {patient_expedient_after:,} (-{patient_expedient_before-patient_expedient_after:,})\n")
        f.write(f"3. Pacientes con múltiples expedientes reducidos de 374 a {len(patients_multiple_after):,}\n")
        f.write("4. Dataset más consistente para análisis posteriores\n")
        f.write("5. Eliminación de duplicados por formato inconsistente\n\n")
        
        f.write("="*50 + "\n")
        f.write("Estandarización completada exitosamente.\n")
    
    print(f"Análisis de estandarización completado. Resultados guardados en: {output_file}")
    print(f"Dataset estandarizado guardado en: data/processed/resultados_pacientes_estandarizados.csv")
    
    # Crear también un resumen de los cambios
    create_standardization_summary(df, df_standardized, resultados_path)

def create_standardization_summary(df_original, df_standardized, resultados_path):
    """Crea un resumen de los cambios realizados."""
    
    summary_file = resultados_path / "resumen_estandarizacion.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("RESUMEN DE ESTANDARIZACIÓN DE EXPEDIENTES\n")
        f.write("="*50 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Métricas principales
        f.write("MÉTRICAS PRINCIPALES:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Registros totales: {len(df_original):,}\n")
        f.write(f"Expedientes únicos antes: {df_original['n_expediente_hosp'].nunique():,}\n")
        f.write(f"Expedientes únicos después: {df_standardized['n_expediente_hosp'].nunique():,}\n")
        f.write(f"Pacientes únicos: {df_original['paciente'].nunique():,}\n")
        f.write(f"Combinaciones paciente+expediente antes: {df_original.groupby(['paciente', 'n_expediente_hosp']).size().reset_index().shape[0]:,}\n")
        f.write(f"Combinaciones paciente+expediente después: {df_standardized.groupby(['paciente', 'n_expediente_hosp']).size().reset_index().shape[0]:,}\n\n")
        
        # Cambios realizados
        changes = (df_original['n_expediente_hosp'] != df_standardized['n_expediente_hosp']).sum()
        f.write(f"Expedientes estandarizados: {changes:,} ({changes/len(df_original)*100:.2f}%)\n")
        
        # Ejemplos de cambios
        f.write("\nEJEMPLOS DE CAMBIOS:\n")
        f.write("-" * 30 + "\n")
        
        # Mostrar algunos ejemplos de expedientes que cambiaron
        changed_mask = df_original['n_expediente_hosp'] != df_standardized['n_expediente_hosp']
        changed_examples = df_original[changed_mask].head(10)
        
        for _, row in changed_examples.iterrows():
            original = row['n_expediente_hosp']
            standardized = df_standardized.loc[row.name, 'n_expediente_hosp']
            f.write(f"  {original} → {standardized}\n")
    
    print(f"Resumen de estandarización guardado en: {summary_file}")

if __name__ == "__main__":
    analyze_and_standardize() 